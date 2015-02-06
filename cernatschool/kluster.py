#!/usr/bin/env python
# -*- coding: utf-8 -*-

#...for the logging.
import logging as lg

#...for copying.
from copy import deepcopy

#...for the MATH.
import numpy as np

##...for the columns.
#from dbhelpers import Table, Column

#...for the data values.
from datavals import *

#...for the pixels.
from pixel import *

#...for the linearity calculations.
from helpers import getLinearity, countEdgePixels

class Kluster:
    """
    Wrapper class for klusters.

    @param [in] rows The number of rows in the originating frame.
    @param [in] cols The number of columns in the originating frame.
    @param [in] ismc Is the cluster from a Monte Carlo simulation?
    """

    def __init__(self, rows, cols, ismc):
        """ Constructor. """

        lg.debug(" Instantiating a Kluster object.")

        self.dbg = True

        ## The number of rows in the frame.
        self.__frame_rows = rows

        self.__frame_cols = cols

        self.total_counts = 0

        ## A list of the XY positions of the pixels used in clustering.
        ## (Note: we cannot use a dictionary for clustering because
        ## the list changes during iteration.)
        self.pixel_xy_list = []

        ## A dictionary of the pixels {X:C} (populated after clustering).
        self.__pixel_dict = {}

        ## Multiline JSON entry for the pixel.
        self.pixel_string = "" #

        # Spatial properties.
        #
        ## The minimum x value.
        self.__xmin = None

        ## The maximum x value.
        self.__xmax = None

        ## The minimum y value.
        self.__ymin = None

        ## The maximum y value.
        self.__ymax = None

        ## The cluster width [pixels].
        self.__width = None

        ## The cluster height [pixels].
        self.__height = None

        ## The unweighted cluster x position [pixels].
        self.__x_uw = None

        ## The unweighted cluster y position [pixels].
        self.__y_uw = None

        # Unweighted (u subsctript)
        self.r_u     = -1.0
        self.spatial_density_u = -1.0

        # Counts-related properties
        #
        ## Total counts.
        self.__total_counts = None

        ## The maximum count value.
        self.__count_max = None

        # Linearity-related properties.
        #
        ## Line of best fit - gradient (m).
        self.__lin_m = None

        ## Line of best fit - y intercept (c).
        self.__lin_c = None

        ## Line of best fit - sum of the residuals (Sum{R}).
        self.__lin_sumR = None

        ## Linearity.
        self.__linearity = None

        # Energy.

        ## Total energy [keV].
        self.__energy_total = None

        ## Max. energy [keV].
        self.__energy_max = None

        # Edge pixel information.

        ## The number of edge pixels.
        self.__n_edge = None

        ## The fraction of inner pixels in the cluster.
        self.__inner_pixels_frac = None

        ## The fraction of outer pixels in the cluster.
        self.__outer_pixels_frac = None

        ## Is the cluster from Monte Carlo simulation?
        self.__is_mc = ismc

        ## Is the cluster on the edge of the frames?
        self.__is_edge_kluster = None

    def __lt__(self, other):
        return self.getNumberOfPixels() < other.getNumberOfPixels()

    def get_pixel_xy_list(self):
        return self.pixel_xy_list

    def insert(self, pixel_xy, pixel):
        self.pixel_xy_list.append(pixel_xy)
        self.total_counts += pixel.getC()

    def contains_pixel(self, pixel_xy):
        return pixel_xy in self.pixel_xy_list

    def getNumberOfPixels(self):
        return len(self.pixel_xy_list)

    def getTotalCounts(self):
        return self.total_counts

    def getWidth(self):
        if self.__width is None: raise IOError("UNPROCESSED_KLUSTER")
        return self.__width

    def getHeight(self):
        if self.__height is None: raise IOError("UNPROCESSED_KLUSTER")
        return self.__height

    def getXMin(self):
        if self.__xmin is None: raise IOError("UNPROCESSED_KLUSTER")
        return self.__xmin

    def getXMax(self):
        if self.__xmax is None: raise IOError("UNPROCESSED_KLUSTER")
        return self.__xmax

    def getYMin(self):
        if self.__ymin is None: raise IOError("UNPROCESSED_KLUSTER")
        return self.__ymin

    def getYMax(self):
        if self.__ymax is None: raise IOError("UNPROCESSED_KLUSTER")
        return self.__ymax

    def getXUW(self):
        return self.__x_uw

    def getYUW(self):
        return self.__y_uw

    def getRadiusUW(self):
        return self.__r_uw

    def getDensityUW(self):
        return self.__rho_uw

    def getMaxCountValue(self):
        return self.__count_max

    def getLineOfBestFitValues(self):
        return self.__lin_m, self.__lin_c, self.__lin_sumR

    def getLinearity(self):
        return self.__linearity

    def getTotalEnergy(self):
        return self.__energy_total

    def getMaxEnergy(self):
        return self.__energy_max

    def getNumberOfEdgePixels(self):
        return self.__n_edge

    def getInnerPixelFraction(self):
        return self.__inner_pixels_frac

    def getOuterPixelFraction(self):
        return self.__outer_pixels_frac

    def isEdgeCluster(self):
        return self.__is_edge_kluster

    def isMC(self):
        return self.__is_mc

    def isGamma(self):
        """ Is the cluster a gamma candidate? """
        npix = self.getNumberOfPixels()
        rad = self.getRadiusUW()
        return npix == 1 or npix == 2 or (npix==3 and rad<TRIPIXEL_RADIUS) or (npix==4 and rad<TETRAPIXEL_RADIUS)

    def process(self, pixels):
        #
        # Note that the pixels are stored in and obtained from the KlusterFinder.

        # Start the string for the pixel JSON
        self.pixels_string  = "pixels = [\n"

        xs = []

        ys = []

        cs = []

        # Loop over the pixels found in the clustering process.
        #for bxy in self.pixel_xy_list:
        for X in self.pixel_xy_list:

            x = float(pixels[X].get_x())

            y = float(pixels[X].get_y())

            c = float(pixels[X].getC())

            xs.append(x)

            ys.append(y)

            cs.append(c)

            # Add the pixel to the pixel JSON text.
            self.pixels_string += "  " + pixels[X].pixel_entry()

            # Add to the cluster's own pixel dictionary.
            self.__pixel_dict[X] = c


        # End the string for the pixel JSON
        self.pixels_string += "]"

        self.__xmin = min(xs)

        self.__xmax = max(xs)

        self.__ymin = min(ys)

        self.__ymax = max(ys)

        self.__width = self.__xmax - self.__xmin + 1

        self.__height = self.__ymax - self.__ymin + 1

        ## The unweighted cluster x position [pixels].
        self.__x_uw = np.mean(xs)

        ## The unweighted cluster y position [pixels].
        self.__y_uw = np.mean(ys)


        # Calculate the cluster radius
        #------------------------------
        # Firstly, we calculate the distance between each pixel and the centre.
        r_i = [np.sqrt( (float(X%256) - self.__x_uw)*(float(X%256) - self.__x_uw) \
                     +  (float(X/256) - self.__y_uw)*(float(X/256) - self.__y_uw) ) \
            for X in self.__pixel_dict.keys()]

        # Then we find the maximum of these distances. This is the cluster radius.
        self.__r_uw = max(r_i)

        # Find the spatial density
        if self.__r_uw > 0.0:
            self.__rho_uw = float(len(self.pixel_xy_list))/(self.__r_uw * self.__r_uw * np.pi)
        else:
            self.__rho_uw = 0.0


        # Cluster counts
        #----------------

        ## The total counts in the cluster.
        self.__total_counts = self.getTotalCounts()

        ## The maximum count value in the cluster.
        self.__count_max = max(cs)

        # Linearity information
        #-----------------------
        self.__lin_m, self.__lin_c, self.__lin_sumR, self.__linearity = getLinearity(self.__pixel_dict)

        # Edge pixel information.
        self.__n_edge = countEdgePixels(self.__pixel_dict, self.__frame_rows, self.__frame_cols)

        self.__outer_pixels_frac = float(self.__n_edge)/float(len(self.__pixel_dict))

        self.__inner_pixels_frac = 1.0 - self.__outer_pixels_frac

        if 0 in xs or 0 in ys or 255 in xs or 255 in ys:
            self.__is_edge_kluster = True
        else:
            self.__is_edge_kluster = False

        # TMP
        self.__energy_total = 0.0
        self.__energy_max = 0.0

        lg.debug("*")
        lg.debug("* NEW CLUSTER:")
        lg.debug("*")
        lg.debug(self.pixels_string)
        lg.debug("*")
        lg.debug("* Cluster properties:")
        lg.debug("*")
        lg.debug("* x_min            = %5d" % self.getXMin())
        lg.debug("* x_max            = %5d" % self.getXMax())
        lg.debug("* y_min            = %5d" % self.getYMin())
        lg.debug("* y_max            = %5d" % self.getYMax())
        lg.debug("*")
        lg.debug("* Width            = %5d" % (self.getWidth()))
        lg.debug("* Height           = %5d" % (self.getHeight()))
        lg.debug("*")
        lg.debug("* Size (N_h)       = %5d" % (self.getNumberOfPixels()))
        lg.debug("*")
        lg.debug("* Total Counts     = %5d" % (self.getTotalCounts()))
        lg.debug("* Max. Count Value = %5d" % (self.getMaxCountValue()))
        lg.debug("*")
        lg.debug("* UNWEIGHTED:")
        lg.debug("* Cluster (x, y) = (%6.2f, %6.2f)" % (self.__x_uw, self.__y_uw))
        lg.debug("* Cluster radius               = %10.5f" % self.__r_uw)
        lg.debug("* Cluster spatial density \\rho = %10.5f" % self.__rho_uw)
        lg.debug("*")
        lg.debug("* Line of best fit:          %f * x %+f" % (self.__lin_m, self.__lin_c))
        lg.debug("* Sum of residuals \Sum{R} = %f" % (self.__lin_sumR))
        lg.debug("* Linearity                = %f" % (self.__linearity))
        lg.debug("*")
        lg.debug("* Number of edge pixels    = %5d" % (self.__n_edge))
        lg.debug("*")

    def getKlusterPropertiesJson(self):

        m, c, sumR = self.getLineOfBestFitValues()

        p = {\
            "size"          : self.getNumberOfPixels(), \
            "xmin"          : self.getXMin(),           \
            "xmax"          : self.getXMax(),           \
            "ymin"          : self.getYMin(),           \
            "ymax"          : self.getYMax(),           \
            "width"         : self.getWidth(),          \
            "height"        : self.getHeight(),         \
            "x_uw"          : self.getXUW(),            \
            "y_uw"          : self.getYUW(),            \
            "radius_uw"     : self.getRadiusUW(),       \
            "density_uw"    : self.getDensityUW(),      \
            "totalcounts"   : self.getTotalCounts(),    \
            "maxcounts"     : self.getMaxCountValue(),  \
            "lin_m"         : m,                        \
            "lin_c"         : c,                        \
            "lin_sumofres"  : sumR,                     \
            "lin_linearity" : self.getLinearity(),      \
            #"n_edgepixels"  :, \
            #"edgefrac"      :, \
            #"innerfrac"     :, \
            #"ismc"          : self.isMC()\
            #"isedgekluster" : , \
            #"totalenergy"   :, \
            #"maxenergy"     :, \
            #"frameid"       :\
            }
        return p

    def getPixelMap(self):
        return self.__pixel_dict


class KlusterFinder:
    """
    Finds Klusters (blobs) in Timepix frames.

    @author Son Hoang (principle author).
    @author T. Whyntie (editor).
    """
    dir_x = [-1, -1,  0,  1,  1,  1,  0, -1]
    dir_y = [ 0,  1,  1,  1,  0, -1, -1, -1]

    def __init__(self, data, r, c, ismc, maskdict={}):

        """
        Constructor.

        @param [in] data A dictionary of pixel data - {X:C}.
        @param [in] r The number of rows in the originating frame.
        @param [in] c The number of columns in the originating frame.
        @param [in] ismc Is the cluster from simulated data?
        @param [in] maskdict A dictionary of masked pixels.
        """
        lg.debug(""); lg.debug(" Instantiating a cluster finder object."); lg.debug("")

        self.dbg = False # True
        #print "DEBUG: KlusterFinder initialize called."
        self.pixels = {} # map of {XY: Pixel}

        self.blob_list = []

        self.rows = r

        self.cols = c

        ## Are we looking at simulated data?
        self.__is_mc = ismc

        self.__pixel_map = deepcopy(data)

        # Remove the masked pixels from the data.
        if maskdict is not None:
            for X in maskdict:
                if X in self.__pixel_map.keys():
                    del self.__pixel_map[X]

        #print "DEBUG: Data supplied has %6d pixels." % \
        #  (len(data))
        #
        # An arbitrary check on number of pixels in the frame.
        #  if data.size() >= 10000 then return
        #
        # Loop over the data supplied to the KlusterFinder.
        # * Puts all of the data into the pixel map;
        # * Assigns neighbouring pixels where it find them.
        for xy, c in self.__pixel_map.iteritems():
            x = xy % self.cols; y = xy / self.cols
            self.pixels[xy] = Pixel(x,y,c,-1, self.rows, self.cols)

            # Loop over the eight possible directions.
            for direction in range(8):
                ny = y + self.dir_y[direction]  # Next row.
                nx = x + self.dir_x[direction]  # Next column.
                nxy = ny * self.cols + nx # The next xy value.

                # If the next row or column is on an edge, skip it.
                if ny<0 or ny>=self.rows or nx<0 or nx>=self.cols:
                    continue
                if nxy in self.pixels:
                    #print "DEBUG: *-----* Found neighbour in self.pixels!"
                    #print "DEBUG: *     \\--* xy = %d" % (nxy)
                    self.pixels[ xy].set_neighbour( direction,     nxy)
                    self.pixels[nxy].set_neighbour((direction+4)%8, xy)

        # Print out all pixels and neighbours
        if self.dbg:
            ## puts "DEBUG:"
            print "DEBUG: Looping over pixels in the @pixel_map:"
            print "DEBUG:---------------------------------------"
            for xy, p in self.pixels.iteritems():
                print "DEBUG: * Pixel at (%10d) -> (%3d, %3d) = %3d" % \
                  (xy, p.get_x(),p.get_y(),p.get_c())
                for direction, n in p.get_neighbours().iteritems():
                    print "DEBUG: *---> Neighbour in direction % 1d with ID=%s" % \
                      (direction, n)
                print "DEBUG:"
            print "DEBUG:"
        # Now loop over the pixels in the KlusterFinder's pixel_map
        # in order to create the blobs.
        #print "DEBUG: Creating the Klusters!"
        #print "DEBUG:"
        #print "DEBUG: Looping over the pixels in the @pixel_map:"
        #print "DEBUG:-------------------------------------------"
        for xy, p in self.pixels.iteritems():
            #print "DEBUG: * Pixel at (%3d, %3d) = %3d, mask = %3d" % \
            #  (p.get_x(),p.get_y(),p.get_c(),p.get_mask())
            # Start a new blob if the pixel hasn't been blobed yet.
            if p.get_mask() == -1:
                blob = Kluster(self.rows, self.cols, self.__is_mc)
                p.set_mask(0)
                #print "DEBUG: Mask set to %3d" % (p.get_mask())
                blob.insert(xy, p)
                # Loop over the list of pixels in the blob.
                for bxy in blob.get_pixel_xy_list():
                    #pb = self.pixels[bxy]
                    for direction in range(8):
                        if direction in self.pixels[bxy].get_neighbours():
                            #print "DEBUG: *---> Pixel found in direction %1d" % (direction)
                            nxy = self.pixels[bxy].get_neighbour(direction)
                            self.pixels[bxy].set_mask(self.pixels[bxy].get_mask() + pow(2, direction))
                            #print "DEBUG: *---> Setting mask to %3d" % \
                            # (self.pixels[bxy].get_mask() + 2.0 ** direction)
                            # If the Pixel isn't already in the Kluster, add it.
                            if not blob.contains_pixel(nxy):
                                blob.insert(nxy, self.pixels[bxy])
                            # end of Pixel presence check.
                        # end of Pixel neighbour in direction existence check.
                # end of loop over the directions.

                self.insert(blob)
            ## end of check on the Pixel mask (as to whether or not blobed).
        # end of loop over the Pixels
        #print "DEBUG:-------------------------------------------"
        if self.dbg:
            print "DEBUG:"
            print "DEBUG: Looping over the found blobs:"
            print "DEBUG:------------------------------"
            for b in self.blob_list:
                print "DEBUG: * %3d pixel(s) found." % (len(b.get_pixel_xy_list()))
            # end of loop over blobs
            print "DEBUG:------------------------------"

        ## The number of gamma candidates.
        self.__n_gammas = 0

        ## The number of monopixel candidates.
        self.__n_g1 = 0

        ## The number of bipixel candidates.
        self.__n_g2 = 0

        ## The number of tripixel candidates.
        self.__n_g3 = 0

        ## The number of tetrapixel candidates.
        self.__n_g4 = 0

        # Calculate the blob properties
        for b in self.blob_list:
            b.process(self.pixels)

            # Count the gamma candidates - we won't store these so we need to
            # know the numbers.
            if   b.getNumberOfPixels() == 1:
                self.__n_g1 += 1
            # Bipixel gamma.
            elif b.getNumberOfPixels() == 2:
                self.__n_g2 += 1
            # Tripixel...
            elif b.getNumberOfPixels() == 3:
                # Tripixel gamma.
                if b.r_u < TRIPIXEL_RADIUS: #0.75
                    self.__n_g3 += 1
            # Tetrapixel...
            elif b.getNumberOfPixels() == 4:
                # Tetrapixel gamma.
                if b.r_u < TETRAPIXEL_RADIUS: #0.71
                    self.__n_g4 += 1

            self.__n_gammas = self.__n_g1 + self.__n_g2 + self.__n_g3 + self.__n_g4

        # Sort the cluster list by cluster size.
        self.blob_list.sort(reverse=True)

    def insert(self, blob):
        self.blob_list.append(blob)

    def getNumberOfKlusters(self):
        return len(self.blob_list)

    def getListOfKlusters(self):
        return self.blob_list

    def getNumberOfGammas(self):
        return self.__n_gammas

    def getNumberOfMonopixels(self):
        return self.__n_g1

    def getNumberOfBipixels(self):
        return self.__n_g2

    def getNumberOfTripixelGammas(self):
        return self.__n_g3

    def getNumberOfTetrapixelGammas(self):
        return self.__n_g4



#class KlustersModel(QSqlRelationalTableModel, Table):
#    """
#    """
#
#    def __init__(self, database):
#        """
#        Constructor.
#        """
#
#        lg.debug(" Instantiating a KlustersModel object.")
#        lg.debug("")
#
#        # Initialise the base classes.
#        QSqlRelationalTableModel.__init__(self, db=database)
#
#        Table.__init__(self, "Klusters", database)
#
#    def addColumns(self):
#
#        # Add the columns.
#
#        self.cols[ 0] = Column("id", 0, primarykey=True, autoincr=True, unique=True, notnull=True)
#        self.cols[ 1] = Column("pixels", 3, notnull=True)
#        self.cols[ 2] = Column("size", 0, notnull=True)
#        self.cols[ 3] = Column("xmin", 0, notnull=True)
#        self.cols[ 4] = Column("xmax", 0, notnull=True)
#        self.cols[ 5] = Column("ymin", 0, notnull=True)
#        self.cols[ 6] = Column("ymax", 0, notnull=True)
#        self.cols[ 7] = Column("width", 0, notnull=True)
#        self.cols[ 8] = Column("height", 0, notnull=True)
#        self.cols[ 9] = Column("x_uw", 1, notnull=True)
#        self.cols[10] = Column("y_uw", 1, notnull=True)
#        self.cols[11] = Column("radius_uw", 1, notnull=True)
#        self.cols[12] = Column("density_uw", 1, notnull=True)
#        self.cols[13] = Column("totalcounts", 0, notnull=True)
#        self.cols[14] = Column("maxcounts", 0, notnull=True)
#        self.cols[15] = Column("lin_m", 1, notnull=True)
#        self.cols[16] = Column("lin_c", 1, notnull=True)
#        self.cols[17] = Column("lin_sumofres", 1, notnull=True)
#        self.cols[18] = Column("lin_linearity", 1, notnull=True)
#        self.cols[19] = Column("n_edgepixels", 0, notnull=True)
#        self.cols[20] = Column("edgefrac", 1, notnull=True)
#        self.cols[21] = Column("innerfrac", 1, notnull=True)
#        self.cols[22] = Column("ismc", 0, notnull=True)
#        self.cols[23] = Column("isedgekluster", 0, notnull=True)
#        self.cols[24] = Column("totalenergy", 1, notnull=True)
#        self.cols[25] = Column("maxenergy", 1, notnull=True)
#        self.cols[26] = Column("frameid", 0, notnull=True, foreignkey="Frames")
#
#
#    def setHeaders(self):
#
#        self.setHeaderData(0, Qt.Horizontal, QVariant(ID_HEADER))
#        self.setHeaderData(1, Qt.Horizontal, QVariant(KLUSTER_PIXELS_HEADER))
#        self.setHeaderData(2, Qt.Horizontal, QVariant(KLUSTER_SIZE_HEADER))
#        self.setHeaderData(3, Qt.Horizontal, QVariant(X_MIN_HEADER))
#        self.setHeaderData(4, Qt.Horizontal, QVariant(X_MAX_HEADER))
#        self.setHeaderData(5, Qt.Horizontal, QVariant(Y_MIN_HEADER))
#        self.setHeaderData(6, Qt.Horizontal, QVariant(Y_MAX_HEADER))
#        self.setHeaderData(7, Qt.Horizontal, QVariant(KLUSTER_WIDTH_HEADER))
#        self.setHeaderData(8, Qt.Horizontal, QVariant(KLUSTER_HEIGHT_HEADER))
#        self.setHeaderData(9, Qt.Horizontal, QVariant(KLUSTER_X_UW_HEADER))
#        self.setHeaderData(10, Qt.Horizontal, QVariant(KLUSTER_Y_UW_HEADER))
#        self.setHeaderData(11, Qt.Horizontal, QVariant(KLUSTER_RADIUS_UW_HEADER))
#        self.setHeaderData(12, Qt.Horizontal, QVariant(KLUSTER_DENSITY_UW_HEADER))
#        self.setHeaderData(13, Qt.Horizontal, QVariant(KLUSTER_TOTAL_COUNTS_HEADER))
#        self.setHeaderData(14, Qt.Horizontal, QVariant(KLUSTER_MAX_COUNT_HEADER))
#        self.setHeaderData(15, Qt.Horizontal, QVariant(KLUSTER_LIN_M_HEADER))
#        self.setHeaderData(16, Qt.Horizontal, QVariant(KLUSTER_LIN_C_HEADER))
#        self.setHeaderData(17, Qt.Horizontal, QVariant(KLUSTER_LIN_SUMOFR_HEADER))
#        self.setHeaderData(18, Qt.Horizontal, QVariant(KLUSTER_LINEARITY_HEADER))
#        self.setHeaderData(19, Qt.Horizontal, QVariant(KLUSTER_N_EDGE_HEADER))
#        self.setHeaderData(20, Qt.Horizontal, QVariant(KLUSTER_OUTERFRAC_HEADER))
#        self.setHeaderData(21, Qt.Horizontal, QVariant(KLUSTER_INNERFRAC_HEADER))
#        self.setHeaderData(22, Qt.Horizontal, QVariant(IS_MC_HEADER))
#        self.setHeaderData(23, Qt.Horizontal, QVariant(IS_EDGE_KLUSTER_HEADER))
#        self.setHeaderData(24, Qt.Horizontal, QVariant(KLUSTER_TOTAL_ENERGY_HEADER))
#        self.setHeaderData(25, Qt.Horizontal, QVariant(KLUSTER_MAX_ENERGY_HEADER))
#        self.setHeaderData(26, Qt.Horizontal, QVariant(FRAME_ID_HEADER))
