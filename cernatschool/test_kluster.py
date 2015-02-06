#!/usr/bin/env python
# -*- coding: utf-8 -*-

#...the usual suspects.
import os, inspect

#...for the unit testing.
import unittest

#...for the logging.
import logging as lg

#...for the JSON handling.
import json

#...for the Pixelman dataset wrapper.
from dataset import Dataset

#...for the klusters.
from kluster import KlusterFinder

class KlusterTest(unittest.TestCase):

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
        ## The cluster finder from the first frame.
        kf = KlusterFinder(frames[0].getPixelMap(), frames[0].getWidth(), frames[0].getHeight(), frames[0].isMC())

        # The number of clusters in the first frame.
        #
        # This frame has 34 clusters.
        self.assertEqual(kf.getNumberOfKlusters(), 9)
        self.assertEqual(kf.getNumberOfGammas(), 5)
        self.assertEqual(kf.getNumberOfMonopixels(), 1)
        self.assertEqual(kf.getNumberOfBipixels(), 0)
        self.assertEqual(kf.getNumberOfTripixelGammas(), 2)
        self.assertEqual(kf.getNumberOfTetrapixelGammas(), 2)

        ## The list of clusters.
        ks = kf.getListOfKlusters()

        # Double check the number of clusters found.
        self.assertEqual(len(ks), 9)

        # The first - and largest - cluster.

        # Cluster size (number of pixels).
        self.assertEqual(ks[0].getNumberOfPixels(), 25)

        # Cluster location (raw pixels).
        self.assertEqual(ks[0].getXMin(), 99)
        self.assertEqual(ks[0].getXMax(), 110)
        self.assertEqual(ks[0].getYMin(), 179)
        self.assertEqual(ks[0].getYMax(), 193)

        # Cluster width and height.
        self.assertEqual(ks[0].getWidth(), 12)
        self.assertEqual(ks[0].getHeight(), 15)

        # Cluster properties based on the unweighted (UW) mean.

        # * Location.
        self.assertAlmostEqual(ks[0].getXUW(), 104.16,  places=6)
        self.assertAlmostEqual(ks[0].getYUW(), 185.320, places=6)

        # * Radius and density.
        self.assertAlmostEqual(ks[0].getRadiusUW(), 8.73430, places=6)
        self.assertAlmostEqual(ks[0].getDensityUW(), 0.104312, places=6)

        # Counts.
        self.assertEqual(ks[0].getTotalCounts(), 851)
        self.assertEqual(ks[0].getMaxCountValue(), 88)

        # Energy.
        self.assertAlmostEqual(ks[0].getTotalEnergy(), 0.0, places=6)
        self.assertAlmostEqual(ks[0].getMaxEnergy(), 0.0, places=6)

        # Linearity.
        m, c, sumR = ks[0].getLineOfBestFitValues()
        self.assertAlmostEqual(m, -1.127456, places=6)
        self.assertAlmostEqual(c, 302.755829, places=6)
        self.assertAlmostEqual(sumR, 16.283415, places=6)

        # Edge pixels.
        self.assertEqual(ks[0].getNumberOfEdgePixels(), 25)
        self.assertAlmostEqual(ks[0].getInnerPixelFraction(), 0.0, places=6)
        self.assertAlmostEqual(ks[0].getOuterPixelFraction(), 1.0, places=6)

        # Is it a Monte Carlo cluster?
        self.assertEqual(ks[0].isMC(), False)

        # Is it an edge cluster?
        self.assertEqual(ks[0].isEdgeCluster(), False)


if __name__ == "__main__":

    lg.basicConfig(filename='log_test_kluster.txt', filemode='w', level=lg.DEBUG)

    lg.info("")
    lg.info("=================================================")
    lg.info(" Logger output from cernatschool/test_kluster.py ")
    lg.info("=================================================")
    lg.info("")

    unittest.main()
