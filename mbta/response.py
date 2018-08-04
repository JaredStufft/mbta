# -*- coding: utf-8 -*-

import json


class Response:

    """ Response
    
    Base class for responses from MBTA APIs
    
    """
    
    def __init__(self, raw_response):
        
        self.raw_response = json.loads(raw_response)

    @property
    def dataframe(self):
        
        return 'pass'

    def parse_response(self):
        
        pass
    
    
class MBTAPerformanceResponse(Response):
    
    """ MBTAPerformanceResponse
    
    Response class for the MBTA Performance API call results
    
    """
    
    def __init__(self, raw_response):
        
        super().__init__(raw_response=raw_response)
