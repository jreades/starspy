import wx
from wx.py.shell import Shell
from control import mapFrame 
from control2 import scatterFrame
from stars.visualization import layers
from stars.data_manager import StarsDatabase
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

        self.db = StarsDatabase("../test.starsdb")
        evts, regions = self.db.tables
        self.evtLayer = layers.EventLayer(evts)
        self.regionLayer = layers.RegionLayer(regions)
        self.frame.model.addLayer(self.evtLayer)
        self.frame.model.addLayer(self.regionLayer)
        self.frame.Bind(wx.EVT_CHAR,self.onKey)

        return True

    def onKey(self,evt):
        n = self.evtLayer.table.num_periods
        for i in range(n):
            self.evtLayer.set_step(i)
            wx.Yield()


if __name__=='__main__':
    app = MapFrameApp(redirect=False)
    app.MainLoop()
