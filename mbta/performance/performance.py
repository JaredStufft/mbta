# -*- coding: utf-8 -*-
import requests
import time
import json
import os


class MBTAPerformance:
    
    host = 'http://realtime.mbta.com/developer/api/v2.1'
    params = {'response_format' : 'json'}
    
    
    def __init__(self, api_key):
        
        self.api_key = api_key
        
    
    @staticmethod
    def _date_to_epoch(date):
        
        """ date_to_epoch
        
        Takes a string in format YYYY-MM-DD and converts to epoch time
        
        INPUTS
        
        @date [str]: Date string in format YYYY-MM-DD
        
        
        RETURNS
        
        @epoch [int]: Integer value representing date in epoch format
        
        """
        
        epoch = int(time.mktime(time.strptime(date), '%Y-%m-%d'))
        
        return epoch
    
    
    def _create_api_host_url(self, endpoint):
        
        """ _create_api_host_url
        
        Creates the endpoint url for the API call.
        
        INPUTS
        
        @endpoint [str]: The API endpoint name for the chosen method
        
        
        RETURNS
        
        @api_url [str]: The full endpoint url for the method.
        
        """
        
        api_url = os.path.join(self.host, endpoint)
        
        return api_url
    
    
    @staticmethod
    def _merge_dicts(dict1, dict2):
        
        """ _merge_dicts
        
        Merges two dictionaries into one.
        
        INPUTS
        
        @dict1 [dict]: First dictionary to merge.
        
        @dict2 [dict]: Second dictionary to merge.
        
        
        RETURNS
        
        @merged [dict]: Merged dictionary
        
        """
        
        merged = {**dict1, **dict2}
        
        return merged
    
    
    def _make_api_call(self, endpoint, params):
        
        """ _make_api_call
        
        Base method for any API call.
        
        INPUTS
        
        @params [dict]: dictionary of API call parameters
        
        @endpoint [str]: the API method being used
        
        
        RETURNS
        
        @response [Response]: The response for the API call
        
        """
        
        call_params = self._merge_dicts(self.params, params)
        
        call_url = self._create_api_host_url(endpoint)
        
        r = requests.get(call_url, params=call_params)
    
        response = json.loads(r.content) #TODO: Add in response class for easier parsing
        
        return response
    
    
    def get_travel_times(self, params):
        
        """ get_travel_times
        
        Retrieve travel time between two given stations for a given date range
        
        INPUTS
        
        @params [dict]: Dictionary of API call parameters
        
        
        RETURNS
        
        @response
        
        """
        
        #TODO: Add call to travel times library
        
        pass
    
    
        