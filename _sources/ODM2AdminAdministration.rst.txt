ODM2 Admin Administration
=========================

The ODM2 entities you can administer with ODM2 Admin are organized in a number of catogories.

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

* **Organizations:** Observations and other Actions can be associated with  the Organization responsible for creating
   or performing them. `see here for more <https://github.com/ODM2/ODM2/blob/master/doc/ODM2Docs/core_organizations.md>`_
* **People:** ODM2 Core people details can be found `here  <https://github.com/ODM2/ODM2/blob/master/doc/ODM2Docs/core_people.md>`_
* **Affiliation:** Relates people and organizations

Variables and Units
-------------------

* **Variables:** ODM2 Core variables details can be found `here <https://github.com/ODM2/ODM2/blob/master/doc/ODM2Docs/core_variables.md>`_
* **Units:** ODM2 Core variables details can be found `here <https://github.com/ODM2/ODM2/blob/master/doc/ODM2Docs/core_units.md>`_
* **Taxonomic Classifiers:** provide a way to classify Results and Specimens according to terms from a formal taxonomy.
    See more details `here <https://github.com/ODM2/ODM2/blob/master/doc/ODM2Docs/core_taxonomicclassifiers.md>`_


Methods and Actions
-------------------

* **Methods:** to encode information about the procedure used to perform an Action. Every Action must be performed
    using a Method. Methods are modeled generically in ODM2 and can be of many types, including
    * Sample collection methods
    * Sample preparation methods
    * Sample analysis methods
    * Observation methods
    See more here `here <https://github.com/ODM2/ODM2/blob/master/doc/ODM2Docs/core_methods.md>`_
* **Actions:** ODM2 Core Action details can be found `here  <https://github.com/ODM2/ODM2/blob/master/doc/ODM2Docs/core_actions.md>`_
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