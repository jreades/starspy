import wx
from control import mapFrame 

class MapFrameApp(wx.App):
    def OnInit(self):
        self.frame = mapFrame()
        self.frame.Show()
        return True

if __name__=='__main__':
    app = MapFrameApp(redirect=False)
    app.MainLoop()
