#!/usr/bin/env python
# -*- coding: utf-8 -*-

#...for the operating system commands.
import os

#...for the logging.
import logging as lg

# Import the JSON library.
import json

class KlusterProperties:
    """ A wrapper class for cluster properties. """

    def __init__(self, jsonpath):
        """ Constructor. """

        ## Path to the cluster JSON file.
        self.__json_path = jsonpath
        #
        if not os.path.exists(self.__json_path):
            raise IOError("* ERROR: '%s' does not exist!" % (self.__json_path))

        kf = open(self.__json_path, "r")

        ## The cluster JSON.
        self.__json = json.load(kf)

        kf.close()

        lg.info(" *")
        lg.info(" * Initialising KlusterProperties object from '%s'." % (self.__json_path))
        lg.info(" *")

        # Get the cluster properties.

        ## The list of clusters.
        self.__klusters = []

        # Create container lists for the cluster properties.
        self.__cluster_size      = []
        self.__cluster_counts    = []
        self.__cluster_maxcounts = []
        self.__cluster_radius_u  = []
        self.__cluster_density_u = []
        self.__cluster_linearity = []
        self.__cluster_innerfrac = []

        # Loop over the klusters.
        for k in self.__json:

            # Add to the cluster property dictionaries.
            if not k["isedgekluster"]:
                self.__cluster_size.append(     k["size"])
                self.__cluster_radius_u.append( k["radius_uw"])
                self.__cluster_density_u.append(k["density_uw"])
                self.__cluster_linearity.append(k["lin_linearity"])
                self.__cluster_innerfrac.append(k["innerfrac"])
                self.__cluster_counts.append(   k["totalcounts"])
                self.__cluster_maxcounts.append(k["maxcounts"])

    def get_number_of_klusters(self):
        return len(self.__cluster_size)

    def get_cluster_size_list(self):
        return self.__cluster_size

    def get_cluster_radius_u_list(self):
        return self.__cluster_radius_u

    def get_cluster_linearity_list(self):
        return self.__cluster_linearity
