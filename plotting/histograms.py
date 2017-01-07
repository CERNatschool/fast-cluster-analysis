#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

CERN@school: Plotting functions for property histograms.

See http://researchinschools.org/CERN for more information.

"""

#...for the logging.
import logging as lg

#...for the MATH.
import math

#...for even more MATH.
import numpy as np

# Import the plotting libraries.
import pylab as plt

#...for the colours. Oh, the colours!
from matplotlib.colors import LogNorm

# Load the LaTeX text plot libraries.
from matplotlib import rc

# Uncomment to use LaTeX for the plot text.
#rc('font',**{'family':'serif','serif':['Computer Modern']})
#rc('text', usetex=True)

class Hist():
    """ Wrapper class for 1D property histograms. """

    def __init__(self, name, num, data, nbins, xlabel, ylabel, outputpath):

        plt.close('all')

        ## The property histogram plot.
        p = plt.figure(num, figsize=(5.0, 3.0), dpi=150, facecolor='w', edgecolor='w')

        # Adjust the position of the axes.
        p.subplots_adjust(bottom=0.17, left=0.15)

        ## The plot axes.
        pax = p.add_subplot(111)

        # y axis
        plt.ylabel('%s' % (ylabel))

        # x axis
        plt.xlabel('%s' % (xlabel))

        # Add a grid.
        plt.grid(1)

        ## The x minimum.
        xmin = 0

        ## The x maximum.
        xmax = max(data) + 5

        if nbins < 0:
            n, bins, patches = plt.hist(data, range(int(xmin),int(xmax),1), histtype='stepfilled')
        else:
            n, bins, patches = plt.hist(data, nbins, histtype='stepfilled')

        # Set the plot's visual properties.
        plt.setp(patches, 'facecolor', 'g', 'alpha', 0.75, 'linewidth', 0.0)

        # Save the figure.
        p.savefig("%s/%s.png" % (outputpath, name))


class Hist2D:
    """
    Wrapper class for 2D property vs. property histograms.

    * FIXME: Implement kwargs for the histogram options.
    """

    def __init__(self, num, name, x_data, x_ax_label, x_nbins, y_data, y_ax_label, y_nbins, outputpath):
        """ Constructor. """

        plt.close('all')

        ## The histogram plot.
        plot = plt.figure(num, figsize=(5.0, 3.0), dpi=150, facecolor='w', edgecolor='w')

        # Adjust the position of the axes.
        plot.subplots_adjust(bottom=0.17, left=0.15)

        ## The plot axes.
        plotax = plot.add_subplot(111)

        # Set the y axis label.
        plt.ylabel(y_ax_label)

        # Set the x axis label.
        plt.xlabel(x_ax_label)

        # Add a grid.
        plt.grid(1)

        # Plot the 2D histogram.
        plt.hist2d(x_data, y_data, bins=[x_nbins, y_nbins], norm=LogNorm())

        # Add a colour bar.
        plt.colorbar()

        # Save the figure.
        plot.savefig("%s/%s.png" % (outputpath, name))


class HistCompare:
    """ Wrapper class for a 1D comparison histogram. """

    def __init__(self, dat, sim, **kwargs):
        lg.info(" *")
        lg.info(" * Initialising HistCompare object...")
        lg.info(" *")

        ## A list of the simulated property data.
        self.__sim = sim

        ## A list of the read property data.
        self.__dat = dat

        # GETTING READY TO MAKE THE PLOTS
        #=================================

        # Reset the matplot lib plotting stuff.
        plt.close()

        # Here we create the figure on which we'll be plotting our results.
        # We assign the figure a number, a size (5" x 3"), set the resolution
        # of the image (150 DPI), and set the background and outline to white.

        ## The figure width [inches].
        self.__fig_w = 5.0
        #
        if "fig_width" in kwargs.keys():
            self.__fig_width = kwargs["fig_width"]

        ## The figure height [inches].
        self.__fig_h = 5.0
        #
        if "fig_height" in kwargs.keys():
            self.__fig_h = kwargs["fig_height"]

        ## The histogram.
        self.__plot = plt.figure(101, figsize=(self.__fig_h, self.__fig_w), dpi=150, facecolor='w', edgecolor='w')

        # Then we give a bit of clearance for the axes.
        self.__plot.subplots_adjust(bottom=0.17, left=0.15)

        # This is the subplot on which we'll actually be plotting.
        self.__plot_ax = self.__plot.add_subplot(111) # hpcplotax->self.__plot_ax

        # Label your axes:

        ## The x axis label.
        self.__x_label = "$x$"
        #
        if "x_label" in kwargs.keys():
            self.__x_label = kwargs["x_label"]
        #
        plt.xlabel(self.__x_label)

        ## The y axis label.
        self.__y_label = "$y$"
        #
        if "y_label" in kwargs.keys():
            self.__y_label = kwargs["y_label"]
        #
        plt.ylabel(self.__y_label)

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

        lg.info(" *")

        # SIMULATED

        # Firstly, we'll choose our histogram bin values. We could - and probably
        # will - use bin widths of one. This means we plot the number of clusters
        # with 1 pixel, with 2 pixes, with 3 pixels, etc. in their own bins.

        # Find the maximum x value (hits per cluster) in the simulated data.
        lg.info(" * Max hits per cluster - sim. -   : %4d" % (max(self.__sim)))
        lg.info(" *")

        # Round this up to the nearest 10.
        sim_max_x    = 10 * (np.floor(max(self.__sim)/10.) + 1)
        lg.info(" * x max          (sim)            : %4d" % (sim_max_x))

        # Set the bin width - we'll stick with one for the moment.
        if "sim_bin_width" in kwargs.keys():
            sim_bin_width = kwargs["sim_bin_width"]
        else:
            sim_bin_width = 1
        lg.info(" * Bin width      (sim)            : %4d" % (sim_bin_width))

        # Create the bin edges array for the simulated data:
        # * Bin width one, rounded-up max x value.
        sim_bins = np.arange(0, sim_max_x+sim_bin_width, sim_bin_width)
        #print("* Bins           (sim)")
        #print sim_bins # uncomment this if you want to see the actual bin edges.
        lg.info(" *")


        # Create a histogram for the simulated data
        # using the bin edges defined above.
        n_s, bins_s, patches_s = plt.hist( \
            self.__sim, \
            bins=sim_bins, \
            histtype='stepfilled', \
            normed=1, \
            log=uselogy)

        # Set the display propertied of the histogram "patches" (bars).
        # We're using translucent green bars with no outline.
        plt.setp(patches_s, 'facecolor', '#CCCCCC', 'alpha', 1.0, 'linewidth', 0.0)

        # THE REAL DATA

        lg.info("*")

        # Again, we'll find the best bin width values using a bit of coding.

        # Find the maximum x value (hits per cluster) in the real data.
        lg.info(" * Max hits per cluster - dat. -   : %4d" % (max(self.__dat)))
        lg.info(" *")

        # Round this up to the nearest 10.
        dat_max_x    = 10 * (np.floor(max(self.__dat)/10.) + 1)
        lg.info(" * x max          (dat)            : %4d" % (dat_max_x))

        # We'll use a bin width of 2 for the data - we have less of it than
        # the simulated data.
        if "dat_bin_width" in kwargs.keys():
            dat_bin_width = kwargs["dat_bin_width"]
        else:
            dat_bin_width = 2
        lg.info(" * Bin width      (dat)            : %4d" % (dat_bin_width))

        # Create the bin edges array for the real data:
        # * Bin width one, rounded-up max x value.
        dat_bins = np.arange(0, dat_max_x+dat_bin_width, dat_bin_width)
        #print("* Bins           (dat)")
        #print hpc_dat_bins # again, uncomment if you want to see the actual
        #                   # bin values.
        lg.info(" *")


        # Create a histogram of the hits per cluster for the real data
        # using the bins defined above.
        n_r, bins_r = np.histogram(self.__dat, bins=dat_bins)
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
        dat_bin_centres = 0.5*(dat_bins[1:]+dat_bins[:-1])
        #print hpc_dat_bin_centres

        # Get the total number of clusters...
        dat_sum = sum(n_r)

        # And multiply by the bin width. We'll need this for the normalisation.
        dat_sum = dat_sum * dat_bin_width
        lg.info(" * Scale factor (for normalisation) = %f" % (dat_sum))

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
        n_r = n_r/dat_sum
        err = err/dat_sum
        #print("* The histogram values after normalisation:")
        #print n_r
        #print("* The errors after normalisation:")
        #print err

        # Plot the real data points as an "errorbar" plot
        plt.errorbar(dat_bin_centres, \
                     n_r, \
                     fmt='d', \
                     color='black', \
                     yerr=err, \
                     ecolor='black', \
                     capthick=2, \
                     elinewidth=1)

        if "x_max" in kwargs.keys():
            plt.xlim([0, kwargs["x_max"]])

        if "y_max" in kwargs.keys():
            plt.ylim([0.0, kwargs["y_max"]])

    def save_plot(self, outputpath, name):
        """ Saves the figure. """
        self.__plot.savefig(outputpath + "/%s.png" % (name))
        self.__plot.savefig(outputpath + "/%s.ps"  % (name))
