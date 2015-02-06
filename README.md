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

```bash
cd $WORKINGDIR # where $WORKINGDIR is your working directory,
               # e.g. /home/twhyntie/dev/CERNatschool/
git clone https://github.com/CERNatschool/fast-cluster-analysis.git
cd fast-cluster-analysis
```

## Getting the data

Two datasets - one real, one simulated - are provided with the code:

* `testdata/kcldata/`: real data from a KCl (Lo Salt) sample;
* `testdata/kclsim/`: simulated data with a KCl test source.

## Running the code

First, process and make the plots for the real data:
```bash
$ mkdir ../tmpkcldata
$ python process-frames.py testdata/kcldata/ ../tmpkcldata
$ python make-plots.py ../tmpkcldata ../tmpkcldata
```

Then process and make the plots for the simulated data:
```bash
$ mkdir ../tmpkclsim
$ python process-frames.py testdata/kclsim/ ../tmpkclsim
$ python make-plots.py ../tmpkclsim ../tmpkclsim
```

Finally, you can make and view the comparison plots:
```bash
$ mkdir ../tmpcompare
$ python compare-plots.py ../tmpkcldata/ ../tmpkclsim/ ../tmpcompare/
$ firefox ../tmpcompare/clusterplots/index.html &
```

## Making changes and exploring the data

Feel free to fork the repo, play with the code, and see what
you can find in the data. We'd love to hear about what
you've done with it!

If you find any errors, or think of ways to improve the code,
please create an "issue" and we'll see what we can do.

## Authors/Editors/Contributors

* Tom Whyntie - @twhyntie - Queen Mary University of London;
* Azaria Coupe - @acoupe - Uni. of Southampton;
* Rebecca Fickling - @fickling - Queen Mary University of London.

## Further information

* [CERN@school homepage](http://cernatschool.web.cern.ch);
* [The Langton Star Centre](http://www.thelangtonstarcentre.org);
* [Strontium-90 sample dataset](http://figshare.com/articles/Sr_90_test_data/867659).
