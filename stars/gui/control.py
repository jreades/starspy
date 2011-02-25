import wx
import mapview_xrc
import stars
from stars.visualization.wxStars import wxMapPanel
from stars.visualization.wxStars import wxMapTools
from stars.visualization.mapModels import MapModel
from stars.visualization import layers
import pysal
DEBUG = True

class mapFrame(mapview_xrc.xrcMapFrame):
    def __init__(self,parent=None):
        stars.remapEvtsToDispatcher(self,self.evtDispatch)
        mapview_xrc.xrcMapFrame.__init__(self,parent)
        self.tools = {}

        #Add Map Panel
        self.model = MapModel()
        self.mapPanel = wxMapPanel(self,self.model)
        sizer = self.mapPanelHolder.GetContainingSizer()
        sizer.Replace(self.mapPanelHolder,self.mapPanel)
        sizer.Layout()
        #setup pan tool
        panTool = wxMapTools.panTool()
        panTool.disable()
        self.mapPanel.addControl(panTool)
        self.tools['panTool'] = panTool
        #setup zoom tool
        zoomTool = wxMapTools.zoomTool()
        zoomTool.disable()
        self.mapPanel.addControl(zoomTool)
        self.tools['zoomTool'] = zoomTool

        self.dispatch = d = {}
        d['FileOpen'] = self.open
        d['openTool'] = self.open
        d['MenuToolPan'] = self.toggle_pan
        d['panTool'] = self.toggle_pan
        d['MenuToolZoom'] = self.toggle_zoom
        d['zoomTool'] = self.toggle_zoom
        d['extentTool'] = self.zoomExtent
        d['MenuToolExtent'] = self.zoomExtent
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
            shp = pysal.open(pth)
            if shp.type == pysal.cg.Polygon:
                layer = layers.PolygonLayer(shp.read())
            elif shp.type == pysal.cg.Point:
                layer = layers.PointLayer(shp.read())
            else:
                print "Unsupported Layer"
                return
            self.model.addLayer(layer)
    def toggle_pan(self,evtName=None,evt=None,value=None):
        self.tools['zoomTool'].disable()
        tool = self.tools['panTool']
        if tool.enabled:
            tool.disable()
        else:
            tool.enable()
        print tool,tool.enabled
    def toggle_zoom(self,evtName=None,evt=None,value=None):
        self.tools['panTool'].disable()
        tool = self.tools['zoomTool']
        if tool.enabled:
            tool.disable()
        else:
            tool.enable()
    def zoomExtent(self,evtName=None,evt=None,value=None):
        self.mapPanel.mapObj.zoom_to_world()
