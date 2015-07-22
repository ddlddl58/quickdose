# -*- coding: utf-8 -*-

from datetime import datetime
import os
import mods.coefficients.nuclide_data as DB

#run directory
TREE_PATH =   "/home/srvx1/tmc/Prepare/Nuclide_ratios/quickdose/Runs/"

#static files path
STATIC = TREE_PATH+os.sep+"Static"

#templates path
TEMPLATES = TREE_PATH+os.sep+"Templates"

#run name
RUN = "Run_Temelin_02"

#number of particles per hour
PART_NUMBER = 1000000

#FLEXPART date format
FP_DATE_FMT = "%Y%m%d%H%M%s"

#meteorological data
METEO_PATH = "/home/srvx1/tmc/ectrans/EN_resol_0250_Dtime3_G1_1/" #  "/Users/jezisek/nuclearrisk.info/FLEXPART/GFS/20150722001p00/"  # "/Users/jezisek/nuclearrisk.info/FLEXPART/GFS/2015050700_1p00/"
AVAILABLE =  "/home/srvx1/tmc/ectrans/EN_resol_0250_Dtime3_G1_1/AVAILABLE"  #  "/Users/jezisek/nuclearrisk.info/FLEXPART/GFS/20150722001p00/AVAILABLE"  # "/Users/jezisek/nuclearrisk.info/FLEXPART/GFS/2015050700_1p00/AVAILABLE"

#FLEXPART executable path for creating symlinks
FLEXPART_NAME = "flexpart_ecmwf_gfortran_025_2spec.out"  #  "flexpart_gfs_1p0.out"  # "flexpart_gfs_0p5.out"
FLEXPART_PATH = ".."+os.sep+".."+os.sep+"Flexpart"+os.sep+FLEXPART_NAME

#coordinates of the source
#lat0, lon0, lat1, lon1 = (49.18, 14.3761, 49.18, 14.3761)

#date format we use
DATE_FORMAT = "%Y%m%d %H%M%S"

#JSON defining source term
SOURCE_TERM = {'species_dict': {1: 1, 2: 16}, 'sources': [[{'lat1': 49.1817, 'lat0': 49.1817, 'h0': 50, 'h1': 50, 'inventory': {'Kr-85m': (33300000000000.0, 1), 'Cs-136': (504000000000.0, 2), 'Sr-90': (482000000000.0, 2), 'Cs-134': (2100000000000.0, 2), 'I-133': (320000000000000.0, 2), 'Xe-135': (683000000000000.0, 1), 'I-131': (157000000000000.0, 2), 'Cs-137': (1320000000000.0, 2), 'I-135': (300000000000000.0, 2), 'Xe-133': (321000000000000.0, 1), 'Kr-88': (104000000000000.0, 1), 'I-132': (228000000000000.0, 2), 'Te-132': (18000000000000.0, 2), 'I-134': (351000000000000.0, 2), 'Sr-89': (4490000000000.0, 2), 'Kr-87': (7030000000000000.0, 1)}, 'lon1': 14.3754, 'lon0': 14.3754}], [{'lat1': 49.1817, 'lat0': 49.1817, 'h0': 50, 'h1': 50, 'inventory': {'Kr-85m': (46600000000000000.0, 1), 'Cs-136': (5670000000000000.0, 2), 'Sr-90': (1450000000000000.0, 2), 'Cs-134': (23600000000000000.0, 2), 'I-133': (22400000000000000.0, 2), 'Xe-135': (95600000000000000.0, 1), 'I-131': (11000000000000000.0, 2), 'Cs-137': (14800000000000000.0, 2), 'I-135': (21000000000000000.0, 2), 'Xe-133': (4.49e+17, 1), 'Kr-88': (14500000000000000.0, 1), 'I-132': (16000000000000000.0, 2), 'Te-132': (6500000000000000.0, 2), 'I-134': (24600000000000000.0, 2), 'Sr-89': (13500000000000000.0, 2), 'Kr-87': (98400000000000000.0, 1)}, 'lon1': 14.3754, 'lon0': 14.3754}], [{'lat1': 49.1817, 'lat0': 49.1817, 'h0': 50, 'h1': 50, 'inventory': {'Kr-85m': (2680000000000000.0, 1), 'Cs-136': (315000000000000.0, 2), 'Sr-90': (60300000000000.0, 2), 'Cs-134': (1310000000000000.0, 2), 'I-133': (6400000000000000.0, 2), 'Xe-135': (5450000000000000.0, 1), 'I-131': (3150000000000000.0, 2), 'Cs-137': (823000000000000.0, 2), 'I-135': (6000000000000000.0, 2), 'Xe-133': (25800000000000000.0, 1), 'Kr-88': (8300000000000000.0, 1), 'I-132': (4550000000000000.0, 2), 'Te-132': (1100000000000000.0, 2), 'I-134': (7000000000000000.0, 2), 'Sr-89': (563000000000000.0, 2), 'Kr-87': (5630000000000000.0, 1)}, 'lon1': 14.3754, 'lon0': 14.3754}], [{'lat1': 49.1817, 'lat0': 49.1817, 'h0': 50, 'h1': 50, 'inventory': {'Kr-85m': (2680000000000000.0, 1), 'Cs-136': (315000000000000.0, 2), 'Sr-90': (60300000000000.0, 2), 'Cs-134': (1310000000000000.0, 2), 'I-133': (6400000000000000.0, 2), 'Xe-135': (5450000000000000.0, 1), 'I-131': (3150000000000000.0, 2), 'Cs-137': (823000000000000.0, 2), 'I-135': (6000000000000000.0, 2), 'Xe-133': (25800000000000000.0, 1), 'Kr-88': (8300000000000000.0, 1), 'I-132': (4550000000000000.0, 2), 'Te-132': (1100000000000000.0, 2), 'I-134': (7000000000000000.0, 2), 'Sr-89': (563000000000000.0, 2), 'Kr-87': (5630000000000000.0, 1)}, 'lon1': 14.3754, 'lon0': 14.3754}], [{'lat1': 49.1817, 'lat0': 49.1817, 'h0': 50, 'h1': 50, 'inventory': {'Kr-85m': (2680000000000000.0, 1), 'Cs-136': (315000000000000.0, 2), 'Sr-90': (60300000000000.0, 2), 'Cs-134': (1310000000000000.0, 2), 'I-133': (6400000000000000.0, 2), 'Xe-135': (5450000000000000.0, 1), 'I-131': (3150000000000000.0, 2), 'Cs-137': (823000000000000.0, 2), 'I-135': (6000000000000000.0, 2), 'Xe-133': (25800000000000000.0, 1), 'Kr-88': (8300000000000000.0, 1), 'I-132': (4550000000000000.0, 2), 'Te-132': (1100000000000000.0, 2), 'I-134': (7000000000000000.0, 2), 'Sr-89': (563000000000000.0, 2), 'Kr-87': (5630000000000000.0, 1)}, 'lon1': 14.3754, 'lon0': 14.3754}], [{'lat1': 49.1817, 'lat0': 49.1817, 'h0': 50, 'h1': 50, 'inventory': {'Kr-85m': (2680000000000000.0, 1), 'Cs-136': (315000000000000.0, 2), 'Sr-90': (60300000000000.0, 2), 'Cs-134': (1310000000000000.0, 2), 'I-133': (6400000000000000.0, 2), 'Xe-135': (5450000000000000.0, 1), 'I-131': (3150000000000000.0, 2), 'Cs-137': (823000000000000.0, 2), 'I-135': (6000000000000000.0, 2), 'Xe-133': (25800000000000000.0, 1), 'Kr-88': (8300000000000000.0, 1), 'I-132': (4550000000000000.0, 2), 'Te-132': (1100000000000000.0, 2), 'I-134': (7000000000000000.0, 2), 'Sr-89': (563000000000000.0, 2), 'Kr-87': (5630000000000000.0, 1)}, 'lon1': 14.3754, 'lon0': 14.3754}]], 't_average': 3600, 'time_step': 3600, 'calc_end': '20130315 120000', 'outgrid': {'numxgrid': 92, 'outlatleft': 35.0, 'outlonlower': -10.0, 'levels': (150,), 'dxoutlon': 0.5, 'numygrid': 61, 'dyoutlat': 0.5}, 'age_group': 5, 'calc_start': '20130315 000000', 'release_start': '20130315 000000', 'outgrid_nest': {'numxgrid': 101, 'outlatleft': 45.0, 'outlonlower': 10.0, 'dxoutlon': 0.1, 'numygrid': 157, 'dyoutlat': 0.064}, 'decay_chains': {}}

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
#TIME_INTEGRATED_CONCENTRATION_DIR = "Time_int_conc"  # (Bq*s/m3)
#TIME_INTEGRATED_CLOUDSHINE_DIR = "Time_int_cloud"  # (Sv)
#TIME_INTEGRATED_GROUNDSHINE_DIR = "Time_int_ground"  # (Sv)
#TIME_INTEGRATED_INHALATION_DIR = "Time_int_inhalation"  # (Sv)
#TIME_INTEGRATED_ALL_PATHWAYS_DIR = "Time_int_all_pathways" # (Sv)

ALL_NUCLIDES_IDENT = "all_nuclides"  # how to denote results summed over all nuclides?
