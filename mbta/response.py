# -*- coding: utf-8 -*-

import json
import datetime as dt


class Response:

    """ Response
    
    Base class for responses from MBTA APIs
    
    """
    
    def __init__(self, raw_response, status_code):
        
        self.raw_response = json.loads(raw_response)
        self.data_as_of = dt.datetime.now()
        self.status_code = status_code
        self._set_data_type_data_list()

        # In response type : (response columns) format
        self.column_map = {'travel_times': ('arr_dt', 'benchmark_travel_time_sec',
                                            'dep_dt', 'direction',
                                            'route_id', 'travel_time_sec'
                                            )
                           }

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

        return data_list, key

    @property
    def columns(self):

        """ columns
        column names in order for the response.

        """

        return self.column_map[self.data_type]

    def _set_data_type_data_list(self):

        """ _set_data_type_data_list

        Sets the data type and data list based on the raw response key and contents.

        """

        data_list_, data_type_ = self._strip_first_layer_of_dict(self.raw_response)

        self.data_list = data_list_
        self.data_type = data_type_

        return

    @property
    def tuples(self):

        """ tuples

        Data parsed into a list of tuples

        """

        tuples = []

        for data_point in self.data_list:

            # Sorts the each data point according to the column order in
            # self.columns, converts first to a list, then a tuple for faster processing later.
            tuple_ = tuple([data_point[key] for key in self.columns])
            tuples.append(tuple_)

        return tuples


class MBTAPerformanceResponse(Response):
    
    """ MBTAPerformanceResponse
    
    Response class for the MBTA Performance API call results
    
    """
    
    def __init__(self, raw_response, status_code):

        super().__init__(raw_response=raw_response, status_code=status_code)
