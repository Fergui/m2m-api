from api import M2M
import logging

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')

params = {
    "datasetName": "landsat_ot_c2_l1",
    "startDate": "2020-08-01",
    "endDate": "2020-08-31",
    "geoJsonPath": "geojson/california.geojson",
    "metadataInfo": {
        "and": [
            ('Sensor Identifier','value','OLI_TIRS'),
            ('Data Type L1','value','L1TP'),
            ('Collection Category','value','T1')
        ]
    },
    "maxResults": 3
}

m2m = M2M()

scenes = m2m.searchScenes(**params)
downloadMeta = m2m.retrieveScenes(params['datasetName'],scenes)
