# -*- coding: utf-8 -*-
__author__ = 'radek hofman'


import rad_config as rcf
from mods.misc import *
import mods.read_header
import mods.read_grid
import mods.tools
import mods.rad_methods

from datetime import datetime as dt
from datetime import timedelta
import numpy
import scipy.io
import os
import logging  # let's log some shit...
today = dt.now().strftime("%Y-%m-%d")
logging.basicConfig(filename='3_log_%s.txt' % today, filemode='w', level=logging.DEBUG)

DEBUG_FMT = "%Y-%m-%d %H:%M"

def calculate_decay(ST, NUC_DB):
    """
    calculates decay of all nuclidesin th source term and gives basic radiological qunatities:
     (concentration)
     (time integrated concentration)
     (deposition)
     (time integrated deposition)

    NUC_DB contains radionuclide data
    :return:
    """

    sources = ST["sources"]

    #preparing time constants
    DATE_FMT = rcf.DATE_FORMAT
    calc_start = dt.strptime(ST["calc_start"], DATE_FMT)  # here assumed to conicide with end of chain reaction
    calc_end = dt.strptime(ST["calc_end"], DATE_FMT)
    release_start = dt.strptime(ST["release_start"], DATE_FMT)
#    release_end = dt.strptime(ST["release_end"], DATE_FMT)
    time_step_length = ST["time_step"]
    delta_step = timedelta(seconds=time_step_length)
    calc_dur = (calc_end - calc_start)
    total_steps_no = int((calc_dur.days * 24 * 3600 + calc_dur.seconds )/time_step_length)

    domain = rcf.DOMAIN

    #which nuclides do we have?
    nuclides_all = ST["sources"][0][0]["inventory"].keys()

    #we need also nuclides form dacay chains
    decay_chains = ST["decay_chains"]

    for entry in decay_chains.keys():
        nuclides_all.append(decay_chains[entry][0])

    nuclides_all = sorted(list(set(nuclides_all)), key=lambda nuc: nuc.split("-")[-1])

    print "All nuclides including those from ingrowth", nuclides_all
    logging.info("All nuclides including those from ingrowth: "+str(nuclides_all))

    #find out dimensions for products
    outgrids = (ST["outgrid"], ST["outgrid_nest"])
    dimx = int(outgrids[domain]["numxgrid"])
    dimy = int(outgrids[domain]["numygrid"])
    dimz = len(outgrids[0]["levels"])

    #fields for output quantities
    basic_products = {}
    for nuc in nuclides_all:
        basic_products[nuc] = {}
        #average concentration in time step Bq/m3
        basic_products[nuc]["conc"] = numpy.zeros((total_steps_no, dimx, dimy, dimz))
        #average deposition in time step Bq/m2
        basic_products[nuc]["depo"] = numpy.zeros((total_steps_no, dimx, dimy))


    #iteration over time steps, each time step can have more sources
    for t, step in enumerate(sources):

        print INFO+" Sources in time step %d = %d" % (t, len(step))
        logging.info("Sources in time step %d = %d" % (t, len(step)))

        #release dates are the same for all sources in this time step!
        curr_rel_start = release_start + t * delta_step  # current release start for this time step
        curr_rel_end = release_start + (t+1) * delta_step  # current release end for this time step

        logging.info("Release %s - %s" % (curr_rel_start.strftime(DEBUG_FMT), curr_rel_end.strftime(DEBUG_FMT)))

        #duration of this particula forward run
        this_calc_dur = (calc_end - curr_rel_start)
        this_rel_steps_no = (this_calc_dur.days * 24 * 3600 + this_calc_dur.seconds)/time_step_length
        steps_offset = total_steps_no - this_rel_steps_no

        for n, source in enumerate(step):
            #for each source we have gridded output in all time steps because
            #all can have a contribution from this release slot

            print INFO+"    Processing source term %d in time %d" % (n, t)
            logging.info("    Processing source term %d in time %d" % (n, t))

            release_path = rcf.TREE_PATH+rcf.RUN+os.sep+mods.tools.get_run_name(t, n)
            output_path = release_path+os.sep+"Output"
            print output_path
            header = mods.read_header.read_header(output_path, nested=domain)

            inventory = source["inventory"]

            #let's split nuclides to groups according to species
            #it will be a dictionary
            inv_nucl = inventory.keys()
            #which nuclides are which species (noble gases, aerosols)
            nuc_spec_groups = {}

            for nuc in inv_nucl:
                species = inventory[nuc][1]
                if not nuc_spec_groups.has_key(species):
                    nuc_spec_groups[species] = []

                nuc_spec_groups[species].append(nuc)

            print "Groups of species: "+str(nuc_spec_groups)
            logging.info("Groups of species: "+str(nuc_spec_groups))

            decay_chains_parents = decay_chains.keys()

            #iteration over time steps of output
            for s in range(this_rel_steps_no):
                #we add offset to not iterate over outputs BEFORE the release
                curr_output_end = calc_start + (steps_offset+s+1)*delta_step  # +1 to have the end interval
                curr_output_end_str = dt.strftime(curr_output_end, files_fmt)

                #times important for calculation of decay, calc_start coincides here with end of chain reaction
                t1_delta = (steps_offset+s)*delta_step  # (curr_rel_start-calc_start).days * 24 * 3600 + (curr_rel_start-calc_start).seconds
                t2_delta = (steps_offset+s+1)*delta_step  # (curr_rel_end-calc_start).days * 24 * 3600 + (curr_rel_end-calc_start).seconds

                t1 = t1_delta.days * 24 * 3600 + t1_delta.seconds
                t2 = t2_delta.days * 24 * 3600 + t2_delta.seconds

                #finally, a loop over species groups:
                for gi in nuc_spec_groups.keys():  # gi = group index
                    #group contains all nuclides of particular type (noble, aerosol)
                    group = nuc_spec_groups[gi]
                    #we load the correct file:
                    #date of the file is the end date of the interval
                    spec_ident = "%3.3d" % int(gi)  # species identifier
                    file_path = output_path+os.sep+grid_names[domain]+curr_output_end_str+"_"+spec_ident

                    logging.debug("Opening file "+file_path)

                    #load all fields from file
                    grid, wetdep, drydep, itime = mods.read_grid._readgridBF(header, file_path)
                    #we are intereseted in summed deposition only
                    total_depo = drydep[:,:,0,0] + wetdep[:,:,0,0]  # there is just 1 level - the ground

                    logging.debug("   Applying radioactive decay")
                    for nuc in group:
                        logging.debug("      "+nuc)
                        halflife = NUC_DB[nuc]['halflife']  # physical halflife of a nuclide
                        lamb = mods.rad_methods.get_lambda(halflife)  # decay constant in seconds, everything is in seconds

                        raddecay = mods.rad_methods.decay(t1, t2, lamb)

                        ###print nuc, lamb, s+steps_offset, raddecay, t1, t2

                        release = inventory[nuc][0]

                        #we apply FP_SCALING = Flexpart scaling 1e-12
                        #this will give us an AVERAGE concentration over the time step including decay!
                        #we have the same basic product fields for releases at all times
                        basic_products[nuc]["conc"][s,:,:,:] += grid[:,:,:,0,0] * raddecay * release * FP_SCALING

                        #the same for deposition, noble gases are ignored
                        #if NUC_DB[nuc]['ground'] != -999: - commented now, it is zero anyway for NG
                        basic_products[nuc]["depo"][s,:,:] += total_depo * raddecay * release * FP_SCALING

                    #and now produce possible daughter nuclide from parent nuclides
                    logging.debug("   Applying decay Chains:")
                    for pnuc in decay_chains_parents:  # pnuc = parent nuclide
                        if pnuc in group:  # we are interested just in parent nuclides from particular group
                            dec_chain = ST["decay_chains"][pnuc]
                            dnuc = dec_chain[0]  # daughter nuclide
                            logging.debug("      "+pnuc+"-->"+dnuc)
                            branch = dec_chain[1]  # branching ratio of the chain
                            halflife_p = NUC_DB[pnuc]['halflife']
                            halflife_d = NUC_DB[dnuc]['halflife']
                            lamb_p = mods.rad_methods.get_lambda(halflife_p)
                            lamb_d = mods.rad_methods.get_lambda(halflife_d)

                            #decay of parent into daughter
                            raddecay_p2d = mods.rad_methods.decay_2(t1, t2, lamb_p, lamb_d, branch)
                            release_p = inventory[pnuc][0] * raddecay_p2d
                            basic_products[dnuc]["conc"][s,:,:,:] += grid[:,:,:,0,0] * release_p * FP_SCALING

                            #we do not do production of noble gas daughters for noble gases
                            if NUC_DB[dnuc]['ground'] != -999:  # this is how we recognize NGs
                                basic_products[dnuc]["depo"][s,:,:] += total_depo * release_p * FP_SCALING

                            #NOTE: pnuc decays in the section above, the same with already existing daughter nuclides

    #important parameters of our domain which we save with data
    numxgrid = int(outgrids[domain]["numxgrid"])
    numygrid = int(outgrids[domain]["numygrid"])
    dxout = outgrids[domain]["dxoutlon"]
    dyout = outgrids[domain]["dyoutlat"]
    outlon0 = outgrids[domain]["outlonlower"]
    outlat0 = outgrids[domain]["outlatleft"]
    outlon1 = outlon0+(numxgrid-1)*dxout
    outlat1 = outlat0+(numygrid-1)*dyout
    levels = outgrids[0]["levels"]

    print "Exporting basic products into matfiles..."

    nuclides = basic_products.keys()
    output_dirs_basic = (rcf.CONCENTRATION_DIR, rcf.DEPOSITION_DIR)
    for nuc in nuclides:
        for i, prod in enumerate(('conc', 'depo')):
            data = basic_products[nuc][prod]
            #print data.shape
            opath = rcf.OUTPUT_PATH+os.sep+output_dirs_basic[i]
            if not os.path.exists(opath):
                os.makedirs(opath)
            scipy.io.savemat(opath+os.sep+nuc, \
                              {"data": data,
                               "numxgrid": numxgrid,
                               "numygrid": numygrid,
                               "dxout": dxout,
                               "dyout": dyout,
                               "outlon0": outlon0,
                               "outlat0": outlat0,
                               "outlon1": outlon1,
                               "outlat1": outlat1,
                               "levels": levels,
                               "time_step_length": time_step_length
                              },
                              do_compression=True)

    print "Done"

if __name__ == "__main__":
    ST = rcf.SOURCE_TERM
    NUC_DB = rcf.DB.d
    calculate_decay(ST, NUC_DB)

