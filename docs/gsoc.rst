GSOC 2020 Status Report
=======================

`GSOC PROJECT URL <https://summerofcode.withgoogle.com/projects/#5857201001857024>`_

| **Organization:** INCF (International Neuroinformatics Coordinating Facility)
| **Mentors:** Greg Operto, Jordi Huguet
| **Student:** Mohammad Asif Hashmi

What is this project about?
---------------------------

* XNAT comes with a native built-in GUI. This project provides a dashboard framework for user to create or use pre defined plots and dashboards for exploring, monitoring, and reviewing data present on their XNAT instance 
* It interacts with the XNAT server instance and fetches the required data from it, using this data, we visualize the information present in it in a summarized form.
* It can be used with any XNAT instance.
* It can be further improve and new features can be added as per the changing requirements or needs of user by developers.

Why this project?
-----------------

* Currently XNAT native GUI lacks flexibility and it’s UX can be improved.
* It is important to provide a system/framework to allow users to monitor some specific measurements, including longitudinal ones, or some advanced ones that may require some time to collect.
* This project tackles these major issues by developing a flexible web dashboard framework, where the users can register and access the information through different visualizations like bar graphs, pie charts, scatter plots and longitudinal graphs.

Dashboards created during GSoC coding period
-----------------------------------------------

5 Dasbhoards are created

* **Overview:** This dashboard contain plots for all data present on the XNAT instance.
* **Per Project:** This dashboards contain plots that specific to a project ID.
* **Projects:** List of projects that are visible to the user.
* **Projects Owned collaborated or member:** List of projects that where user is a Member, Collaborator or Owner.
* **Longitudinal:** It contain plots for longitudinal data.

BBRC specific dashboard
~~~~~~~~~~~~~~~~~~~~~~~

1 Dashboard is created

**TEST GRID:** This dashboard contain data of each session of a project in a grid format with color **GREEN** (Test status successfull), **RED** (Test Status failed), **GREY** (Test skipped), **BLACK** (No information for the particular test).

Dashboards Features created during GSoC coding period
-----------------------------------------------------

* User can **login from the registered username and password created on XNAT instance**.
* **Counter** for number of projects, subjects, experiments, scans.
* **Compatible with multiple browser platforms**.
* **5 types of plots** are provided. **Bar graph**, **Stacked graph**, **Pie chart**, **Line chart**, **scatter plot**.
* User can **add detailed description of each plots** using dashboard configuration file.
* User can **define visiblity to each graph** based on user role from dashboard configuration file.
* User can **change color for each graph**
* User can **view the project, subject, experiment and scans ID** from the plots.
* **Links are provided** to each id.
* Installation using **pip** is available.
* Scripts to **run directly from command line**.
* **Tests are provided** for different parts of code.
* **Code documentation** are available.
* **User guide** is available for creating new plots and dashboards.
* **Developer guide** is available for creating new plots and dashboards,development and testing.
* **Password are never saved in any pickle or database**, First software checks whether user details are present in XNAT instance using Pyxnat and then show pickle data based on user role assigned by the admin to user in dashboard configuration file.

BBRC specific Features
~~~~~~~~~~~~~~~~~~~~~~

* Test status pop ups.
* Test grid can be exported to excel file
* Filter test grid based on version


Plots/Metrics created during GSoC coding period
-----------------------------------------------

Total of 27 plots were created.

*    **Imaging Sessions:** Total number of different types of session visible
*    **Projects Visibility:** Total project visible and their visiblity type
*    **Sessions types/Project:** Number of sessions types for each visible project
*    **Subjects/Project:** Number of Subjects or patient in each visible project
*    **Age Range:** Age distribution of patients or subjects
*    **Gender:** Gender distribution of patients
*    **Handedness:** Number of patients with their dominant hand count
*    **Experiments/Subject:** Number of sessions for each patient
*    **Experiment Types:** Different types of Sessions
*    **Experiments/Project:** Number of sessions for each project visible
*    **Scans Quality:** How many scans are of usable quality
*    **Scan Types:** Different scan types present and there count
*    **XSI Scan Types:** Different XSI types of scans
*    **Scans/Project:** Number of scans present in each project
*    **Scans/Subject:** Number of scans for each patient
*    **Resources/Project:** Number of resources present in each project
*    **Resource Types:** Different type of resources present. No data field represent session don't have any resource object.
*    **Resources/Session:** Number of resources present for each session
*    **Sessions/Resource type:** Click on one of the resource types, corresponding sessions which have the resource type will be shown
*    **Projects:** Number of projects over time saved in XNAT instance.
*    **Subjects:** Number of projects over time saved in XNAT instance.
*    **Experiments:** Number of projects over time saved in XNAT instance.
*    **Scans:** Number of projects over time saved in XNAT instance.
*    **Resources:** Number of projects over time saved in XNAT instance.
*    **Experiments Proportions:** Graph shows how many subjects have 1, 2 or n number of experiments
*    **Scans Proportions:** Graph shows how many subjects have 1, 2 or n number of scans
*    **Session resource count/Project:** Graphs shows how many sessions have 1,2 or n number of resources

BBRC specific Plots/Metrics
~~~~~~~~~~~~~~~~~~~~~~~~~~~

8 Plost/Metrics specific to BBRC resources were created

*    **Freesurfer end and start hour difference:** Difference between the freesurfer start and end time in hours.
*    **Free Surfer:** Shows whether free surfer resource details exist or not.
*    **UsableT1:** Number of usable and non usable T1 for each session done on patient
*    **Archiving Validator:** Number of session which have archiving validators
*    **Version Distribution:** Different versions of Archiving validator for each sessions
*    **BBRC validator:** BBRC validator present in resources for each session
*    **Consistent Acquisition Date:** Whether acqisition date field is present in resources. No data means acquistion date for session isn't present
*    **Dates Diff:** Difference between insertion dates and acquisition dates per session, if acqusition date present in session test


Improvement that can be done after GSoC 2020
--------------------------------------------

* Making creation of dashboards purely dependent on backend changes and independent from fontend changes, as of now only plots and graphs can be created from backend changes without a need to change frontend.
* More frontend features, UX and UI Improvement.
* Improvement in code quality and tests.
* Increasing robustness of code.
* Automation script for downloading data.
