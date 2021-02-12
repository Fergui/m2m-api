Machine-to-Machine (M2M) Python API
===================================

Python interface to use functionalities from the new Machine-to-Machine (M2M) `USGS API <https://m2m.cr.usgs.gov/>`__.

The functionalities currently implemented are from endpoints: *login*, *dataset-search*, *dataset-filters*, *scene-search*, and *logout*.

Examples
--------

Connect to the M2M USGS API
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The interface will prompt to the user to specify the username (or email) and the password. It can also be specified when initializing the object using paramaters *username* and *password*.

.. code:: python

  from api import M2M
  m2m = M2M()
  

Search for all available USGS datasets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When the interface is initialized, it automatically search for all the datasets. So, the name of all the datasets is already an attribute of the object.

.. code:: python
  
  m2m.datasetNames
  
If you need more information for every dataset, you can also search all the datasets doing:

.. code:: python

  datasets = m2m.searchDatasets()
  
wich provides metadata for every dataset.

Search for all available filters for a specific USGS dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can look for specific metadata filters that you can apply to a specfic dataset doing:

.. code:: python

  datasetFilters = m2m.datasetFilters(datasetName="landsat_ot_c2_l1")

which returns a metadata with all the possible filters that one can apply to the metadata of this specific dataset. To then filter by this metadata, you can use *metadataInfo* explained in the next sections.

Send a spatio-temporal query to the USGS API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can search for scenes using different parameters. The parameters currently implemented on the interface are:

- *datasetName*:
- *startDate*:
- *endDate*:
- *maxResults*
- *boundingBox*:
- *geoJsonType*:
- *geoJsonCoords*:
- *geoJsonPath*:
- *minCC*:
- *maxCC*:
- *includeUnknownCC*:
- *metadataInfo*:

** Search by boundingBox **

.. code:: python

  params = {
        "datasetName": "landsat_ot_c2_l1",
        "startDate": "2020-08-01",
        "endDate": "2020-08-31",
        "boundingBox": (-126.47175275298368, -112.426440180154,
                        32.13566490555765, 42.399334704429755),
        "maxResults": 10000
  }
  scenes = m2m.searchScenes(**params)
  
