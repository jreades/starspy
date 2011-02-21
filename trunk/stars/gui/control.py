import wx
import mapview_xrc
import stars
DEBUG = True

class mapFrame(mapview_xrc.xrcMapFrame):
    def __init__(self,parent=None):
        stars.remapEvtsToDispatcher(self,self.evtDispatch)
        mapview_xrc.xrcMapFrame.__init__(self,parent)
        self.dispatch = d = {}
        d['FileOpen'] = self.open
        d['openTool'] = self.open
        #self.SetMenuBar(mapview_xrc.xrcmapMenuBar())
    def evtDispatch(self,evtName,evt):
        evtName,widgetName = evtName.rsplit('_',1)
        if widgetName in self.dispatch:
            self.dispatch[widgetName](evtName,evt)
        else:
            if DEBUG: print "not implemented:", evtName,widgetName
    def open(self,evtName=None,evt=None,value=None):
        dlg = wx.FileDialog(self,"Open Shapefile", wildcard="ESRI ShapeFile (*.shp)|*.shp")
        if dlg.ShowModal() == wx.ID_OK:
            pth = dlg.GetPath()
            if not pth.endswith('.shp'):
                pth = pth+'.shp'
            print pth
        
