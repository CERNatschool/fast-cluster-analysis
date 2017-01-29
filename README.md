# CERN@school: Fast Cluster Analysis
This code can be used to perform a "fast" cluster analysis on
data collected with a
[Timepix detector](http://medipix.web.cern.ch), for use in
research conducted as part of the CERN@school programme.
An example analysis using the radiation profile methods
described in Section 4 of the CERN@school
**Contemporary Physics** paper
([Whyntie et al. 2015](http://dx.doi.org/10.1080/00107514.2015.1045193))
is included.
The datasets featured in the paper are included with the code,
but may also be found on FigShare
[here](http://doi.org/10.6084/m9.figshare.4588276.v2).


## Introduction


_Please note: the **linearity** cluster variable currently
fits the line of best fit by measuring the pixel distances from
the line in y coordinate. This means it is not technically
rotationally invariant as a cluster variable.
To fix this, the perpendicular distance of each pixel
from the line of best fit should be calculated and used in the
minimisation function. This is left as an exercise for the reader._


## Disclaimers
* _This code dates from 2016. While every attempt has been
made to ensure that it is usable, some work may be required to get it
running on your own particular system.
We recommend using a GridPP CernVM; please refer to
[this guide](http://doi.org/10.6084/m9.figshare.4552825.v1)
for further instructions.
Unfortunately CERN@school cannot guarantee further support for this code.
Please proceed at your own risk_.
* _This repository is now deprecated, and remains here for legacy purposes.
For future work regarding CERN@school, please refer to the
[Institute for Research in Schools](http://researchinschools.org) (IRIS)
[GitHub repository](https://github.com/InstituteForResearchInSchools).
Please also feel free to fork and modify this code as required for
your own research._


## Getting the code
First, clone the `fast-cluster-analysis` repo into your working directory:

```bash
$ git clone https://github.com/CERNatschool/fast-cluster-analysis.git
$ cd fast-cluster-analysis
```

To prepare for running, run the `setup.sh` script with the following
command:

```bash
$ source setup.sh
```

_Note: if you are not using a GridPP CernVM, the `setup.sh` script
will not work as you won't have access to the CERN@school CVMFS
repository and will have to source your own version of the Python
libraries such as `matplotlib` via e.g. the
[Anaconda Python distribution](http://anaconda.org)._


## Getting the datasets
Two datasets - one real, one simulated - are provided with the code:

* `testdata/kcldata/`: real data from a KCl (Lo Salt) sample;
* `testdata/kclsim/`: simulated data with a KCl test source.

You may also find the datasets in the
[FigShare](http://figshare.org) repository
[here](http://doi.org/10.6084/m9.figshare.4588276.v2).


## Running the code

First, process and make the plots for the real data:
```bash
$ mkdir ../tmpkcldata
$ python process-frames.py testdata/kcldata/ ../tmpkcldata
$ python make-plots.py ../tmpkcldata ../tmpkcldata
```

_Note: this will process all 120 frames, which may take some time.
To process fewer frames, use the `--maxframe` option
for the `process-frames.py` script like so:_

```bash
$ python process-frames.py --maxframes=5 testdata/kcldata/ ../tmpkcldata
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

These are Figures 6 a), b) and c) from
([Whyntie et al. 2015](http://dx.doi.org/10.1080/00107514.2015.1045193)).
By using your own data, for example collected from your own KCl source,
you can make your own versions of these plots to use in your own research.


## Making changes and exploring the data
Feel free to fork the repo, play with the code, and see what
you can find in the data. We'd love to hear about what
you've done with it - get in touch with
[IRIS](http://researchinschools.org) if you do!


## Authors/Editors/Contributors

* T. Whyntie - @twhyntie - Queen Mary University of London;
* A. Coupe - @acoupe - Uni. of Southampton;
* R. Fickling - @fickling - Queen Mary University of London.


## Acknowledgements
The cluster finder is based on C++ code
originally supplied to the CERN@school project by
Son Hoang (NASA/Uni. Houston).
It has been adapted to include plotting functionality
from the `NumPy` and `PyLab` libraries.
The authors would like to thank the 2016 MoEDAL summer students for
constructive feedback and suggestions for improving the code.
A. Coupe's 2014 summer placement was kindly supported by
[SEPnet](http://www.sepnet.ac.uk).
R. Fickling's project was supervised by J. Wilson of the
QMUL Particle Physics Research Centre (PPRC).

CERN@school was supported by
the UK [Science and Technology Facilities Council](http://www.stfc.ac.uk) (STFC)
via grant numbers ST/J000256/1 and ST/N00101X/1,
as well as a Special Award from the Royal Commission for the Exhibition of 1851.


## Useful links
* [Setting up a GridPP CernVM](http://doi.org/10.6084/m9.figshare.4552825.v1);
* [Whyntie et al. 2015](http://dx.doi.org/10.1080/00107514.2015.1045193) - the CERN@school Contemporary Physics paper featuring this experiment (Section 4);
* The [datasets](http://doi.org/10.6084/m9.figshare.4588276.v2) on FigShare;
* The [Institute for Research in Schools](http://researchinschools.org) (IRIS) homepage;
* The [IRIS CERN@school website](http://researchinschools.org/CERN);
* The [Official IRIS GitHub Organization](https://github.com/InstituteForResearchInSchools).
