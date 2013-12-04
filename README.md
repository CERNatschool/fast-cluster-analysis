#Fast Cluster Analysis
========================

## Introduction

This simple cluster finder and analyser is based on C++ code
originally supplied to the CERN@school project by
Son Hoang (NASA/Uni. of Florida).

It has been adapted to include plotting functionality
from the NumPy and PyLab libraries.


## Getting the code

Clone the `fast-cluster-analysis` repo into your working directory:

    cd $WORKINGDIR # where $WORKINGDIR is your working directory,
                   # e.g. /home/twhyntie/dev/python/CERNatschool/
    git clone https://github.com/CERNatschool/fast-cluster-analysis.git
    cd fast-cluster-analysis

## Getting the data

A sample of strontium-90 data taken with a CERN@school MX-10 detector
can be found
[here](http://files.figshare.com/1302362/sr90_testdata_0_00mm.tar).
To download it and unpack it, type the following commands:

    cd $DATADIR # i.e. wherever you're putting your data.
    wget http://files.figshare.com/1302362/sr90_testdata_0_00mm.tar
    tar -xvf sr90_testdata_0_00mm.tar

You should now have 600 data files (and accompanying detector settings
files) in your `$DATADIR`.

(You may even wish to set $DATADIR as an environment variable, e.g.

    export DATADIR=/home/twhyntie/data/samples/sr90
    echo $DATADIR

so that you don't have to keep typing it out.)

### On PythonAnywhere

Coming soon?

## Running the code

Once you've got your data in your `$DATADIR`, run the code as follows:

    cd $WORKINGDIR
    python fast-cluster.py $DATADIR

## Viewing the results

The `fast-cluster.py` program generates an `html` file that
you can use a browser to view:

    cd $WORKINGDIR
    python fast-cluster.py
    firefox index.html &

This should open a new browser window that will display your
results.

### On PythonAnywhere

Go to the **Dashboard** and click on the **Files** tab.
Then go to the `fast-cluster-analysis` folder (i.e. where you've
been working) and click on the **Download** button (a down-facing
arrow) next to `index.html`. You won't actually download the
file; rather, the browser will display the `.html` page
featuring your results.


## Making changes and exploring the data

Feel free to fork the repo, play with the code, and see what
you can find in the data. We'd love to hear about what
you've done with it!

If you find any errors, or think of ways to improve the code,
please create an "issue" and we'll see what we can do.

## Authors/Editors

* Tom Whyntie (twhyntie) - Queen Mary, University of London
* Azaria Coupe (acoupe) - Uni. of Southampton

## Further information

* [CERN@school homepage](http://cernatschool.web.cern.ch);
* [The Langton Star Centre](http://www.thelangtonstarcentre.org);
* [Strontium-90 sample dataset](http://figshare.com/articles/Sr_90_test_data/867659).
