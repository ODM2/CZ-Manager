ODM2 Admin Walkthrough
======================

Below is a tutorial which explains many of the features of ODM2 Admin. This tutorial was developed for the 2017
BiG-CZ / ODM2 Hands-On Workshop, November 15-16, 2017 at UC Riverside, CA. It is meant as a demonstration of the
capabilities of ODM2 Admin and as a use case for ODM2. Links contained here access a demonstartion
version of ODM2 Admin populated with data from the `Luquillo Critical Zone Observatory <http://criticalzone.org/luquillo/>`_
and hosted by `CUAHSI <https://www.cuahsi.org/>`_   . If you would like access to the sandbox please email
leonmi@sas.upenn.edu

You can login to  the sandbox here: https://dev-odm2admin.cuahsi.org/Sandbox/

After logging in you will see the ODM2 Admin Home page:

.. image:: /images/ODM2AdminHomePage.png

This page consists of several parts, links to log out and change your password, the ODM2 Admin Shortcuts, ODM2 Admin
administration, authentication and authorization, and recent actions.

ODM2 Admin Shortcuts
--------------------

Upon logging into ODM2 Admin you will see the below navigation shortcuts across the top.

.. image:: /images/ODM2AdminShortcuts.png

* The first shortcut, displayed here as 'ODM2 Admin' with a cog icon, provides a list of all of the ODM2 pages.
* The second, 'Add Sensor Data', provides links to where you should enter information if you are trying to add
  new sensor data or you want to make changes to information relavent to sensor data.
* Third, 'Add Soil Profile Data' provides links for adding or editing Profile result data.
* Fourth, 'Record an Action', provides links for adding or editing actions and methods
  ( standarized method for how to perform an action).
* Fifth, Manage Citations, provides links for managing and exporting citations.
* Sixth, Graph My Data, provides links for data plotting and a map of your sites.


The ODM2 Admin Administration link will take you to a list of all 44 ODM2 entities that can be directly managed in
ODM2 Admin. See the ODM2 Admin Forms for details about the ODM2 Admin Forms :ref:`ODM2-Administration`.

Recent actions show changes you have recently completed in ODM2 Admin such as adding or editing an item in the forms.

Additional entities exist within the ODM2 information model these need to be managed with another tool
Such as with the ODM2PythonAPI. Django models exist for each ODM2 entity so it is also possible to write Python scripts
using the Django Object relational mapper. See :ref:`Managing-ODM2-With-The-Django-ORM` for details on using the Django
ORM with ODM2 databases.


.. toctree::
   :maxdepth: 1

   1) The ODM2 Admin Forms <ODM2AdminAdministration>
   2) Using Data Logger Files <DataLoggerFiles>
   3) Managing Profile Results With ODM2 Admin <ProfileResults>
   4) Time series QA/QC <DataQAQC>
   5) Data visualization and URL parameters <DataVisualizationTips>
   6) Using the Django ORM <ManagingODM2WithTheDjangoORM>


* :ref:`ODM2 Admin docs home page <ODM2-Admin>`
* :ref:`Search the docs <search>`

