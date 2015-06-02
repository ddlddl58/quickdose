# -*- coding: utf-8 -*-
__author__ = 'radek hofman'

from datetime import datetime
import os
import mods.coefficients.nuclide_data as DB


######################################################################################################
### GENERAL SETTINGS
######################################################################################################

#run directory
TREE_PATH =   "/Volumes/SSD_/Users/panda/Krablak/nuclearrisk.info/QuickDose/Runs"

#static files path
STATIC = TREE_PATH+os.sep+"Static"

#templates path
TEMPLATES = TREE_PATH+os.sep+"Templates"

#run name
RUN = "Run_rad004"

#number of particles
PART_NUMBER = 100000

#FLEXPART date format
FP_DATE_FMT = "%Y%m%d%H%M%s"

#date format we use in COMMAND etc.
DATE_FORMAT = "%Y%m%d %H%M%S"

#meteorological data
METEO_PATH = "/Volumes/Panda/Users/hofmanr8/nuclearrisk.info/data/2015052700_1p00/"
AVAILABLE = "/Volumes/Panda/Users/hofmanr8/nuclearrisk.info/data/2015052700_1p00/AVAILABLE"

#FLEXPART executable path for creating symlinks
FLEXPART_NAME = "flexpart_gfs_gfort_1p0.out"
FLEXPART_PATH = TREE_PATH+os.sep+"Flexpart"+os.sep+FLEXPART_NAME


######################################################################################################
### DEFINING SOURCE TERM
######################################################################################################

#coordinates of the source
lat0, lon0, lat1, lon1 = (49.18, 14.3761, 49.18, 14.3761)

#JSON defining source term
SOURCE_TERM = {
    "time_step" : 3600,  # time step in seconds:
    "t_average" : 3600,
    "release_start" : "20150527 000000",
#    "release_end"   : "20150527 010000",  # e.g. a 2 hours of release, i.e. two time steps of length 1 hour
    "calc_start" : "20150527 000000",
    "calc_end"   : "20150530 000000",
    "outgrid" : {
        "outlonlower": -179.0,
        "outlatleft": -90.0,
        "numxgrid": 359,
        "numygrid": 180,
        "dxoutlon": 1.0,  # deg
        "dyoutlat": 1.0,  # deg
        "levels": (150, 500, 1000),
        },
    "outgrid_nest" : {
        "outlonlower": 5.0,
        "outlatleft": 42.0,
        "numxgrid": 160,
        "numygrid": 140,
        "dxoutlon": 0.12,  # deg
        "dyoutlat": 0.1,  # deg
        },
    "species_dict": {1: 1, 2: 16},  # IMPORTANT! which species in FLEXPART are which in source term
    "sources":  [  # an array with list of sources acting at that time (list of lists)
                   #THE ORDER OF SPECIES TYPES MUST BE THE SAME AS IN THE RELEASES FILE!!!

                    # TIME STEP 1
                    [{"lat0":lat0,  # source 1 for time step 1
                      "lon0":lon0,
                      "lat1":lat1,
                      "lon1":lon1,
                      "h0":  0,  # bottom of layer in meters
                      "h1": 50,  # top of layer in meters
                      "inventory": {"Kr-85m": (3.53e11, 1),
                                    "Kr-88": (8e11, 1),
                                    "I-131": (1.28e11, 2),
                                    "I-132": (1.71e11, 2),
                                    "I-133": (2.51e11, 2),
                                    "I-134": (2.37e11, 2),
                                    "I-135": (2.51e11, 2),
                                    "Te-132": (2.89e8, 2),
                                    "Cs-134": (3.7e10, 2),
                                    "Cs-136": (1.60e10, 2),
                                    "Cs-137": (1.85e10, 2),
                                    "Xe-133": (4.09e12, 1),
                                    "Xe-135": (1.07e12, 1)
                                    }  # (release, species)
                     }
                   ]
                ],
    #definition of possible decay chains
    "decay_chains": {
            "I-133": ("Xe-133", 0.971),
            "I-135": ("Xe-135", 0.846),
            "I-135": ("Xe-135m", 0.154)
            },
    "age_group": 5  # select from: 0: 0-1y, 1: 1-2y, 2: 2-7y, 3: 7y-12y, 4: 12-17y, 5: adults
    }

NUCLIDE_DB = DB  # justa passing nuclide DB


######################################################################################################
### PARAMETERS FOR PROCESSING OF FLEXPART OUTPUT
######################################################################################################

#which domain to process?
DOMAIN = 1  # mother = 0, nest = 1

OUTPUT_PATH = TREE_PATH+os.sep+RUN+os.sep+"Results"+os.sep+"Data"
IMAGES_PATH = TREE_PATH+os.sep+RUN+os.sep+"Results"+os.sep+"Images"

#output dirs should be defined for all target radiological quantities
#  basic quantities with radiological decay applied:
CONCENTRATION_DIR = "Conc"  # (Bq/m3)
DEPOSITION_DIR = "Depo"  # (Bq/m2)

#  derived and time integrated quantities
CLOUDSHINE_DIR = "Cloud_GDR"  # external gamma dose rate due to cloudshine (Sv/s)
GROUNDSHINE_DIR = "Ground_GDR"  # external gamma dose rate due to deposition (Sv/s)
INHALATION_DIR = "Inhalation_GDR"  # internal irradiation due to inhalation (Sv/s)
ALL_PATHWAYS_DIR = "All_pathways_GDR"  # dose rate from all pathways
TIME_INTEGRATED_CONCENTRATION_DIR = "Time_int_conc"  # (Bq*s/m3)
TIME_INTEGRATED_CLOUDSHINE_DIR = "Time_int_cloud"  # (Sv)
TIME_INTEGRATED_GROUNDSHINE_DIR = "Time_int_ground"  # (Sv)
TIME_INTEGRATED_INHALATION_DIR = "Time_int_inhalation"  # (Sv)
TIME_INTEGRATED_ALL_PATHWAYS_DIR = "Time_int_all_pathways" # (Sv)

ALL_NUCLIDES_IDENT = "all_nuclides"  # how to denote results summed over all nuclides?





