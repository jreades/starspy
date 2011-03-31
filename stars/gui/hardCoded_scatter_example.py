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
        self.frame.model.addPath("/Users/charlie/Documents/data/stl_hom/stl_hom.shp")
        layer = self.frame.model.layers[0]
        self.SetTopWindow(self.frame)
        self.frame.Show()

        #hard coded scatter plot
        #x = layer.data_table.by_col('HR8893')
        #y = layer.data_table.by_col('PE87')
        #somePoints = map(pysal.cg.Point,zip(x,y))
        #for i,pt in enumerate(somePoints):
        #    pt.id = i+1
        #self.frame2 = scatterFrame(None,somePoints)#,shellFrame)
        #layer2 = self.frame2.model.layers[0]
        #layer2.name = "HR8893 vs PE87"
        #self.frame2.Show()
        #hard coded scatter plot
        x = layer.data_table.by_col('HR7984')
        y = layer.data_table.by_col('PE77')
        somePoints = map(pysal.cg.Point,zip(x,y))
        for i,pt in enumerate(somePoints):
            pt.id = i+1
        layer2 = layers.ScatterLayer(somePoints)
        layer2.name = "HR7984 vs PE77"
        layer2.data_table = layer.data_table

        x = layer.data_table.by_col('HR8893')
        y = layer.data_table.by_col('PE87')
        somePoints = map(pysal.cg.Point,zip(x,y))
        for i,pt in enumerate(somePoints):
            pt.id = i+1
        layer3 = layers.ScatterLayer(somePoints)
        layer3.name = "HR8893 vs PE87"
        layer3.data_table = layer.data_table

        frame = scatterFrame(None)#,shellFrame)
        frame.model.addLayer(layer2)
        frame.SetTitle(layer2.name)
        frame.Show()
        frame = scatterFrame(None)#,shellFrame)
        frame.model.addLayer(layer3)
        frame.SetTitle(layer3.name)
        frame.Show()


        self.linker = SelectionLinker([layer, layer2, layer3])
        return True

if __name__=='__main__':
    app = MapFrameApp(redirect=False)
    app.MainLoop()
