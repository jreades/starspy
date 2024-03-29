import pysal
import os.path
from model import AbstractModel
import layers
from transforms import WorldToViewTransform

class CanvasModel(WorldToViewTransform):
    """ Base model for all Canvas views.
        Maintains the state of the view,
            Current extent, layer order, etc.
        Handles View Events,
            Pan, Zoom, Selection, etc.
    """
    def __init__(self,layers=[],initial_size=(500,500)):
        self._data = {'selected_layer':None,'layers':[],'world_extent':pysal.cg.Rectangle(0,0,0,0)}
        WorldToViewTransform.__init__(self,self.world_extent,*initial_size)
        for layer in layers:
            self.addLayer(layer)
        self.zoom_to_world()
    def __len__(self):
        """
        Returns len(self.layers)
        """
        return len(self._data['layers'])
    def _layerListener(self,layer,tag):
        """
        Propgates layer events to anyone listening to the map.
        """
        lid = self._data['layers'].index(layer)
        self.update('%s:%d'%(tag,lid))
    def addLayer(self,layer):
        """
        Add a layer to the current map.
        Layers are made selectable when added.
        """
        if issubclass(type(layer),layers.BaseLayer) and layer not in self._data['layers']:
            layer.is_selectable = True
            self._data['layers'].insert(0,layer)
            layer.addListener(self._layerListener)
            self._data['world_extent'] = pysal.cg.Rectangle(0,0,0,0)
            self.selected_layer = layer
            if not self.extent:
                self.extent = self.world_extent
                self.zoom_to_world()
            self.update('layers')
            return layer
        return False
    def removeLayer(self,layer):
        """
        Remove the layer from the map.

        layer should be a layer instance or it's index in self.layers

        The remove layer object is returned.
        """
        idx = None
        if issubclass(type(layer),layers.BaseLayer) and layer in self._data['layers']:
            idx = self._data['layers'].index(layer)
        elif type(layer) == int:
            idx = layer
        if idx != None:
            l = self._data['layers'].pop(idx)
            self.update('layers')
            self.selected_layer = None
            self._data['world_extent'] = pysal.cg.Rectangle(0,0,0,0)
            return l
        
    @property
    def layers(self):
        return self._data['layers'][:]
    @property
    def world_extent(self):
        if not self._data['world_extent']:
            n = len(self)
            if n == 1:
                self._data['world_extent'] = self._data['layers'][0].extent
            elif n > 1:
                self._data['world_extent'] = pysal.cg.get_bounding_box([layer.extent for layer in self.layers])
        return self._data['world_extent']
    def zoom_to_world(self):
        """
        Zoom the current transform to the extent of the world.
        """
        self.extent = self.world_extent
    def __set_selected_layer(self,value):
        if value != None:
            if issubclass(type(value),layers.BaseLayer):
                self._data['selected_layer'] = value
            else:
                raise TypeError,"selected_layer must be a a Layer"
        else:
            self._data['selected_layer'] = None
        self.update('selected_layer')
    def __get_selected_layer(self):
        """
        Get/Set the current selected layer.
        This is useful for operations that need to be performs on a given layer.
        The last layer added to the map will be selected by default.
        Clear the selection by setting it to None.
        """
        return self._data['selected_layer']
    selected_layer = property(fget=__get_selected_layer,fset=__set_selected_layer)
        
    def moveLayer(self,start_pos,end_pos):
        """
        Move the layer from the start_pos to the end_pos in the 1 Dimmension layer list
        
        Example:
        >>> m = MapModel(layers=[layerA,layerB])
        >>> m.layers
        [layerA,layerB]
        >>> m.moveLayer(1,0)
        >>> m.layers
        [layerB,layerA]
        """
        layer = self._data['layers'].pop(start_pos)
        self._data['layers'].insert(end_pos,layer)
        self.update('layers')

class MapModel(CanvasModel):
    """ Base Model for all Maps 
    """
    def addPath(self,path):
        """
        Attempts to add the path as a new layer.
        Returns the layer if successful, else False
        """
        layer = None
        if os.path.exists(path):
            f = pysal.open(path,'r')
            if hasattr(f,'type'):
                if f.type == pysal.cg.Polygon:
                    layer = layers.PolygonLayer(f.read())
                if f.type == pysal.cg.Point:
                    layer = layers.PointLayer(f.read())
            if path.endswith('shp') and os.path.exists(path[:-4]+'.dbf'):
                dbf = pysal.open(path[:-4]+'.dbf','r')
                layer.data_table = dbf
            elif layer:
                layer.data_table = layers.NullDBF(len(layer))
        if layer:
            layer.name = os.path.splitext(os.path.basename(path))[0]
            return self.addLayer(layer)
        return False



if __name__=='__main__':
    import pysal
    stl = pysal.open('/Users/charlie/Documents/data/stl_hom/stl_hom.shp').read()
    polys = layers.PolygonLayer(stl)
    #pts = layers.PointLayer([p.centroid for p in stl])

    mapObj = MapModel([polys])
    #mapObj.addLayer(polys)
    #mapObj.addLayer(pts)
