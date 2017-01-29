#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

 CERN@school - Compare Real and Simulated Data

 See the README.md file for more information.

"""

#...for the operating system commands.
import os

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

#...for processing and wrapping the kluster properties.
from cernatschool.klusterhelpers import KlusterProperties

#...for the comparison histograms.
from plotting.histograms import HistCompare

if __name__ == "__main__":

    print("*")
    print("*=============================*")
    print("* CERN@school - compare plots *")
    print("*=============================*")

    # Get the datafile path from the command line.
    parser = argparse.ArgumentParser()
    parser.add_argument("inputPathDat",    help="Path to the data dataset.")
    parser.add_argument("inputPathSim",    help="Path to the simulated dataset.")
    parser.add_argument("outputPath",      help="The path for the output files.")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    args = parser.parse_args()

    ## The path to the real data.
    datpath = args.inputPathDat

    ## The path to the simulated data.
    simpath = args.inputPathSim

    ## The output path.
    outputpath = args.outputPath

    # Check if the output directory exists. If it doesn't, quit.
    if not os.path.isdir(outputpath):
        raise IOError("* ERROR: '%s' output directory does not exist!" % (outputpath))

    # Set the logging level.
    if args.verbose:
        level=lg.DEBUG
    else:
        level=lg.INFO

    # Configure the logging.
    lg.basicConfig(filename=outputpath + '/log_compare-plots.log', filemode='w', level=level)

    print("*")
    print("* Real data           : '%s'" % (datpath))
    print("* Simulated data      : '%s'" % (simpath))
    print("* Output path         : '%s'" % (outputpath))
    print("*")


    # Set up the directories
    #------------------------

    # Create the subdirectories.

    ## The path to the cluster plots.
    kppath = (outputpath + "/clusterplots/").replace('//', '/')
    #
    if os.path.isdir(kppath):
        rmtree(kppath)
        lg.info(" * Removing directory '%s'..." % (kppath))
    os.mkdir(kppath)
    lg.info(" * Creating directory '%s'..." % (kppath))
    lg.info("")

    ## The path to the real data klusters JSON.
    dat_klusters_path = (datpath + "/klusters.json").replace('//', '/')
    #
    if not os.path.exists(dat_klusters_path):
        raise IOError("* ERROR: '%s' does not exist!" % (dat_klusters_path))

    ## The real data cluster properties wrapper.
    dat_kl_prop = KlusterProperties(dat_klusters_path)

    ## The path to the simulated data klusters JSON.
    sim_klusters_path = (simpath + "/klusters.json").replace('//', '/')
    #
    if not os.path.exists(sim_klusters_path):
        raise IOError("* ERROR: '%s' does not exist!" % (sim_klusters_path))

    ## The simulated data cluster properties wrapper.
    sim_kl_prop = KlusterProperties(sim_klusters_path)


    # Cluster plots
    #---------------

    ## The cluster size comparison plot.
    cluster_size_plot = HistCompare(dat_kl_prop.get_cluster_size_list(),
                                    sim_kl_prop.get_cluster_size_list(),
                                    fig_width=2.0, fig_height=4.0,
                                    dat_bin_width = 2,
                                    x_label="$n_j$", x_max=60,
                                    y_label="Number of clusters", y_max=0.12)

    # Save the plot.
    cluster_size_plot.save_plot(kppath, "kls")

    ## The cluster radius (unweighted) comparison plot.
    cluster_radius_u_plot = HistCompare(dat_kl_prop.get_cluster_radius_u_list(),
                                        sim_kl_prop.get_cluster_radius_u_list(),
                                        fig_width=2.0, fig_height=4.0,
                                        dat_bin_width=1,
                                        x_label="$r_j$",
                                        y_label="Number of clusters")

    # Save the plot.
    cluster_radius_u_plot.save_plot(kppath, "klr")

    ## The cluster linearity comparison plot.
    cluster_linearity_plot = HistCompare(dat_kl_prop.get_cluster_linearity_list(),
                                         sim_kl_prop.get_cluster_linearity_list(),
                                         fig_width=2.0, fig_height=4.0,
                                         dat_bin_width=0.1,
                                         sim_bin_width=0.1,
                                         x_label="Linearity", x_max=3.0,
                                         y_label="Number of clusters", y_max=2.5)

    # Save the plot.
    cluster_linearity_plot.save_plot(kppath, "kll")


    # Make the plot display page.
    kp = ""
    kp += "<!DOCTYPE html>\n"
    kp += "<html>\n"
    kp += "  <head>\n"
    #kp += "    <link rel=\"stylesheet\" type=\"text/css\" "
    #kp += "href=\"assets/css/style.css\">\n"
    kp += "  </head>\n"
    kp += "  <body>\n"
    kp += "    <h1>Data vs. Simulation: Cluster Properties</h1>\n"
    kp += "    <h2>Dataset summary</h2>\n"
    kp += "    <p>\n"
    kp += "      <ul>\n"
    kp += "        <li>Real data path      = '%s'</li>\n" % (datpath)
    kp += "        <li>Simulated data path = '%s'</li>\n" % (simpath)
    kp += "        <li>Number of clusters (dat.) = %d</li>\n" % (dat_kl_prop.get_number_of_klusters())
    kp += "        <li>Number of clusters (sim.) = %d</li>\n" % (sim_kl_prop.get_number_of_klusters())
    kp += "      </ul>\n"
    kp += "    </p>\n"
    kp += "    <h2>Cluster properties - comparisons</h2>\n"
    kp += "    <table>\n"
    kp += "      <caption>Fig. 1.1: Cluster size.</caption>\n"
    kp += "      <tr><td><img src=\"kls.png\" /></td></tr>\n"
    kp += "    </table>\n"
    kp += "    <table>\n"
    kp += "      <caption>Fig. 1.4: Cluster radii.</caption>\n"
    kp += "      <tr><td><img src=\"klr.png\" /></td></tr>\n"
    kp += "    </table>\n"
    kp += "    <table>\n"
    kp += "      <caption>Fig. 1.7: Cluster linearity.</caption>\n"
    kp += "      <tr><td><img src=\"kll.png\" /></td></tr>\n"
    kp += "    </table>\n"
    kp += "  </body>\n"
    kp += "</html>"

    cluster_page_path = (kppath + "/index.html").replace("//", "/")

    # Write out the cluster property index page.
    with open(cluster_page_path, "w") as clusterpage:
        clusterpage.write(kp)

    # Now you can view the "index.html" files to see the results!
    print("*")
    print("* Plotting complete.")
    print("* View your results by opening '%s' in a browser, e.g." % (cluster_page_path))
    print("* $ firefox %s &" % (cluster_page_path))
