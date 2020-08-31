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
and project that should be visible to each role.

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
XNAT instance. For this, you will need valid credentials.
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
it as pickle. This saved pickle is used for plotting graphs and other
information of the XNAT instance from which it fetched data.

Script to download_data as pickle file::

    download_data.py -i 'path to xnat config file' -o 'path where the pickle will be saved'

Example

- Pickle file to be generated at xnat_dashboards/config/name.pickle
- XNAT configuration file is present at xnat_dashboards/config/name.cfg

Script to download_data as pickle file::

    download_data.py -i 'xnat_dashboards/config/name.cfg' -o 'xnat_dashboards/config/name.pickle'

Starting the server
-------------------

Running the server is the process of assigning path of pickle, dashboard configuration file,
assigning url and port number to the flask server.

Script::

    run_dashboards.py -p 'path to saved pickle file' -c 'path to dashboard configuration file'

This above script will start the server on this `URL <localhost:5000>`_


- Change server URL default as 'localhost'
- Change server port default as '5000'
- Change debug as 1 default as 0

Extra Arguments::

    run_dashboards.py -p 'path to saved pickle file' -c 'path to dashboard configuration file' -port 'port number' -url 'URL' -debug 1

Example:

- Pickle file is present at xnat_dashboards/config/name.pickle
- Dashboard configuration file is present at xnat_dashboards/config/name.json

Script to download_data as pickle file::

    run_dashboards.py -p 'xnat_dashboards/config/name.pickle' -c 'xnat_dashboards/config/name.json'
