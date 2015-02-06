#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Various helper functions for processing CERN@school Timepix datasets.
"""

#...for the logging.
import logging as lg

#...for the MATH.
import numpy as np

#...for the least squares stuff.
from scipy.optimize import leastsq

#...for the data values.
from datavals import *

def getConsistentValue(thelist, error, emptyval=None):
    """
    Function for extracting a consistent value from a list,
    and throwing an error if:
    a) there are differing values present, or;
    b) the list is empty but no 'empty' value is supplied.
    """
    if len(thelist) > 0:
        # Check that the values are consistent.
        if thelist.count(thelist[0]) != len(thelist):
            # Raise the exception with the user supplied error string.
            raise IOError(error)
        # If they are, return the first value.
        return thelist[0]

    else:
        if emptyval is not None:
            return emptyval
        else:
            raise ValueError("Empty list supplied but no empty value given!")

def getFormat(fn):

    ## Open the file and look at the first line.
    with open(fn, "r") as f:

        l = f.readline().strip()

        lg.debug("")
        lg.debug(" *--> First line is:")
        lg.debug("\n\n%s\n" % (l))
        lg.debug("")

        ## The file type value.
        filetypeval = 0

        # Is it a DSC file?
        # TODO: check all possible DSC file starts...
        if   l == "A000000001":
            filetypeval = -1
            lg.debug(" *--> This is a %s file." % (DATA_FILE_TYPES[filetypeval]))
            return filetypeval

        # Is the file empty?
        if l == "":
            filetypeval = 4114
            lg.debug(" *--> This is a %s file." % (DATA_FILE_TYPES[filetypeval]))
            return filetypeval

        # Try to break up the first line into tab-separated integers.

        try:
            ## Values separated by tab
            tabvals = [int(x) for x in l.split('\t')]

            lg.debug(" %d tab separated values found in the first line." % (len(tabvals)))

            if len(tabvals) == 2:
                filetypeval = 8210
            elif len(tabvals) == 3:
                filetypeval = 4114
            lg.debug(" *--> This is a %s file." % (DATA_FILE_TYPES[filetypeval]))
            return filetypeval

        except ValueError:
            lg.debug(" Tab separation into integers failed!")
            pass

        try:
            ## Values separated by spaces.
            spcvals = [int(x) for x in l.split(' ')]

            lg.debug(" %d space separated values found in the first line." % (len(spcvals)))

            if len(spcvals) == 256:
                filetypeval = 18
            lg.debug(" *--> This is a %s file." % (DATA_FILE_TYPES[filetypeval]))
            return filetypeval

        except ValueError:
            lg.debug(" Space separation into integers failed!")
            pass

        lg.debug(" This is not a valid data file.")

        return filetypeval


def residuals(p, y, x):
    """ The residual function required by leastsq."""

    ## The gradient of the line.
    m = p[0]

    ## The intercept with the y axis.
    c = p[1]

    ## The model we're testing - a straight line in this case.
    model = m*x + c

    ## The result to return.
    res = y - model

    # Return it!
    return res

def getLinearity(pixel_dict):
    """
    A helper function for finding the linearity of a cluster.

    The residuals are the perpendicular distances of each pixel
    from the line of best fit.

    @param [in] pixel_dict A dictionary of pixel {X:C} values.
    @returns m The gradient of the line of best fit.
    @returns c The intercept of the line of best fit.
    @returns sumR The sum of the residuals.
    @returns lin The linearity, sumR/N_pixels.
    """

    lg.debug("*")
    lg.debug("*--> getLinearity called:")
    lg.debug("* %d pixels found." % (len(pixel_dict)))

    #m, c, sumR, lin = 0.0, 0.0, 0.0, 0.0

    ## The list of pixel x values.
    xs = []

    ## The list of pixel y values.
    ys = []

    # Loop over the pixels provided to get the x and y values.
    for X, C in pixel_dict.iteritems():
        x = float(X % 256)
        y = float(X / 256)
        xs.append(x)
        ys.append(y)

    ## An array of the pixel x values.
    x_array = np.array(xs)

    ## The y values.
    y_array = np.array(ys)

    # If there are no pixels, return 0.0.
    if len(pixel_dict) == 0:
        lg.debug("*--> No pixels provided; exiting returning 0.0!")
        return None, None, None, None

    # Check that it's not just a single pixel cluster.
    if len(x_array) == 1:
        lg.debug("*--> I am only one pixel! Exiting!")
        #return None, None, None, None
        return 0.0, x_array[0], 0.0, 0.0

    # Get the equation of the line
    #------------------------------

    # Vertical line
    # For a vertical line of pixels, all of the x values will be identical.
    if xs.count(xs[0]) == len(xs): # Nifty little trick picked up from SE.
        # d is the intercept on the x axis
        #d = x_array[0]
        return 999999.9, 999999.9, 0.0, 0.0

    # Horizontal line
    # For a horizontal line of pixels, all of the y values will be identical.
    # We can just set m to 0 and c to y_i.
    elif ys.count(ys[0]) == len(ys):
        return 0.0, ys[0], 0.0, 0.0

    # The line is at an angle to the axes - a bit more interesting!
    else:
        # A first guess from the "end" pixels.
        # Note, however, that the "end" pixels may not be at the extremes
        # of the cluster (to be investigated further...).
        #
        lg.debug("* --> Initial guesses from (%3d, %3d) - (%3d, %3d):" % \
            (x_array[0], y_array[0], x_array[-1], y_array[-1]))

        #m_init = ((y_array[-1])-(y_array[0]))/((x_array[-1])-(x_array[0]))
        m_init = 0.0

        c_init = y_array[0] - (m_init*(x_array[0]))

        # A list of the initial guess parameters.
        p0 = [m_init, c_init]
        lg.debug("*--> Initial [m, c] = [% f, % f]" % (p0[0], p0[1]))

        # The results of the least-squares finding.
        plsq = leastsq(residuals, p0, args = (np.array(y_array), np.array(x_array)))

        ## The gradient of the line.
        m = plsq[0][0]

        ## The intercept with the y axis.
        c = plsq[0][1]

        lg.debug("*--> Found   [m, c] = [% f, % f]" % (m, c))

        # Now find the perpendicular distance of the pixel from the
        # line (the residuals).

        ## The denominator of |d| (the perpendicular distance).
        #
        # We only need this once, so we do it at the start of the loop.
        denom = np.sqrt(1 + m*m)

        ## The list of distances, one for each pixel.
        ds = []

        # Loop over the pixels and calculate the distances.
        for X, C in pixel_dict.iteritems():
            x = X % 256
            y = X / 256

            ## The numerator of |d| (the perpendicular distance).
            numerator = np.fabs(m * x - y + c)

            ds.append(numerator/denom)

        return m, c, sum(ds), sum(ds)/(float(len(pixel_dict)))

    print("* ERROR - should not reach this point...")

def countEdgePixels(pixels_dict, rows, cols):
    """ Count the number of edge pixels in the cluster. """

    dir_x = [-1, -1,  0,  1,  1,  1,  0, -1]

    dir_y = [ 0,  1,  1,  1,  0, -1, -1, -1]

    ## The number of edge pixels in the cluster.
    num_edge_pixels = 0

    # Loop over the pixels in the cluster.
    for X in pixels_dict.keys():

        x = X%256

        y = X/256

        is_edge_pixel = False

        # Loop over the directions.
        for direction in range(8):

            # The y poxition of the next pixel to scan.
            ny = y + dir_y[direction]

            # The x position of the next pixel to scan.
            nx = x + dir_x[direction]

            # The next pixel's X value.
            nX = ny * cols + nx

            #print "DEBUG: *-----* %1d->(% 1d, % 1d) is (%3d,%3d)->(%10d)" % \
            #  (direction, self.dir_x[direction], self.dir_y[direction], nx, ny, nxy)
            # If the next row or column is on an edge, skip it.
            #if ny<0 or ny>=self.rows or nx<0 or nx>=self.cols:
            #    continue

            # If the next X value is not in the pixel keys, we have an edge pixel.
            if nX not in pixels_dict.keys():
                #print "DEBUG: *-----* Found neighbour in self.pixels!"
                #print "DEBUG: *     \\--* xy = %d" % (nxy)
                #self.pixels[ xy].set_neighbour( direction,     nxy)
                #self.pixels[nxy].set_neighbour((direction+4)%8, xy)
                is_edge_pixel = True
                break

        if is_edge_pixel:
            num_edge_pixels += 1

    return num_edge_pixels


def getKlusterPropertiesJson(klusterid, k):
    """ Return a JSON containing the cluster properties. """

    # Get the line of best fit values for the cluster.
    m, c, sumR = k.getLineOfBestFitValues()

    p = {\
        "id"            : klusterid,                  \
        "size"          : k.getNumberOfPixels(),      \
        "xmin"          : k.getXMin(),                \
        "xmax"          : k.getXMax(),                \
        "ymin"          : k.getYMin(),                \
        "ymax"          : k.getYMax(),                \
        "width"         : k.getWidth(),               \
        "height"        : k.getHeight(),              \
        "x_uw"          : k.getXUW(),                 \
        "y_uw"          : k.getYUW(),                 \
        "radius_uw"     : k.getRadiusUW(),            \
        "density_uw"    : k.getDensityUW(),           \
        "totalcounts"   : k.getTotalCounts(),         \
        "maxcounts"     : k.getMaxCountValue(),       \
        "lin_m"         : m,                          \
        "lin_c"         : c,                          \
        "lin_sumofres"  : sumR,                       \
        "lin_linearity" : k.getLinearity(),           \
        "n_edgepixels"  : k.getNumberOfEdgePixels(),  \
        "edgefrac"      : k.getOuterPixelFraction(),  \
        "innerfrac"     : k.getInnerPixelFraction(),  \
        "ismc"          : k.isMC(),                   \
        "isedgekluster" : k.isEdgeCluster()           \
        #"totalenergy"   :, \
        #"maxenergy"     :, \
        #"frameid"       :\
        }

    return p
