#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

 CERN@school - Processing Frames

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

#...for processing the datasets.
from cernatschool.dataset import Dataset

#...for making the frame and clusters images.
from visualisation.visualisation import makeFrameImage, makeKlusterImage

#...for getting the cluster properties JSON.
from cernatschool.helpers import getKlusterPropertiesJson


if __name__ == "__main__":

    print("*")
    print("*======================================*")
    print("* CERN@school - local frame processing *")
    print("*======================================*")

    # Get the datafile path from the command line.
    parser = argparse.ArgumentParser()
    parser.add_argument("inputPath",       help="Path to the input dataset.")
    parser.add_argument("outputPath",      help="The path for the output files.")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    parser.add_argument("-g", "--gamma",   help="Process gamma candidates too", action="store_true")
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
    lg.basicConfig(filename=outputpath + '/log_process-frames.log', filemode='w', level=level)

    print("*")
    print("* Input path          : '%s'" % (datapath))
    print("* Output path         : '%s'" % (outputpath))
    if args.gamma:
        print("* Gamma candidate clusters WILL be processed.")
    else:
        print("* Gamma candidate clusters WILL NOT be processed.")
    print("*")


    # Set up the directories
    #------------------------

    # Check if the output directory exists. If it doesn't, quit.
    if not os.path.isdir(outputpath):
        raise IOError("* ERROR: '%s' output directory does not exist!" % (outputpath))

    # Create the subdirectories.

    ## The path to the frame images.
    frpath = outputpath + "/frames/"
    #
    if os.path.isdir(frpath):
        rmtree(frpath)
        lg.info(" * Removing directory '%s'..." % (frpath))
    os.mkdir(frpath)
    lg.info(" * Creating directory '%s'..." % (frpath))
    lg.info("")

    ## The path to the cluster images.
    klpath = outputpath + "/clusters/"
    #
    if os.path.isdir(klpath):
        rmtree(klpath)
        lg.info(" * Removing directory '%s'..." % (klpath))
    os.mkdir(klpath)
    lg.info(" * Creating directory '%s'..." % (klpath))
    lg.info("")

    ## The dataset to process.
    ds = Dataset(datapath + "/ASCIIxyC/")

    # Get the metadata from the JSON.

    ## The frame metadata.
    fmd = None
    #
    with open(datapath + "/metadata.json", "r") as fmdf:
        fmd = json.load(fmdf, fmd)
    #
    ## Latitude of the dataset [deg.].
    lat = fmd[0]['lat'] # [deg.]
    #
    ## Longitude of the dataset [deg.].
    lon = fmd[0]['lon'] # [deg.]
    #
    ## Altitude of the dataset [m].
    alt = fmd[0]['alt'] # [m]

    ## The pixel mask.
    pixel_mask = {}

    with open(datapath + "/masked_pixels.txt", "r") as mpf:
        rows = mpf.readlines()
        for row in rows:
            vals = [int(val) for val in row.strip().split("\t")]
            x = vals[0]; y = vals[1]; X = (256*y) + x; C = 1
            pixel_mask[X] = C

    ## The frames from the dataset.
    frames = ds.getFrames((lat, lon, alt), pixelmask = pixel_mask)

    lg.info("* Found %d datafiles." % (len(frames)))

    ## A list of frames.
    mds = []

    # Clusters
    #----------

    ## A list of clusters.
    klusters = []

    # Loop over the frames and upload them to the DFC.
    for f in frames:

        ## The basename for the data frame, based on frame information.
        bn = "%s_%d-%06d" % (f.getChipId(), f.getStartTimeSec(), f.getStartTimeSubSec())

        # Create the frame image.
        makeFrameImage(bn, f.getPixelMap(), frpath)

        # Create the metadata dictionary for the frame.
        metadata = {
            "id"          : bn,
            #
            "chipid"      : f.getChipId(),
            "hv"          : f.getBiasVoltage(),
            "ikrum"       : f.getIKrum(),
            #
            "lat"         : f.getLatitude(),
            "lon"         : f.getLongitude(),
            "alt"         : f.getAltitude(),
            #
            "start_time"  : f.getStartTimeSec(),
            "end_time"    : f.getEndTimeSec(),
            "acqtime"     : f.getAcqTime(),
            #
            "n_pixel"     : f.getNumberOfUnmaskedPixels(),
            "occ"         : f.getOccupancy(),
            "occ_pc"      : f.getOccupancyPc(),
            #
            "n_kluster"   : f.getNumberOfKlusters(),
            "n_gamma"     : f.getNumberOfGammas(),
            "n_non_gamma" : f.getNumberOfNonGammas(),
            #
            "ismc"        : int(f.isMC())
            }

        # Add the frame metadata to the list of frames.
        mds.append(metadata)

        # The cluster analysis
        #----------------------

        # Loop over the clusters.
        for i, kl in enumerate(f.getKlusterFinder().getListOfKlusters()):

            if not args.gamma and kl.isGamma():
                continue

            ## The kluster ID.
            klusterid = bn + "_k%05d" % (i)

            # Get the cluster properties JSON entry and add it to the list.
            klusters.append(getKlusterPropertiesJson(klusterid, kl))

            # Make the cluster image.
            makeKlusterImage(klusterid, kl, klpath)

        #break # TMP - uncomment to only process the first frame.

    # Write out the frame information to a JSON file.
    with open(outputpath + "/frames.json", "w") as jf:
        json.dump(mds, jf)

    # Write out the cluster information to a JSON file.
    with open(outputpath + "/klusters.json", "w") as jf:
        json.dump(klusters, jf)
