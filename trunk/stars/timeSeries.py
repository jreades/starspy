import numpy
import pysal

class TimeSeries(object):
    """
    Models a Stars Time Series.

    Time Series are STATIC (for now) aggregations of events over space and time.
    """
    def __init__(self, y_by_t, meta):
        self.__k = 5
        self.__k_method = pysal.esda.mapclassify.Natural_Breaks
        self.y_by_t = y_by_t
        self.meta = meta
        self.i, self.j = y_by_t.shape
        self._t = self.j-1 # default to last time period
        self.__cl_by_t = None
        #self.eventLayer = None
        self.regionLayer = None
    @property
    def cl_by_t(self):
        if not self.__cl_by_t:
            cl = [0 for x in range(self.j)]
            for j in range(self.j):
                print "classify:",j
                cl[j] = self.k_method(self.y_by_t[:, j], self.k)
            self.__cl_by_t = cl
        return self.__cl_by_t

    def __set_k_method(self, value):
        self.__k_method = value
        self.__cl_by_t = None
    def __get_k_method(self):
        return self.__k_method
    k_method = property(__get_k_method, __set_k_method)
    def __set_k(self,value):
        self.__k = value
        self.__cl_by_t = None
    def __get_k(self):
        return self.__k
    k = property(__get_k, __set_k)

    def __set_t(self, value):
        if value >= 0 and value < self.j:
            self._t = value
            self.update_layers()
    def __get_t(self):
        return self.meta[self._t]
    t = property(__get_t, __set_t)

    def update_layers(self):
        if self.regionLayer:
            self.regionLayer.classification = self.cl_by_t[self._t]

if __name__ == '__main__':
    from data_manager import StarsDatabase
    db = StarsDatabase("test.starsdb")
    regions = db.region_tables[0]
    y_by_t, meta = regions.event_count_by_period()
    ts = TimeSeries(y_by_t,meta)


