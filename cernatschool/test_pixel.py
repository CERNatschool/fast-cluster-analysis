#!/usr/bin/env python
# -*- coding: utf-8 -*-

#...the usual suspects.
import os, inspect

#...for the unit testing.
import unittest

#...for the logging.
import logging as lg

#...for the pixel wrapper class.
from pixel import Pixel

class PixelTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_pixel(self):


        p = Pixel(100, 200, 1234, -1, 256, 256)

        # The tests
        #-----------
        self.assertEqual(p.get_x(), 100)
        self.assertEqual(p.get_y(), 200)
        self.assertEqual(p.getX(), 51300)
        self.assertEqual(p.getC(), 1234)
        self.assertEqual(p.get_mask(), -1)
        self.assertEqual(p.get_neighbours(), {})
        self.assertEqual(p.pixel_entry(), "{\"x\":100, \"y\":200, \"c\":1234},\n")


if __name__ == "__main__":

    lg.basicConfig(filename='log_test_pixel.txt', filemode='w', level=lg.DEBUG)

    lg.info("")
    lg.info("===============================================")
    lg.info(" Logger output from cernatschool/test_pixel.py ")
    lg.info("===============================================")
    lg.info("")

    unittest.main()
