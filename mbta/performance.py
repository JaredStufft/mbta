"""
filename: mbta/performance.py
author: Jared Stufft, jared@stufft.us
desc: Contains wrapper around the MBTA performance API. Allows a pythonic approach to retrieving historic performance
data for MBTA travels.
"""

import mbta.response
import mbta.utils


class MBTAPerformanceAPI:
    
    HOST = 'http://realtime.mbta.com/developer/api/v2.1'
    DOCUMENTATION = 'https://cdn.mbta.com/sites/default/files/developers/2018-10-30-mbta-realtime-performance-api' \
                    '-documentation-version-0-9-5-public.pdf'
    API_KEY_ENV_VARIABLE = 'MBTA_PERFORMANCE_API_KEY'

    def __init__(self, api_key=None):

        self.params = {
            'format': 'json',
            'api_key': mbta.utils.authorize_api(api_key, self.API_KEY_ENV_VARIABLE)
        }

    def get_travel_times(self, from_datetime, to_datetime, from_stop, to_stop, route=None):
        
        """ get_travel_times
        
        Retrieve travel time between two given stations for a given date range
        
        INPUTS
        
        @from_datetime [str]: a string in YYYY-MM-DD format denoting the beginning of the time interval to search for.

        @to_datetime [str]: a string in YYYY-MM-DD format denoting the end of the time interval to search for.

        @from_stop [str]: The stop_id for the beginning of the travel. Can be found using `get_gtfs_utility_data`
            function from mbta.utils with 'stops.txt' file.

        @to_stop [str]: The stop_id for the end of the travel. Can be found using `get_gtfs_utility_data`
            function from mbta.utils with 'stops.txt' file.

        @route [str]: The route name for the travel. If not included, will return all travels between the stops.
        
        
        RETURNS
        
        @response [MBTAPerformanceResponse]: Response from the travel times API endpoint
        
        """

        params = {
            'from_datetime': mbta.utils.date_to_epoch(from_datetime),
            'to_datetime': mbta.utils.date_to_epoch(to_datetime),
            'from_stop': from_stop,
            'to_stop': to_stop
        }

        if route:
            params['route'] = route

        call_params = mbta.utils.merge_dicts(params, self.params)

        content, status_code = mbta.utils.make_api_call(self.HOST, ['traveltimes'], params=call_params)

        response = mbta.response.MBTAPerformanceResponse(content, status_code)
        
        return response

    def get_dwell_times(self, from_datetime, to_datetime, stop, route=None, direction=None):

        """ get_dwell_times

        Retrieve dwell time at a given station for a given date range

        INPUTS

        @from_datetime [str]: a string in YYYY-MM-DD format denoting the beginning of the time interval to search for.

        @to_datetime [str]: a string in YYYY-MM-DD format denoting the end of the time interval to search for.

        @stop [str]: The stop_id for the dwell time. Can be found using `get_gtfs_utility_data`
            function from mbta.utils with 'stops.txt' file.

        @route [str]: The route name for the travel. If not included, will return all travels between the stops.

        @direction [str]: The direction of travel during which the vehicle stopped.


        RETURNS

        @response [MBTAPerformanceResponse]: Response from the dwell times API endpoint

        """

        params = {
            'from_datetime': mbta.utils.date_to_epoch(from_datetime),
            'to_datetime': mbta.utils.date_to_epoch(to_datetime),
            'stop': stop
        }

        if route:
            params['route'] = route

        if direction:
            params['direction'] = direction

        call_params = mbta.utils.merge_dicts(params, self.params)

        content, status_code = mbta.utils.make_api_call(self.HOST, ['dwells'], params=call_params)

        response = mbta.response.MBTAPerformanceResponse(content, status_code)

        return response

    def get_headway_times(self, from_datetime, to_datetime, stop, to_stop=None, route=None):

        """ get_headway_times

        Retrieve headway time at a given station for a given date range

        INPUTS

        @from_datetime [str]: a string in YYYY-MM-DD format denoting the beginning of the time interval to search for.

        @to_datetime [str]: a string in YYYY-MM-DD format denoting the end of the time interval to search for.

        @stop [str]: The stop_id for the headway time. Can be found using `get_gtfs_utility_data`
            function from mbta.utils with 'stops.txt' file.

        @to_stop [str]: The stop_id for the end of the travel. Can be found using `get_gtfs_utility_data`
            function from mbta.utils with 'stops.txt' file.

        @route [str]: The route name for the travel. If not included, will return all travels between the stops.



        RETURNS

        @response [MBTAPerformanceResponse]: Response from the headways API endpoint

        """

        params = {
            'from_datetime': mbta.utils.date_to_epoch(from_datetime),
            'to_datetime': mbta.utils.date_to_epoch(to_datetime),
            'stop': stop
        }

        if route:
            params['route'] = route

        if to_stop:
            params['to_stop'] = to_stop

        call_params = mbta.utils.merge_dicts(params, self.params)

        content, status_code = mbta.utils.make_api_call(self.HOST, ['headways'], params=call_params)

        response = mbta.response.MBTAPerformanceResponse(content, status_code)

        return response

    def get_daily_metrics(self, from_datetime, to_datetime, route=None):

        """ get_daily_metrics

        Retrieve daily performance metrics for a given date range

        INPUTS

        @from_datetime [str]: a string in YYYY-MM-DD format denoting the beginning of the time interval to search for.

        @to_datetime [str]: a string in YYYY-MM-DD format denoting the end of the time interval to search for.

        @route [str]: The route name for the travel. If not included, will return all travels between the stops.



        RETURNS

        @response [MBTAPerformanceResponse]: Response from the daily metrics API endpoint

        """

        params = {
            'from_service_date': from_datetime,
            'to_service_date': to_datetime
        }

        if route:
            params['route'] = route

        call_params = mbta.utils.merge_dicts(params, self.params)

        content, status_code = mbta.utils.make_api_call(self.HOST, ['dailymetrics'], params=call_params)

        response = mbta.response.MBTAPerformanceResponse(content, status_code)

        return response

    def get_current_metrics(self, route=None):

        """ get_current_metrics

        Retrieve current performance metrics for a given date range

        INPUTS

        @route [str]: The route name for the travel. If not included, will return all travels between the stops.

        RETURNS

        @response [MBTAPerformanceResponse]: Response from the daily metrics API endpoint

        """

        params = {}

        if route:
            params['route'] = route

        call_params = mbta.utils.merge_dicts(params, self.params)

        content, status_code = mbta.utils.make_api_call(self.HOST, ['currentmetrics'], params=call_params)

        response = mbta.response.MBTAPerformanceResponse(content, status_code)

        return response

    def get_daily_prediction_metrics(self, from_datetime, to_datetime, route=None):

        """ get_daily_prediction_metrics

        Retrieve daily metrics for arrival predictions for a given date range

        INPUTS

        @from_datetime [str]: a string in YYYY-MM-DD format denoting the beginning of the time interval to search for.

        @to_datetime [str]: a string in YYYY-MM-DD format denoting the end of the time interval to search for.

        @route [str]: The route name for the travel. If not included, will return all travels between the stops.


        RETURNS

        @response [MBTAPerformanceResponse]: Response from the daily metrics API endpoint

        """

        params = {
            'from_service_date': from_datetime,
            'to_service_date': to_datetime
        }

        if route:
            params['route'] = route

        call_params = mbta.utils.merge_dicts(params, self.params)

        content, status_code = mbta.utils.make_api_call(self.HOST, ['dailypredictionmetrics'], params=call_params)

        response = mbta.response.MBTAPerformanceResponse(content, status_code)

        return response

    def get_prediction_metrics(self, from_datetime, to_datetime, stop=None, route=None, direction=None):

        """ get_prediction_metrics

        Get prediction metrics for a given time period aggregated by thirty minute slices

        @from_datetime [str]: a string in YYYY-MM-DD format denoting the beginning of the time interval to search for.

        @to_datetime [str]: a string in YYYY-MM-DD format denoting the end of the time interval to search for.

        @stop [str]: The stop_id for the dwell time. Can be found using `get_gtfs_utility_data`
            function from mbta.utils with 'stops.txt' file.

        @route [str]: The route name for the travel. If not included, will return all travels between the stops.

        @direction [str]: The direction of travel during which the vehicle stopped.


        RETURNS

        @response [MBTAPerformanceResponse]: Response from the daily metrics API endpoint

        """

        params = {
            'from_datetime': mbta.utils.date_to_epoch(from_datetime),
            'to_datetime': mbta.utils.date_to_epoch(to_datetime)
        }

        if route:
            params['route'] = route

        if direction:
            params['direction'] = direction

        if stop:
            params['stop'] = stop

        call_params = mbta.utils.merge_dicts(params, self.params)

        content, status_code = mbta.utils.make_api_call(self.HOST, ['predictionmetrics'], params=call_params)

        response = mbta.response.MBTAPerformanceResponse(content, status_code)

        return response

    def get_travel_events(self, from_datetime, to_datetime, vehicle_label=None, stop=None, route=None, direction=None):

        """ get_travel_events

        This query returns a list of arrival and departure events during the time period defined in the call.

        INPUTS

        @vehicle_label [str]: human-readable, publicly visible identifier for the vehicle

        @from_datetime [str]: a string in YYYY-MM-DD format denoting the beginning of the time interval to search for.

        @to_datetime [str]: a string in YYYY-MM-DD format denoting the end of the time interval to search for.

        @stop [str]: The stop_id for the dwell time. Can be found using `get_gtfs_utility_data`
            function from mbta.utils with 'stops.txt' file.

        @route [str]: The route name for the travel. If not included, will return all travels between the stops.

        @direction [str]: The direction of travel during which the vehicle stopped.


        RETURNS

        @response [MBTAPerformanceResponse]: Response from the daily metrics API endpoint

        """

        params = {
            'from_datetime': mbta.utils.date_to_epoch(from_datetime),
            'to_datetime': mbta.utils.date_to_epoch(to_datetime)
        }

        if vehicle_label:
            params['vehicle_label'] = vehicle_label

        if route:
            params['route'] = route

        if direction:
            params['direction'] = direction

        if stop:
            params['stop'] = stop

        call_params = mbta.utils.merge_dicts(params, self.params)

        content, status_code = mbta.utils.make_api_call(self.HOST, ['events'], params=call_params)

        response = mbta.response.MBTAPerformanceResponse(content, status_code)

        return response

    # TODO: Add this back in when there's time to parse the response.
    # def get_past_alerts(self, from_datetime, to_datetime, trip=None, stop=None, route=None):
    #
    #     """ get_past_alerts
    #
    #     This query returns a list of arrival and departure events during the time period defined in the call.
    #
    #     INPUTS
    #
    #     @vehicle_label [str]: human-readable, publicly visible identifier for the vehicle
    #
    #     @from_datetime [str]: a string in YYYY-MM-DD format denoting the beginning of the time interval to search for.
    #
    #     @to_datetime [str]: a string in YYYY-MM-DD format denoting the end of the time interval to search for.
    #
    #     @stop [str]: The stop_id for the dwell time. Can be found using `get_gtfs_utility_data`
    #         function from mbta.utils with 'stops.txt' file.
    #
    #     @route [str]: The route name for the travel. If not included, will return all travels between the stops.
    #
    #     @trip [str]: trip_id value for which alerts should be returned.
    #
    #
    #     RETURNS
    #
    #     @response [MBTAPerformanceResponse]: Response from the daily metrics API endpoint
    #
    #     """
    #
    #     params = {
    #         'from_datetime': mbta.utils.date_to_epoch(from_datetime),
    #         'to_datetime': mbta.utils.date_to_epoch(to_datetime)
    #     }
    #
    #     if trip:
    #         params['trip'] = trip
    #
    #     if route:
    #         params['route'] = route
    #
    #     if stop:
    #         params['stop'] = stop
    #
    #     call_params = mbta.utils.merge_dicts(params, self.params)
    #
    #     content, status_code = mbta.utils.make_api_call(self.HOST, ['pastalerts'], params=call_params)
    #
    #     response = mbta.response.MBTAPerformanceResponse(content, status_code)
    #
    #     return response
