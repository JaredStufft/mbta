# -*- coding: utf-8 -*-


class Response:

    """ Response
    
    Base class for responses from MBTA APIs
    
    """
    
    def __init__(self, data):
        
        pass

    @property
    def raw_data(self):
        
        return 'pass'

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
