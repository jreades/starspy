from collections import defaultdict

class MetaData(defaultdict):
    """
    MetaData is a simple default dict
    If the MetaData objection does not contain the requested key an empty string a returned.

    It also supports getting and setting keys as attributes.

    eg.
    >>> meta = MetaData()
    >>> meta['label'] = "A Label"
    >>> meta.label
    "A Label"
    """
    def __init__(self,d={}):
        defaultdict.__init__(self,str)
        self.update(d)
    def __getattr__(self,key):
        return self[key]
    def __setattr__(self,key,value):
        self[key] = value
        
