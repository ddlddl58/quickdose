# QuickLook (beta)#

QuickDose is a set of tools for written in [Python](http://www.python.org) producing radiological outputs with Langrangian particle dispersion model [FLEXPART](http://flexpart.eu). QuickDose was inspired by [flexRISK](http://flexrisk.boku.ac.at/) project. Output of QuickDose can be something like [this simulated release](http://stradi.utia.cas.cz/temelin/) from NPP Temelin.

The project is under development. Currently it has following features:

* Prepares a set of FLEXPART runs corresponding with a given source term needed for dose calculation
* Calculates radioactive decay (including parent-daughter decay chains) and actual releases of all nuclides form the source term
* Calculates external gamma dose rate (GDR) from cloud and deposition
* Calculates internal GDR from inhalation
* Contains a tool for simple plotting of results using [Matplotlib Basemap](http://matplotlib.org/basemap/) (including [transparent overlays](http://stradi.utia.cas.cz/temelin/) for [GoogleMaps](maps.google.com))

Dose conversion coefficients for circa 70 nuclides and 5 age groups contained in QuickDose are taken from:

Radiation Protection Bureau, Health Canada, Atomic Energy Control Board, Atomic Energy of Canada Limited: *Recommendations on Dose Coefficients for Assessing Doses from Accidental Radionuclide Releases to the Environment* (1999).

## Prerequisites ##

You need following to use QuickLook:

* Working FLEXPART binary compiled for your machine, source can be found [here](http://flexpart.eu/downloads). Currently, QuickDose works with FLEXPART 9.0. With newer FLEXPART version there could be a problem with routines for reading FLEXPART inputs and outputs.
* Python 2.7
* [Numpy](http://www.numpy.org/)
* [Matplotlib](http://matplotlib.org/)
* [Scipy](http://www.scipy.org) (intermediate results are stored as Matlab `*.mat` files)

## How does it work? ##

### Preparing environment ###

Everything start by creating a configuration file for a dose calculation project which must be located at `QuickDose/Src/rad_config.py` (or sym-linked from elsewhere:).

Firstly, you have to configure input and output paths. The most important is to set `TREE_PATH` containing all projects. All output paths are then relative to this one and should work well in default setting. What regards input paths, you have to set variables `METEO_PATH` and `AVAILABLE` containing meteorological fields and the `AVAILABLE` file. The you have to configure location and name of FLEXPART binary using variables `FLEXPART_PATH` and `FLEXPART_NAME`.

### Preparing FLEXPART runs ###

To be able to apply radiological post-processing to FLEXPART output we need a separate source-receptor sensitivity field for each elemental release. To accmplish so, there is a separate FLEXPART run for each release in QuickLook. This so called run tree is constructed automatically given a `SOURCE_TERM` in `rad_decay.py`.

#### Source term ####

Source term is a JSON structure defining all essential aspects of the release. A samples source term can look like this:

```python
#JSON defining source term
SOURCE_TERM = {
    "time_step" : 3600,  # time step in seconds:
    "t_average" : 3600,
    "release_start" : "20150507 000000",
    "release_end"   : "20150508 000000",  # e.g. a 2 hours of release, i.e. two time steps of length 1 hour
    "calc_start" : "20150507 000000",
    "calc_end"   : "20150510 000000",
    "outgrid" : {
        "outlonlower": -179.0,
        "outlatleft": -90.0,
        "numxgrid": 359,
        "numygrid": 180,
        "dxoutlon": 1.0,  # deg
        "dyoutlat": 1.0,  # deg
        "levels": (100, 500, 1000),
        },
    "outgrid_nest" : {
        "outlonlower": 8.0,
        "outlatleft": 45.0,
        "numxgrid": 110,
        "numygrid": 100,
        "dxoutlon": 0.12,  # deg
        "dyoutlat": 0.1,  # deg
        },
    "species_dict": {1: 1, 2: 16},  # which species in flexpart is which in source term
    "sources":  [  # an array with list of sources acting at that time (list of lists)
                   #THE ORDER OF SPECIES TYPES MUST BE THE SAME AS IN THE RELEASES FILE!!!
                    # TIME STEP 1
                    [{"lat0":lat0,  # source 1 for time step 1
                      "lon0":lon0,
                      "lat1":lat1,
                      "lon1":lon1,
                      "h0":  0,  # bottom of layer in meters
                      "h1": 50,  # top of layer in meters
                      "inventory": {"Cs-137": (1e10, 2), "I-131": (1e11, 2), "Xe-133": (1e10, 1)}  # (release, species)
                     },
                     {"lat0":lat0,  # source 2 for time step 1
                      "lon0":lon0,
                      "lat1":lat1,
                      "lon1":lon1,
                      "h0":  50,  # bottom of layer in meters
                      "h1": 200,  # top of layer in meters
                      "inventory": {"Cs-137": (1e11, 2), "I-131": (1e12, 2), "Xe-133": (1e13, 1)}
                     }],
                    # TIME STEP 2
                    [{"lat0":lat0,  # source 1 for time step 2
                      "lon0":lon0,
                      "lat1":lat1,
                      "lon1":lon1,
                      "h0":  0,  # bottom of layer in meters
                      "h1": 50,  # top of layer in meters
                      "inventory": {"Cs-137": (1e9, 2), "I-131": (1e10, 2), "Xe-133": (0., 1)}
                     },
                     {"lat0":lat0,  # source 2 for time step 2
                      "lon0":lon0,
                      "lat1":lat1,
                      "lon1":lon1,
                      "h0":  50,  # bottom of layer in meters
                      "h1": 200,  # top of layer in meters
                      "inventory": {"Cs-137": (1e10, 2), "I-131": (1e11,2), "Xe-133": (0., 1)}
                     }]
                ],
    #definition of possible decay chains
    "decay_chains" : {
            "I-131": ("Xe-131m", 1.0),
            },
    "age_group": 5  # select from: 0: 0-1y, 1: 1-2y, 2: 2-7y, 3: 7y-12y, 4: 12-17y, 5: adults
    }
```

#### Executing runs ####

### Calculation of doses ###

### Plotting results ###