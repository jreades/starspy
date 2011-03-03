import pysal
import wx
from control import TableViewer 

class MapFrameApp(wx.App):
    def OnInit(self):
        db = pysal.open('/Users/charlie/Documents/data/stl_hom/stl_hom.dbf')
        self.frame = TableViewer(None,db)
        self.frame.Show()
        return True

if __name__=='__main__':
    app = MapFrameApp(redirect=False)
    app.MainLoop()
