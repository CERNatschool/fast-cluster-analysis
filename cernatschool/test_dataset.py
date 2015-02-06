#!/usr/bin/env python
# -*- coding: utf-8 -*-

#...the usual suspects.
import os, inspect

#...for the unit testing.
import unittest

#...for the logging.
import logging as lg

#...for the dataset wrapper.
from dataset import Dataset

class DatasetTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_import_dataset(self):

        ## The Pixelman dataset object.
        pds = Dataset("testdata/B06-W0212/2014-04-02-150255/ASCIIxyC/")

        # The tests.

        # The number of datafiles.
        self.assertEqual(pds.getNumberOfDataFiles(), 60)

        # The data format of the folder.
        self.assertEqual(pds.getFolderFormat(), "ASCII [x, y, C]")


if __name__ == "__main__":

    lg.basicConfig(filename='log_test_dataset.log', filemode='w', level=lg.DEBUG)

    lg.info("")
    lg.info("=================================================")
    lg.info(" Logger output from cernatschool/test_dataset.py ")
    lg.info("=================================================")
    lg.info("")

    unittest.main()
