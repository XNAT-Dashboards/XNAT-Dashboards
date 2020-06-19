# XNAT Dashboards

[![pipeline status](https://gitlab.com/Udolf47/xnat_dashboards/badges/develop/pipeline.svg)](https://gitlab.com/Udolf47/xnat_dashboards/commits/develop)
[![coverage report](https://gitlab.com/Udolf47/xnat_dashboards/badges/develop/coverage.svg)](https://gitlab.com/Udolf47/xnat_dashboards/commits/develop)


## Getting Started

### Installing

Install the dependencies using ```pip3 install -r requirements.txt```

### Starting the server

```python3 run.py```

To access the Central XNAT server a type.json file is already provided.

### To access other XNAT server

- Open graph_generator.py
- In the last line add the credentials of your different server.
- run python pyxnat_connection/graph_generator.py in the root of the project.
- for each required input field type ```bar```.
- This will generate a graph_type.json file in utils directory.

- Start the server using ```python3 run.py```