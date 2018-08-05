# -*- coding: utf-8 -*-

import json
import datetime as dt
import time


class Response:

    """ Response
    
    Base class for responses from MBTA APIs
    
    """
    
    def __init__(self, raw_response):
        
        self.raw_response = json.loads(raw_response)
        self.data_as_of = dt.datetime.now()
        self.columns = ()

    @staticmethod
    def _strip_first_layer_of_dict(data):

        """ _strip_first_layer_of_dict

        MBTA responses come in a nested dictionary with one initial key. This will strip
        the first layer away to get a list of dictionaries.

        INPUTS

        data [dict]: Single dictionary. This will remove the first layer.


        RETURNS

        data_list [list of dicts]: List of subsequent data.

        """

        key = list(sorted(data.keys()))[0]

        data_list = data[key]

        return data_list

    @property
    def data_list(self):

        """ data_list

        List of single-point dictionaries.

        """

        data_list = self._strip_first_layer_of_dict(self.raw_response)

        return data_list

    @property
    def tuples(self):
        """ tuples

        Data parsed into a list of tuples

        """

        tuples = []

        for data_point in self.data_list:

            # Sorts the each data point according to the column order in
            # self.columns, converts first to a list, then a tuple for faster processing later.
            tuple_ = tuple([value for key, value in sorted(data_point.items(), key=lambda i:self.columns.index(i[0]))])
            tuples.append(tuple_)

        return tuples

    @staticmethod
    def _epoch_to_datetime(epoch):

        """ _epoch_to_datetime

        Converts an integer epoch timestamp into a datetime string.

        INPUTS

        epoch [int]: Integer timestamp to convert to a datetime string.


        RETURNS

        date [str]: Converted datetime string in YYYy-MM-DD HH:MM:SS format.

        """

        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch))

        return date


class MBTAPerformanceResponse(Response):
    
    """ MBTAPerformanceResponse
    
    Response class for the MBTA Performance API call results
    
    """
    
    def __init__(self, raw_response):

        self.data_type = 'Travel Times'
        self.columns = (
            'arr_dt', 'benchmark_travel_time_sec',
            'dept_dt', 'direction',
            'route_id', 'travel_time_sec'
        )
        super().__init__(raw_response=raw_response)


