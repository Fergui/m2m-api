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

Search scenes by parameters using the USGS API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can search for scenes using different parameters. The parameters currently implemented on the interface are:

+--------------------+---------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Parameters**     |                  **Format**                 | **Description**                                                                                                                                                                                                            |
+====================+=============================================+============================================================================================================================================================================================================================+
| *datasetName*      |                    String                   | Name of the USGS dataset. To search for what are the available datasets, look at previous sections. Example: *"landsat_ot_c2_l1"*.                                                                                         |  
+--------------------+---------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| *startDate*        |           ISO 8601 Formatted Date           | Start date of acquisition. Default value is "2000-01-01". Example: *"2020-08-01"*.                                                                                                                                         |
+--------------------+---------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| *endDate*          |           ISO 8601 Formatted Date           | End date of acquisition. Default value is current time. Example: *"2020-08-31"*.                                                                                                                                           |
+--------------------+---------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| *maxResults*       |                    Integer                  | Maximum number of scenes to return. Default value is 100. Example: *10000*.                                                                                                                                                |
+--------------------+---------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| *boundingBox*      |                 Tuple (length 4)            | Spatial bounding box expressed as (min_lon,max_lon,min_lat,max_lat) in EPSG:4326 projection. Example: *(-126.471753, -112.426439, 32.135664, 42.399335)*.                                                                  |
+--------------------+---------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| *geoJsonType*      |                    String                   | Geometry types supported by GeoJson. Example: *"Polygon"*.                                                                                                                                                                 |
+--------------------+---------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| *geoJsonCoords*    |                 List of lists               | Coordinates for the GeoJson expressed as [lon,lat] in EPSG:4326 projection. Example: *[[[-126.471753,32.135664], [-126.471753,42.399335], [-112.426439,42.399335], [-112.426439,32.135664], [-126.471753,32.135664]]]*.    |
+--------------------+---------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| *geoJsonPath*      |                    String                   | Path to a GeoJson file. Example: *"geojson_files/california.geojson"*.                                                                                                                                                     |
+--------------------+---------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| *minCC*            |                    Integer                  | Used to limit results by minimum cloud cover (for supported datasets). Default is 0. Example: *10*.                                                                                                                        |
+--------------------+---------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| *maxCC*            |                    Integer                  | Used to limit results by maximum cloud cover (for supported datasets). Default is 100. Example: *90*.                                                                                                                      |
+--------------------+---------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| *includeUnknownCC* |                    Boolean                  | Used to determine if scenes with unknown cloud cover values should be included in the results. Default is True. Example: *False*.                                                                                          |
+--------------------+---------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| *metadataInfo*     |                   Dictionary                | Dictionary with information about filtering from metadata. More information in next sections.                                                                                                                              |
+--------------------+---------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+


**Search by boundingBox**

.. code:: python

  params = {
        "datasetName": "landsat_ot_c2_l1",
        "startDate": "2020-08-01",
        "endDate": "2020-08-31",
        "boundingBox": (-126.471753, -112.426439, 
                        32.135664, 42.399335),
        "maxResults": 10000
  }
  scenes = m2m.searchScenes(**params)
  
  
**Search by geoJson information**

.. code:: python

  params = {
        "datasetName": "landsat_ot_c2_l1",
        "startDate": "2020-08-01",
        "endDate": "2020-08-31",
        "geoJsonType": "Polygon",
        "geoJsonCoords": [[[-126.471753, 32.135664], 
                           [-126.471753, 42.399335], 
                           [-112.426439, 42.399335], 
                           [-112.426439, 32.135664], 
                           [-126.471753, 32.135664]]],
        "maxResults": 10000
  }
  scenes = m2m.searchScenes(**params)
 
**Search by geoJson file**

.. code:: python

  params = {
        "datasetName": "landsat_ot_c2_l1",
        "startDate": "2020-08-01",
        "endDate": "2020-08-31",
        "geoJsonPath": "geojson_files/california.geojson",
        "maxResults": 10000
  }
  scenes = m2m.searchScenes(**params)
  
**Search by metadata info**


