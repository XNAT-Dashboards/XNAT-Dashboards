[![pipeline status](https://gitlab.com/xnat-dashboards/xnat-dashboards/badges/development/pipeline.svg)](https://gitlab.com/xnat-dashboards/xnat-dashboards/-/commits/development)
[![coverage report](https://gitlab.com/xnat-dashboards/xnat-dashboards/badges/development/coverage.svg)](https://gitlab.com/xnat-dashboards/xnat-dashboards/-/commits/development)
[![MIT License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://gitlab.com/xnat-dashboards/xnat-dashboards/-/blob/development/LICENSE)

# XNAT Dashboards

XNAT Dashboards is a responsive dashboard framework for extensive exploration, monitoring, and reviewing large neurological imaging datasets present on the XNAT server instance. It fetches data from any XNAT instance servers and generates highly-visualized, summarized representations of complex scientific data present on the servers and facilitate user navigation through large cohorts. 

## Built with

- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [Pyxnat](https://pyxnat.github.io/pyxnat/)
- [Pandas](https://pandas.pydata.org/)
- [Plotly.js](https://plotly.com/javascript/)
- [Bootstrap](https://getbootstrap.com/)

## Prerequisite

- XNAT Instance.
- Username and Password for that xnat instance.
- If no local instance available you can register at [CENTRAL](https://central.xnat.org)

## Installation

Xnat dashboards can be installed using pip python package index.  
```pip install xnat-dashboards```

## Installation from Sources
Clone the repository
```python setup.py install```

## Tests
Pytest is used as a testing framework to run test  

```pytest tests```          (Without coverage)  
```pytest --cov tests```    (With coverage)  

## Documentation

- Official Documentation can be found at https://xnat-dashboards.gitlab.io/xnat-dashboards.
- Users who want to install and run the dashboards read [user guide](https://xnat-dashboards.gitlab.io/xnat-dashboards/user_guide.html)
- Developers who wants to install, develop, test or add more features to the dashboards read both [user guide](https://xnat-dashboards.gitlab.io/xnat-dashboards/user_guide.html) and [developers guide](https://xnat-dashboards.gitlab.io/xnat-dashboards/developer_guide.html).
