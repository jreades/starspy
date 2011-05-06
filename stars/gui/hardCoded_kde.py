import wx
from wx.py.shell import Shell
from control import mapFrame 
from control2 import scatterFrame
from stars.visualization import layers
from stars.data_manager import StarsDatabase
import pysal

class MapFrameApp(wx.App):
    def OnInit(self):
        self.SetAppName("STARS")
        #shellFrame = wx.Frame(None)
        #sh = Shell(shellFrame)
        self.frame = mapFrame(None)#,shellFrame)
        self.SetTopWindow(self.frame)
        self.frame.Show()

        polys = '/Users/charlie/Documents/Work/NIJ/Target1/Mesa Data/Mesa_Beats/Mesa_Cleaned_withCrimeData.shp'
        fname = '/Users/charlie/Documents/Work/NIJ/Target1/Mesa Data/Mesa_ResBurgAllYears/Mesa_ResBurgAllYears.shp'
        #fname = '/Users/charlie/Documents/data/stl_hom/tmp.shp'
        print 'get points'
        pts = pysal.open(fname).read()
        print 'got points:',len(pts)
        self.kdeLayer = layers.KernelDensityLayer(pts)
        print 'got kdeLayer'
        self.frame.model.addLayer(self.kdeLayer)
        self.frame.model.addLayer(layers.PolygonLayer(pysal.open(polys).read()))
        print 'added kdeLayer'
        self.frame.Bind(wx.EVT_CHAR,self.onKey)
        return True

    def onKey(self,evt):
        if chr(evt.GetKeyCode()).lower() == 'a':
            self.kdeLayer.animate()
            while 1:
                if self.kdeLayer.animate2() == 0:
                    break
                else:
                    wx.Yield()
        if chr(evt.GetKeyCode()).lower() == 's':
            self.kdeLayer.animate()


if __name__=='__main__':
    app = MapFrameApp(redirect=False)
    app.MainLoop()
