import wx
import pysal
import colors
from model import AbstractModel
from kernelDensityTime import KernelDensity
import random
def rcolor():
    randint = random.randint
    return randint(0,255), randint(0,255), randint(0,255)

class SqlDBF(object):
    """
    Helper Class for Sqlite tables, not really a layer.

    TODO: Move this.

    Example:
    >>> db = SqlDBF(table)
    >>> len(db)
    60
    >>> db[:5]
    [0, 1, 2, 3, 4]
    """
    def __init__(self,table):
        self.table = table
        self.n = table.meta['n']
        self.header = table.meta['header']
        self.field_spec = [table.meta['spec'][key] for key in self.header]
    def __len__(self):
        return self.n
    def __getitem__(self,key):
        if issubclass(type(key), basestring):
            raise TypeError, "index should be int or slice"
        if issubclass(type(key), int) or isinstance(key, slice):
            rows = key
            cols = None
        elif len(key) > 2:
            raise TypeError, "DataTables support two dimmensional slicing,  % d slices provided"    % len(key)
        elif len(key) == 2:
            rows, cols = key
        else:
            raise TypeError, "Key: % r,  is confusing me.  I don't know what to do"% key
        if isinstance(rows, slice):
            row_start, row_stop, row_step = rows.indices(len(self))
            data = self.table.rows()[row_start, row_stop, row_step]
        else:
            data = self.table.rows()[ slice(rows).indices(len(self))[1] ]
        if cols is not None:
            if isinstance(cols, slice):
                col_start, col_stop, col_step = cols.indices(len(data[0]))
                data = [r[col_start:col_stop:col_step] for r in data]
            else:
                #col_start, col_stop, col_step = cols, cols+1, 1
                data = [r[cols] for r in data]
        return data

    
class NullDBF(object):
    """
    Helper Class for Shapefiles with No DBF, not really a layer.

    TODO: Move this.

    Example:
    >>> db = NullDBF(60)
    >>> len(db)
    60
    >>> db[:5]
    [0, 1, 2, 3, 4]

    """
    def __init__(self,n):
        self.n = n
    @property
    def header(self):
        return ["ID"]
    @property
    def field_spec(self):
        return [('N',len(str(self.n)),0)]
    def __len__(self):
        return self.n
    def __getitem__(self,key):
        if issubclass(type(key), basestring):
            raise TypeError, "index should be int or slice"
        if issubclass(type(key), int) or isinstance(key, slice):
            rows = key 
            cols = None
        elif len(key) > 2:
            raise TypeError, "DataTables support two dimmensional slicing,  % d slices provided"% len(key)
        elif len(key) == 2:
            rows, cols = key 
        else:
            raise TypeError, "Key: % r,  is confusing me.  I don't know what to do"% key 
        if isinstance(rows, slice):
            row_start, row_stop, row_step = rows.indices(len(self))
            if row_stop >= self.n:
                row_stop = self.n
            return range(row_start,row_stop,row_step)
        else:
            if rows >= self.n:
                rows = self.n
            return [rows]

class BaseLayer(AbstractModel):
    """
    Represents a Basic Layer
    All other layers must inheret from BaseLayer

    Layers might be usable outside of just mapping.
    E.g. scatter plots are just PointLayers?
    """
    def __init__(self):
        AbstractModel.__init__(self)
        self._data = {'type':'BaseLayer', 'extent':pysal.cg.Rectangle(0,0,0,0), 'selection':set(),
                        'data':None, 'selectable':False, 'classification':None, 'colors':colors.ColorScheme([rcolor()]), 'name':''}
        self._locator = None
    def __len__(self):
        d = self.data
        if d:
            return len(d)
        else:
            return 0
    @property
    def locator(self):
        return self._locator
    @property
    def extent(self):
        return self._data['extent']
    @property
    def type(self):
        return self._data['type']
    def __get_data(self):
        return self._data['data']
    def __set_data(self,val):
        self._data['data'] = val
        self.update('data')
    data = property(fget=__get_data,fset=__set_data)
    def __get_classification(self):
        """
        The classification should be a standard pysal classification object.
        """
        return self._data['classification']
    def __set_classification(self,value):
        if len(value.yb) == len(self.data):
            self._data['classification'] = value
            if value.k != len(self.colors):
                #self.colors = colors.fade(value.k,(0,0,255),(255,0,0))
                self.colors = colors.brewer(value.k)
        self.update('classification')
    classification = property(fget=__get_classification,fset=__set_classification)
    def __get_colors(self):
        return self._data['colors']
    def __set_colors(self,value):
        self._data['colors'] = value
        self.update('classification')
    colors = property(fget=__get_colors,fset=__set_colors)
    def select(self,id):
        if not self.is_selectable:
            return
        if id not in self.selection and type(id) == int and id < len(self.data):
            self._data['selection'].add(id)
            self.update('selection')
    def unselect(self,id):
        if not self.is_selectable:
            return
        if id in self._data['selection']:
            self._data['selection'].remove(id)
            self.update('selection')
    def __get_selection(self):
        return self._data['selection']
    def __set_selection(self,value):
        #Note: this try/except is not obvious.
        # Case one, value is not a set.
        #   Maybe it's a list, if we can't make it a set, bail.
        # Case two, value is a set.
        #   set(setA) returns a copy of setA.
        #   If you don't make a copy of the set, changes to setA would change the selection outside the setter, not triggering the update.
        if not self.is_selectable:
            return
        try:
            value = set(value)
        except:
            return
        if self.selection != value:
            self._data['selection'] = value
            self.update('selection')
    selection = property(fget=__get_selection,fset=__set_selection)
    def __get_selectable(self):
        """
        Determines if a layer is selectable. If the layer is not selectable calls to select() and unselect() will be ignored
        Setting the selection property will also be ignored. (Maybe change this?)
        """
        return self._data['selectable']
    def __set_selectable(self,value):
        try:
            self._data['selectable'] = bool(value)
            self.update('selectable')
        except:
            return
    is_selectable = property(fget=__get_selectable,fset=__set_selectable)
    def __get_name(self):
        return self._data['name']
    def __set_name(self,value):
        self._data['name'] = str(value)
        self.update('name')
    name = property(fget=__get_name,fset=__set_name)
class PointLayer(BaseLayer):
    """
    Represents a collection of Points
    """
    def __init__(self,points):
        BaseLayer.__init__(self)
        self._data['type'] = 'PointLayer'
        self._data['data'] = points
        self._data['extent'] = pysal.cg.get_bounding_box(points)
        self._locator = pysal.cg.PointLocator(points)
class EventLayer(PointLayer):
    """
    Represents a collection of Events
    """
    def __init__(self,stars_evt_table):
        self.table = table = stars_evt_table
        table._fields = "geom"
        points = [x[0] for x in table.rows()]
        PointLayer.__init__(self, points)
        self.name = table.meta['title']
        self.data_table = NullDBF(table.meta['n'])
    def set_step(self,n):
        self.data = [x[0] for x in self.table.period(n)]
    @property
    def num_periods(self):
        return self.table.num_periods
    @property
    def periods(self):
        if hasattr(self.table,'_periods'):
            return self.table._periods
        else:
            return []
        
class TimeSeriesPlot(BaseLayer):
    """
    Models a Stars Time Series.

    Time Series are STATIC (for now) aggregations of events over space and time.
    """
    def __init__(self, y_by_t, meta):
        BaseLayer.__init__(self)

        self.y_by_t = y_by_t
        self.meta = meta

        self._data['type'] = 'TimeSeriesPlot'
        self._data['data'] = y_by_t

        self._locator = None
        series,periods = y_by_t.shape
        self.__k = 5
        self.__k_method = pysal.esda.mapclassify.Natural_Breaks
        self.i, self.j = y_by_t.shape
        self._t = self.j-1 # default to last time period
        self.__cl_by_t = None
        self.regionLayer = None
    def __len__(self):
        return 1
    @property
    def extent(self):
        return pysal.cg.Rectangle(0,self.y_by_t.min(),self.j,self.y_by_t.max())

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
        self.update("classification")
    def __get_k_method(self):
        return self.__k_method
    k_method = property(__get_k_method, __set_k_method)
    def __set_k(self,value):
        self.__k = value
        self.__cl_by_t = None
        self.update("classification")
    def __get_k(self):
        return self.__k
    k = property(__get_k, __set_k)

    def __set_t(self, value):
        if value >= 0 and value < self.j:
            self._t = value
            self.update("selection")
            self.update_layers()
    def __get_t(self):
        return self.meta[self._t]
    t = property(__get_t, __set_t)
    def update_layers(self):
        if self.regionLayer:
            self.regionLayer.classification = self.cl_by_t[self._t]

class ScatterLayer(BaseLayer):
    """
    Represents a collection of 2 vectors
    """
    def __init__(self,points):
        BaseLayer.__init__(self)
        self._data['type'] = 'ScatterLayer'
        self._data['data'] = points
        dims = len(points[0])
        if dims == 2:
            d0 = [x[0] for x in points]
            d0,D0 = min(d0),max(d0)
            d1 = [x[1] for x in points]
            d1,D1 = min(d1),max(d1)
            self._data['extent'] = pysal.cg.Rectangle(d0,d1,D0,D1)
        else:
            raise NotImplementedError, "Only 2D scatter plots are supported at this point."
    def __get_loc(self):
        self._locator = pysal.cg.PointLocator(self.data)
    def __set_loc(self,v):
        pass
    _locator = property(__get_loc,__set_loc)
    @property
    def extent(self):
        points = self.data
        d0 = [x[0] for x in points]
        d0,D0 = min(d0),max(d0)
        d1 = [x[1] for x in points]
        d1,D1 = min(d1),max(d1)
        return pysal.cg.Rectangle(d0,d1,D0,D1)
class PolygonLayer(BaseLayer):
    """
    Represents a collection of Polygons
    Handles Classifcation

    Because it extends AbstractModel,
      set_classification -> self.update('classification') -> map.update(this, 'classification')
    i.e. The map adds itself as a listner to the Layer.
    A Scatter plot can also listen to this layer.
    """
    def __init__(self,polys):
        BaseLayer.__init__(self)
        self._data['type'] = 'PolygonLayer'
        self._data['data'] = polys
        self._data['extent'] = pysal.cg.get_bounding_box(polys)
        self._locator = pysal.cg.PolygonLocator(polys)
class RegionLayer(PolygonLayer):
    """
    Represents a collection of Regions in an SQLITE table.
    """
    def __init__(self,stars_region_table):
        self.table = table = stars_region_table
        polys = [x[0] for x in table.rows(fields="geom")]
        PolygonLayer.__init__(self, polys)
        self.name = table.meta['title']
        self.data_table = NullDBF(table.meta['n'])
        self.__default_kmeth = "Natural_Breaks"
        self.__default_kClasses = 5
        self.__y = None
        self.__cl_cache = {}
    def update_evts(self):
        try:
            self.__y, meta = self.table.event_count_by_period()
            self.__cl_cache = {}
        except:
            return None #no evt table set.
    @property
    def num_periods(self):
        if self.table.evtTable:
            return self.table.evtTable.num_periods
        else:
            return 0
    @property
    def periods(self):
        if hasattr(self.table,'_evtTable'):
            return self.table._evtTable._periods
        else:
            return []
    def set_step(self,n):
        if self.__y != None:
            if n in self.__cl_cache:
                self.classification = self.__cl_cache[n]
            else:
                y = self.__y[:,n]
                cl = pysal.esda.mapclassify.kmethods[self.__default_kmeth](y,self.__default_kClasses)
                self.__cl_cache[n] = cl
                self.classification = cl
        else:
            self.update_evts()

class KernelDensityLayer(BaseLayer):
    """
    Represents a Kernal Density Raster
    """
    def __init__(self,points):
        BaseLayer.__init__(self)
        self._data['type'] = 'KernelDensityLayer'
        self._data['extent'] = pysal.cg.get_bounding_box(points)
        kd = KernelDensity(self._data['extent'],400,3500)
        self._points = points
        random.shuffle(self._points)
        for x,y in points:
            kd.update(x,y)
        self._data['data'] = kd
        self._cur = 0
    def animate(self):
        kd = KernelDensity(self._data['extent'],400,3500)
        self._data['data'] = kd
    def animate2(self):
        if self._cur >= len(self._points):
            self._cur = 0
            return 0
        x,y = self._points[self._cur]
        self._cur+=1
        self.data.update(x,y)
        self.update('data')
        return self._cur

if __name__=='__main__':
    import pysal
    stl = pysal.open('../../examples/stl_hom/stl_hom.shp').read()
    polys = PolygonLayer(stl)
    polys.is_selectable = True
    pts = PointLayer([p.centroid for p in stl])
    pts.is_selectable = True


    def sample_listener(mdl,tag):
        print '%r was updated the "%s" was changed!'%(mdl,tag)
        print "The new %s is %r"%(tag,mdl.getByTag(tag))
    polys.addListener(sample_listener)

    polys.select(5)
    polys.select(8)
    polys.select(30)
    polys.select(1)
    polys.selection = set()

    # This is not the best way to manage selections, just showing what's possible.
    def make_same(mdl,tag):
        if tag == 'selection':
            if mdl == pts:# and polys.selection != pts.selection:
                polys.selection = pts.selection
            if mdl == polys:# and polys.selection != pts.selection:
                pts.selection = polys.selection
    pts.addListener(make_same)
    polys.addListener(make_same)
    pts.select(5)
    pts.select(8)
    pts.select(30)
    polys.unselect(8)
    assert pts.selection == polys.selection == set([5,30])
