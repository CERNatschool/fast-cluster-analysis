#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Pixel:
    """
    Class representing a (hit) pixel.

    The "direction" value corresponds to the i^th value in these lists:
    dir_x = [-1, -1,  0,  1,  1,  1,  0, -1]
    dir_y = [ 0,  1,  1,  1,  0, -1, -1, -1]
    """
    def __init__(self, x, y, C, m, rows, cols):

        ## The pixel x position.
        self.x = x

        ## The pixel y position.
        self.y = y

        ## The number of counts.
        self.__C = C

        ## The pixel mask value (for clustering).
        self.m = m

        ## The number of rows in the detector matrix.
        self.__rows = rows

        ## The number of columns in the detector matrix.
        self.__cols = cols

        self.neighbours = {} # {direction: XY}

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def getC(self):
        return self.__C

    def getX(self):
        return (self.__cols * self.y) + self.x

    def get_mask(self):
        return self.m

    def set_mask(self, m):
        self.m = m

    def get_neighbours(self):
        return self.neighbours

    def get_neighbour(self, direction):
        if direction in self.neighbours:
            return self.neighbours[direction]
        else:
            return False

    def set_neighbour(self, direction, pixel_xy):
        self.neighbours[direction] = pixel_xy

    def pixel_entry(self):
        return "{\"x\":%d, \"y\":%d, \"c\":%d},\n" % (self.x, self.y, self.__C)

    def output(self):
        print(self.pixel_entry)
