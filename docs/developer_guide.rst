Developer Guide
===============

This guide is for the developers or user that will be using this dashboard
for creating new dashboards or want to add more graphs.

Modules Understanding
---------------------

- **saved data processing** is used to process and format data fetched from pickle for displaying on frontend.
- **pyxnat Interface** is an interface that is used to fetch data from the XNAT instance and save it in pickle format.
- **app** contains the code of both frontend and backend.  
- **config** contains all configuration and pickle files required.    

Understanding Workflow
----------------------------------

- Login user details are checked through App **->** Auth **->** Model
- It is then routed to the dashboard overview page App **->** Dashboard **->** Controller.
- Controller uses the data from saved pickle and checks whether server url provided by user and server url of pickle is same.
- GraphGenerator(pickle data) **->** GetInfo(pickle data)
- GetInfo first filter out the projects data that should not be visible to the user and GetInfo(filtered data) **->** DataFormatter(filtered data).
- Data formatter creates different graphs and other stats data. Then it creates a dictionary which should follow as specific structure.
- DataFormatter(filtered and formatted data) **->** GetInfo (filtered and processed data).
- GetInfo(filtered and formatted data) **->** GraphGenerator (filtered and formatted data).
- GraphGenerator then process those dictionary that will be used to plot graphs.
- It add specific Id, Color, Description, Name and checks whether the graphs should be visible as per the role assigned to the user.
- Then it returns this data to the backend Controller.
- This backend Controller send this data to frontend and frontend uses this data to plot graphs using Python Jinja and HTML, CSS and Javascript.


Add a new plot
--------------

Read the :doc:`developer_guide` for better understanding before adding a plot.

Adding a plot requires to make changes on DataFormatter, GetInfo and dashboard_config files.

Create a new method in DataFormatter file.

There are 2 options to add a plot:

1 -> Using predifined methods in DataFormatter file.

2 -> Using own logic in DataFormatter file.

Example for option 1::

    Create graph of different type of scans.
    Use a list of dict that is fetched form XNAT and saved in pickle.

    example_data_list = [
        {'id': 'sc1', 'type': 'type1'},
        {'id': 'sc2', 'type': 'type2'},
        {'id': 'sc3', 'type': 'type3'},
        {'id': 'sc4', 'type': 'type4'},
        {'id': 'sc5', 'type': 'type5'}
    ]

    If this graph is for overview dashboard then use method dict_generator_overview() else use method dict_generator_per_view()

In each method provide the arguments::

    1st arg= example_data_list
    2nd arg= Value on Xaxis since on x axis we will have scan type use 'type' for this example_data_list
    3rd arg= Value on Yaxis since on y axis we will have counted values of each scan type use 'id'
    4th arg= Provide a name for values displayed on Xaxis if you want the same name as in 'type' write 'id'
    
This method will return a dictionary of following format::

    d1 = {
        'count': {'x1': 'y1', 'x2': 'y2'},
        'list': {'x1': [list of id present in y1], 'x2': [list of id present in y2]}
    }

Example for option 2:

If you want have a different example_data_list.

Write a code logic that will create a dict of following format in the end::

    d2 = {
        'count': {'x1': 'y1', 'x2': 'y2'},
        'list': {'x1': [list of id present in y1], 'x2': [list of id present in y2]}
    }

After creating these dict you need to assign a name to these graph::

    {
        Graph_name: d1
    }

Now call this created method in GetInfo __preprocessor and add this the returned dict in the final_json_dict dictionary.

Backend changes are done, open dashboard_config file and add the following::

    {
    "graph_config": {
        "Graph_name": {
            "type":"Graph type",
            "description": "Graph description",
            "visibility": ['list of roles graph should be visible to'],
            "color":"Graph color"
        }
    }

Add new dashboards
-----------------------

To create new dashboards on a new page change in frontend and backend is required.

Developers need to have knowledge of **Python**, **Pandas** (if need to add plots), **Javascript**, **HTML**, **CSS**, **Jinja**.

Steps to create a new dashboard frontend:

- Create a new html file in xnat_dashboards/app/templates/dashboards/new.html
- Copy the html page of already present dashboards.
- Remove all the jinja code and other imports.

Steps to send data from backend to the new dashboards frontend:

- Create the plots from using :doc:`add_plots` or other data in DataFormatter.
- Use the above workflow and code documenation to make the appropriate changes.
- This is then sent to backend.
- Use jinja formatting to display on frontend.

Frontend Understanding
----------------------

Frontend is writtend in HTML, CSS, Javascript, plotly.js and bootstrap.

- All frontend code for creating plots from backend is sent to a Javascript file that can be found on 'app/static/dashboards/js/plotly_chart_generator.js'
- Using Jinja html template we loop through each graph data sent from backend and call the method present on the above file for creating plots.
- This file contains code for creating bar, stacked bar, pie, scatter, line graphs.
- Other js file in the same directory is for differnt part of page.

Example graph data sent from backend to frontend::

    [
        [
            Graph1stName: {
                'count': {'x1': 'y1', 'x2': 'y2'},
                'list': {'x1': [list of id present in y1], 'x2': [list of id present in y2]},
                'description': 'Graph description',
                'type': 'Graph type',
                'id': 'Graph ID',
                'color': 'Color'
            },
            Graph2ndName: {
                'count': {'x1': 'y1', 'x2': 'y2'},
                'list': {'x1': [list of id present in y1], 'x2': [list of id present in y2]},
                'description': 'Graph description',
                'type': 'Graph type',
                'id': 'Graph ID',
                'color': 'Color'
            }
        ]
    ]

We loop through each graph and send the details for each graph to function chart_generator() in plotly_chart_generator.js.

This plots a graph using plotly and create a specific div with a specific id to contain the graph.
