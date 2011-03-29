from visualization.model import *

class StarsProject(object):
    """Stars Project Class...
    
    See alternate definition in stars.py
    """
    def __init__(self, fname=None):
        if fname:
            if not self.open(fname):
                self.new(fname)
        else:
            self.new()
    def open(self, fname):
        return False
    def new(self, fname=None):
        pass
    def add_data_source(self, connector):
        pass
class StarsDataSrouce(object):
    """ Abstract class representing a Stars Data Srouce

        Subclasses are data sources that stars understands.
    """
    def __init__(self, connector):
        if issubclass(type(connector),basestring):
            #parse the connection string
            obj = pysal.open(connector)
        self._has_space = False
        self._has_time = False
        self._has_attributes = False
        self._temporal_model = None
    @property
    def provides_space(self):
        """ bool -- True if this data source provides a spatial dimmension """
        return self._has_space
    @property
    def provides_time(self):
        """ bool -- True if this data source provides a temporal dimmension
            Check time_model for imformation about the time functionality.
        """
        return self._has_time
    @property
    def time_model(self):
        """ string -- Returns the type of time this data source provide or None.
        
            Currently Available types are,
            "seqential" -- [t0, t1, t2], each period may be labeled.
            "date events" -- Events each with a given date.
            "datetime events" -- Events each with a given date and time.
        """
    @property
    def provides_attributes(self):
        """ bool -- True if this data source provides a attribute data """
        return self._has_attributes
    
