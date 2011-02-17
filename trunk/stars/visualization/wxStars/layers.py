import pysal
from model import AbstractModel

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
                        'data':None, 'selectable':False, 'classification':None, 'colors':None}
    def __len__(self):
        d = self.data
        if d:
            return len(d)
        else:
            return 0
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
        The classification should be a standard pysal classifcation object.
        """
        return self._data['classification']
    def __set_classification(self,value):
        if len(value.yb) == len(self.data):
            self._data['classification'] = value
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
class PointLayer(BaseLayer):
    """
    Represents a collection of Points
    """
    def __init__(self,points):
        BaseLayer.__init__(self)
        self._data['type'] = 'PointLayer'
        self._data['data'] = points
        self._data['extent'] = pysal.cg.get_bounding_box(points)
class PolygonLayer(BaseLayer):
    """
    Represents a collection of Polygons
    Handles Classifcation

    Because it extends AbstractModel,
      set_classification -> self.update('classifcation') -> map.update(this, 'classification')
    i.e. The map adds itself as a listner to the Layer.
    A Scatter plot can also listen to this layer.
    """
    def __init__(self,polys):
        BaseLayer.__init__(self)
        self._data['type'] = 'PolygonLayer'
        self._data['data'] = polys
        self._data['extent'] = pysal.cg.get_bounding_box(polys)

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
