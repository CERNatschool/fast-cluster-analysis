#!/usr/bin/env python
# -*- coding: utf-8 -*-

#...for the logging.
import logging as lg

##...for the data values.
#from datavals import *

#...for the HANDLING.
from handlers import getPixelmanTimeString, getPixelsStringFromPixelMap

#...for the Klusters (Clusters).
from kluster import KlusterFinder

class Frame:
    """
    A wrapper class for Timepix frames.
    """

    def __init__(self, **kwargs):
        """
        Constructor.
        """
        lg.debug(" Instantiating a Frame object.")

        # Geospatial information
        #------------------------

        if "lat" not in kwargs.keys():
            raise IOError("FRAME_NO_LAT")

        ## The frame latitude [deg.].
        self.__lat = kwargs["lat"]

        if "lon" not in kwargs.keys():
            raise IOError("FRAME_NO_LON")

        ## The frame longitude [deg.].
        self.__lon = kwargs["lon"]

        if "alt" not in kwargs.keys():
            raise IOError("FRAME_NO_ALT")

        ## The frame altitude [m].
        self.__alt = kwargs["alt"]

        ## The roll angle of the lab. frame [deg.].
        self.__roll = 0.0
        if "roll" in kwargs.keys():
            # TODO: validate the value.
            self.__roll = kwargs["roll"]

        ## The pitch angle of the lab. frame [deg.].
        self.__pitch = 0.0
        if "pitch" in kwargs.keys():
            # TODO: validate the value.
            self.__pitch = kwargs["pitch"]

        ## The yaw angle of the lab. frame [deg.].
        self.__yaw = 0.0
        if "yaw" in kwargs.keys():
            # TODO: validate the value.
            self.__yaw = kwargs["yaw"]

        ## The Omega_x of the lab frame [deg. s^{-1}].
        self.__omegax = 0.0
        if "omegax" in kwargs.keys():
            self.__omegax = kwargs["omegax"]

        ## The Omega_y of the lab frame [deg. s^{-1}].
        self.__omegay = 0.0
        if "omegay" in kwargs.keys():
            self.__omegay = kwargs["omegay"]

        ## The Omega_z of the lab frame [deg. s^{-1}].
        self.__omegaz = 0.0
        if "omegaz" in kwargs.keys():
            self.__omegaz = kwargs["omegaz"]

        # For the detector.

        if "chipid" not in kwargs.keys():
            raise IOError("FRAME_NO_CHIPID")

        ## The chip ID.
        self.__chipid = kwargs["chipid"]

        if "biasvoltage" not in kwargs.keys():
            raise IOError("FRAME_NO_HV")

        ## The bias voltage (HV) [V].
        self.__hv = kwargs["biasvoltage"]

        if "ikrum" not in kwargs.keys():
            raise IOError("FRAME_NO IKRUM")

        ## The detector I_Krum value.
        self.__ikrum = kwargs["ikrum"]

        ## The detector x position [mm].
        self.__det_x = 0.0
        if "detx" in kwargs.keys():
            self.__det_x = kwargs["detx"]

        ## The detector y position [mm].
        self.__det_y = 0.0
        if "dety" in kwargs.keys():
            self.__det_y = kwargs["dety"]

        ## The detector z position [mm].
        self.__det_z = 0.0
        if "detz" in kwargs.keys():
            self.__det_z = kwargs["detz"]

        ## The detector Euler angle a [deg.].
        self.__det_euler_a = 0.0
        if "deteulera" in kwargs.keys():
            self.__det_euler_a = kwargs["deteulera"]

        ## The detector Euler angle b [deg.].
        self.__det_euler_b = 0.0
        if "deteulerb" in kwargs.keys():
            self.__det_euler_b = kwargs["deteulerb"]

        ## The detector Euler angle c [deg.].
        self.__det_euler_c = 0.0
        if "deteulerc" in kwargs.keys():
            self.__det_euler_c = kwargs["deteulerc"]


        # Temporal information
        #----------------------

        if "starttime" not in kwargs.keys() or "acqtime" not in kwargs.keys():
            raise IOError("BAD_FRAME_TIME_INFO")

        ## The start time [s].
        self.__starttime = kwargs["starttime"]

        ## The acquisition time [s].
        self.__acqtime = kwargs["acqtime"]

        self.__starttimesec, self.__starttimesubsec, sts = \
            getPixelmanTimeString(self.__starttime)
        lg.debug(" Frame found with start time: '%s'." % (sts))

        ## The end time [s].
        self.__endtime = self.__starttime + self.__acqtime

        self.__endtimesec, self.__endtimesubsec, ets = \
            getPixelmanTimeString(self.__endtime)


        # Payload information
        #--------------------

        ## The frame width.
        self.__width = 256

        if "width" in kwargs.keys():
            self.__width = kwargs["width"]

        ## The frame height.
        self.__height = 256

        if "height" in kwargs.keys():
            self.__height = kwargs["height"]

        if "format" not in kwargs.keys():
            raise IOError("FRAME_NO_FORMAT")

        ## The payload format.
        self.__format = kwargs["format"]

        ## The map of the pixels.
        self.__pixelmap = {}

        if "pixelmap" in kwargs.keys():
            self.__pixelmap = kwargs["pixelmap"]

        ## The pixel mask map.
        self.__pixel_mask_map = {}

        if "pixelmask" in kwargs.keys():
            self.__pixel_mask_map = kwargs["pixelmask"]

        ## Is the data from a Monte Carlo simulation?
        self.__isMC = False
        if "ismc" in kwargs.keys():
            self.__ismc = kwargs["ismc"]

        if "skipclustering" in kwargs.keys():
            if kwargs["skipclustering"]:
                #print("SKIPPING THE CLUSTERING!")
                self.__n_klusters = -1
                return None

        # Do the clustering.

        ## The frame's cluster finder.
        self.__kf = KlusterFinder(self.getPixelMap(), self.getWidth(), self.getHeight(), self.isMC(), self.__pixel_mask_map)

        self.__n_klusters = self.__kf.getNumberOfKlusters()

    # Accessor methods
    #==================

    # Geospatial information
    #------------------------

    def getLatitude(self):
        return self.__lat

    def getLongitude(self):
        return self.__lon

    def getAltitude(self):
        return self.__alt

    def getRoll(self):
        return self.__roll

    def getPitch(self):
        return self.__pitch

    def getYaw(self):
        return self.__yaw

    def getOmegax(self):
        return self.__omegax

    def getOmegay(self):
        return self.__omegay

    def getOmegaz(self):
        return self.__omegaz

    def getDetx(self):
        return self.__det_x

    def getDety(self):
        return self.__det_y

    def getDetz(self):
        return self.__det_z

    def getDetEulera(self):
        return self.__det_euler_a

    def getDetEulerb(self):
        return self.__det_euler_b

    def getDetEulerc(self):
        return self.__det_euler_c

    def getChipId(self):
        return self.__chipid

    def getBiasVoltage(self):
        return self.__hv

    def getIKrum(self):
        return self.__ikrum

    # Temporal information
    #----------------------

    def getStartTime(self):
        return self.__starttime

    def getStartTimeSec(self):
        return self.__starttimesec

    def getStartTimeSubSec(self):
        return self.__starttimesubsec

    def getEndTime(self):
        return self.__endtime

    def getEndTimeSec(self):
        return self.__endtimesec

    def getEndTimeSubSec(self):
        return self.__endtimesubsec

    def getAcqTime(self):
        return self.__acqtime

    # Payload information
    #---------------------

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def getFormat(self):
        return self.__format

    def getPixelMap(self):
        return self.__pixelmap

    def getPixelMask(self):
        return self.__pixel_mask_map

    def getRawNumberOfPixels(self):
        return len(self.__pixelmap)

    def getNumberOfUnmaskedPixels(self):
        unmasked = 0
        #lg.debug(self.__pixelmap)
        #lg.debug(self.__pixel_mask_map)
        #for X in self.__pixel_mask_map.keys():
        #    lg.debug(" * %5d -> (%5d,%5d)." % (X, X%256, X/256))
        for X in self.__pixelmap.keys():
            #lg.debug(" * Is %5d -> (%5d,%5d) in the map?" % (X, X%256, X/256))
            if X not in self.__pixel_mask_map.keys():
                #lg.debug(" *---> NO!")
                unmasked += 1
            #else:
            #    lg.debug(" *---> YES!")
        return unmasked

    def getNumberOfMaskedPixels(self):
        return len(self.__pixel_mask_map)

    def getOccupancy(self):
        return len(self.__pixelmap)

    def getOccupancyPc(self):
        return float(len(self.__pixelmap))/float(self.__width * self.__height)

    def isMC(self):
        return self.__ismc

    def getPixelsString(self):
        s = ""

    def getNumberOfKlusters(self):
        return self.__n_klusters

    def getNumberOfGammas(self):
        return self.__kf.getNumberOfGammas()

    def getNumberOfMonopixels(self):
        return self.__kf.getNumberOfMonopixels()

    def getNumberOfBipixels(self):
        return self.__kf.getNumberOfBipixels()

    def getNumberOfTripixelGammas(self):
        return self.__kf.getNumberOfTripixelGammas()

    def getNumberOfTetrapixelGammas(self):
        return self.__kf.getNumberOfTetrapixelGammas()

    def getNumberOfNonGammas(self):
        return self.getNumberOfKlusters() - self.getNumberOfGammas()

    def getKlusterFinder(self):
        return self.__kf
