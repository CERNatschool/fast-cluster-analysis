#!/usr/bin/env python

"""
Wrapper class and helper methods for the Timepix DSC files.
"""

# The usual suspects.
import os, glob, inspect

#...for the logging.
import logging as lg

#...for the data values.
from datavals import *

#...for the DSC values.
from dscvals import *

#...for the handling.
from handlers import isChipIdValid, getPixelmanTimeString

#...for the HELPING.
from helpers import getFormat

class DscFile:
    """
    A wrapper class for the Pixelman DSC files.
    """

    def __init__(self, dscfilename):
        """ The constructor. """

        # Check if the file exists. If it doesn't, throw an exception.
        if not os.path.exists(dscfilename):
            raise IOError("NOT_EXIST")

        # Check that the file is, indeed, a file.
        if not os.path.isfile(dscfilename):
            raise IOError("NOT_FILE")

        ## The frame width.
        self.__fWidth = None

        ## The frame height.
        self.__fHeight = None

        ## The acquisition mode.
        self.__acqMode = None

        ## The acquisition time.
        self.__acqTime = None

        ## The chip ID.
        self.__chipid = None

        ## The DAC values.
        self.__dacs = None

        ## The firmware version.
        self.__firmwarev = None

        ## The bias voltage.
        self.__hv = None

        ## The HW timer mode.
        self.__hwTimerMode = None

        ## The interface.
        self.__interface = None

        ## The Medipix clock value.
        self.__mpxClock = None

        ## The Medipix type.
        self.__mpxType = None

        ## The Pixelman version.
        self.__pixelmanv = None

        ## The polarity.
        self.__polarity = None

        ## The start time.
        self.__startTime = None

        ## The start time (string).
        self.__startTimeS = None

        ## The Timepix clock value.
        self.__tpxClock = None

        ## The name and serial number.
        self.__nameAndSN = None

        ## The DSC file name.
        self.__dscfilename = dscfilename

        ## The data file name.
        self.__datafilename = dscfilename[:-4]

        if not os.path.exists(self.__datafilename):
            raise IOError #("MISSING_DAT")

        # Process the DSC file.
        self.processDscFile()

        ## The pixel map.
        self.__pixelmap = {}

        ## The data file format.
        self.__format = getFormat(self.__datafilename)

        # Process the data file.
        self.processDataFile()

    def __lt__(self, other):
        return self.getStartTime() < other.getStartTime()

    def getDscFilename(self):
        return self.__dscfilename

    def getDataFilename(self):
        return self.__datafilename

    def getFrameWidth(self):
        return self.__fWidth

    def getFrameHeight(self):
        return self.__fHeight

    def getAcqMode(self):
        return self.__acqMode

    def getAcqTime(self):
        return self.__acqTime

    def getChipId(self):
        return self.__chipid

    def getDACs(self):
        return self.__dacs

    def getFirmwareVersion(self):
        return self.__firmwarev

    def getBiasVoltage(self):
        return self.__hv

    def getIKrum(self):
        return self.__IKrum

    def getDisc(self):
        return self.__Disc

    def getPreamp(self):
        return self.__Preamp

    def getBuffAnalogA(self):
        return self.__BuffAnalogA

    def getBuffAnalogB(self):
        return self.__BuffAnalogB

    def getHist(self):
        return self.__Hist

    def getTHL(self):
        return self.__THL

    def getTHLCoarse(self):
        return self.__THLCoarse

    def getVcas(self):
        return self.__Vcas

    def getFBK(self):
        return self.__FBK

    def getGND(self):
        return self.__GND

    def getTHS(self):
        return self.__THS

    def getBiasLVDS(self):
        return self.__BiasLVDS

    def getRefLVDS(self):
        return self.__RefLVDS

    def getHwTimerMode(self):
        return self.__hwTimerMode

    def getInterface(self):
        return self.__interface

    def getMpxClock(self):
        return self.__mpxClock

    def getMpxType(self):
        return self.__mpxType

    def getPixelmanVersion(self):
        return self.__pixelmanv

    def getPolarity(self):
        return self.__polarity

    def getStartTime(self):
        return self.__startTime

    def getStartTimeS(self):
        return self.__startTimeS

    def getTpxClock(self):
        return self.__tpxClock

    def getNameAndSerialNumber(self):
        return self.__nameAndSN

    def getBSPreampEnabled(self):
        return self.__bspenabled

    def getPixelMap(self):
        return self.__pixelmap

    def processDscFile(self):
        """ Process the detector settings file (.dsc). """

        # The DSC file.
        f = open(self.__dscfilename, "r")

        ## The lines of the DSC file.
        ls = f.readlines()

        # Close the DSC file.
        f.close()

        lg.debug("")

        # The frame width and height.
        whvals = ls[2].strip().split(" ")

        try:
            self.__fWidth = int(whvals[2].split("=")[1])
        except TypeError:
            raise IOError("BAD_WIDTH")

        if self.__fWidth < 256 or self.__fWidth > 1024:
            raise IOError("BAD_WIDTH")

        try:
            self.__fHeight = int(whvals[3].split("=")[1])
        except TypeError:
            raise IOError("BAD_HEIGHT")

        if self.__fHeight < 256 or self.__fHeight > 1024:
            raise IOError("BAD_HEIGHT")

        lg.debug(" * Frame dimensions: %d [pix.] x %d [pix.]." % (self.__fWidth, self.__fHeight))

        # Loop over the lines of the DSC file.
        for i, l in enumerate(ls):
            #print("%5d: %s" % (i, l.strip()))

            # Acquisition mode.
            if DSC_ACQ_MODE_STRING in l:
                try:
                    self.__acqMode = int(ls[i+2].strip())
                except ValueError:
                    raise IOError("BAD_ACQ_MODE")
                lg.debug(" * Acquisition mode is '%s'." % (ACQ_MODES[self.__acqMode]))

            elif DSC_ACQ_TIME_STRING in l:
                try:
                    self.__acqTime = float(ls[i+2].strip())
                except ValueError:
                    raise IOError("BAD_ACQ_TIME")
                lg.debug(" * Acquisition time is '%f' [%s]." % (self.__acqTime, ACQ_TIME_UNITS_SHORT))

            elif DSC_CHIPID_STRING in l:

                chipid = ls[i+2].strip()
                if not isChipIdValid(chipid):
                    raise IOError("Invalid chip ID in the DSC file.")
                self.__chipid = chipid
                lg.debug(" * Chip ID is '%s'." % (self.__chipid))

            elif DSC_DACS_STRING in l:

                # Break down the DAC string.
                self.__dacs = [int(x) for x in ls[i+2].strip().split(" ")]

                self.__IKrum       = self.__dacs[0]
                self.__Disc        = self.__dacs[1]
                self.__Preamp      = self.__dacs[2]
                self.__BuffAnalogA = self.__dacs[3]
                self.__BuffAnalogB = self.__dacs[4]
                self.__Hist        = self.__dacs[5]
                self.__THL         = self.__dacs[6]
                self.__THLCoarse   = self.__dacs[7]
                self.__Vcas        = self.__dacs[8]
                self.__FBK         = self.__dacs[9]
                self.__GND         = self.__dacs[10]
                self.__THS         = self.__dacs[11]
                self.__BiasLVDS    = self.__dacs[12]
                self.__RefLVDS     = self.__dacs[13]

                lg.debug(" * DAC values:")
                lg.debug(" * --> IKrum           = %4d" % (self.__IKrum))
                lg.debug(" * --> Disc            = %4d" % (self.__Disc))
                lg.debug(" * --> Preamp          = %4d" % (self.__Preamp))
                lg.debug(" * --> BuffAnalogA     = %4d" % (self.__BuffAnalogA))
                lg.debug(" * --> BuffAnalogB     = %4d" % (self.__BuffAnalogB))
                lg.debug(" * --> Hist            = %4d" % (self.__Hist))
                lg.debug(" * --> THL             = %4d" % (self.__THL))
                lg.debug(" * --> THLCoarse       = %4d" % (self.__THLCoarse))
                lg.debug(" * --> Vcas            = %4d" % (self.__Vcas))
                lg.debug(" * --> FBK             = %4d" % (self.__FBK))
                lg.debug(" * --> GND             = %4d" % (self.__GND))
                lg.debug(" * --> THS             = %4d" % (self.__THS))
                lg.debug(" * --> BiasLVDS        = %4d" % (self.__BiasLVDS))
                lg.debug(" * --> RefLVDS         = %4d" % (self.__RefLVDS))

            elif DSC_FIRMWARE_STRING in l:
                self.__firmwarev = ls[i+2].strip()

            # Note - needs 'lower()' because of a 2.1.1/2.2.2 mismatch...
            elif DSC_BIAS_VOLTAGE_STRING.lower() in l.lower():
                try:
                    hv = float(ls[i+2].strip())
                except ValueError:
                    raise IOError("BAD_HV_VALUE")

                if hv < 0.0 or hv > 100.0:
                    raise IOError("BAD_HV_VALUE")

                self.__hv = hv
                lg.debug(" * Bias voltage (HV) is %f [V]." % (self.__hv))

            elif DSC_HW_TIMER_STRING in l:
                try:
                    self.__hwTimerMode = int(ls[i+2].strip())
                except ValueError:
                    raise IOError("BAD_HW_TIMER_MODE")
                lg.debug(" * Hardware time mode is '%s'." % (HW_TIME_MODES[self.__hwTimerMode]))

            elif DSC_INTERFACE_STRING in l:
                self.__interface = ls[i+2].strip()
                lg.debug(" * Interface is '%s'." % (self.__interface))

            elif DSC_MPX_CLOCK_STRING in l:
                try:
                    mpxClock = float(ls[i+2].strip())
                except ValueError:
                    raise IOError("BAD_MPX_CLOCK")
                self.__mpxClock = mpxClock
                lg.debug(" * Medipix clock is %f [MHz]." % (self.__mpxClock))

            elif DSC_MPX_TYPE_STRING in l:
                try:
                    mpxType = int(ls[i+2].strip())
                except ValueError:
                    raise IOError("BAD_MPX_TYPE")
                if mpxType not in [1,2,3]:
                    raise IOError("BAD_MPX_TYPE")
                self.__mpxType = mpxType
                lg.debug(" * Detector type is '%s'." % (MPX_TYPES_LONG[self.__mpxType]))

            elif DSC_PIXELMAN_VERSION_STRING in l:
                self.__pixelmanv = ls[i+2].strip()
                lg.debug(" * Pixelman version is '%s'." % (self.__pixelmanv))

            elif DSC_POLARITY_STRING in l:
                try:
                    pol = int(ls[i+2].strip())
                except ValueError:
                    raise IOError("BAD_POLARITY")
                if pol not in [0,1]:
                    raise IOError("BAD_POLARITY")
                self.__polarity = pol
                lg.debug(" * Polarity is '%s'." % (POLARITIES[self.__polarity]))

            elif DSC_START_TIME_STRING in l:

                try:
                    ## The full start time.
                    st = float(ls[i+2].strip())

                    self.__startTime = st

                except:
                    raise IOError("BAD_START_TIME")

                sec, sub, sts = getPixelmanTimeString(st)

                self.__startTimeS = sts

                lg.debug(" * Start time is %20.6f [s]." % (self.__startTime))
                lg.debug(" *--> Converted to string: '%s'." % (sts))

                # Check if the start time matches the supplied string.
                #if self.__startTimeS is not None and sts != self.__startTimeS:
                #    lg.debug(" * A mismatch between the start times.")
                #    raise IOError("START_TIME_MISMATCH")

            #elif DSC_START_TIME_S_STRING in l:
            #
            #    # Set the start time string from the DSC file.
            #    self.__startTimeS = ls[i+2].strip()
            #
            #    lg.debug(" * Start time (string) is '%s'." % (self.__startTimeS))
            #
            #    #if self.__startTime is not None:
            #    #    sec, sub, sts = getPixelmanTimeString(self.__startTime)
            #    #    #if self.__startTimeS != sts:
            #    #    #    raise IOError("START_TIME_MISMATCH")

            elif DSC_TPX_CLOCK_STRING.lower() in l.lower():

                if "byte[1]" in ls[i+1].strip():

                    val = int(ls[i+2].strip())

                    if val not in [0,1,2,3]:
                        raise("BAD_TPX_CLOCK_MODE")

                    self.__tpxClock = TPX_CLOCK_VALS[val]
                    lg.debug(" * Timepix clock = %f [MHz]." % (self.__tpxClock))

                elif "double[1]" in ls[i+1].strip():
                    self.__tpxClock = float(ls[i+2].strip())
                else:
                    raise IOError("BAD_TPX_CLOCK")

            elif DSC_NAME_SN_STRING in l:
                self.__nameAndSN = ls[i+2].strip()
                lg.debug(" * Name and serial no. = '%s'." % (self.__nameAndSN))

        lg.debug("")

    def processDataFile(self):
        """ Process the accompanying Timepix datafile. """

        df = open(self.__datafilename, "r")
        ls = df.readlines()
        df.close()

        # Loop over the lines in the file.
        for j, l in enumerate(ls):

            if   self.__format == 4114: # ASCII xyC.
                vals = l.strip().split("\t")
                self.__pixelmap[self.__fHeight * int(vals[1]) + int(vals[0])] = int(vals[2])
            elif self.__format == 18: # ASCII matrix.
                vals = [int(val) for val in l.strip().split(" ")]
                for i, C in enumerate(vals):
                    if C > 0:
                        self.__pixelmap[(self.__fHeight * j) + i] = C
            elif self.__format == 8210: # ASCII XC
                vals = [int(val) for val in l.strip().split("\t")]
                self.__pixelmap[vals[0]] = vals[1]
            else:
                raise IOError("FRAME_BAD_FORMAT")
