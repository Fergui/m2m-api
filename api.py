import logging
import requests
import json
import random
import time
import os.path as osp
from getpass import getpass

from .filters import Filter

M2M_ENDPOINT = 'https://m2m.cr.usgs.gov/api/api/json/{}'

class M2MError(Exception):
    """
    Raised when an M2M gets an error.
    """
    pass

class M2M(object):
    """M2M EarthExplorer API."""

    def __init__(self, username=None, password=None, version="stable"):
        self.apiKey = None
        if username is None:
            username = input("Enter your username (or email): ")
        self.username = username
        self.serviceUrl = M2M_ENDPOINT.format(version)
        self.login(password)
        allDatasets = self.sendRequest('dataset-search')
        self.datasetNames = [dataset['datasetAlias'] for dataset in allDatasets]
        self.permissions = self.sendRequest('permissions')

    def sendRequest(self, endpoint, data={}, max_retries=5):
        url = osp.join(self.serviceUrl, endpoint)
        logging.info('sendRequest - url = {}'.format(url))
        json_data = json.dumps(data)
        if self.apiKey == None:
            response = retry_connect(url, json_data, max_retries=max_retries)
        else:
            headers = {'X-Auth-Token': self.apiKey}   
            response = retry_connect(url, json_data, headers=headers, max_retries=max_retries)
        if response == None:
            raise M2MError("No output from service")
        status = response.status_code 
        try:
            output = json.loads(response.text)
        except:
            output = response.text
        if status != 200:
            if isinstance(output,dict):
                msg = "{} - {} - {}".format(status,output['errorCode'],output['errorMessage'])
            else:
                msg = "{} - {}".format(status,output)
            raise M2MError(msg)
        else:
            if isinstance(output,dict): 
                if output['data'] is None and output['errorCode'] is not None and endpoint != 'logout':
                    msg = "{} - {}".format(output['errorCode'],output['errorMessage'])
                    raise M2MError(msg)
            else:
                msg = "{} - {}".format(status,output)
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

    def datasetFilters(self, **args):
        args['processList'] = ['datasetName']
        params = Filter(args)
        return self.sendRequest('dataset-filters', params)

    def searchScenes(self, datasetName, **args):
        if datasetName not in self.datasetNames:
            raise M2MError("Dataset {} not one of the available datasets {}".format(datasetName,self.datasetNames))
        args['datasetName'] = datasetName
        if 'metadataInfo' in args and len(args['metadataInfo']):
            args['datasetFilters'] = self.datasetFilters(**args)
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

def retry_connect(url, json_data, headers={}, max_retries=5, sleep_seconds=1):
    retries = 0
    while retries < max_retries:
        try:
            response = requests.post(url, json_data, headers=headers, timeout=5)
        except:
            retries += 1
            logging.info('Connection Timeout - retry number {} of {}'.format(retries,max_retries))
            sec = random.random() * sleep_seconds
            time.sleep(sec)
        else:
            return response
    raise M2MError("Maximum retries exceeded")
