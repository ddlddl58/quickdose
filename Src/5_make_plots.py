# -*- coding: utf-8 -*-
__author__ = 'radek hofman'

import rad_config as rcf
import plt_config as pcf
#import mods.vizu.plotters as plotters

import matplotlib.pyplot as plt
from datetime import datetime as dt
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import LogNorm, Normalize
import numpy
import scipy.io
import os
import logging
today = dt.now().strftime("%Y-%m-%d")
logging.basicConfig(filename='5_log_%s.txt' % today, filemode='w', level=logging.DEBUG)
import math
from mods.misc import *
import datetime

def create_colorbar(c1, nuclide, outpath, unitlabel):
    """
    creates only colorbar of given range
    """
    fig = plt.figure()
    ax = fig.add_axes([0.05, 0.80, 0.9, 0.05])
    try:
        cbar = plt.colorbar(c1, cax=ax, orientation='horizontal', cmap=pcf.C_MAP)
        cbar.set_label(unitlabel)
    except:
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.set_frame_on(False)
        print "No data > 0, no colorabar, saving empty figure..."

    plt.savefig(outpath+os.sep+"colorbar_%s.svg" % nuclide,  bbox_inches='tight', pad_inches=0, transparent=True)
    plt.close(fig)


def plot_field(path, image_outpath, unitlabel, product_name):
    """
    :return:

    """

    """
    creates single frame (from one flepart output file)
    time step is given by the file
    spatial domain is given by lon0, lon1, lat0, lat1, z0, z1

            |-----------------lon1, lat1
            |                     |
            |                     |
        lon0, lat0 ---------------|

    z0 is lower vertica level, z1 is the upper


    Developer note..:

        For most map projections, the map projection region can either be specified by setting these keywords:

        Keyword    Description
        llcrnrlon    longitude of lower left hand corner of the desired map domain (degrees).
        llcrnrlat    latitude of lower left hand corner of the desired map domain (degrees).
        urcrnrlon    longitude of upper right hand corner of the desired map domain (degrees).
        urcrnrlat    latitude of upper right hand corner of the desired map domain (degrees).
        or these

        Keyword    Description
        width    width of desired map domain in projection coordinates (meters).
        height    height of desired map domain in projection coordinates (meters).
        lon_0    center of desired map domain (in degrees).
        lat_0    center of desired map domain (in degrees).


        resolution:  c (crude), l (low), i (intermediate), h (high), f (full)
        more at http://matplotlib.org/basemap/api/basemap_api.html
    """

    d = scipy.io.loadmat(path)

    numxgrid = d["numxgrid"][0,0]
    numygrid = d["numygrid"][0,0]
    dxout = d["dxout"][0,0]
    dyout = d["dyout"][0,0]
    outlon0 = d["outlon0"][0,0]
    outlat0 = d["outlat0"][0,0]
    outlon1 = d["outlon1"][0,0]
    outlat1 = d["outlat1"][0,0]
    levels = d["levels"]
    time_step = d["time_step_length"][0,0]
    data0 = d["data"]

    logging.debug("domain: %6.2f-%6.2f %6.2f %6.2f" % (outlon0, outlon1, outlat0, outlat1))

    #this is better I think than the originla script
    lons0 = numpy.linspace(outlon0, outlon1, numxgrid)
    lats0 = numpy.linspace(outlat0, outlat1, numygrid)
    lons, lats = numpy.meshgrid(lons0, lats0)

    #"canvas" ready, now let's plot something
    steps = data0.shape[0]

    nuclide = path.split(os.sep)[-1].split(".")[0]

    if pcf.MAX_D != -999:
        max_d = pcf.MAX_D
    else:
        if len(data0.shape) == 4:
            max_d = data0[:,:,:,0].max()
        elif len(data0.shape) == 3:
            max_d = data0[:,:,:].max()


    print INFO+"Processing: %s" % (nuclide)


    fig = plt.figure(figsize=(pcf.FIG_X,pcf.FIG_Y))


    if pcf.DO_OVERLAY:
        #fig = plt.figure(figsize=(15,15), dpi=400)
        ax = fig.add_axes([0., 0., 1., 1.])
        #ax = axes([0,0,1,1], frameon=False)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.set_frame_on(False)

        map = Basemap(projection=pcf.PROJECTION,
                    llcrnrlon = outlon0, llcrnrlat = outlat0,
                    urcrnrlon = outlon1, urcrnrlat = outlat1,
                    resolution=pcf.BASEMAP_RESOLUTION, area_thresh=pcf.BASEMAP_AREA_THR,ax=ax)
    else:
        map = Basemap(projection=pcf.PROJECTION,
                    llcrnrlon = outlon0, llcrnrlat = outlat0,
                    urcrnrlon = outlon1, urcrnrlat = outlat1,
                    resolution=pcf.BASEMAP_RESOLUTION, area_thresh=pcf.BASEMAP_AREA_THR)


    #now we create a mesh for plotting data
    x, y = map(lons, lats)

    release_start_str = rcf.SOURCE_TERM["release_start"]
    release_start = dt.strptime(release_start_str, rcf.DATE_FORMAT)
    delta_step = datetime.timedelta(seconds=rcf.SOURCE_TERM["time_step"])

    c1 = False

    for t in range(steps):
        #clear the previous image, we use the same figure and Basemap instance
        if not pcf.DO_OVERLAY:
            plt.clf()


        if len(data0.shape) == 4:
            data = data0[t,:,:,0].transpose()
        elif len(data0.shape) == 3:
            data = data0[t,:,:].transpose()

        if max_d > 0:

            log_max = math.ceil(math.log10(max_d))

            levels = numpy.logspace(log_max-pcf.NUMBER_OF_ORDERS, log_max, 4*pcf.NUMBER_OF_ORDERS+1)

            #if c1: # remove old plot in OVERLAY mode
            #    c1.remove()
            if data.max() > 0.:
                if pcf.DO_OVERLAY:
                    ax.clear()

                """ # huuuuge SVGs :(
                c1 = map.pcolormesh(x, y, data,
                                  #shading='gouraud',
                                  norm=LogNorm(vmin=levels[0], vmax=levels[-1]),
                                  cmap=pcf.C_MAP,
                                  alpha=pcf.ALPHA)

                """
                c1 = map.contourf(x, y, data,
                                  #shading='gouraud',
                                  levels = levels,
                                  norm=LogNorm(vmin=levels[0], vmax=levels[-1]),
                                  cmap=pcf.C_MAP,
                                  alpha=pcf.ALPHA)

                """
                c1 = map.contour(x, y, data,
                                  #shading='gouraud',
                                  levels = levels,
                                  norm=LogNorm(vmin=levels[0], vmax=levels[-1]),
                                  cmap=pcf.C_MAP,
                                  alpha=1.0)
                """
                """ # cannot be used with mercator, uniform grid does not fit
                outlon0m, outlat0m = map(outlon0, outlat0)
                outlon1m, outlat1m = map(outlon1, outlat1)

                c1 = map.imshow(data,
                          interpolation='nearest',
                          extent=(outlon0m, outlon1m, outlat0m, outlat1m),
                          origin='lower',
                          norm=LogNorm(vmin=levels[0], vmax=levels[-1]),
                          cmap=pcf.C_MAP,
                          alpha=pcf.ALPHA)
                """

                if not pcf.DO_OVERLAY:
                    cbar = map.colorbar(c1, location="bottom", pad="7%")
                    cbar.set_label(unitlabel)


        par_step = pcf.NESTED_PAR_STEP
        mer_step = pcf.NESTED_MER_STEP

        if not pcf.DO_OVERLAY:

            parallels = numpy.arange(-90., 90., par_step)
            map.drawparallels(parallels, labels=[True, False, False, True], fontsize=10)

            # draw meridians
            meridians = numpy.arange(-180.0, 180.0, mer_step)
            map.drawmeridians(meridians, labels=[True, False, False, True], fontsize=10)

            map.drawcoastlines()
            map.drawcountries()

        out_fname = nuclide+"_t=%3.3d" % t

        date = release_start+t*delta_step

        if not pcf.DO_OVERLAY:
            plt.title(product_name+" of "+nuclide+" "+date.strftime("(%Y-%m-%d %H:%M)"))

        if pcf.PDFS_FLAG: #pdfs will be also saved
            out_fname += ".pdf"
        if pcf.JPGS_FLAG: #produce JPGs?
            out_fname += ".jpeg"
        if pcf.PNGS_FLAG: #produce PNGs?
            out_fname += ".png"
        if pcf.SVGS_FLAG: #produce PNGs?
            out_fname += ".svg"



        print "Saving to ", image_outpath+os.sep+out_fname

        if pcf.TIGHT_LAYOUT or pcf.DO_OVERLAY:
            plt.savefig(image_outpath+os.sep+out_fname, bbox_inches='tight', pad_inches=0, transparent=True)
        else:
            plt.savefig(image_outpath+os.sep+out_fname,  transparent=True)

    if pcf.DO_OVERLAY:
        create_colorbar(c1, nuclide, image_outpath, unitlabel)

    plt.close(fig)

def plot_results():
    """
    plots all results in OUTPUT_PATH
    :return:
    """

    data_paths = (rcf.OUTPUT_PATH+os.sep+rcf.CONCENTRATION_DIR,
                rcf.OUTPUT_PATH+os.sep+rcf.DEPOSITION_DIR,
                rcf.OUTPUT_PATH+os.sep+rcf.CLOUDSHINE_DIR,
                rcf.OUTPUT_PATH+os.sep+rcf.GROUNDSHINE_DIR,
                rcf.OUTPUT_PATH+os.sep+rcf.INHALATION_DIR,
                rcf.OUTPUT_PATH+os.sep+rcf.ALL_PATHWAYS_DIR,)

    image_paths = (rcf.IMAGES_PATH+os.sep+rcf.CONCENTRATION_DIR,
                rcf.IMAGES_PATH+os.sep+rcf.DEPOSITION_DIR,
                rcf.IMAGES_PATH+os.sep+rcf.CLOUDSHINE_DIR,
                rcf.IMAGES_PATH+os.sep+rcf.GROUNDSHINE_DIR,
                rcf.IMAGES_PATH+os.sep+rcf.INHALATION_DIR,
                rcf.IMAGES_PATH+os.sep+rcf.ALL_PATHWAYS_DIR,)

    unitlabels = (r"$Bq/m$^3$",
                  r"$Bq/m$^2$",
                  r"$Sv/s$",
                  r"$Sv/s$",
                  r"$Sv/s$",
                  r"$Sv/s$")

    product_names = ("Activity concentration",
                    "Deposition",
                    "Cloudshine dose rate",
                    "Groundshine dose rate",
                    "Inhalation dose rate",
                    "All pathways (cloud+ground+inhalation) dose rate")

    print "Creating plots..."

    for i, o, u, p in zip(data_paths, image_paths, unitlabels, product_names):
        files = os.listdir(i)
        files = filter(lambda x:  x.endswith(".mat"), files)

        if not os.path.exists(o):
            os.makedirs(o)

        for file in files:
            plot_field(i+os.sep+file, o, u, p)

if __name__ == "__main__":
    plot_results()