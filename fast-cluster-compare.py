#!/usr/bin/env python

#=======================================================
# Fast Cluster Comparison Analysis Code for CERN@school
#=======================================================
#
#
#
# See the README.md for more information.

# Import the code needed to manage files.
import os, inspect, glob, argparse

# Import the plotting libraries.
import pylab as plt
from matplotlib import rc

# Uncomment to use LaTeX for the plot text.
rc('font',**{'family':'serif','serif':['Computer Modern']})
rc('text', usetex=True)

# Import the clustering and web-page writing code.
from clustering import *
from pagemaker  import *
from analysis   import *

# Get the path of the current directory
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

#
# The main program.
#
if __name__=="__main__":
    print("==============================================")
    print("  CERN@school Fast Cluster Analysis (Python)  ")
    print("==============================================")

    # Get the datafile path from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("datapath", \
        help="Path to the folder containing your data."  )
    parser.add_argument("simpath", \
        help="Path to the folder containing your simulation results."  )
    args = parser.parse_args()

    # Set the data file path.
    datapath = args.datapath

    # Set the simulation results file path.
    simpath = args.simpath

    # Update the user as to what's going on.
    print("*")
    print("* datapath is '%s'" % datapath)
    print("* simpath  is '%s'" % simpath)
    print("*")
    print("* [PROCESSING...]")
    print("*")


    # Firstly, let's get lists in the form [val1, val2, etc.] of
    # the cluster sizes for the real data and the simulated data.

    # The "analyse" takes four arguments:
    # * The path to the folder containing the data files;
    # * The minimum cluster size to be considered;
    # * The minimum cluster radius to be considered;
    # * Whether or not to analyse only one frame (useful for testing).

    # We can change the requirements on the clusters here:
    min_size = 1    # single pixels
    min_rad  = 0.0  # single pixels

    cluster_size_dat = analyse(datapath, min_size, min_rad, False)
    cluster_size_sim = analyse(simpath,  min_size, min_rad, False)

    # It's the contents of these lists that we want to plot.

    # GETTING READY TO MAKE THE PLOTS
    #=================================

    # Reset the matplot lib plotting stuff.
    plt.close()

    # Here we create the figure on which we'll be plotting our results.
    # We assign the figure a number, a size (5" x 3"), set the resolution
    # of the image (150 DPI), and set the background and outline to white.

    # Fig. 1: Hits Per Cluster Frequency Histogram
    hpcplot = plt.figure(101, figsize=(5.0, 3.0), dpi=150, facecolor='w', edgecolor='w')

    # Then we give a bit of clearance for the axes.
    hpcplot.subplots_adjust(bottom=0.17, left=0.15)

    # This is the subplot on which we'll actually be plotting.
    hpcplotax = hpcplot.add_subplot(111)

    # Label your axes:
    # The y axis
    plt.ylabel('Number of clusters')
    # The x axis
    plt.xlabel('$N_h$')
    #
    # Add gridlines.
    plt.grid(1)

    # Should be we use a logarithmic scale for the y axis?
    # Not yet, but we might do later.
    uselogy = False

    # Now we have set up our figure, we can plot the results of our analysis.

    # Comparing simulated data vs. real data
    #========================================
    # Before the make the plots, we'll need to find out a little bit about
    # the contents of cluster_size_dat and cluster_size_sim in order to
    # make good-looking, useful plots.
    #
    # We don't make plots of the raw data per se - we want to make a frequency
    # histogram of the different cluster size values.

    print("*")

    # SIMULATED

    # Firstly, we'll choose our histogram bin values. We could - and probably
    # will - use bin widths of one. This means we plot the number of clusters
    # with 1 pixel, with 2 pixes, with 3 pixels, etc. in their own bins.

    # Find the maximum x value (hits per cluster) in the simulated data.
    print("* Max hits per cluster - sim. -   : %4d" % (max(cluster_size_sim)))
    print("*")

    # Round this up to the nearest 10.
    hpc_sim_max_x    = 10 * (np.floor(max(cluster_size_sim)/10.) + 1)
    print("* x max          (sim)            : %4d" % (hpc_sim_max_x))

    # Set the bin width - we'll stick with one for the moment.
    hpc_sim_bin_width = 1
    print("* Bin width      (sim)            : %4d" % (hpc_sim_bin_width))

    # Create the bin edges array for the simulated data:
    # * Bin width one, rounded-up max x value.
    hpc_sim_bins = np.arange(0, hpc_sim_max_x+hpc_sim_bin_width, hpc_sim_bin_width)
    #print("* Bins           (sim)")
    #print hpc_sim_bins # uncomment this if you want to see the actual bin edges.
    print("*")


    # Create a histogram of the hits per cluster for the simulated data
    # using the bin edges defined above.
    n_s, bins_s, patches_s = plt.hist( \
        cluster_size_sim, \
        bins=hpc_sim_bins, \
        histtype='stepfilled', \
        normed=1, \
        log=uselogy)

    # Set the display propertied of the histogram "patches" (bars).
    # We're using translucent green bars with no outline.
    plt.setp(patches_s, 'facecolor', 'g', 'alpha', 0.75, 'linewidth', 0.0)

    # THE REAL DATA

    print("*")

    # Again, we'll find the best bin width values using a bit of coding.

    # Find the maximum x value (hits per cluster) in the real data.
    print("* Max hits per cluster - dat. -   : %4d" % (max(cluster_size_dat)))
    print("*")

    # Round this up to the nearest 10.
    hpc_dat_max_x    = 10 * (np.floor(max(cluster_size_dat)/10.) + 1)
    print("* x max          (dat)            : %4d" % (hpc_dat_max_x))

    # We'll use a bin width of 2 for the data - we have less of it than
    # the simulated data.
    hpc_dat_bin_width = 2
    print("* Bin width      (dat)            : %4d" % (hpc_dat_bin_width))

    # Create the bin edges array for the real data:
    # * Bin width one, rounded-up max x value.
    hpc_dat_bins = np.arange(0, hpc_dat_max_x+hpc_dat_bin_width, hpc_dat_bin_width)
    #print("* Bins           (dat)")
    #print hpc_dat_bins # again, uncomment if you want to see the actual
    #                   # bin values.
    print("*")


    # Create a histogram of the hits per cluster for the real data
    # using the bins defined above.
    n_r, bins_r = np.histogram(cluster_size_dat, bins=hpc_dat_bins)
    #print("* n_r before normalisation:")
    #print n_r

    # Now, it's traditional in particle physics to plot the simulated data
    # as filled bars (as, generally speaking, there are more stats so these
    # look nice and smooth). However, real data is more scarce and messy,
    # so we'll plot the corresponding data points as points with error bars.
    # This is a little more complicated...

    # Firstly, we'll need an array of the bin centres to put the points
    # at (rather than the bin edges). Note the slicing of the bin edges
    # array to get the N bins (as otherwise we'd have N+1 bin edges).
    hpc_dat_bin_centres = 0.5*(hpc_dat_bins[1:]+hpc_dat_bins[:-1])
    #print hpc_dat_bin_centres

    # Get the total number of clusters...
    hpc_dat_sum = sum(n_r)

    # And multiply by the bin width. We'll need this for the normalisation.
    hpc_dat_sum = hpc_dat_sum * hpc_dat_bin_width
    #print("* Scale factor (for normalisation) = %f" % (hpc_dat_sum))

    # Some bins will be empty. To avoid plotting these, we can replace
    # the contents of that bin with "nan" (not a number).
    # matplotlib then cleverly skips over these, leaving the x axis
    # clean and shiny.
    n_r = [np.nan if x==0 else float(x) for x in n_r]
    #print("* n_r after zero-bin replacement:")
    #print n_r

    # Calculate the errors on the number of clusters counted (Poisson).
    err = np.sqrt(n_r)
    #print("* The errors on each bin: ")
    #print err

    # Normalise the histogram entries and the errors.
    n_r = n_r/hpc_dat_sum
    err = err/hpc_dat_sum
    #print("* The histogram values after normalisation:")
    #print n_r
    #print("* The errors after normalisation:")
    #print err

    # Plot the real data points as an "errorbar" plot
    plt.errorbar(hpc_dat_bin_centres, \
                 n_r, \
                 fmt='d', \
                 color='black', \
                 yerr=err, \
                 ecolor='black', \
                 capthick=2, \
                 elinewidth=1)

    # Uncomment these lines and change the values to play with the axis limits.
    #plt.ylim([0.0, 0.1])
    plt.xlim([0, 40])

    # Save the figure.
    hpcplot.savefig("hpc.png")

    # Generate the html page, index.html
    make_page(path, datapath, len(cluster_size_dat))

    # Now you can view "index.html" to see your results!
    print("*")
    print("* Analysis complete!")
    print("* View your results by opening 'index.html' in a browser, e.g.")
    print("* firefox index.html &")
