User Guide
===============

This guide is for the users that will be using this dashboard
for exploring data present on their XNAT instance.


Prerequisites
-------------
Before starting, make sure that you have the :mod:`xnat_dashboards` distribution
:doc:`installed <installation>`. In the Python shell, the following
should run without raising an exception:

.. code-block:: python

  >>> import xnat_dashboards

This tutorial also assumes that you have access to an XNAT instance.
You may also use `XNAT Central <https://central.xnat.org>`_, which is a public
instance managed by the XNAT team and updated on a regular basis.

Understanding dashboard configuration file
------------------------------------------

Their are 4 types of roles:

- admin (Access to all content).
- superuser (Access to content defined by admin).
- guest (Access to very less information defined by admin).
- forbidden (User who are not allowed to login).


**roles_config** this key value contains information regarding user, their assigned roles
and project that should be visbile to each role.

user roles::

    Used to assign roles to user based on their names on the XNAT instance.
    {
        'username_on_xnat': 'role'
    }

project_visible::

    List of project that should be visible to each role.
    {
        'role': ['p1', 'p2'],
        'role2': ['*'] user * for all projects
    }

graph_config::

    This key contains information regarding each graphs.

    {
        'Graph_1_name':{
            "type":"graph type",
            "description": "Description of graph",
            "visibility": ["list of roles for which it should be visible"],
            "color":"Graph Color"
        }
    }

Creating the configuration files
--------------------------------

Step-1 Create a configuration file for connecting with the
XNAT instance with :class:`~pyxnat.Interface`. For this, you will need valid credentials.
Make sure you have them or request them through the web interface of the targeted host.

.. code-block:: python

   >>> central = Interface(server="https://central.xnat.org")
       User:my_login
       Password:my_password

The easiest way to create this XNAT configuration file is to use the
:func:`~pyxnat.Interface.save_config()` method on an existing interface.

.. code-block:: python

   >>> central.save_config('central.cfg')

Step-2 Create dashboard configuration file. You can copy the content of already
create dashboard configuration file using the following link
`dashboard_config <https://gitlab.com/Udolf47/xnat_dashboards/-/blob/development/xnat_dashboards/config/dashboard_config.json>`_.
Edit it as per requirements and need.

Changes that can be done using dashboard configuration file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Assign roles to different users, using username present on xnat instance.

- Set visibility of different projects of your xnat instance.

- Change which graphs can be visible to which user roles.

Downloading Data
----------------

Downloading data is the process of fetching data from the XNAT instance and saving
it as pickle. This saved pickcle is used for plotting graphs and information other
informations of the XNAT instance from which it fetched data.

Create a python file with following content and name it download_data.py

.. code-block:: python

    from xnat_dashboards.pyxnat_interface import pickle_saver
    from xnat_dashboards import path_creator
    import os
    import argparse


    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-i", "--cfg", type=str,
        help="Path to pyxnat configuration file")
    ap.add_argument(
        "-o", "--pickle", type=str,
        help="Path where the pickle file will be created")

    args = vars(ap.parse_args())

    if __name__ == "__main__":

        path_creator.set_pickle_path(
            os.path.abspath(args['pickle']))

        pickle_saver.PickleSaver(args['cfg'], True)

Run the python file to download the data

Script::

    python download_data.py -i 'path to xnat config file' -o 'path where the pickle will be saved'

Starting the server
-------------------

Running the server is the process of assigning path of pickle, dashboard configuration file,
assigning url and port number to the flask server.

Create a python file with following content and name it as server.py

.. code-block:: python

    from xnat_dashboards.app import app
    from xnat_dashboards import path_creator
    import os
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-p", "--pickle", type=str,
        help="Path to saved pickle file")
    ap.add_argument(
        "-c", "--config", type=str,
        help="Path to configuration file")
    args = vars(ap.parse_args())


    if __name__ == "__main__":

        if args['pickle'] is None or args['config'] is None:
            print("Please provide path to both pickle and config file")
        else:
            # Path to configuration and pickle files
            path_creator.set_dashboard_config_path(
                os.path.abspath(args['config']))
            path_creator.set_pickle_path(
                os.path.abspath(args['pickle']))
            # Change localhost url or port here
            app.run(debug=True)

Run this python file to start the server.

Script::

    python server.py -p 'path to saved pickle file' -c 'path to dashboard configuration file'

This above script will start the server on this `URL <localhost:5000>`_

