#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

 CERN@school - Make Plots

 See the README.md file and the GitHub wiki for more information.

 http://cernatschool.web.cern.ch

"""

# Import the code needed to manage files.
import os, glob

#...for parsing the arguments.
import argparse

#...for the logging.
import logging as lg

#...for file manipulation.
from shutil import rmtree

# Import the JSON library.
import json

#...for the histograms.
from plotting.histograms import Hist, Hist2D

if __name__ == "__main__":

    print("*")
    print("*==============================*")
    print("* CERN@school - make the plots *")
    print("*==============================*")

    # Get the datafile path from the command line.
    parser = argparse.ArgumentParser()
    parser.add_argument("inputPath",       help="Path to the input dataset.")
    parser.add_argument("outputPath",      help="The path for the output files.")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    args = parser.parse_args()

    ## The path to the data file.
    datapath = args.inputPath

    ## The output path.
    outputpath = args.outputPath

    # Set the logging level.
    if args.verbose:
        level=lg.DEBUG
    else:
        level=lg.INFO

    # Configure the logging.
    lg.basicConfig(filename=outputpath + '/log_make-plots.log', filemode='w', level=level)

    print("*")
    print("* Input path          : '%s'" % (datapath))
    print("* Output path         : '%s'" % (outputpath))
    print("*")


    # Set up the directories
    #------------------------

    # Check if the output directory exists. If it doesn't, quit.
    if not os.path.isdir(outputpath):
        raise IOError("* ERROR: '%s' output directory does not exist!" % (outputpath))

    # Create the subdirectories.

    ## The path to the frame plots.
    fppath = outputpath + "/frameplots/"
    #
    if os.path.isdir(fppath):
        rmtree(fppath)
        lg.info(" * Removing directory '%s'..." % (fppath))
    os.mkdir(fppath)
    lg.info(" * Creating directory '%s'..." % (fppath))
    lg.info("")

    ## The path to the cluster plots.
    kppath = outputpath + "/clusterplots/"
    #
    if os.path.isdir(kppath):
        rmtree(kppath)
        lg.info(" * Removing directory '%s'..." % (kppath))
    os.mkdir(kppath)
    lg.info(" * Creating directory '%s'..." % (kppath))
    lg.info("")

    ## The frame properties JSON file - FIXME: check it exists...
    ff = open(datapath + "/frames.json", "r")
    #
    fd = json.load(ff)
    ff.close()

    ## The cluster properties JSON file - FIXME: check it exists...
    kf = open(datapath + "/klusters.json", "r")
    #
    kd = json.load(kf)
    kf.close()


    # The frames
    #------------

    ## The number of clusters per frame.
    ncs = []

    ## The number of non-gamma clusters per frame.
    nlcs = []

    ## The number of gamma candidates per frame.
    ngs = []

    # Loop over the frames.
    for f in fd:

        # Add to the frame property dictionaries.
        ncs.append( f["n_kluster"])
        nlcs.append(f["n_non_gamma"])
        ngs.append( f["n_gamma"])

    ## The number of clusters plot.
    nlcsplot = Hist("ncs", 101, ncs, -1, "Number of clusters", "Number of frames", fppath)

    ## The number of non-gamma clusters plot.
    ncsplot = Hist("nls", 102, nlcs, -1, "Number of non-gamma clusters", "Number of frames", fppath)

    ## The number of gamma clusters plot.
    ngsplot = Hist("ngs", 103, ngs, -1, "Number of gamma clusters", "Number of frames", fppath)

    # Make the plot display page.
    fp = ""
    fp += "<!DOCTYPE html>\n"
    fp += "<html>\n"
    fp += "  <head>\n"
    fp += "    <link rel=\"stylesheet\" type=\"text/css\" "
    fp += "href=\"assets/css/style.css\">\n"
    fp += "  </head>\n"
    fp += "  <body>\n"
    fp += "    <h1>Cluster Sorting: Frame Properties</h1>\n"
    fp += "    <h2>Dataset summary</h2>\n"
    fp += "    <p>\n"
    fp += "      <ul>\n"
    fp += "        <li>Dataset path = '%s'</li>\n" % (datapath)
    fp += "        <li>Number of frames = %d</li>\n" % (len(fd))
    fp += "        <li>Number of clusters (dat.) = %d</li>\n" % (len(kd))
    fp += "      </ul>\n"
    fp += "    </p>\n"
    fp += "    <h2>Frame properties</h2>\n"
    fp += "    <table>\n"
    fp += "      <caption>Fig. 1: Clusters per frame.</caption>\n"
    fp += "      <tr><td><img src=\"ncs.png\" /></td></tr>\n"
    fp += "    </table>\n"
    fp += "    <table>\n"
    fp += "      <caption>Fig. 2: Non-gamma clusters per frame.</caption>\n"
    fp += "      <tr><td><img src=\"nls.png\" /></td></tr>\n"
    fp += "    </table>\n"
    fp += "    <table>\n"
    fp += "      <caption>Fig. 3: Gamma clusters per frame.</caption>\n"
    fp += "      <tr><td><img src=\"ngs.png\" /></td></tr>\n"
    fp += "    </table>\n"
    fp += "  </body>\n"
    fp += "</html>"

    # Write out the frame property index page.
    with open("%s/index.html" % (fppath), "w") as framepage:
        framepage.write(fp)


    # Clusters
    #----------

    ## A list of clusters.
    klusters = []

    # Create container lists for the cluster properties.
    cluster_size      = []
    cluster_counts    = []
    cluster_maxcounts = []
    cluster_radius_u  = []
    cluster_density_u = []
    cluster_linearity = []
    cluster_innerfrac = []

    # Loop over the klusters.
    for k in kd:

        # Add to the cluster property dictionaries.
        if not k["isedgekluster"]:
            cluster_size.append(     k["size"])
            cluster_radius_u.append( k["radius_uw"])
            cluster_density_u.append(k["density_uw"])
            cluster_linearity.append(k["lin_linearity"])
            cluster_innerfrac.append(k["innerfrac"])
            cluster_counts.append(   k["totalcounts"])
            cluster_maxcounts.append(k["maxcounts"])

    # Cluster plots
    #---------------

    ksplot = Hist("kls", 1001, cluster_size,       -1, "$N_{h}$",     "Number of clusters", kppath)
    kcplot = Hist("klc", 1002, cluster_counts,    100, "$N_{C}$",     "Number of clusters", kppath)
    krplot = Hist("klr", 1003, cluster_radius_u,  100, "$r$",         "Number of clusters", kppath)
    kdplot = Hist("kld", 1004, cluster_density_u, 100, "$\\rho$",     "Number of clusters", kppath)
    klplot = Hist("kll", 1005, cluster_linearity, 100, "Linearity",   "Number of clusters", kppath)
    kiplot = Hist("kli", 1006, cluster_innerfrac, 100, "Inner frac.", "Number of clusters", kppath)
    kmplot = Hist("klm", 1007, cluster_maxcounts, 100, "Max. Count",  "Number of clusters", kppath)

    # Figure - hits vs radius.
    hits_vs_rad = Hist2D(201, "hvr", cluster_size,     "$N_h$", max(cluster_size), \
                                     cluster_radius_u, "$r$",   100,               \
                                     kppath)

    # Figure - hits vs counts.
    hits_vs_counts = Hist2D(202, "hvc", cluster_size,   "$N_h$", max(cluster_size), \
                                        cluster_counts, "$N_c$", 100,               \
                                        kppath)

    # Figure - hits vs linearity.
    hits_vs_lin = Hist2D(203, "hvl", cluster_size,      "$N_h$", max(cluster_size), \
                                     cluster_linearity, "Linearity", 100,           \
                                     kppath)
    # Figure - radius vs linearity.
    rad_vs_lin = Hist2D(204, "rvl", cluster_radius_u, "$r$", 100,        \
                                    cluster_linearity, "Linearity", 100, \
                                    kppath)

    # Figure - density vs linearity.
    rho_vs_lin = Hist2D(205, "dvl", cluster_density_u, "$\\rho$", 100,   \
                                    cluster_linearity, "Linearity", 100, \
                                    kppath)

    # Make the plot display page.
    kp = ""
    kp += "<!DOCTYPE html>\n"
    kp += "<html>\n"
    kp += "  <head>\n"
    kp += "    <link rel=\"stylesheet\" type=\"text/css\" "
    kp += "href=\"assets/css/style.css\">\n"
    kp += "  </head>\n"
    kp += "  <body>\n"
    kp += "    <h1>Cluster Sorting: Cluster Properties</h1>\n"
    kp += "    <h2>Dataset summary</h2>\n"
    kp += "    <p>\n"
    kp += "      <ul>\n"
    kp += "        <li>Dataset path = '%s'</li>\n" % (datapath)
    kp += "        <li>Number of frames = %d</li>\n" % (len(fd))
    kp += "        <li>Number of clusters (dat.) = %d</li>\n" % (len(cluster_size))
    kp += "      </ul>\n"
    kp += "    </p>\n"
    kp += "    <h2>Cluster properties</h2>\n"
    kp += "    <h3>Individual plots</h3>\n"
    kp += "    <table>\n"
    kp += "      <caption>Fig. 1.1: Cluster size.</caption>\n"
    kp += "      <tr><td><img src=\"kls.png\" /></td></tr>\n"
    kp += "    </table>\n"
    kp += "    <table>\n"
    kp += "      <caption>Fig. 1.2: Total counts per cluster.</caption>\n"
    kp += "      <tr><td><img src=\"klc.png\" /></td></tr>\n"
    kp += "    </table>\n"
    kp += "    <table>\n"
    kp += "      <caption>Fig. 1.3: Max. count value in the cluster.</caption>\n"
    kp += "      <tr><td><img src=\"klm.png\" /></td></tr>\n"
    kp += "    </table>\n"
    kp += "    <table>\n"
    kp += "      <caption>Fig. 1.4: Cluster radii.</caption>\n"
    kp += "      <tr><td><img src=\"klr.png\" /></td></tr>\n"
    kp += "    </table>\n"
    kp += "    <table>\n"
    kp += "      <caption>Fig. 1.5: Cluster density &rho;.</caption>\n"
    kp += "      <tr><td><img src=\"kld.png\" /></td></tr>\n"
    kp += "    </table>\n"
    kp += "    <table>\n"
    kp += "      <caption>Fig. 1.6: Fraction of inner pixels.</caption>\n"
    kp += "      <tr><td><img src=\"kli.png\" /></td></tr>\n"
    kp += "    </table>\n"
    kp += "    <table>\n"
    kp += "      <caption>Fig. 1.7: Cluster linearity.</caption>\n"
    kp += "      <tr><td><img src=\"kll.png\" /></td></tr>\n"
    kp += "    </table>\n"
    kp += "    <h3>Comparison plots</h3>\n"
    kp += "    <table>\n"
    kp += "      <caption>Fig. 2.1: Cluster size vs radius.</caption>\n"
    kp += "      <tr><td><img src=\"hvr.png\" /></td></tr>\n"
    kp += "    </table>\n"
    kp += "    <table>\n"
    kp += "      <caption>Fig. 2.2: Cluster size vs counts.</caption>\n"
    kp += "      <tr><td><img src=\"hvc.png\" /></td></tr>\n"
    kp += "    </table>\n"
    kp += "    <table>\n"
    kp += "      <caption>Fig. 2.3: Cluster size vs linearity.</caption>\n"
    kp += "      <tr><td><img src=\"hvl.png\" /></td></tr>\n"
    kp += "    </table>\n"
    kp += "    <table>\n"
    kp += "      <caption>Fig. 2.4: Cluster radius vs linearity.</caption>\n"
    kp += "      <tr><td><img src=\"rvl.png\" /></td></tr>\n"
    kp += "    </table>\n"
    kp += "    <table>\n"
    kp += "      <caption>Fig. 2.5: Cluster density vs linearity.</caption>\n"
    kp += "      <tr><td><img src=\"dvl.png\" /></td></tr>\n"
    kp += "    </table>\n"
    kp += "  </body>\n"
    kp += "</html>"

    # Write out the cluster property index page.
    with open("%s/index.html" % (kppath), "w") as clusterpage:
        clusterpage.write(kp)

    # Now you can view the "index.html" files to see the results!
    print("*")
    print("* Plotting complete.")
    print("* View your results by opening '%s' or '%s' in a browser, e.g." % (fppath, kppath))
    print("* $ firefox %s/index.html &" % (fppath))
    print("* $ firefox %s/index.html &" % (kppath))
