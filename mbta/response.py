import json
import datetime as dt
import mbta.utils


class Response:

    """ Response
    
    Base class for responses from MBTA APIs
    
    """

    # In response type : (response columns) format
    column_map = dict()

    prettify_functions = dict()
    
    def __init__(self, raw_response, status_code):
        
        self.raw_response = json.loads(raw_response)
        self.data_as_of = dt.datetime.now()
        self.status_code = status_code
        self._set_data_type_data_list()

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

    @property
    def pretty_tuples(self):

        """ pretty_tuples

        Data parsed into a list of tuples with prettify'd responses

        """

        tuples = []

        for data_point in self.data_list:
            # Sorts the each data point according to the column order in
            # self.columns, converts first to a list, then a tuple for faster processing later.
            tuple_ = tuple([self.prettify_response(key, data_point[key]) for key in self.columns])
            tuples.append(tuple_)

        return tuples

    def prettify_response(self, column_name, data_point):

        """ prettify_response

        Converts individual data points into something prettier, such as converting epoch timestamps to datetimes.

        INPUTS

        @column_name [str]: The column name to convert. Used to find the correct rule.

        @data_point [various]: The data point to convert.

        """

        transform_func = self.prettify_functions.get(column_name)

        if transform_func:
            return transform_func(data_point)

        return data_point


class MBTAPerformanceResponse(Response):
    
    """ MBTAPerformanceResponse
    
    Response class for the MBTA Performance API call results
    
    """

    # In response type : (response columns) format
    column_map = {'travel_times': ('arr_dt', 'dep_dt', 'travel_time_sec', 'benchmark_travel_time_sec', 'direction',
                                   'route_id'
                                   ),

                  'dwell_times': ('arr_dt', 'dep_dt', 'dwell_time_sec', 'direction', 'route_id')
                  }

    prettify_functions = {
        'dep_dt': mbta.utils.epoch_to_datetime,
        'arr_dt': mbta.utils.epoch_to_datetime,
        'travel_time_sec': int,
        'benchmark_travel_time_sec': int,
    }
    
    def __init__(self, raw_response, status_code):

        super().__init__(raw_response=raw_response, status_code=status_code)
