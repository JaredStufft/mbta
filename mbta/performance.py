# -*- coding: utf-8 -*-
import requests
import time
import json
import os
from mbta.response import MBTAPerformanceResponse


class MBTAPerformance:
    
    host = 'http://realtime.mbta.com/developer/api/v2.1'
    params = {'response_format': 'json'}

    def __init__(self, api_key=None):
        
        self.params['api_key'] = self.authorize_api(api_key)

    @staticmethod
    def authorize_api(api_key):

        """ authorize_api

        Checks if the user provided an API key during class instance
        creation. If none found, searches for environment variable
        `MBTA_PERFORMANCE_API_KEY`.

        INPUTS

        @api_key [str]: Key for MBTA Performance API, to be received
        from the class instance created if used.


        RETURNS

        @valid_api_key [str]: The proper API key for the performance API.

        """

        if not api_key:

            valid_api_key = os.getenv('MBTA_PERFORMANCE_API_KEY')

            return valid_api_key

        valid_api_key = api_key

        return valid_api_key

    @staticmethod
    def _date_to_epoch(date):
        
        """ date_to_epoch
        
        Takes a string in format YYYY-MM-DD and converts to epoch time
        
        INPUTS
        
        @date [str]: Date string in format YYYY-MM-DD
        
        
        RETURNS
        
        @epoch [int]: Integer value representing date in epoch format
        
        """
        
        epoch = int(time.mktime(time.strptime(date, '%Y-%m-%d')))
        
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
    
        response = MBTAPerformanceResponse(r.content)
        
        return response

    def get_travel_times(self, from_datetime, to_datetime, from_stop, to_stop):
        
        """ get_travel_times
        
        Retrieve travel time between two given stations for a given date range
        
        INPUTS
        
        @from_datetime [str]:

        @to_datetime [str]:

        @from_stop [str]:

        @to_stop [str]:
        
        
        RETURNS
        
        @response [MBTAPerformanceResponse]: Response from the travel times API endpoint
        
        """

        params = {
            'from_datetime': self._date_to_epoch(from_datetime),
            'to_datetime': self._date_to_epoch(to_datetime),
            'from_stop': from_stop,
            'to_stop': to_stop
        }

        response = self._make_api_call('traveltimes', params=params)
        
        return response
