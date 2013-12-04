#!/usr/bin/env python

class Pixel:
    """
    Class representing a (hit) pixel.
    """
    def __init__(self, x, y, c, m):
        self.x = x
        self.y = y
        self.c = c
        self.m = m
        self.neighbours = {} # {direction: XY}

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_c(self):
        return self.c

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
        return "{\"x\":%d, \"y\":%d, \"c\":%d},\n" % (self.x, self.y, self.c)

    def output(self):
        print(self.pixel_entry)
