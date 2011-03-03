import pysal
from model import AbstractModel
from layers import BaseLayer, PointLayer, PolygonLayer
from transforms import WorldToViewTransform

class MapModel(WorldToViewTransform):
    """ Base Model for all Maps 
        Maintains the state of the map,
            The current view extent, layer order, etc
        Handles Map Events,
            Pan, Zoom, Selection, etc.
    """
    def __init__(self,layers=[],initial_size=(500,500)):
        self._data = {'selectionLayer':0,'layers':[],'world_extent':pysal.cg.Rectangle(0,0,0,0)}
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
        if issubclass(type(layer),BaseLayer) and layer not in self._data['layers']:
            layer.is_selectable = True
            self._data['layers'].append(layer)
            layer.addListener(self._layerListener)
            self._data['world_extent'] = pysal.cg.Rectangle(0,0,0,0)
            self.update('layers')
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



if __name__=='__main__':
    import pysal
    stl = pysal.open('/Users/charlie/Documents/data/stl_hom/stl_hom.shp').read()
    polys = PolygonLayer(stl)
    #pts = PointLayer([p.centroid for p in stl])

    mapObj = MapModel([polys])
    #mapObj.addLayer(polys)
    #mapObj.addLayer(pts)
