# -*- coding: utf-8 -*-
__author__ = 'radek hofman'


import rad_config as rcf
import os
import shutil
import mods.tools
from datetime import datetime as dt
import datetime

FP_DATE_FMT = "%Y%m%d %H%M%S"  # flexpart date format


def create_levels_in_outgrid(levels):
    """

    :return:

    sample levels in outgrid looks like:
    10. -----.-           4X, F7.1
          100.0
        LEVEL 1           HEIGHT OF LEVEL (UPPER BOUNDARY)

    10. -----.-           4X, F7.1
          500.0
        LEVEL 2           HEIGHT OF LEVEL (UPPER BOUNDARY)

    10. -----.-           4X, F7.1
         1000.0
        LEVEL 3           HEIGHT OF LEVEL (UPPER BOUNDARY)

    10. -----.-           4X, F7.1
         1500.0
        LEVEL 4           HEIGHT OF LEVEL (UPPER BOUNDARY)

    10. -----.-           4X, F7.1
         2000.0
        LEVEL 5           HEIGHT OF LEVEL (UPPER BOUNDARY)
        """

    ret = ""

    for i, level in enumerate(levels):
        ret += """10. -----.-           4X, F7.1
      %10.2f
    LEVEL %d           HEIGHT OF LEVEL (UPPER BOUNDARY)

""" % (level, i+1)

    return ret


def paste_into_template(template, dict_of_values):
    """
    pastes dict values into a template according to keys similarly to Genshi
    """

    for key in dict_of_values.keys():
        template = template.replace("$"+key, str(dict_of_values[key]))

    return template

def create_outgrid_file(outgrid, outgrid_path):
    """
    creates outgrid file
    """

    with open(rcf.TEMPLATES+os.sep+'outgrid.tmpl', "r+") as f:
        s = f.read()
        d = {"outlonlower": "%10.2f" % outgrid["outlonlower"],
             "outlatleft": "%10.2f" % outgrid["outlatleft"],
             "numxgrid": "%d" % int(outgrid["numxgrid"]),
             "numygrid": "%d" % int(outgrid["numygrid"]),
             "dxoutlon": "%10.2f" % outgrid["dxoutlon"],
             "dyoutlat": "%10.2f" % outgrid["dyoutlat"],
             "levels": create_levels_in_outgrid(outgrid["levels"]),
             }

        s = paste_into_template(s, d)

    #writing into file
    with open(outgrid_path, "w+") as f:
        f.write(s)

def create_outgrid_nest_file(outgrid_nest, outgrid_nest_path):
    """
    creates outgrid_nest file
    """

    with open(rcf.TEMPLATES+os.sep+'outgrid_nest.tmpl', "r+") as f:
        s = f.read()
        d = {"outlonlower": "%10.2f" % outgrid_nest["outlonlower"],
             "outlatleft": "%10.2f" % outgrid_nest["outlatleft"],
             "numxgrid": "%d" % int(outgrid_nest["numxgrid"]),
             "numygrid": "%d" % int(outgrid_nest["numygrid"]),
             "dxoutlon": "%10.2f" % outgrid_nest["dxoutlon"],
             "dyoutlat": "%10.2f" % outgrid_nest["dyoutlat"]
             }

        s = paste_into_template(s, d)


    #writing into file
    with open(outgrid_nest_path, "w+") as f:
        f.write(s)


def create_command_file(this_rel_start, calc_end, time_step_length, t_average, comm_path):
    """
    writes command file for each release
    """

    #using command file template from templates directory
    with open(rcf.TEMPLATES+os.sep+'command.tmpl', "r+") as f:
        s = f.read()
        d = {"simul_start": mods.tools.make_flexpart_date(this_rel_start),
             "simul_end": mods.tools.make_flexpart_date(calc_end),
             "time_step": str(time_step_length),
             "t_average": str(t_average)
             }

        s = paste_into_template(s, d)


    #writing into file
    with open(comm_path, "w+") as f:
        f.write(s)


def create_release_file(source, spec_dict, this_rel_start, this_rel_end, t, n, rel_path):
    """
    writes command file for each release

    one time step can have multiple releases (different nuclides in different height)
    releases with just a different species can be calculated using a single run
    samples source:
                    {"lat0":lat0,  # source 1 for time step 1
                      "lon0":lon0,
                      "lat1":lat1,
                      "lon1":lon1,
                      "h0":  0,  # bottom of layer in meters
                      "h1": 50,  # top of layer in meters
                      "inventory": {"Cs-137": (1e10, 16), "I-131": (1e11, 16), "Xe-133": (1e10, 1)}  # (release, species)
                     }

    glob_rel_start: global release start, in combination with time step and its length serves
     for calculation of particular release period

    """

    inventory = source["inventory"]
    spec_types = []
    species = inventory.keys()
    for spec in species:
        #release_magnitude = inventory[spec][0]
        spec_type = spec_dict[inventory[spec][1]]
        spec_types.append(spec_type)

    spec_types = sorted(list(set(spec_types)))

    spec_no = len(spec_types)
    specs = ""
    mps = ""
    for spec_type in spec_types:
        specs += str(spec_type)+"\n"
        mps += str(1.0)+"\n"

    #using command file template from templates directory
    with open(rcf.TEMPLATES+os.sep+'releases_universal.tmpl', "r+") as f:
        s = f.read()
        d = {"spec_no": spec_no,
             "specs": specs,
             "rel_start": this_rel_start.strftime(FP_DATE_FMT),
             "rel_end":  this_rel_end.strftime(FP_DATE_FMT),
             "x0": source["lon0"],
             "x1": source["lon1"],
             "y0": source["lat0"],
             "y1": source["lat1"],
             "z1": "%10.2f" % source["h0"],
             "z2": "%10.2f" % source["h1"],
             "parts_number": rcf.PART_NUMBER,
             "mass_per_spec": mps,
             "comment": "time %4.4d source %4.4d" % (t, n)
             }

        s = paste_into_template(s, d)

    #writing into file
    with open(rel_path, "w+") as f:
        f.write(s)


def create_pathnames(path):
    """
    creates the file pathnames at "path"
    """
    s = ""

    s += "."+os.sep+"Options"+os.sep+"\n"
    s += "."+os.sep+"Output"+os.sep+"\n"
    s += rcf.METEO_PATH+"\n"
    s += rcf.AVAILABLE

    with open(path+os.sep+"pathnames", "w+") as f:
        f.write(s)


def make_tree(ST):
    """
    prepares a directory structure for forward run and subsequent calculation of doses

    ST : JSON with source term structure
    """

    sources = ST["sources"]

    #preparing time constants
    DATE_FMT = rcf.DATE_FORMAT
    calc_start = dt.strptime(ST["calc_start"], DATE_FMT)
    calc_end = dt.strptime(ST["calc_end"], DATE_FMT)
    release_start = dt.strptime(ST["release_start"], DATE_FMT)
#    release_end = dt.strptime(ST["release_end"], DATE_FMT)
    time_step_length = ST["time_step"]
    delta_step = datetime.timedelta(seconds=time_step_length)
#    rel_dur = (release_end - release_start)
#    steps = (rel_dur.days * 24 * 3600 + rel_dur.seconds )/time_step_length
    tree_path = rcf.TREE_PATH+os.sep+rcf.RUN
    t_average = ST["t_average"]
    spec_dict = ST["species_dict"]

    #creating the tree root
    if os.path.exists(tree_path):
        print  "Removing previous run tree..."
        shutil.rmtree(tree_path)

    print "Creating a new tree of runs..."
    os.makedirs(tree_path)

    #building run tree in tree root
    for t, step in enumerate(sources):

        print "Sources in time step %d = %d" % (t, len(step))

        #release dates are the same for all sources in this time step!
        curr_rel_start = release_start + t * delta_step  # current release start for this time step
        curr_rel_end = release_start + (t+1) * delta_step  # current release end for this time step

        for n, source in enumerate(step):
            dir_name = mods.tools.get_run_name(t, n)
            release_path = tree_path+os.sep+dir_name
            os.makedirs(release_path)

            #pathnames file
            create_pathnames(release_path)

            #now we populate each run in the tree with data
            os.makedirs(release_path+os.sep+"Output")
            options_path = release_path+os.sep+"Options"
            os.makedirs(options_path)

            this_rel_start = release_start + t * delta_step
            this_rel_end = release_start + (t+1) * delta_step

            #create COMMAND file
            comm_path = options_path+os.sep+"COMMAND"
            #we use this_rel_start in order not to calculate periods with no release
            create_command_file(this_rel_start, calc_end, time_step_length, t_average, comm_path)

            #create RELEASES file
            rel_path = options_path+os.sep+"RELEASES"
            create_release_file(source, spec_dict, this_rel_start, this_rel_end, t, n, rel_path)

            #create OUTGRID file
            outgrid_path = options_path+os.sep+"OUTGRID"
            create_outgrid_file(ST["outgrid"], outgrid_path)

            #create OUTGRID_NEST file
            outgrid_nest_path = options_path+os.sep+"OUTGRID_NEST"
            create_outgrid_nest_file(ST["outgrid_nest"], outgrid_nest_path)

            #make symlinks of all static files
            static_files = os.listdir(rcf.STATIC)
            for sfile in static_files:
                ssrc = rcf.STATIC+os.sep+sfile
                sdst = options_path+os.sep+sfile
                os.symlink(ssrc, sdst)

            #create symlink of Flexpart executable
            flex_src = rcf.FLEXPART_PATH
            flex_dst = release_path+os.sep+rcf.FLEXPART_NAME
            os.symlink(flex_src, flex_dst)


if __name__ == "__main__":
    ST = rcf.SOURCE_TERM
    make_tree(ST)