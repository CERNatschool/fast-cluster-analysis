#!/usr/bin/env python

import numpy as np

from pixel import *

###/*! \brief Container class for Blobs (blobs).
### * @author Son Hoang (principle author).
### * @author T. Whyntie (editor for CERN@school).
### */
class Blob:
    """
    """
    def __init__(self):
        self.dbg = False #True

        self.total_counts = 0

        self.pixel_xy_list = [] # List of the XY positions of the pixels
                                # in the cluster
        #
        # Size - covered by the get_size method.
        self.pixel_string = "" # multiline JSON entry for the pixel
        #
        # Convenience values
        self.x_min = 256
        self.x_max = 0
        self.y_min = 256
        self.y_max = 0
        self.c_max = 0
        #
        # Spatial properties
        #
        # Unweighted (u subsctript)
        self.x_bar_u = -1.0
        self.y_bar_u = -1.0
        self.r_u     = -1.0
        self.spatial_density_u = -1.0
        #
        # Weighted by pixel counts
        self.x_bar_c = -1.0
        self.y_bar_c = -1.0
        self.r_c     = -1.0


    def get_pixel_xy_list(self):
        return self.pixel_xy_list

    def insert(self, pixel_xy, pixel):
        self.pixel_xy_list.append(pixel_xy)
        self.total_counts += pixel.get_c()

    def contains_pixel(self, pixel_xy):
        return pixel_xy in self.pixel_xy_list

    def get_size(self):
        return len(self.pixel_xy_list)

    def get_total_counts(self):
        return self.total_counts

    def process(self, pixels):
        #
        # Note that the pixels are stored in and obtained from the BlobFinder.

        # Start the string for the pixel JSON
        self.pixels_string  = "pixels = [\n"

        xs = []; ys = []; cs = []; xcs = []; ycs = []

        # Loop over the pixels
        for bxy in self.pixel_xy_list:
            #
            x = float(pixels[bxy].x); y = float(pixels[bxy].y)
            c = float(pixels[bxy].c)
            xs.append(x); ys.append(y); cs.append(c)
            xcs.append(x*c); ycs.append(y*c)

            # Add the pixel to the pixel JSON text.
            self.pixels_string += "  " + pixels[bxy].pixel_entry()

            # Find the min and max x, y and c values
            if pixels[bxy].x < self.x_min: self.x_min = pixels[bxy].x
            if pixels[bxy].x > self.x_max: self.x_max = pixels[bxy].x
            if pixels[bxy].y < self.y_min: self.y_min = pixels[bxy].y
            if pixels[bxy].y > self.y_max: self.y_max = pixels[bxy].y
            if pixels[bxy].c > self.c_max: self.c_max = pixels[bxy].c

        self.x_bar_u = np.mean(xs)
        self.y_bar_u = np.mean(ys)

        # Find the cluster radii
        rmax = 0.0
        for bxy in self.pixel_xy_list:
            r_x = float(pixels[bxy].x) - self.x_bar_u
            r_y = float(pixels[bxy].y) - self.y_bar_u
            if (r_x*r_x + r_y*r_y) > rmax: rmax = r_x*r_x + r_y*r_y
        self.r_u = np.sqrt(rmax)

        # Find the spatial density
        if self.r_u > 0.0:
            self.spatial_density_u = float(len(self.pixel_xy_list))/(self.r_u * self.r_u * np.pi)
        else:
            self.spatial_density_u = 0.0

        # End the string for the pixel JSON
        self.pixels_string += "]"

        if self.dbg:
            print(self.pixels_string)
            print("* x_min       = %3d" % self.x_min)
            print("* x_max       = %3d" % self.x_max)
            print("* y_min       = %3d" % self.y_min)
            print("* y_max       = %3d" % self.y_max)
            print("*")
            print("* c_max       = %3d" % self.c_max)
            print("*")
            print("* UNWEIGHTED:")
            print("* Blob (x, y) = (%6.2f, %6.2f)" % (self.x_bar_u, self.y_bar_u))
            print("* Blob radius               = %10.5f" % self.r_u)
            print("* Blob spatial density \\rho = %10.5f" % self.spatial_density_u)

class BlobFinder:
    """
    Finds Blobs (blobs) in Timepix frames.
    @author Son Hoang (principle author).
    @author T. Whyntie (editor).
    """
    dir_x = [-1, -1,  0,  1,  1,  1,  0, -1]
    dir_y = [ 0,  1,  1,  1,  0, -1, -1, -1]

    def __init__(self, data, r, c):
        self.dbg = False # True
        #print "DEBUG: BlobFinder initialize called."
        self.pixels = {} # map of {XY: Pixel}

        self.blob_list = []
        self.rows = r
        self.cols = c

        #print "DEBUG: Data supplied has %6d pixels." % \
        #  (len(data))
        #
        # An arbitrary check on number of pixels in the frame.
        #  if data.size() >= 10000 then return
        #
        # Loop over the data supplied to the BlobFinder.
        # * Puts all of the data into the pixel map;
        # * Assigns neighbouring pixels where it find them.
        #print "DEBUG:"
        #print "DEBUG: BlobFinder - looping over the pixel data "
        #print "DEBUG:------------------------------------------"
        for xy, c in data.iteritems():
            x = xy % self.cols; y = xy / self.cols
            self.pixels[xy] = Pixel(x,y,c,-1)
            #print "DEBUG: * Pixel created (%10d) -> (%3d, %3d) = %3d" % \
            #  (xy,x,y,c)

            # Loop over the eight possible directions.
            #print "DEBUG: *--> Looping over the eight possible directions:"
            for direction in range(8):
                ny = y + self.dir_y[direction]  # Next row.
                nx = x + self.dir_x[direction]  # Next column.
                nxy = ny * self.cols + nx # The next xy value.
                #print "DEBUG: *-----* %1d->(% 1d, % 1d) is (%3d,%3d)->(%10d)" % \
                #  (direction, self.dir_x[direction], self.dir_y[direction], nx, ny, nxy)
                # If the next row or column is on an edge, skip it.
                if ny<0 or ny>=self.rows or nx<0 or nx>=self.cols:
                    continue
                if nxy in self.pixels:
                    #print "DEBUG: *-----* Found neighbour in self.pixels!"
                    #print "DEBUG: *     \\--* xy = %d" % (nxy)
                    self.pixels[ xy].set_neighbour( direction,     nxy)
                    self.pixels[nxy].set_neighbour((direction+4)%8, xy)
            #print "DEBUG:"
        ## puts "DEBUG: End of loop over the supplied pixel data." if dbg
        ## puts "DEBUG:------------------------------------------" if dbg
        #print "DEBUG:"
        #print "DEBUG: Size of the BlobFinder's pixel_map = %d" % \
        #  (len(self.pixels))

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
        # Now loop over the pixels in the BlobFinder's pixel_map
        # in order to create the blobs.
        #print "DEBUG: Creating the Blobs!"
        #print "DEBUG:"
        #print "DEBUG: Looping over the pixels in the @pixel_map:"
        #print "DEBUG:-------------------------------------------"
        for xy, p in self.pixels.iteritems():
            #print "DEBUG: * Pixel at (%3d, %3d) = %3d, mask = %3d" % \
            #  (p.get_x(),p.get_y(),p.get_c(),p.get_mask())
            # Start a new blob if the pixel hasn't been blobed yet.
            if p.get_mask() == -1:
                blob = Blob()
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
                            # If the Pixel isn't already in the Blob, add it.
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

        # Calculate the blob properties
        for b in self.blob_list:
            #print("Processing blob with size %d" % b.get_size())
            b.process(self.pixels)
            #print

    def insert(self, blob):
        self.blob_list.append(blob)

    def get_size(self):
        return len(self.blob_list)


#end of BlobFinder class definition.
