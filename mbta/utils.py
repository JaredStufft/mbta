"""
filename: mbta/utils.py.py
author: Jared Stufft, jared@stufft.us
desc: Allows for access to some helper data and functions.
"""

import requests
import os
import datetime as dt
from zipfile import ZipFile
from io import BytesIO
import time


GTFS_CONTENT_URL = r'https://cdn.mbta.com/MBTA_GTFS.zip'


def get_gtfs_utility_data(file_name):

    """ get_gtfs_utility_data

    Retrieves the utility data for the GTFS network specific to the MBTA API. This contains things like stop_ids
    for other parts of the API. This content changes over time, so this function should allow the user to always
    have the latest distribution.

    INPUTS

    @file_name [str]: the file name for the utility data the user wishes to retrieve. The content comes as a zip
    file, so this chooses which piece of the zip to return.

    """

    r = requests.get(GTFS_CONTENT_URL)

    with ZipFile(BytesIO(r.content)) as zip_file:
        with zip_file.open(file_name) as stops_file:
            lines = stops_file.readlines()

    return lines


def date_to_epoch(date):

    """ date_to_epoch

    Takes a string in format YYYY-MM-DD and converts to epoch time

    INPUTS

    @date [str]: Date string in format YYYY-MM-DD


    RETURNS

    @epoch [int]: Integer value representing date in epoch format

    """

    epoch = int(time.mktime(time.strptime(date, '%Y-%m-%d')))

    return epoch


def epoch_to_datetime(epoch):

    """ _epoch_to_datetime

    Converts an integer epoch timestamp into a datetime string.

    INPUTS

    epoch [int]: Integer timestamp to convert to a datetime string.


    RETURNS

    date [datetime]: Converted datetime in YYYy-MM-DD HH:MM:SS format.

    """

    return dt.datetime.strptime(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(epoch))), '%Y-%m-%d %H:%M:%S')


def date_string_to_datetime(date_string):
    return dt.datetime.strptime(date_string, '%Y-%m-%d')


def create_api_host_url(host, endpoints):

    """ create_api_host_url

    Creates the endpoint url for the API call.

    INPUTS

    @host [str]: The base URL for the API call.

    @endpoints [list]: The API endpoint names for the chosen method

    RETURNS

    @api_url [str]: The full endpoint url for the method.

    """

    api_url = '/'.join((host, *endpoints))

    return api_url


def merge_dicts(dict1, dict2):

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


def make_api_call(host, endpoints, params):

    """ _make_api_call

    Base method for any API call.

    INPUTS

    @params [dict]: dictionary of API call parameters

    @endpoint [str]: the API method being used


    RETURNS

    @response [Response]: The response for the API call

    """

    call_url = create_api_host_url(host, endpoints)

    r = requests.get(call_url, params=params)

    r.raise_for_status()  # HTTPError if 4XX or 5XX status code on response.

    return r.content, r.status_code


def authorize_api(api_key, api_key_env):

    """ authorize_api

    Checks if the user provided an API key during class instance
    creation. If none found, searches for named environment variable.

    INPUTS

    @api_key [str]: Key for the particular API, to be received
    from the class instance created if used.


    RETURNS

    @valid_api_key [str]: The proper API key for the given API.

    """

    if not api_key:

        valid_api_key = os.getenv(api_key_env)

        return valid_api_key

    valid_api_key = api_key

    return valid_api_key
