import wx
from wx.py.shell import Shell
from control import mapFrame 
from control2 import scatterFrame
from stars.visualization import layers
from stars.data_manager import StarsDatabase
#from stars.timeSeries import TimeSeries
import pysal

class SelectionLinker:
    def __init__(self, layers = []):
        """ Links the selection of the layers """
        self.layers = []
        for layer in layers:
            self.addLayer(layer)
    def addLayer(self, layer):
        if layer not in self.layers:
            self.layers.append(layer)
            layer.addListener(self.listener)
    def removeLayer(self, layer):
        if layer in self.layers:
            self.layers = [l for l in self.layer is l != layer]
            layer.removeListener(self.listener)
    def listener(self, src, tag):
        for layer in self.layers:
            if layer != src:
                if layer.selection != src.selection:
                    layer.selection = src.selection
    
class MapFrameApp(wx.App):
    def OnInit(self):
        self.SetAppName("STARS")
        #shellFrame = wx.Frame(None)
        #sh = Shell(shellFrame)
        self.frame = mapFrame(None)#,shellFrame)
        self.SetTopWindow(self.frame)
        self.frame.Show()

        self.frame.model.addPath("/Users/charlie/Documents/Work/NIJ/Target1/Mesa Data/Burglaries_Mesagrids0609/projected.shp")
        layer = self.frame.model.layers[0]
    
        self.db = StarsDatabase("../test.starsdb")
        regions = self.db.region_tables[0]
        y_by_t, meta = regions.event_count_by_period()
        self.ts = layers.TimeSeriesPlot(y_by_t,meta)
        self.ts.regionLayer = layer
        self.ts.update_layers()
        #evts, regions = self.db.tables
        #self.evtLayer = layers.EventLayer(evts)
        #self.regionLayer = layers.RegionLayer(regions)
        #self.frame.model.addLayer(self.evtLayer)
        #self.frame.model.addLayer(self.regionLayer)
        self.frame.Bind(wx.EVT_CHAR,self.onKey)


        from control3 import CanvasFrame
        frame = CanvasFrame(None)
        #y = self.ts.y_by_t
        #y = (y - y.mean()) / y.std()
        #self.ts.y_by_t = y
        self.ts_layer = self.ts
        frame.model.addLayer(self.ts)
        frame.Show()

        self.linker = SelectionLinker([layer,self.ts])

        return True

    def onKey(self,evt):
        n = self.ts.j
        for i in range(n):
            self.ts.t = i
            self.ts_layer.update("selection")
            wx.Yield()


if __name__=='__main__':
    app = MapFrameApp(redirect=False)
    app.MainLoop()
