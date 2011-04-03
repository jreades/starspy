import wx
import wx.aui
from wx.py.shell import Shell
import mapview_xrc
import stars
from stars.visualization.wxStars import wxCanvas
from stars.visualization.wxStars import wxCanvasTools
from stars.visualization.mapModels import MapModel, CanvasModel
from stars.visualization import layers
from tableViewer import TableViewer
from layerControl import LayersControl
from control import *
import pysal
import numpy
import os
import json
DEBUG = True

class CanvasFrame(mapview_xrc.xrcCanvasFrame):
    """
    Simple frame around Stars' wxCanvas with Pan/Zoom/Select tools
    """
    def __init__(self,parent=None):
        stars.remapEvtsToDispatcher(self,self.evtDispatch)
        mapview_xrc.xrcCanvasFrame.__init__(self,parent)

        #Setup Panel and Layers Control
        self.model = CanvasModel()
        self.model.addListener(self.able)
        self.CanvasPanel = wxCanvas(self,self.model)

        # Setup Tools
        self.tools = {}
        #setup status tool
        statusTool = StatusTool(self.status,3)
        self.CanvasPanel.addControl(statusTool)
        #setup pan tool
        panTool = wxCanvasTools.panTool()
        self.CanvasPanel.addControl(panTool)
        self.tools['panTool'] = panTool,self.panTool.GetId(),self.menuToolPan.GetId()
        #setup zoom tool
        zoomTool = wxCanvasTools.zoomTool()
        self.CanvasPanel.addControl(zoomTool)
        self.tools['zoomTool'] = zoomTool,self.zoomTool.GetId(),self.menuToolZoom.GetId()
        #setup select tool
        selectTool = wxCanvasTools.selectTool()
        selectTool.disableBrushing()
        self.CanvasPanel.addControl(selectTool)
        self.tools['selectTool'] = selectTool,self.selectTool.GetId(),self.menuToolSelect.GetId()
        self.setTool('panTool',False)

        self.dispatch = d = {}
        d['menuToolPan'] = self.toggle_pan
        d['panTool'] = self.toggle_pan
        d['menuToolZoom'] = self.toggle_zoom
        d['zoomTool'] = self.toggle_zoom
        d['selectTool'] = self.toggle_select
        d['menuToolSelect'] = self.toggle_select
        d['menuToolBrush'] = self.brushing
        d['brushTool'] = self.brushing
        d['extentTool'] = self.zoomExtent
        d['MenuToolExtent'] = self.zoomExtent
        d['menuEditCopy'] = self.onCopy
        d['menuViewIcons'] = self.toolbarIcons
        d['menuViewText'] = self.toolbarText
        d['menuLayerZoom'] = self.zoomLayer

    def evtDispatch(self,evtName,evt):
        evtName,widgetName = evtName.rsplit('_',1)
        if widgetName in self.dispatch:
            self.dispatch[widgetName](evtName,evt)
        else:
            if DEBUG: print "not implemented:", evtName,widgetName
    def able(self,mdl=None,tag=None):
        """
        Enables/Disables GUI Widgets based on the model's state.
        """
        if self.model.selected_layer:
            self.menuViewTable.Enable(True)
            self.MenuBar.Check(self.menuLayerSelectable.GetId(),self.model.selected_layer.is_selectable)
        else:
            self.menuViewTable.Enable(False)
            self.MenuBar.Check(self.menuLayerSelectable.GetId(),False)
    def onCopy(self,evtName=None,evt=None,value=None):
        """ Copies the current display buffer to the Clipboard """
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.BitmapDataObject(self.CanvasPanel.buffer))
            wx.TheClipboard.Close()
        else:
            wx.Bell()
            print "Could not open the clipboard?"
    def setTool(self,toolname,state=None):
        tool,tid,mid = self.tools[toolname]
        if state == None:
            state = tool.enabled^True #Toggle state.
        self.canvasToolBar.ToggleTool(tid,state)
        self.MenuBar.Check(mid,state)
        if state:
            tool.enable()
        else:
            tool.disable()
        for key in self.tools:
            if key!=toolname:
                tool,tid,mid = self.tools[key]
                tool.disable()
                self.canvasToolBar.ToggleTool(tid,False)
                self.MenuBar.Check(mid,False)
    def brushing(self,evtName=None,evt=None,value=None):
        state = self.tools['selectTool'][0].isBrushing()^True
        self.canvasToolBar.ToggleTool(self.brushTool.GetId(),state)
        self.MenuBar.Check(self.menuToolBrush.GetId(),state)
        if state:
            self.tools['selectTool'][0].enableBrushing()
            self.setTool('selectTool',True)
        else:
            self.tools['selectTool'][0].disableBrushing()
    def toolbarIcons(self,evtName=None,evt=None,value=None):
        self.canvasToolBar.ToggleWindowStyle(wx.TB_NOICONS)
        self.MenuBar.Check(self.menuViewIcons.GetId(), self.canvasToolBar.HasFlag(wx.TB_NOICONS)^True)
    def toolbarText(self,evtName=None,evt=None,value=None):
        self.canvasToolBar.ToggleWindowStyle(wx.TB_TEXT)
        self.MenuBar.Check(self.menuViewText.GetId(), self.canvasToolBar.HasFlag(wx.TB_TEXT))
    def toggle_pan(self,evtName=None,evt=None,value=None):
        self.setTool('panTool')
    def toggle_zoom(self,evtName=None,evt=None,value=None):
        self.setTool('zoomTool')
    def toggle_select(self,evtName=None,evt=None,value=None):
        self.setTool('selectTool')
    def zoomExtent(self,evtName=None,evt=None,value=None):
        self.CanvasPanel.model.zoom_to_world()
    def zoomLayer(self,evtName=None,evt=None,value=None):
        self.model.extent = self.model.selected_layer.extent
    def OnClose(self,evt):
        self.Hide()

if __name__ == "__main__":
    
    class myApp(wx.App):
        def OnInit(self):
            self.SetAppName("STARS")
            self.frame = CanvasFrame(None)#,shellFrame)
            self.SetTopWindow(self.frame)
            self.frame.Show()
            data = pysal.open('/Users/Charlie/Documents/data/stl_hom/stl_hom.dbf')
            #hard coded scatter plot
            x = data.by_col('HR7984')
            y = data.by_col('PE77')
            somePoints = map(pysal.cg.Point,zip(x,y))
            for i,pt in enumerate(somePoints):
                pt.id = i+1
            layer = layers.ScatterLayer(somePoints)
            layer.name = "HR7984 vs PE77"

            self.frame.model.addLayer(layer)

            return True

    app = myApp(redirect=False)
    app.MainLoop()
