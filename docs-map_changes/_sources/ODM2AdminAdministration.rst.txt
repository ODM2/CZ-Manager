.. _ODM2-Administration:

ODM2 Admin Forms
================

The ODM2 entities you can administer with ODM2 Admin Forms are organized in a number of catogories.

* People and Organizations
* Variables and Units
* Methods and Actions
* Sampling Features and Sites
* Result Definitions
* Result Values
* Citations
* Data Logger Files
* Data Quality
* External Identifier Systems

Details about ODM2 entities and database schemas can be found on the ODM2 wiki https://github.com/ODM2/ODM2/wiki/documentation

Many of the below entities use controlled vocabularies which can be found here http://vocabulary.odm2.org/

People and Organizations
------------------------

* **Organizations:** Observations, Sensor deployments retrievals and other Actions can be associated with  the Organization responsible for creating
   or performing them. `see here for ODM2 Organizations doc <https://github.com/ODM2/ODM2/blob/master/doc/ODM2Docs/core_organizations.md>`_
* **People:** ODM2 Core people details can be found `here ODM2 people doc <https://github.com/ODM2/ODM2/blob/master/doc/ODM2Docs/core_people.md>`_
* **Affiliation:** Relates people and organizations

Variables and Units
-------------------

* **Variables:** ODM2 Core variables details can be found `here ODM2 Variables doc <https://github.com/ODM2/ODM2/blob/master/doc/ODM2Docs/core_variables.md>`_
* **Units:** ODM2 Core variables details can be found `here ODM2 Units doc <https://github.com/ODM2/ODM2/blob/master/doc/ODM2Docs/core_units.md>`_
* **Taxonomic Classifiers:** provide a way to classify Results and Specimens according to terms from a formal taxonomy.
    For more see the `ODM2 Taxonomic Classifiers doc <https://github.com/ODM2/ODM2/blob/master/doc/ODM2Docs/core_taxonomicclassifiers.md>`_


Methods and Actions
-------------------

* **Methods:** to encode information about the procedure used to perform an Action. Every Action must be performed
  using a Method. Methods are modeled generically in ODM2 and can be of many types, including:

    * Sample collection methods
    * Sample preparation methods
    * Sample analysis methods
    * Observation methods
    * Instrument calibration
    *Instrument Maintenance

    See the `ODM2 Methods doc <https://github.com/ODM2/ODM2/blob/master/doc/ODM2Docs/core_methods.md>`_
* **Actions:** ODM2 Core Action details can be found at the `ODM2 Actions doc  <https://github.com/ODM2/ODM2/blob/master/doc/ODM2Docs/core_actions.md>`_
  Actions are used to encode information about activities or actions that are performed in the process of making observations.
  Some types of actions include:

    * Observation act (produces a Result)
    * Sample collection
    * Sample preparation
    * Sample analysis (produces a Result)
    * Site visit
    * Instrument deployment (Produces a Result)
    * Instrument maintenance
    * Instrument calibration
    * Etc.

* **Related actions:** Allow you to setup sequences of actions by relating one action to another.



Sampling Features and Sites
---------------------------

* **Sampling Features:** Every Action must be performed on or at a Sampling Feature. For example, a "Site visit" Action
  is made to a Site Sampling Feature. A "Laboratory analysis" Action is performed on a Specimen Sampling Feature.
  For more see the `ODM2 docs <https://github.com/ODM2/ODM2/blob/master/doc/ODM2Docs/core_samplingfeatures.md>`_

  * Feature actions, sampling feature external identifiers, sampling feature extension property values, and sites
    are inline forms in sampling features.
* **Related Features:** labeled as 'relate two features' in ODM2 Admin, allows you to establish relationships between
  sampling features such as parent child relationships.

* **Feature action:** labeled as 'Sampling feature actions' in ODM2 Admin. For more see `ODM2 Feature actions doc <https://github.com/ODM2/ODM2/blob/master/doc/ODM2Docs/core_featureactions.md>`_

* **Sites** Sampling features could also be specimens if they are locations then they need to have an associated site.

* **Saptial References:**  a coordinate-based local, regional or global system used to locate geographical entities.

Results
-------

* **Results:** The outcome of an action, such as sensor deployment or specimen observation. These are labeled as data
results in ODM2 Admin. For more see `ODM2 Results doc https://github.com/ODM2/ODM2/blob/master/doc/ODM2Docs/core_results.md`_

* **Datasets:** The Datasets entity is used to encode information about groups of Results that are logically related.
  A Dataset has a type, title, an abstract, and is the entity in ODM2 that would receive a citation.
  For more see the `ODM2 Datasets doc <https://github.com/ODM2/ODM2/blob/master/doc/ODM2Docs/core_datasets.md>`_

* **Dataset Results:** Results that are part of a dataset.

* **Processing Levels:** Each Result recorded in ODM2 has a ProcessingLevel, which specifies the level of quality
  control or data processing that the Result has been subjected to. For more see `ODM2 Processing Levels doc <https://github.com/ODM2/ODM2/blob/master/doc/ODM2Docs/core_processinglevels.md>`_

Result Values
-------------

* **Time Series Results:** A Time Series Result consists of a series of ResultValues for a single Variable,
  measured on or at a single SamplingFeature (e.g., a Site), using a single Method (e.g., sensor), with specific Units,
  and having a specific ProcessingLevel, but measured over time. For more see `ODM2 Time Series Coverage Results doc <https://github.com/ODM2/ODM2/blob/master/doc/ODM2Docs/ext_results_timeseries.md>`_

* **Time Series Result Values:** Values for a given time series.

* **Measurement Results:** A Measurement Result consists of a single ResultValue for a single Variable, measured on or
  at a single SamplingFeature (e.g., in most cases a Specimen), using a single Method (e.g., laboratory analytical
  Method), with specific Units, and having a specific ProcessingLevel. For more see `ODM2 Measurement Results doc <https://github.com/ODM2/ODM2/blob/master/doc/ODM2Docs/ext_results_measurement.md>`_

* **Measurement Result Values:** Values for a measurement result.

* **Profile Results:** An Depth Profile Coverage Result consists of a series of ResultValues for a single Variable, at
  a single location, measured using a single Method, with specific Units, having a specific ProcessingLevel, but
  measured over multiple depths. For more see `ODM2 Profile Results doc <https://github.com/ODM2/ODM2/blob/master/doc/ODM2Docs/ext_results_profile.md>`_

* **Profile Result Values:** Values for a profile result.

* **Related Results:** Results can be related to one another. In ODM2 Admin they can be used to say that one result is
  derived from another using derivation equations.

* **Related Derivation Equations:** relate derivation equations and results. derived results can have derivation
  equations, You can derive them using related results.

.. image:: /images/DerivingValues.png

* **Derivation equation:** An equation used to derive values from a time series. These allow you to transform things
  like stage height into discharge using a ratings curve. Or an instrument measurement say in millivolts into an
  observation of interest.

citations
---------

* **Citations:** A citation

* **Author list:** A list of Authors

* **Dataset citations:** link a dataset to a citation

* **Method citations:** link a method to a citation

* **Extension properties:** define extra metrics about citations, can be applied to other objects

* **Citation extension properties values:** track extra metrics about citations

Data logger files
-----------------

For details about how to use data logger files see :ref:`Using Data Logger Files <DataLoggerFiles>`

* **Data logger program files:** The program used by the data logger while logging values.

* **Data logger files:** Files containing time series result values.

* **Data logger file columns:** Columns associated with data logger files these match columns in the file.

* **Process data logger files:** Used to ingest data logger files.

* **Instrument output variables:** Associated with a data logger file column.

* **Equipment models:** That recorded some data values in a data logger file.

Data quality
------------

* **Data quality:** The optional DataQuality extension enables ODM2 users to encode specific information about the
  quality of their Results. The DataQuality entity provides values for the precision, detection limit, etc. for Results.
  For more see the `ODM2 Data quality doc <https://github.com/ODM2/ODM2/blob/master/doc/ODM2Docs/ext_dataquality.md>`_

* **results data quality:** Specify the data quality for specific data results.

External identifier systems
---------------------------

* **External identifier systems:** Such as an IGSN or ORCiD.

:ref:`2) ODM2 Admin Site Management <ODM2AdminSiteManagement>`

* :ref:`ODM2 Admin docs home page <ODM2-Admin>`
* :ref:`Search the docs <search>`