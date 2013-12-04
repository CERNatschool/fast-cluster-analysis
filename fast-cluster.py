#!/usr/bin/env python

#============================================
# Fast Cluster Analysis Code for CERN@school
#============================================
#
# See the README.md for more information.

# Import the code needed to manage files.
import os, inspect, glob, argparse

# Import the plotting libraries.
import pylab as plt
from matplotlib import rc

# Make our plots compatible with CERN@school LaTeX reports.
rc('font',**{'family':'serif','serif':['Computer Modern']})
rc('text', usetex=True)

# Import the clustering and web-page writing code.
from clustering import *
from pagemaker  import *

# Get the path of the current directory
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

#
# The main program.
#
if __name__=="__main__":
    print("============================================")
    print("  CERN@school Fast Blob Analysis (Python)   ")
    print("============================================")

    # Get the datafile path from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("datapath", \
        help="Path to the folder containing your data."  )
    args = parser.parse_args()

    # Set the data file path.
    datapath = args.datapath

    print("*")
    print("* datapath is '%s'" % datapath)
    print("*")
    print("* [PROCESSING...]")

    # Create container lists for the cluster properties.
    cluster_size      = []
    cluster_counts    = []
    cluster_radius_u  = []
    cluster_density_u = []

    # Loop over the datafiles and read the data.
    for datafilename in glob.glob(datapath + "/*.txt"):

        # Open the file and read in the data.
        f = open(datafilename, 'r')
        data = f.read()
        f.close()

        # Create a "dictionary" for the pixel information.
        pixels = {}

        # Loop over the X Y C values in the file and add them to the
        # pixel dictionary.
        for datarow in data.splitlines():
            #print dataline
            v = datarow.split('\t') # Separates the I J C values
            x = int(v[0]); y = int(v[1]); c = int(v[2])
            xy = 256 * y + x
            pixels[xy] = c

        # Create a "BlobFinder" to cluster the pixels we've just extracted.
        # See clustering.py for more about how this is done.
        blob_finder = BlobFinder(pixels, 256, 256)

        # Loop over the blobs found in the blob finder and record their
        # properties for plotting.
        for b in blob_finder.blob_list:
            cluster_size.append(b.get_size())
            cluster_counts.append(b.get_total_counts())
            cluster_radius_u.append(b.r_u)
            cluster_density_u.append(b.spatial_density_u)

        #break # uncomment this to only read the first file in the folder.
               # Useful when testing!

    #-------------------------------------------------------------------------

    # Now we've made read in the data and recorded the cluster properties,
    # we can make the plots.

    # Fig. 1: Hits Per Cluster Frequency Histogram
    hpcplot = plt.figure(101, figsize=(5.0, 3.0), dpi=150, facecolor='w', edgecolor='w')
    hpcplot.subplots_adjust(bottom=0.17, left=0.15)
    hpcplotax = hpcplot.add_subplot(111)
    # y axis
    plt.ylabel('Number of clusters')
    # x axis
    plt.xlabel('$N_h$')
    #
    plt.grid(1)
    #
    n, bins, patches = plt.hist(cluster_size, range(0,max(cluster_size)+5,1), histtype='stepfilled')
    plt.setp(patches, 'facecolor', 'g', 'alpha', 0.75, 'linewidth', 0.0)
    #
    # Save the figure.
    hpcplot.savefig("hpc.png")

    # Fig. 2: Counts Per Cluster Frequency Histogram
    cpcplot = plt.figure(102, figsize=(5.0, 3.0), dpi=150, facecolor='w', edgecolor='w')
    cpcplot.subplots_adjust(bottom=0.17, left=0.15)
    cpcplotax = cpcplot.add_subplot(111)
    # y axis
    plt.ylabel('Number of clusters')
    # x axis
    plt.xlabel('$N_c$')
    #
    plt.grid(1)
    #
    n, bins, patches = plt.hist(cluster_counts, range(0,max(cluster_counts)+5,20), histtype='stepfilled')
    plt.setp(patches, 'facecolor', 'b', 'alpha', 0.75, 'linewidth', 0.0)
    #
    # Save the figure.
    cpcplot.savefig("cpc.png")

    # Fig. 3: Cluster radius (unweighted) histogram
    cruplot = plt.figure(103, figsize=(5.0, 3.0), dpi=150, facecolor='w', edgecolor='w')
    cruplot.subplots_adjust(bottom=0.17, left=0.15)
    cruplotax = cruplot.add_subplot(111)
    # y axis
    plt.ylabel('Number of clusters')
    # x axis
    plt.xlabel('$r_{u}$')
    #
    plt.grid(1)
    #
    n, bins, patches = plt.hist(cluster_radius_u, bins=100, histtype='stepfilled')
    plt.setp(patches, 'facecolor', 'r', 'alpha', 0.75, 'linewidth', 0.0)
    #
    # Save the figure.
    cruplot.savefig("cru.png")

    # Fig. 4: Cluster density (unweighted) histogram
    cduplot = plt.figure(104, figsize=(5.0, 3.0), dpi=150, facecolor='w', edgecolor='w')
    cduplot.subplots_adjust(bottom=0.17, left=0.15)
    cduplotax = cduplot.add_subplot(111)
    # y axis
    plt.ylabel('Number of clusters')
    # x axis
    plt.xlabel('$\\rho_{u}$')
    #
    plt.grid(1)
    #
    n, bins, patches = plt.hist(cluster_density_u, bins=100, histtype='stepfilled')
    plt.setp(patches, 'facecolor', '#FFBB00', 'alpha', 0.75, 'linewidth', 0.0)
    #
    # Save the figure.
    cduplot.savefig("cdu.png")

    # Generate the html page, index.html
    make_page(path, datapath)

    # Now you can view "index.html" to see your results!
    print("*")
    print("* Analysis complete!")
    print("* View your results by opening 'index.html' in a browser, e.g.")
    print("* firefox index.html &")
