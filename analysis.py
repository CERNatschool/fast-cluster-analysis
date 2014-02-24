#!/usr/bin/env python

#=============================================================================

# Import the code needed to manage files.
import os, inspect, glob, argparse

# Import the clustering and web-page writing code.
from clustering import *

def analyse(path, min_size, min_rad, oneframe):

    cluster_size = []

    # Loop over the datafiles and read the data.
    for datafilename in glob.glob(path + "/*.txt"):

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
            if b.get_size() >= min_size and b.r_u >= min_rad:
                cluster_size.append(b.get_size())
                #cluster_counts.append(b.get_total_counts())
                #cluster_radius_u.append(b.r_u)
                #cluster_density_u.append(b.spatial_density_u)

        if oneframe:
            break

    return cluster_size
