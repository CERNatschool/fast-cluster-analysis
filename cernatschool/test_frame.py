#!/usr/bin/env python
# -*- coding: utf-8 -*-

#...the usual suspects.
import os, inspect

#...for the unit testing.
import unittest

#...for the logging.
import logging as lg

#...for the JSON.
import json

#...for the Pixelman dataset wrapper.
from dataset import Dataset

class FrameTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_asciixyc_frame(self):

        ## The dataset wrapper.
        ds = Dataset("testdata/B06-W0212/2014-04-02-150255/ASCIIxyC/")

        ## The frame metadata.
        fmd = None
        #
        with open("testdata/B06-W0212/2014-04-02-150255/metadata.json", "r") as fmdf:
            fmd = json.load(fmdf, fmd)
        #
        lat, lon, alt = fmd[0]['lat'], fmd[0]['lon'], fmd[0]['alt']

        ## The pixel mask.
        pixel_mask = {}

        with open("testdata/B06-W0212/2014-04-02-150255/masked_pixels.txt", "r") as mpf:
            rows = mpf.readlines()
            for row in rows:
                vals = [int(val) for val in row.strip().split("\t")]
                x = vals[0]; y = vals[1]; X = (256*y) + x; C = 1
                pixel_mask[X] = C

        ## The frames from the dataset.
        frames = ds.getFrames((lat, lon, alt), pixelmask=pixel_mask)

        # The tests
        #-----------
        #
        # The number of frames.
        self.assertEqual(len(frames), 60)
        #
        # Spatial information.
        self.assertEqual(frames[0].getLatitude(),  51.261015)
        self.assertEqual(frames[0].getLongitude(), -1.084127)
        self.assertEqual(frames[0].getAltitude(),  48.0     )
        #
        self.assertEqual(frames[0].getRoll(), 0.0)
        self.assertEqual(frames[0].getPitch(), 0.0)
        self.assertEqual(frames[0].getYaw(), 0.0)
        #
        self.assertEqual(frames[0].getOmegax(), 0.0)
        self.assertEqual(frames[0].getOmegay(), 0.0)
        self.assertEqual(frames[0].getOmegaz(), 0.0)
        #
        # Temporal information.
        self.assertEqual(frames[0].getStartTime(), 1396447375.004957)
        self.assertEqual(frames[0].getStartTimeSec(), 1396447375)
        self.assertEqual(frames[0].getStartTimeSubSec(), 4957)
        self.assertEqual(frames[0].getEndTime(), 1396447435.004957)
        self.assertEqual(frames[0].getEndTimeSec(), 1396447435)
        self.assertEqual(frames[0].getEndTimeSubSec(), 4957)
        self.assertEqual(frames[0].getAcqTime(), 60.0)
        #
        # Detector information.
        self.assertEqual(frames[0].getChipId(), "B06-W0212")
        #
        self.assertEqual(frames[0].getBiasVoltage(), 95.0)
        self.assertEqual(frames[0].getIKrum(), 1)
        #
        self.assertEqual(frames[0].getDetx(), 0.0)
        self.assertEqual(frames[0].getDety(), 0.0)
        self.assertEqual(frames[0].getDetz(), 0.0)
        self.assertEqual(frames[0].getDetEulera(), 0.0)
        self.assertEqual(frames[0].getDetEulerb(), 0.0)
        self.assertEqual(frames[0].getDetEulerc(), 0.0)
        #
        # Payload information.
        self.assertEqual(frames[0].getWidth(), 256)
        self.assertEqual(frames[0].getHeight(), 256)
        self.assertEqual(frames[0].getFormat(), 4114)
        self.assertEqual(frames[0].getRawNumberOfPixels(), 57)
        self.assertEqual(frames[0].getOccupancy(), 57)
        self.assertAlmostEqual(frames[0].getOccupancyPc(), 0.000870, places=6)
        self.assertEqual(frames[0].getNumberOfUnmaskedPixels(), 57)
        self.assertEqual(frames[0].getNumberOfMaskedPixels(), 29)
        #
        self.assertEqual(frames[0].isMC(), False)

        # The masked pixels.
        self.assertEqual(frames[0].getNumberOfMaskedPixels(), 29)

        #
        # Cluster information.
        self.assertEqual(frames[0].getNumberOfKlusters(), 9)
        self.assertEqual(frames[0].getNumberOfGammas(), 5)
        self.assertEqual(frames[0].getNumberOfMonopixels(), 1)
        self.assertEqual(frames[0].getNumberOfBipixels(), 0)
        self.assertEqual(frames[0].getNumberOfTripixelGammas(), 2)
        self.assertEqual(frames[0].getNumberOfTetrapixelGammas(), 2)
        self.assertEqual(frames[0].getNumberOfNonGammas(), 4)


if __name__ == "__main__":

    lg.basicConfig(filename='log_test_frame.txt', filemode='w', level=lg.DEBUG)

    lg.info("")
    lg.info("===============================================")
    lg.info(" Logger output from cernatschool/test_frame.py ")
    lg.info("===============================================")
    lg.info("")

    unittest.main()
