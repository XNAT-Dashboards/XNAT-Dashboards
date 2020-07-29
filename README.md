[![pipeline status](https://gitlab.com/Udolf47/xnat_dashboards/badges/development/pipeline.svg)](https://gitlab.com/Udolf47/xnat_dashboards/-/commits/development)
[![coverage report](https://gitlab.com/Udolf47/xnat_dashboards/badges/development/coverage.svg)](https://gitlab.com/Udolf47/xnat_dashboards/-/commits/development)


# XNAT Dashboards

This project is about creating a responsive dashboard framework for extensive exploration, monitoring, and reviewing large neurological imaging datasets present on the XNAT server instance. This dashboard will fetch data from any XNAT instance servers and will generate highly-visualized, summarized representations of complex scientific data present on the servers and facilitate user navigation through large cohorts. This dashboard will be a light-weight, flexible and modular framework that can adapt and change as per the new needs of the users.

## Prerequisite

- XNAT instance.
- Username and Password for that xnat instance.
- If no local instance available you can register at [CENTRAL](https://central.xnat.org)
- Graph type assignment file present in util/graph_type.json
- [MongoDB Instance](https://www.mongodb.com/) or save data using pickle

## Getting Started

To run this project locally for testing or development

- Install Python 3
- Install virtual env
- Tests can be found in test directory

### Installing

- ```Create a virtual environment```
- ```source env/bin/activate```
- ```pip3 install -r requirements.txt```
```
Create a json file with following format:
{
    'username': 'username',
    'password': 'password',
    'server': 'server url',
    'ssl': 'Empty if you want to verify remote host'
}
```
- ```python download_resources.py -p <Relative path to the above JSON file>``` to download data.
- ``` 3 configuration files are provided with following functionalities: ```
```
- db_config.json
    This file is used to change the url on which MongoDB is hosted
- graph_config.json
    This file can be used to change graphs configuration.
        User can change graphs types.
        What roles can view which graph can be changed.
        Change the tooltip information for each graph.
        Default color are assigned to each graph which can be changed as per need.
- roles_config.json
    This file can be used to change roles configurations.
        Users can be added or removed.
        Users roles can be changed.
        Adding projects for users which they will be able to access.
```

### Starting the server

```python3 run.py```

## Running the tests

Pytest is used as a testing framework to run test

- ``` pytest tests ```          (Without coverage)
- ``` pytest --cov tests ```    (With coverage)

To access the Central XNAT server a type.json file is already provided.

## Access other XNAT server

- Open graph_generator.py
- In the last line add the credentials of your different server.
- Use the following command to run graph generator if graph_type.json gets deleted ``` python generators/graph_generator.py ```
- for each required input field type ```bar```,```pie```,```scatter```,```line```.
- This will generate a graph_type.json file in utils directory.
- Start the server using ```python3 run.py``
