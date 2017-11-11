ODM2 Admin Managing Profile Results
===================================

Some of the sampling features, accessible from the ODM2 Admin Map contian sampling features such as

   .. image:: /images/FieldArea.png


Field area Palm SJH, WS 2015 represents a set of soil pits making up a study area. Soils taken from this study area were
analyzed for Acid phophatase, Ammonium oxalate extractable aluminum and other compounds. A graph of these values can be
viewed here:
https://dev-odm2admin.cuahsi.org/Sandbox/profilegraph/selectedrelatedfeature=15/popup=true/

We can for example plot the percent clay content:

   .. image:: /images/ProfileResultClay.png

We can export the data from this page then we get the below, the method here has been shortend for space.

.. csv-table::  Palm SJH, WS 2015 Clay values
    :header: "databaseid","depth","sampling feature/location","sampling feature uri","method","citation"," Clay -unit-Percent-processing level-L1 passed QAQC , L1 passed QAQC"
    :widths: 10, 20, 50,50,400,20,20,20

    6196, 0.0-10.0 CM- Centimeter ," Elfin- Plot 61-Block 5- SJH-WS-2015",,"  We tested the influence of anaerobiosis...",,13.40865635
    6198, 10.0-20.0 CM- Centimeter ," Elfin- Plot 61-Block 5- SJH-WS-2015",," We tested the influence of anaerobiosis...",,14.3594963551
    6200, 0.0-10.0 CM- Centimeter ," Elfin- Plot 62-Block 5- SJH-WS-2015",,"  We tested the influence of anaerobiosis...",,12.8595966657

The export contains a database id record for the profile result value, the depth which is the difference between
the current profile result value's intended depth and the previous profile result value intended depth where the profile
results have  the same sampling feature.

