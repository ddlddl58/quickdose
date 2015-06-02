# -*- coding: utf-8 -*-
__author__ = 'radek hofman'

import rad_config as rcf

from datetime import datetime as dt
import numpy
import os
import scipy.io
import logging  # let's log some shit...
today = dt.now().strftime("%Y-%m-%d")
logging.basicConfig(filename='4_log_%s.txt' % today, filemode='w', level=logging.DEBUG)

def prepare_data_dict(outgrids, domain, time_step_length, data):
    """
    prepares a dictionary to save with data including domain-related info
    """
    numxgrid = int(outgrids[domain]["numxgrid"])
    numygrid = int(outgrids[domain]["numygrid"])
    dxout = outgrids[domain]["dxoutlon"]
    dyout = outgrids[domain]["dyoutlat"]
    outlon0 = outgrids[domain]["outlonlower"]
    outlat0 = outgrids[domain]["outlatleft"]
    outlon1 = outlon0+(numxgrid-1)*dxout
    outlat1 = outlat0+(numygrid-1)*dyout
    levels = outgrids[0]["levels"]

    d = {"data": data,
        "numxgrid": numxgrid,
        "numygrid": numygrid,
        "dxout": dxout,
        "dyout": dyout,
        "outlon0": outlon0,
        "outlat0": outlat0,
        "outlon1": outlon1,
        "outlat1": outlat1,
        "levels": levels,
        "time_step_length": time_step_length}

    return d

def calc_dose_rates(ST, NUC_DB, BR):
    """
    Dose rate from external sources:

        EXT - external dose from cloudshine of groundshine
        EC - conversion coefficient for cloud or deposition

        EXT = C(t) * EC

    Committed effective dose rate due to inhalation INH (Sv/s):

        BR - breathing rate (ventilation) (m3/s)
        C(t) - concentration in air (Bq/m3)
        DC - nuclide specific conversion coefficient for inhalation

        INH = C(t) * BR * DC

    dose rates are stored in one array GDR

    GDR = numpy.zeros((nuclide_count, 3, dimx, dimy, total_steps_no))
    # 0 - cloudshine, 1 - groundshine, 2 - deposition
    """

    #domain related data which we save along with data
    domain = rcf.DOMAIN
    outgrids = (ST["outgrid"], ST["outgrid_nest"])
    dimx = int(outgrids[domain]["numxgrid"])
    dimy = int(outgrids[domain]["numygrid"])
    #we do not need dimz, we always use the ground level

    #preparing time constants
    DATE_FMT = rcf.DATE_FORMAT
    calc_start = dt.strptime(ST["calc_start"], DATE_FMT)  # here assumed to conicide with end of chain reaction
    calc_end = dt.strptime(ST["calc_end"], DATE_FMT)
    time_step_length = ST["time_step"]
    calc_dur = (calc_end - calc_start)
    total_steps_no = int((calc_dur.days * 24 * 3600 + calc_dur.seconds )/time_step_length)

    #which age group do we want?
    age_group = ST["age_group"]

    #which nuclides do we have?
    nuclides_all = ST["sources"][0][0]["inventory"].keys()
    ncount = len(nuclides_all)  # nuclides count

    #common field for all nuclides and GDR types
    # 0 - cloudshine, 1 - groundshine, 2 - inhalation
    GDR = numpy.zeros((ncount, 3, total_steps_no, dimx, dimy))

    #correction factor for cloudshine and groundshine for the first two agegroups
    corr_fact = 1.0
    if age_group < 2:
        corr_fact = 1.5

    print "Calculatinng doses"
    logging.info("Calculatinng doses")

    for n, nuclide in enumerate(nuclides_all):
        print "    Processing nuclide no. %d: %s" % (n, nuclide)
        logging.info("    Processing nuclide no. %d: %s" % (n, nuclide))

        conc_path = rcf.OUTPUT_PATH+os.sep+rcf.CONCENTRATION_DIR
        depo_path = rcf.OUTPUT_PATH+os.sep+rcf.DEPOSITION_DIR

        #concentration and deposition dictionaries
        conc = scipy.io.loadmat(conc_path+os.sep+nuclide)["data"]
        depo = scipy.io.loadmat(depo_path+os.sep+nuclide)["data"]

        #dose conversion coefficients
        coef_cloud = NUC_DB[nuclide]["cloud"] * corr_fact
        coef_depo = max(NUC_DB[nuclide]["ground"] * corr_fact, 0.)  # for noble gasses -999
        coef_inhal = max(NUC_DB[nuclide]["inhalation"][age_group], 0.)  # for noble gasses -999

        #cloushine dose
        GDR[n,0,:,:,:] = conc[:,:,:,0] * coef_cloud # we take the ground level
        #groundshine
        GDR[n,1,:,:,:] = depo[:,:,:] * coef_depo
        #inhalation dose
        GDR[n,2,:,:,:] = conc[:,:,:,0] * BR * coef_inhal  # we take the ground level

    #now we save results to fields
    output_dirs_gdr = (rcf.CLOUDSHINE_DIR, rcf.GROUNDSHINE_DIR, rcf.INHALATION_DIR)

    #nuclide specific GDR outputs
    for n, nuclide in enumerate(nuclides_all):
        print "    Saving dose rates for nuclide no. %d: %s" % (n, nuclide)
        logging.info("    Saving dose rates for nuclide no. %d: %s" % (n, nuclide))

        #nuclide specific and pathway specific results
        for gdr_type in range(3): # 0 - cloudshine, 1 - groundshine, 2 - inhalation
            opath = rcf.OUTPUT_PATH+os.sep+output_dirs_gdr[gdr_type]
            if not os.path.exists(opath):
                os.makedirs(opath)
            data = GDR[n,gdr_type,:,:,:]
            scipy.io.savemat(opath+os.sep+nuclide,
                             prepare_data_dict(outgrids, domain, time_step_length, data),
                             do_compression=True)

        #nuclide spcific, all pathways summed up
        opath = rcf.OUTPUT_PATH+os.sep+rcf.ALL_PATHWAYS_DIR
        if not os.path.exists(opath):
            os.makedirs(opath)

        data = numpy.sum(GDR[n,:,:,:,:], axis=0)

        scipy.io.savemat(opath+os.sep+nuclide,
                         prepare_data_dict(outgrids, domain, time_step_length, data),
                         do_compression=True)

    print "    Saving dose rates summed over nuclides"
    logging.info("    Saving dose rates summed over nuclides")
    #results integrated over nulides
    for gdr_type in range(3): # 0 - cloudshine, 1 - groundshine, 2 - inhalation
        opath = rcf.OUTPUT_PATH+os.sep+output_dirs_gdr[gdr_type]
        data = numpy.sum(GDR[:,gdr_type,:,:,:], axis=0)
        scipy.io.savemat(opath+os.sep+rcf.ALL_NUCLIDES_IDENT,
                         prepare_data_dict(outgrids, domain, time_step_length, data),
                         do_compression=True)

    #summed over nuclides and over all pathways
    opath = rcf.OUTPUT_PATH+os.sep+rcf.ALL_PATHWAYS_DIR
    data = numpy.sum(numpy.sum(GDR[:,:,:,:,:], axis=0), axis=0)
    scipy.io.savemat(opath+os.sep+rcf.ALL_NUCLIDES_IDENT,
                     prepare_data_dict(outgrids, domain, time_step_length, data),
                     do_compression=True)

    print "Done!"
    return GDR


def calc_doses():
    """
    time integration of GDR
    """

if __name__ == "__main__":
    #so, let's calculate some derived radiological quantities, cho cho cho!
    ST = rcf.SOURCE_TERM
    BREATHING_RATE = rcf.DB.breathing_rates[ST["age_group"]] / (24.*60.*60.)  # (m3/s)
    NUC_DB = rcf.DB.d
    #we calculate and save gamma dose rates
    GDR = calc_dose_rates(ST, NUC_DB, BREATHING_RATE)
    #now we can integrate gamma dose rates to obtain some doses
    calc_doses(GDR, ST, NUC_DB, BREATHING_RATE)







