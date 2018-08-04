# -*- coding: utf-8 -*-

import json


class Response:

    """ Response
    
    Base class for responses from MBTA APIs
    
    """
    
    def __init__(self, data):
        
        self.raw_data = json.loads(data)

    @property
    def dataframe(self):
        
        return 'pass'

    def parse_response(self):
        
        pass
    
    
class MBTAPerformanceResponse(Response):
    
    """ MBTAPerformanceResponse
    
    Response class for the MBTA Performance API call results
    
    """
    
    def __init__(self):
        
        super().__init__()
