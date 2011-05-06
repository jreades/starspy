import wx
from wx.py.shell import Shell
from control import mapFrame 
import time

class MapFrameApp(wx.App):
    def OnInit(self):
        self.SetAppName("STARS")
        #shellFrame = wx.Frame(None)
        #sh = Shell(shellFrame)
        self.frame = mapFrame(None)#,shellFrame)
        self.frame.model.addPath('/Users/charlie/Documents/data/usa/usa.shp')
        mdl = self.frame.model
        mdl.pan(0,-100)
        self.SetTopWindow(self.frame)
        self.frame.Show()
        t0 = time.time()
        for j in xrange(100):
            mdl.pan(0,2)
            wx.Yield()
        for j in xrange(100):
            mdl.pan(0,-2)
            wx.Yield()
        t1 = time.time()
        print t1-t0
        print (t1-t0)/200.0
        self.frame.Destroy()
        return True

if __name__=='__main__':
    app = MapFrameApp(redirect=False)
    app.MainLoop()
