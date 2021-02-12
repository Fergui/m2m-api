# Machine-to-Machine (M2M) Python API

Python interface to use functionalities from the new Machine-to-Machine (M2M) `USGS API <https://m2m.cr.usgs.gov/>`__.

The functionalities currently implemented are from endpoints:

- login
- logout
- dataset-search
- dataset-filters
- scene-search

Example
-------

Connect to the M2M USGS API
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

  from api import M2M
  m2m = M2M()
  

Search for all available USGS datasets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python
  
  m2m.datasetNames
  
  
Send a spatio-temporal query to the USGS API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# By boundingBox

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
  
