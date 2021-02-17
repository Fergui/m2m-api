Machine-to-Machine (M2M) Python API
===================================

Python interface to use functionalities from the new Machine-to-Machine (M2M) `USGS API <https://m2m.cr.usgs.gov/>`__.

The functionalities currently implemented are from endpoints: *login*, *dataset-search*, *dataset-filters*, *scene-search*, *permissions*, *download-options*, *download-request*, *download-retrieve*, *download-search*, and *logout*.

For ordering and downloading data from USGS, one need to request access at https://ers.cr.usgs.gov/profile/access doing:
  
1) Login to your USGS account.
2) Press *Request Access* bottom.
3) Select *MACHINE* access type. 
4) Fill survey about data use.
5) Wait a couple of days before acceptance.

Once request access is accepted, permissions should return ['download', 'order'].

Connect to the M2M USGS API
---------------------------

The interface will prompt to the user to specify the username (or email) and the password.

.. code:: python

  from api import M2M
  m2m = M2M()
  
It can also be specified when initializing the object using paramaters *username* and *password*.

.. code:: python

  from api import M2M
  m2m = M2M(username, password)
  
By default, the stable version of the M2M USGS API is used. To use another version, one can define *version* as string doing:

.. code:: python

  from api import M2M
  m2m = M2M(version=version)
  
Look at your M2M USGS API permissions
-------------------------------------

When the interface is initialized, it automatically looks at your permissions. So, the permissions is already an attribute of the object.

.. code:: python

  m2m.permissions


Search for all available USGS datasets
--------------------------------------

When the interface is initialized, it automatically search for all the datasets. So, the name of all the datasets is already an attribute of the object.

.. code:: python
  
  m2m.datasetNames
  
If you need more information for every dataset, you can also search all the datasets doing:

.. code:: python

  datasets = m2m.searchDatasets()
  
wich provides metadata for every dataset.

Search for all available filters for a specific USGS dataset
------------------------------------------------------------

You can look for specific metadata filters that you can apply to a specfic dataset doing:

.. code:: python

  datasetFilters = m2m.datasetFilters(datasetName="landsat_ot_c2_l1")

which returns a metadata with all the possible filters that one can apply to the metadata of this specific dataset. To then filter by this metadata, you can use *metadataInfo* explained in the next sections.

Search scenes by parameters using the USGS API
----------------------------------------------

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

Metadata information dictionary starts with an "and" or "or" field containing a list of tuples. Each tuple has size 3 and represents one metadata filter condition. To know what metadata filters are available for a specific dataset, look at the previous section. Each metadata filter contains

* **Field Name**: Name of the metadata filter (fieldLabel field in datasetFilters).
* **Field Type**: Type of metadata filter. Options are: 

    * *'value'*: set a specific value.
    * *'between'*: set a range of values.  
    
* **Field Value**: Value of the metadata filter. Depending on the Field Type:

    * *'value'*: Field Value is a single value (format depends on the data format of the metadata field).
    * *'between'*: Field Value is a list of two values (format depends on the data format of the metadata field).

Example: 

.. code:: python

  "metadataInfo": {
          "and": [
              ('Sensor Identifier','value','OLI_TIRS'),
              ('Data Type L1','value','L1TP'),
              ('Collection Category','value','T1')
          ]
   }


Search by a Bounding Box
^^^^^^^^^^^^^^^^^^^^^^^^

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
  print("{} - {} hits - {} returned".format(datasetName,scenes['totalHits'],scenes['recordsReturned']))
  
Search by GeoJson information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
  print("{} - {} hits - {} returned".format(datasetName,scenes['totalHits'],scenes['recordsReturned']))
 
Search by GeoJson file
^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

  params = {
      "datasetName": "landsat_ot_c2_l1",
      "startDate": "2020-08-01",
      "endDate": "2020-08-31",
      "geoJsonPath": "geojson/california.geojson",
      "maxResults": 10000
  }
  scenes = m2m.searchScenes(**params)
  print("{} - {} hits - {} returned".format(datasetName,scenes['totalHits'],scenes['recordsReturned']))
  
Search by Cloud Cover range
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

  params = {
      "datasetName": "landsat_ot_c2_l1",
      "startDate": "2020-08-01",
      "endDate": "2020-08-31",
      "geoJsonPath": "geojson_files/california.geojson",
      "minCC": 10,
      "maxCC": 70,
      "includeUnknownCC": False,
      "maxResults": 10000
  }
  scenes = m2m.searchScenes(**params)
  cloudCovers = [float(r['cloudCover']) for r in scenes['results']]
  print("{} - {} hits - {} returned - min_cc={} - max_cc={}".format(datasetName, scenes['totalHits'],
                                                                    scenes['recordsReturned'],
                                                                    min(cloudCovers),max(cloudCovers)))

Search by Metadata information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

  params = {
      "datasetName": "landsat_ot_c2_l1",
      "startDate": "2020-08-01",
      "endDate": "2020-08-31",
      "geoJsonPath": "geojson_files/california.geojson",
      "metadataInfo": {
          "and": [
              ('Sensor Identifier','value','OLI_TIRS'),
              ('Data Type L1','value','L1TP'),
              ('Collection Category','value','T1')
          ]
      },
      "maxResults": 10000
  }
  scenes = m2m.searchScenes(**params)
  print("{} - {} hits - {} returned".format(datasetName,scenes['totalHits'],scenes['recordsReturned']))

Download options search
-----------------------

For a single or multiple scenes, you can search the download options using the *datasetName* and a single or a list of *entityIds*. The *entityId* can be found in the scene dictionary found using any search from previous sections. For instance, if we want to look at the download options for the first scene found for the "landsat_ot_c2_l1" dataset, we would do:

.. code:: python

  downloadOptions = m2m.downloadOptions("landsat_ot_c2_l1", scenes['results'][0]['entityId'])

The results, show that for every scene, one has 8 different options to download. In order to filter specific options depending on arguments of the *downloadOptions*, one can use the *filterOptions* argument. Using that argument, scenes can be filtered using a key argument and a function to evaluate if valid or not. So, *filterOptions* is a dictionary with:

- Keys from the *downloadOptions* dictionary that the user want to filter on.
- Function taking the values from the *downloadOptions* dictionary as argument and returning False or True if filter or not filter out.

For instance, if we only want products available for bulk download, one can do:

.. code:: python

  filterOptions = {'bulkAvailable': lambda x: x}

or if we only want products that are Full-Resolution Browse (Natural Color) GeoTIFFs, you can do:

.. code:: python

  filterOptions = {'productName': lambda x: x == 'Full-Resolution Browse (Natural Color) GeoTIFF'}

and then do:

.. code:: python

  downloadOptions = m2m.downloadOptions("landsat_ot_c2_l1", scenes['results'][0]['entityId'], filterOptions=filterOptions)


Download scenes using the USGS API
----------------------------------

Download scenes searched using the M2M USGS API can be downloaded specifying the *datasetName* of the search and the list of scenes retrieved using *searchScenes* from the previous section.

Default download
^^^^^^^^^^^^^^^^

In this case, the default download is to download all available data from DDS in zip format. For instance:

.. code:: python

  downloadMetadata = m2m.retrieveScenes("landsat_ot_c2_l1", scenes)

Filter scenes to download
^^^^^^^^^^^^^^^^^^^^^^^^^

Other filters can be specified using *filterOptions* arguments. The default download, defines the filter to be:

.. code:: python

  filterOptions = {'downloadSystem': lambda x: x == 'dds_zip', 'available': lambda x: x}
  
However, the user can specify custom keys and functions to evaluate as seen in previous sections and do:

.. code:: python

  downloadMetadata = m2m.retrieveScenes("landsat_ot_c2_l1", scenes, filterOptions=filterOptions)


Cutom M2M USGS API request
--------------------------

To make a custom request to the M2M USGS API, one needs to define the *endpoint* which is the endpoint string. Possible string endpoints can be found at `here <https://m2m.cr.usgs.gov/api/docs/reference/>`__. Most endpoints need some data which can be defined using a python dictionary. The dictionary can be created using the test application of the M2M USGS API `here <https://m2m.cr.usgs.gov/api/test/json/>`__.

.. code:: python

  r = m2m.sendRequest(endpoint, data)
