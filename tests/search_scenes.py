from api import M2M
import logging
import sys

_examples_params = {
    '0': {
        "datasetName": "landsat_ot_c2_l1",
        "startDate": "2020-08-01",
        "endDate": "2020-08-31",
        "boundingBox": (-126.47175275298368, -112.426440180154,
                        32.13566490555765, 42.399334704429755),
        "maxResults": 10000
    },
    '1': {
        "datasetName": "landsat_ot_c2_l1",
        "startDate": "2020-08-01",
        "endDate": "2020-08-31",
        "geoJsonType": "Polygon",
        "geoJsonCoords": [[[-126.47175275298368,32.13566490555765], 
                            [-126.47175275298368,42.399334704429755], 
                            [-112.426440180154,42.399334704429755], 
                            [-112.426440180154,32.13566490555765], 
                            [-126.47175275298368,32.13566490555765]]],
        "maxResults": 10000
    },
    '2': {
        "datasetName": "landsat_ot_c2_l1",
        "startDate": "2020-08-01",
        "endDate": "2020-08-31",
        "geoJsonPath": "geojson/california.geojson",
        "maxResults": 10000
    },
    '3': {
        "datasetName": "landsat_ot_c2_l1",
        "startDate": "2020-08-01",
        "endDate": "2020-08-31",
        "geoJsonPath": "geojson/california.geojson",
        "minCC": 10,
        "maxCC": 70,
        "includeUnknownCC": False,
        "maxResults": 10000
    },
    '4': {
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
        "maxResults": 10000
    },
    '5': {
        "datasetName": "landsat_ot_c2_l2",
        "startDate": "2020-08-01",
        "endDate": "2020-08-31",
        "geoJsonPath": "geojson/california.geojson",
        "metadataInfo": {
            "and": [
                ('Sensor Identifier','value','OLI_TIRS'),
                ('Collection Category','value','T1')
            ]
        },
        "maxResults": 10000
    }
}

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if len(sys.argv) != 2 or sys.argv[1] not in _examples_params.keys():
    print('Error: {} example'.format(sys.argv[0]))
    print('       possible examples: {}'.format(sorted(map(int,_examples_params.keys()))))
    sys.exit(1)

example = sys.argv[1]
print_scenes = False

m2m = M2M()

params = _examples_params[example]
scenes = m2m.searchScenes(**params)
cloudCovers = [float(r['cloudCover']) for r in scenes['results']]
print("{} - {} hits - {} returned - min_cc={} - max_cc={}".format(params['datasetName'],scenes['totalHits'],
                                                                  scenes['recordsReturned'],
                                                                  min(cloudCovers),max(cloudCovers)))

if print_scenes:
    nId = str(len(scenes["results"][0]["displayId"])+2)
    nSd = str(len(scenes["results"][0]["temporalCoverage"]["startDate"])+2)
    disp = "{{: <{}s}} {{: <{}s}} {{}}".format(nId,nSd)
    print(disp.format("displayId","startDate","endDate"))
    for scene in scenes['results']:
        print("{} - {} - {}".format(scene["displayId"],scene["temporalCoverage"]["startDate"],scene["temporalCoverage"]["endDate"]))
