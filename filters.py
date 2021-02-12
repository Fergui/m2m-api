import time
import json
import os.path as osp

def dateCorrection(startDate,endDate):
    if startDate is None:
        startDate = '2000-01-01'
    if endDate is None:
        endDate = time.strftime('%Y-%m-%d')
    return startDate,endDate

class FilterError(Exception):
    """
    Raised when a Filter gets an error.
    """
    pass

class Filter(dict):
    def __init__(self, args):
        params = self.processParams(args)
        super(Filter, self).__init__(params)

    def processParams(self,args):
        processList = args.get('processList',[])
        params = {}
        for elem in processList:
            if elem == 'maxResults':
                maxResults = args.get(elem,None)
                params.update(self.maxResults(maxResults))
            elif elem == 'datasetName':
                datasetName = args.get(elem,None)
                params.update(self.datasetName(datasetName))
            elif elem == 'datasetId':
                datasetId = args.get(elem,None)
                params.update(self.datasetId(datasetId))
            elif elem == 'temporalFilter':  
                kargs = {
                    'startDate': args.get('startDate',None),
                    'endDate': args.get('endDate',None)
                }
                params.update(self.temporalFilter(**kargs))
            elif elem == 'acquisitionFilter':
                kargs = {
                    'startDate': args.get('startDate',None),
                    'endDate': args.get('endDate',None)
                }
                params.update(self.acquisitionFilter(**kargs))
            elif elem == 'spatialFilter':
                kargs = {
                    'boundingBox': args.get('boundingBox',None),
                    'geoJsonType': args.get('geoJsonType',None),
                    'geoJsonCoords': args.get('geoJsonCoords',None),
                    'geoJsonPath': args.get('geoJsonPath',None)
                }
                params.update(self.spatialFilter(**kargs))
            elif elem == 'sceneFilter':
                kargs = {
                    'startDate': args.get('startDate',None),
                    'endDate': args.get('endDate',None),
                    'boundingBox': args.get('boundingBox',None),
                    'geoJsonType': args.get('geoJsonType',None),
                    'geoJsonCoords': args.get('geoJsonCoords',None),
                    'geoJsonPath': args.get('geoJsonPath',None),
                    'minCC': args.get('minCC',None),
                    'maxCC': args.get('maxCC',None),
                    'includeUnknownCC': args.get('includeUnknownCC',None),
                    'metadataInfo': args.get('metadataInfo',{}),
                    'datasetFilters': args.get('datasetFilters',[])
                }
                params.update(self.sceneFilter(**kargs))
        return params

    @staticmethod
    def maxResults(maxResults):
        if maxResults is None:
            return {}
        return {
            'maxResults': maxResults
        }

    @staticmethod
    def datasetName(datasetName):
        if datasetName is None:
            return {}
        return {
            'datasetName': datasetName
        }

    @staticmethod
    def datasetId(datasetId):
        if datasetId is None:
            return {}
        return {
            'datasetName': datasetId
        }

    @staticmethod
    def temporalFilter(startDate, endDate):
        startDate,endDate = dateCorrection(startDate,endDate)
        return {
            'temporalFilter': {
                'start': startDate, 
                'end': endDate
            }
        }

    @staticmethod
    def spatialFilter(boundingBox,geoJsonType,geoJsonCoords,geoJsonPath):
        if geoJsonPath is None:
            if geoJsonType is None:
                if boundingBox is None:
                    spatialFilter = {}
                else:
                    spatialFilter = {
                        'filterType': "mbr",
                        'lowerLeft': {
                            'latitude': boundingBox[2], 
                            'longitude': boundingBox[0]
                        },
                        'upperRight': {
                            'latitude': boundingBox[3], 
                            'longitude': boundingBox[1]
                        }
                    }
            else:
                spatialFilter = {
                    'filterType': "geojson",
                    'geoJson': {
                        'type': geoJsonType,
                        'coordinates': geoJsonCoords
                    }
                }
        else:
            spatialFilter = {
                'filterType': "geojson",
                'geoJson': json.load(open(osp.join(osp.dirname(__file__),geoJsonPath),'r'))
            }

        if len(spatialFilter):
            return {
                'spatialFilter': spatialFilter
            }
        else:
            return {}

    @staticmethod
    def acquisitionFilter(startDate,endDate):
        startDate,endDate = dateCorrection(startDate,endDate)
        return {
            'acquisitionFilter': {
                'start': startDate, 
                'end': endDate
            }
        }

    @staticmethod
    def cloudCoverFilter(minCC,maxCC,includeUnknownCC):
        cloudCoverFilter = {}
        if minCC is not None:
            cloudCoverFilter.update({'min': minCC})
        if maxCC is not None:
            cloudCoverFilter.update({'max': maxCC})
        if includeUnknownCC is not None:
            cloudCoverFilter.update({'includeUnknown': includeUnknownCC})
        if len(cloudCoverFilter):
            return {
                'cloudCoverFilter': cloudCoverFilter
            }
        else:
            return {}

    @staticmethod
    def metadataFilter(datasetFilters,metadataInfo):
        if len(metadataInfo): 
            if 'and' in metadataInfo and len(metadataInfo['and']): 
                metadataInfo = metadataInfo['and']
                metadataFilter = {
                    'filterType': 'and'
                } 
            elif 'or' in metadataInfo and len(metadataInfo['or']):
                metadataInfo = metadataInfo['or']
                metadataFilter = {
                    'filterType': 'or'
                }
            else:
                return {}
            metadataFilter.update({'childFilters': []})
            for metaName,metaType,metaValue in metadataInfo:
                metaInfo = [df for df in datasetFilters if df['fieldLabel'] == metaName][0]
                childFilter = {
                    'filterId': metaInfo['id'],
                    'filterType': metaType,
                }
                if metaType == 'value':
                    childFilter.update({'value': metaValue, 
                                        'operand': '='})
                elif metaType == 'between':
                    childFilter.update({'firstValue': metaValue[0], 
                                        'secondValue': metaValue[1]})
                metadataFilter['childFilters'].append(childFilter)
            return {
                'metadataFilter': metadataFilter
            }
        else:
            return {}

    def sceneFilter(self,startDate,endDate,boundingBox,geoJsonType,geoJsonCoords,geoJsonPath,minCC,maxCC,includeUnknownCC,metadataInfo,datasetFilters):
        sceneFilter = {}
        sceneFilter.update(self.acquisitionFilter(startDate,endDate))
        sceneFilter.update(self.cloudCoverFilter(minCC,maxCC,includeUnknownCC))
        sceneFilter.update(self.spatialFilter(boundingBox,geoJsonType,geoJsonCoords,geoJsonPath))
        sceneFilter.update(self.metadataFilter(datasetFilters,metadataInfo))

        return {
            'sceneFilter': sceneFilter
        }

