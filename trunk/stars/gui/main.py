import wx
from wx.py.shell import Shell
from control import mapFrame 

class MapFrameApp(wx.App):
    def OnInit(self):
        self.frame = mapFrame()
        self.frame.Show()
        shellFrame = wx.Frame(None)
        sh = Shell(shellFrame)
        shellFrame.Show()
        return True

if __name__=='__main__':
    app = MapFrameApp(redirect=False)
    app.MainLoop()
