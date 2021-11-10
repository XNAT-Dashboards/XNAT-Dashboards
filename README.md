[![build](https://travis-ci.com/XNAT-Dashboards/XNAT-Dashboards.svg?branch=master)](https://github.com/XNAT-Dashboards/XNAT-Dashboards/commits/master)
[![coverage](https://coveralls.io/repos/github/XNAT-Dashboards/XNAT-Dashboards/badge.svg?branch=master)](https://coveralls.io/github/XNAT-Dashboards/XNAT-Dashboards?branch=master)
[![MIT License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://github.com/XNAT-Dashboards/XNAT-Dashboards/blob/master/LICENSE)
[![version](https://img.shields.io/badge/version-v0.3.0-brightgreen)](https://github.com/XNAT-Dashboards/XNAT-Dashboards/commits/master)

# Dashboards for XNAT

**Dashboards for XNAT** is a framework for extensive exploration, review and monitoring of large neuroimaging datasets hosted on an XNAT instance. The project was initiated in 2020 during the [Google Summer of Code](https://summerofcode.withgoogle.com/archive/2020/projects/5685130842079232/) program by Mohammad Asif Hashmi.

The project is now maintained by Greg Operto, Jordi Huguet and Marina Garcia Prat
of the [BarcelonaBeta Brain Research Center](http://barcelonabeta.org) (BBRC).

The project was designed to be compatible with any generic XNAT instance. However,
to date the development version includes some features that are specific to BBRC.
While future work will alleviate that specificity, it is worth underlining that
the project provides a *framework* to build tailored visualizations rather than
 ready-made dashboards to use off the shelf.

## Built with

- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [pyxnat](https://pyxnat.github.io/pyxnat/)
- [pandas](https://pandas.pydata.org/)
- [plotly](https://plotly.com/javascript/)
- [bootstrap](https://getbootstrap.com/)

## Prerequisite

A running XNAT instance and read access rights to it are required prior to using
**Dashboards for XNAT**.


## Installation

Installation from source is advised at this current stage of development of the
project.

However, version v0.3 of **Dashboards for XNAT** can be installed using `pip`. That
version was released at the end of the [Google Summer of Code 2020](https://summerofcode.withgoogle.com/archive/2020/projects/5685130842079232/).

```pip install xnat-dashboards```


## Tests

Running the test suite requires the following:

  - *python-nose* v1.2.1+
  - *coveralls*

Run the tests with the following command:

```nosetests xnat-dashboards/tests```


## Documentation

While the project has gone under a significant refactoring process over the last
months and require new efforts on documentation, the [original materials](https://xnat-dashboards.gitlab.io/xnat-dashboards) are still available along with a [user guide](https://xnat-dashboards.gitlab.io/xnat-dashboards/user_guide.html) and a [developer guide](https://xnat-dashboards.gitlab.io/xnat-dashboards/developer_guide.html).
