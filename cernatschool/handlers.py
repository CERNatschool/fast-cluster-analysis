#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Handler methods for various parts of the Timepix datafiles.
"""

#...for the logging.
import logging as lg

#...for the regex module.
import re

#...for the time functionality.
import time

def isChipIdValid(chipid):
    """ Does the chip ID conform to the UVV-XYYYY format? """

    # regex match for the chipboard ID.
    r = re.compile(r'[A-Z]\d{2,2}-[A-Z]\d{4,4}')

    if r.match(chipid) is not None:
        return True
    else:
        return False

def isStartTimeStringValid(sts):
    """ Check the format of the time string. """

    # regex match for the start time string.
    r_starttime = re.compile(r'[A-Z][a-z][a-z] [A-Z][a-z][a-z] \d{2,2} \d{2,2}:\d{2,2}:\d{2,2}.\d{6,6} \d{4,4}')

    if r_starttime.match(sts) is not None:
        return True
    else:
        return False

def getPixelmanTimeString(st):
    """ Get the timestring in the Pixelman (custom) format. """

    ## The seconds from the start time provided.
    sec = int(str(st).split(".")[0])

    ## The seb-second value.
    sub = int(("%.6f" % st).strip().split(".")[1])

    ## The time represented as a Python time object.
    mytime = time.gmtime(sec)

    ## The time in the Pixelman format.
    sts = time.strftime("%a %b %d %H:%M:%S.", mytime) + str(sub) + time.strftime(" %Y", mytime)

    return sec, sub, sts

def getPixelsStringFromPixelMap(pixelmap):
    """ Convert a pixel dictionary to a string in the X, C format. """

    ## The string (X Y C values) to return.
    s = ""

    n = 0; last = len(pixelmap)

    for X, hits in pixelmap.iteritems():
        s += "%d %d" % (X, hits)
        n += 1
        if n != last:
            s += "\n"

    return s
