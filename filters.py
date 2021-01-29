import time

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
                startDate = args.get('startDate',None)
                endDate = args.get('endDate',None)
                params.update(self.temporalFilter(startDate,endDate))
            elif elem == 'acquisitionFilter':
                startDate = args.get('startDate',None)
                endDate = args.get('endDate',None)
                params.update(self.acquisitionFilter(startDate,endDate))
            elif elem == 'spatialFilter':
                bbox = args.get('bbox',None)
                params.update(self.spatialFilter(bbox))
            elif elem == 'sceneFilter':
                startDate = args.get('startDate',None)
                endDate = args.get('endDate',None)
                bbox = args.get('bbox',None)
                params.update(self.sceneFilter(startDate,endDate,bbox))
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
    def spatialFilter(bbox):
        if bbox is None:
            return {}
        return {
            'spatialFilter': {
                'filterType': "mbr",
                'lowerLeft': {
                    'latitude': bbox[2], 
                    'longitude': bbox[0]
                },
                'upperRight': {
                    'latitude': bbox[3], 
                    'longitude': bbox[1]
                }
            }
        }

    @staticmethod
    def acquisitionFilter(startDate,endDate):
        startDate,endDate = dateCorrection(startDate,endDate)
        return {
            'acquisitionFilter': {
                'start': startDate, 
                'end': endDate
            }
        }

    def sceneFilter(self,startDate,endDate,bbox):
        sceneFilter = {}
        sceneFilter.update(self.acquisitionFilter(startDate,endDate))
        sceneFilter.update(self.spatialFilter(bbox))
        return {
            'sceneFilter': sceneFilter
        }