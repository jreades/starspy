import wx
from wx.py.shell import Shell
from control import mapFrame 

class MapFrameApp(wx.App):
    def OnInit(self):
        #shellFrame = wx.Frame(None)
        #sh = Shell(shellFrame)
        self.frame = mapFrame(None)#,shellFrame)
        self.frame.Show()
        return True

if __name__=='__main__':
    app = MapFrameApp(redirect=False)
    app.MainLoop()
