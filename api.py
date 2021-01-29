import requests
import json
import os.path as osp
from getpass import getpass

from filters import Filter

M2M_ENDPOINT = 'https://m2m.cr.usgs.gov/api/api/json/{}'

class M2MError(Exception):
    """
    Raised when an M2M gets an error.
    """
    pass

class M2M(object):
    """M2M EarthExplorer API."""

    def __init__(self, username, password=None, version="stable"):
        self.apiKey = None
        self.username = username
        self.serviceUrl = M2M_ENDPOINT.format(version)
        self.login(password)
        allDatasets = self.sendRequest('dataset-search')
        self.datasetNames = [dataset['datasetAlias'] for dataset in allDatasets]
        self.datasetIds = [dataset['datasetId'] for dataset in allDatasets]

    def sendRequest(self, endpoint, data=None):
        url = osp.join(self.serviceUrl, endpoint)
        json_data = json.dumps(data)
        if self.apiKey == None:
            response = requests.post(url, json_data)
        else:
            headers = {'X-Auth-Token': self.apiKey}              
            response = requests.post(url, json_data, headers = headers)    
        if response == None:
            raise M2MError("No output from service")
        status = response.status_code 
        output = json.loads(response.text)  
        if status != 200:
            msg = "{} - {} - {}".format(status,output['errorCode'],output['errorMessage'])
            raise M2MError(msg)
        elif output['data'] is None and endpoint != 'logout':
            msg = "{} - {}".format(output['errorCode'],output['errorMessage'])
            raise M2MError(msg)
        response.close()
        return output['data']

    def login(self, password=None):
        if password is None:
            password = getpass()
        loginParameters = {'username' : self.username, 'password' : password}
        self.apiKey = self.sendRequest('login',loginParameters)

    def searchDatasets(self, **args):
        args['processList'] = ['datasetName','acquisitionFilter','spatialFilter']
        params = Filter(args)
        return self.sendRequest('dataset-search', params)

    def searchScenes(self, datasetName, **args):
        if datasetName not in self.datasetNames:
            raise M2MError("Dataset {} not one of the available datasets {}".format(datasetName,self.datasetNames))
        args['datasetName'] = datasetName
        args['processList'] = ['datasetName','sceneFilter','maxResults']
        params = Filter(args)
        return self.sendRequest('scene-search', params)

    def logout(self):
        r = self.sendRequest('logout')
        if r != None:
            raise M2MError("Not able to logout")
        self.apiKey = None

    def __exit__(self):
        self.logout()
