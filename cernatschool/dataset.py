#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Wrapper class for the CERN@school Timepix datasets.
"""

# The usual suspects.
import os, glob, inspect

#...for the logging.
import logging as lg

#...for the data values.
from datavals import *

#...for processing the file format.
from helpers import getFormat

#...for the DSC file wrapper class.
from dsc import DscFile

#...for the frames.
from frame import Frame

class Dataset:
    """ Wrapper class for the CERN@school Timepix datasets. """

    def __init__(self, foldername):

        # Check if the folder exists. If it doesn't, throw an exception.
        if not os.path.exists(foldername):
            #raise IOError("The folder doesn't exist.")
            raise IOError("NOT_EXIST")

        ## The folder name.
        self.foldername = foldername

        ## The list of names of files in the folder (sorted).
        self.filenames = sorted(glob.glob(foldername + "/*"))

        # Throw an exception if the supplied folder is empty.
        if len(self.filenames) == 0:
            #raise IOError("The folder is empty.")
            raise IOError("FOLDER_EMPTY")

        ## The datafile names.
        self.datfilenames = {}

        ## The DSC file names.
        self.dscfilenames = {}

        ## The datafile formats.
        self.datfileformats = {}

        # Loop over the files found in the folder.
        lg.debug("")
        lg.debug(" Files found in '%s':" % (foldername))
        lg.debug("")
        for i, fn in enumerate(self.filenames):

            ## The basename of the file.
            bn = os.path.basename(fn)

            lg.debug(" * '%s'" % (bn))

            # If the "file" is a directory, raise an exception.
            if os.path.isdir(fn):
                raise IOError("CONTAINS_DIR")

            formatval = getFormat(fn)

            ## If the file isn't recognised, raise an exception.
            if formatval == 0:
                lg.debug("'%s' is in an unrecognised format." % (bn))
                raise IOError("BAD_FORMAT")
            elif formatval > 0:
                lg.debug(" *--> Adding '%s' ('%s' format) to the data files." \
                    % (bn, DATA_FILE_TYPES[formatval]))

                self.datfilenames[i] = bn

                self.datfileformats[i] = formatval

            else:
                lg.debug(" *--> Adding '%s' ('%s' format) to the DSC files." \
                    % (bn, DATA_FILE_TYPES[formatval]))

                self.dscfilenames[i] = bn

        lg.debug("")

        # Check the consistency of the data file formats.
        if not self.areFormatsConsistent():
            lg.debug(" The file formats are inconsistent!")
            raise IOError("FORMAT_MISMATCH")

        # Check that each data file has a matching DSC file.
        if not self.dscFilesPresent():
            lg.debug(" There are DSC files missing!")
            raise IOError("MISSING_DSC")

        lg.debug(" There are %d data files." % (self.getNumberOfDataFiles())); lg.debug("")

        # Now process the DSC files to extract the information we need
        # to build the data set information.

        ## The DSC file wrappers.
        self.dscfiles = sorted([DscFile(foldername + "/" + fn) for fn in self.dscfilenames.values()])


    def areFormatsConsistent(self):
        """ Check if the data files found are all the same format. """

        try:

            ## The list of format values.
            formats = self.datfileformats.values()

            # Check if the formats are all identical.
            result = formats.count(formats[0]) == len(formats)

            if result:
                lg.debug(" The formats are consistent (%s)." % (DATA_FILE_TYPES[formats[0]]))
                lg.debug("")

            return result

        except IndexError:
            print("* ERROR: calling areFormatsConsistent() with no files!")
            return False

    def dscFilesPresent(self):
        """ Check if the corresponding detector settings files exist. """

        # Loop through the data files and check if a matching
        # DSC file has been found.
        for i, bn in self.datfilenames.iteritems():

            ## The DSC file name for the data file.
            dscn = bn + ".dsc"

            if not dscn in self.dscfilenames.values():
                lg.debug("Data file '%s' is missing a DSC file." % (bn))
                return False

        lg.debug(" All files have corresponding DSC files."); lg.debug("")

        return True

    def getNumberOfDataFiles(self):
        return len(self.datfilenames)

    def getFolderFormat(self):
        """ Gets the format of the datafiles in the folder supplied. """
        if self.areFormatsConsistent():
            return DATA_FILE_TYPES[self.datfileformats[0]]
        else:
            return "various"

    def getFrames(self, geo, **kwargs):
        """ Extract the frames from the dataset. """

        # Get the geospatial information from the tuple provided.
        lat = geo[0]; lon = geo[1]; alt = geo[2]

        ## The list of frames to return.
        frames = []

        # Loop over the DSC files to get each frame.
        for df in self.dscfiles:
            #print df.getDscFilename(), df.getDataFilename()

            frameargs = {\
                "lat"         : lat, \
                "lon"         : lon, \
                "alt"         : alt, \
                #
                "chipid"      : df.getChipId(), \
                "biasvoltage" : df.getBiasVoltage(), \
                "ikrum"       : df.getIKrum(), \
                #
                "starttime"   : df.getStartTime(), \
                "acqtime"     : df.getAcqTime(), \
                "width"       : df.getFrameWidth(), \
                "height"      : df.getFrameHeight(), \
                "format"      : self.datfileformats[0], \
                "pixelmap"    : df.getPixelMap(), \
                "ismc"        : False\
                }

            # Optional properties.
            for key, arg in kwargs.iteritems():
                frameargs[key] = kwargs[key]

            # Add the frame to the list of frames.
            frames.append(Frame(**frameargs))

        return frames
