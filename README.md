# QuickLook (beta)#

QuickDose is a set of tools for written in [Python](http://www.python.org) producing radiological outputs with Langrangian particle dispersion model [FLEXPART](http://flexpart.eu). QuickDose was inspired by [flexRISK](http://flexrisk.boku.ac.at/) project. Output of QuickDose can be something like [this](http://stradi.utia.cas.cz/temelin/) simulated release from NPP Temelin.

The project is under development. Currently it has following features:

* Prepares a set of FLEXPART runs corresponding with a given source term needed for dose calculation
* Calculates radioactive decay (including parent-daughter decay chains) and actual releases of all nuclides form the source term
* Calculates external gamma dose rate (GDR) from cloud and deposition
* Calculates internal GDR from inhalation
* Contains a tool for simple plotting of results using [Matplotlib Basemap](http://matplotlib.org/basemap/) (including [transparent overlays](http://stradi.utia.cas.cz/temelin/) for [GoogleMaps](maps.google.com))

Dose conversion coefficients for circa 70 nuclides and 5 age groups contained in QuickDose are taken from:

Radiation Protection Bureau, Health Canada, Atomic Energy Control Board, Atomic Energy of Canada Limited: *Recommendations on Dose Coefficients for Assessing Doses from Accidental Radionuclide Releases to the Environment* (1999).

## Prerequisites ##

* Working FLEXPART binary compiled for your machine, source can be found here:
* Python 2.7
* Following python packages:
 - [numpy](http://www.numpy.org/)
 - [matplotlib](http://matplotlib.org/)
 - [scipy](http://www.scipy.org) (intermediate results are stored as Matlab `*.mat` files)

## How does it work? ##


### Calculation of doses ###

### Plotting results ###