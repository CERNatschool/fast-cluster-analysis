#!/usr/bin/env python

import glob

def make_page(path, datapath, numclusters):

    homepagename = path + "/index.html"

    f = open(homepagename, "w")
    f.write("<!DOCTYPE html>\n")
    f.write("<html>\n")
    f.write("  <head>\n")
    f.write("    <link rel=\"stylesheet\" type=\"text/css\" ")
    f.write("href=\"assets/css/style.css\">\n")
    f.write("  </head>\n")
    f.write("  <body>\n")
    f.write("    <a href='http://cernatschool.web.cern.ch'><img class='logo' src='assets/images/rect_web_large.png' /></a>\n")
    f.write("    <h1>Basic Cluster Analysis</h1>\n")
    f.write("    <h2>Dataset summary</h2>\n")
    f.write("    <p>\n")
    f.write("      <ul>\n")
    f.write("        <li>Dataset path = '%s'</li>\n" % datapath)
    f.write("        <li>Number of frames = %d</li>\n" % len(glob.glob(datapath + "/*.txt")))
    f.write("        <li>Number of clusters (dat.) = %d</li>\n" % (numclusters))
    f.write("      </ul>\n")
    f.write("    </p>\n")
    f.write("    <h2>Cluster properties</h2>\n")
    f.write("    <table>\n")
    f.write("      <caption>Fig. 1: Hits per cluster.</caption>\n")
    f.write("      <tr><td><img src=\"hpc.png\" /></td></tr>\n")
    f.write("    </table>\n")
#    f.write("    <table>\n")
#    f.write("      <caption>Fig. 2: Counts per cluster.</caption>\n")
#    f.write("      <tr><td><img src=\"cpc.png\" /></td></tr>\n")
#    f.write("    </table>\n")
#    f.write("    <table>\n")
#    f.write("      <caption>Fig. 3: Cluster radius (unweighted).</caption>\n")
#    f.write("      <tr><td><img src=\"cru.png\" /></td></tr>\n")
#    f.write("    </table>\n")
#    f.write("    <table>\n")
#    f.write("      <caption>Fig. 4: Cluster density (unweighted).</caption>\n")
#    f.write("      <tr><td><img src=\"cdu.png\" /></td></tr>\n")
#    f.write("    </table>\n")
    f.write("  </body>\n")
    f.write("</html>")


    f.close()
