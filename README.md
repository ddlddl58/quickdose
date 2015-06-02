# QuickDose (beta)#

Author: Radek Hofman

QuickDose is a set of tools for written in [Python](http://www.python.org) producing radiological outputs with Langrangian particle dispersion model [FLEXPART](http://flexpart.eu). QuickDose was inspired by [flexRISK](http://flexrisk.boku.ac.at/) project. Output of QuickDose can be something like [this simulated release](http://stradi.utia.cas.cz/temelin/) from NPP Temelin.

![quickdose.png](https://bitbucket.org/repo/A9EgjE/images/3747294764-quickdose.png)

The project is under development. Currently it has following features:

* Prepares a set of FLEXPART runs corresponding with a given source term needed for dose calculation
* Calculates radioactive decay (including parent-daughter decay chains) and actual releases of all nuclides form the source term. More details in this [ipython notebook](http://nbviewer.ipython.org/url/bitbucket.org/radekhofman/quickdose/raw/master/Materials/rad_postproc.ipynb) 
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

### Preparing QuickDose project ###

To be able to apply radiological post-processing to FLEXPART output we need a separate source-receptor sensitivity field for each elemental release. To accmplish so, there is a separate FLEXPART run for each release in QuickLook. This so called run tree is constructed automatically given a `SOURCE_TERM` in `rad_decay.py`.

#### Source term definition ####

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

It contains 4 elemental releases in two phases of length `time_step` in seconds. In each phase we release nuclides from sources 0-50 and 50-200 meters. Generally, the structure of `sources` is as follows:

```
sources = [
   [phase_1_release_1, phase_1_release_2,..., phase_1_release_N1],
    ...
   [phase_M_release_1, phase_M_release_2,...,phase_M_release_NM]
]
```

All release phases must have the same duration `time_step`. It is clear that a release of any complexity can be transformed into this "canonical" form given a sufficiently short `time_step`.

We release three nuclides: `Cs-137, I-131, Xe-133`. Neither number of phases nor nuclides is not limited. Just note that in all phases we have to define all nuclides even if their release is zero (as in the case of `Xe-133` in the second phase). Besides the overal magnitude for each phase (Bq), we define also a species type of respective nuclides. `SOURCE_TERM` entry 

```python 
"species_dict": {1: 1, 2: 16}
```

defines which species in `SOURCE_TERM`corresponds to which species in FLEXPART. Number 1 corresponds to FLEPXART species 1 (an air tracer with no deposition and thus suitable for noble gases) and number 2 corresponds to number 16 in FLEXPART which is an aerosol. All species definitions in FLEXPART can be found in `FLEXPART/Option/SPECIES`. 

Decay chains can be also defined. `SOURCE_TERM` entry 

```python
    "decay_chains" : {
            "I-131": ("Xe-131m", 1.0),
            },
```

tells us that we assume decay chain `I-131 -> Xe-131m` with fraction `1.0`. Please note, that in theses cases when a particulate decays to noble gas, the noble gas contribution from deposition is ignored! This could be properly handles only "on the flow" during a FLEXPART run, not in post-processing.

Number of decay chains is not limited. The only condition, similarly to definition of inventories, is that both parent and daughter nuclides must have their corresponding entries in nuclide database contained in `Src/mods/coefficients/nuclide_data.py`. It is a JSON containing for each nuclides its half-life, inhalation dose conversion coefficients for 5 age groups, cloudshine and groundshine conversion coefficients:

```python
#breathing rates 3m, 1y, 5y, 10y, 15y and adults(> 17 years) in m3/day
breathing_rates = (2.86, 5.16, 8.72, 15.3, 20.1, 22.2)

d = {
#particulates
'Sb-122': {'halflife': 233280.0, 'inhalation': (8.3e-09, 5.7e-09, 2.8e-09, 1.8e-09, 1.3e-09, 1e-09), 'cloud': 2.02e-14, 'ground': 4.85e-16},
'Sb-124': {'halflife': 5201280.0, 'inhalation': (3.1e-08, 2.4e-08, 1.4e-08, 9.6e-09, 7.7e-09, 6.4e-09), 'cloud': 8.62e-14, 'ground': 1.7e-15},
'Sb-125': {'halflife': 87354720.0, 'inhalation': (2e-08, 1.6e-08, 1e-08, 6.8e-09, 5.8e-09, 4.8e-09), 'cloud': 1.87e-14, 'ground': 4.09e-16},
'Te-132': {'halflife': 281664.0, 'inhalation': (1.6e-08, 1.3e-08, 6.4e-09, 4e-09, 2.6e-09, 2e-09), 'cloud': 1.17e-13, 'ground': 2.47e-15},
...}
```

Age groups are as follows: `(0-1y, 1-2y, 2-7y, 7y-12y, 12-17y, adults)`.

What remains is to put other FLEXPART inputs and templates for special files into directories defined by variables `STATIC` and `TEMPLATES` (this should be OK in default settings).

#### Making a run tree ####

Run tree is automatically created by running a script `Src/1_make_tree.py` in `TREE_PATH/RUN`. The naming convention for runs of elemental releases is: `R_t=dddd_id=dddd`, where `t` is phase number and `id` is source term number in phase `t`.

#### Executing runs ####

Runs should be executed in an automated fashion by the script `Src/2_run_tree.py`. Unfortunately, this is not implemented yet so the runs must be executed manually or using a tool like [sbatch](https://computing.llnl.gov/linux/slurm/sbatch.html) or similar.

### Calculation of nuclide specific outputs ###

This step reads FLEXPART output for unit releases and calculates actual concentration and deposition fields of different nuclides including radioactive decay. The methodology of computing radioactive decay under assumption of constant concentration and deposition within a given time step is described in this [ipython notebook](http://nbviewer.ipython.org/url/bitbucket.org/radekhofman/quickdose/raw/master/Materials/rad_postproc.ipynb). Decayed products (concentration and deposition fields are stored in directories defined by variable `CLOUDSHINE_DIR` and `DEPOSITION_DIR`). Each nuclide has a separate `nuclide_name.mat` file of dimensions `(time_step, dimx, dimy, dimz)` for concentration and `(time_step, dimx, dimy)` for deposition. To do this, simply run `Src/3_calculate_decay.py`

### Calculation of doses ###

When all runs are finished, we can calculate doses. Currently, following is calculated:

* External gamma dose rate due to cloudshine (Sv/s) (results in directory defined by `CLOUDSHINE_DIR`)
* External gamma dose rate due to deposition (Sv/s) (results in directory defined by `GROUNDSHINE_DIR`)
* Internal irradiation due to inhalation (Sv/s) (results in directory defined by `INHALATION_DIR`)
* Dose rate from all pathways (Sv/s) (results in directory defined by `ALL_PATHWAYS_DIR`)

Each nuclide has again its separate `nuclide_name.mat` file of dimensions `(time_step, dimx, dimy)`. There is also a file `all_nuclides.mat` where a sum over nuclides is stored. 

To calculate doses we run script `Src/4_calculate_radiological_quantities.py`

### Plotting results and other processing ###

Finally, we can plot results. Plotting has its own configuration file derived from project [QuickLook](https://bitbucket.org/radekhofman/quicklook) called `plt_config.py`. Please look inside and see what can be configured. In default settings, by running script `Src/5_make_plots.py` we obtain figures for each frame of each nuclide, which could be quite high number of figures:) Instead of plotting, the results can be integrated to obtain doses etc.

## Plans ##

* Implementation of doses (time integrals of GDR)
* Introduce dose shielding factors etc.
* Broaden nuclide library
* De-bug everything :)

## Final warning ##

This is a beta version and it is quite likely, that there are bugs.