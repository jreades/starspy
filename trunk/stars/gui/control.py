import wx
import wx.aui
from wx.py.shell import Shell
import mapview_xrc
import stars
from stars.visualization.wxStars import wxMapPanel
from stars.visualization.wxStars import wxMapTools
from stars.visualization.mapModels import MapModel
from stars.visualization import layers
from tableViewer import TableViewer
from layerControl import LayersControl
import pysal
import os
DEBUG = True

COLOR_SAMPLE_WIDTH = 20
COLOR_SAMPLE_HEIGHT = 20

class StatusTool(wxMapTools.wxMapControl):
    def __init__(self,wx_status_bar,status_field,enabled=True):
        self.status = wx_status_bar
        self.field = status_field
        wxMapTools.wxMapControl.__init__(self,enabled)
    def _onEvent(self,evt):
        x,y = self.mapObj.mapObj.pixel_to_world(*evt.Position)
        self.status.SetStatusText("%f, %f"%(x,y),self.field)

class mapFrame(mapview_xrc.xrcMapFrame):
    def __init__(self,parent=None):
        stars.remapEvtsToDispatcher(self,self.evtDispatch)
        mapview_xrc.xrcMapFrame.__init__(self,parent)

        self._mgr = wx.aui.AuiManager(self)

        shell = wx.Frame(self)
        shell.Bind(wx.EVT_CLOSE,self.shell)
        shell.SetTitle("STARS -- Console")
        sh = Shell(shell) 
        
        self.__shell = shell
        #self.__tables = []
        self.tools = {}

        #Add Map Panel
        self.model = MapModel()
        self.mapPanel = wxMapPanel(self,self.model)
        #sizer = self.mapPanelHolder.GetContainingSizer()
        #sizer.Replace(self.mapPanelHolder,self.mapPanel)
        #sizer.Layout()


        #AUI Setup
        self._mgr.AddPane(self.mapPanel, wx.CENTER)


        #tc = wx.TextCtrl(self,-1,'Side Pane', wx.DefaultPosition, wx.Size(200,150), wx.NO_BORDER | wx.TE_MULTILINE)
        self.layers = LayersControl(self,size=(150,400))
        self.layers.mapModel = self.mapPanel.mapObj
        self._mgr.AddPane(self.layers, wx.aui.AuiPaneInfo().Name('layers').Caption('Layers').Left().MaximizeButton().Hide() )
        self._mgr.Update()
        self.toggleLayers()



        #setup status tool
        statusTool = StatusTool(self.status,3)
        self.mapPanel.addControl(statusTool)
        #setup pan tool
        panTool = wxMapTools.panTool()
        self.mapPanel.addControl(panTool)
        self.tools['panTool'] = panTool,self.panTool.GetId(),self.menuToolPan.GetId()
        #setup zoom tool
        zoomTool = wxMapTools.zoomTool()
        self.mapPanel.addControl(zoomTool)
        self.tools['zoomTool'] = zoomTool,self.zoomTool.GetId(),self.menuToolZoom.GetId()
        #setup select tool
        selectTool = wxMapTools.selectTool()
        selectTool.disableBrushing()
        self.mapPanel.addControl(selectTool)
        self.tools['selectTool'] = selectTool,self.selectTool.GetId(),self.menuToolSelect.GetId()
        self.setTool('panTool',True)

        self.dispatch = d = {}
        d['FileOpen'] = self.open
        d['openTool'] = self.open
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
        d['consoleTool'] = self.shell
        d['menuViewConsole'] = self.shell
        d['menuEditCopy'] = self.onCopy
        d['menuViewIcons'] = self.toolbarIcons
        d['menuViewText'] = self.toolbarText
        d['tableTool'] = self.table
        d['menuViewTable'] = self.table
        d['menuViewLayers'] = self.toggleLayers
        d['layersTool'] = self.toggleLayers

    def evtDispatch(self,evtName,evt):
        evtName,widgetName = evtName.rsplit('_',1)
        if widgetName in self.dispatch:
            self.dispatch[widgetName](evtName,evt)
        else:
            if DEBUG: print "not implemented:", evtName,widgetName
    def onCopy(self,evtName=None,evt=None,value=None):
        """ Copies the current display buffer to the Clipboard """
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.BitmapDataObject(self.mapPanel.buffer))
            wx.TheClipboard.Close()
        else:
            wx.Bell()
            print "Could not open the clipboard?"
    def open(self,evtName=None,evt=None,value=None):
        dlg = wx.FileDialog(self,"Open Shapefile", wildcard="ESRI ShapeFile (*.shp)|*.shp")
        if dlg.ShowModal() == wx.ID_OK:
            pth = dlg.GetPath()
            if not pth.endswith('.shp'):
                pth = pth+'.shp'
            print "Adding Layer:",pth
            layer = self.model.addPath(pth)
    def setTool(self,toolname,state=None):
        tool,tid,mid = self.tools[toolname]
        if state == None:
            state = tool.enabled^True #Toggle state.
        self.mapToolBar.ToggleTool(tid,state)
        self.MenuBar.Check(mid,state)
        if state:
            tool.enable()
        else:
            tool.disable()
        for key in self.tools:
            if key!=toolname:
                tool,tid,mid = self.tools[key]
                tool.disable()
                self.mapToolBar.ToggleTool(tid,False)
                self.MenuBar.Check(mid,False)
    def brushing(self,evtName=None,evt=None,value=None):
        state = self.tools['selectTool'][0].isBrushing()^True
        self.mapToolBar.ToggleTool(self.brushTool.GetId(),state)
        self.MenuBar.Check(self.menuToolBrush.GetId(),state)
        if state:
            self.tools['selectTool'][0].enableBrushing()
        else:
            self.tools['selectTool'][0].disableBrushing()
    def shell(self,evtName=None,evt=None,value=None):
        state = self.__shell.IsShown()^True
        self.mapToolBar.ToggleTool(self.consoleTool.GetId(),state)
        self.MenuBar.Check(self.menuViewConsole.GetId(),state)
        if state:
            self.__shell.Show()
        else:
            self.__shell.Hide()
    def table(self,evtName=None,evt=None,value=None):
        cur_table = self.layers.layer
        if cur_table != None:
            layer = self.model.layers[cur_table]
            if not hasattr(layer,'tableView'):
                layer.tableView = TableViewer(self,layer)
                layer.tableView.SetTitle("STARS -- Attribute Table for %s"%layer.name)
            layer.tableView.Show()
            layer.tableView.Raise()
    def toggleLayers(self,evtName=None,evt=None,value=None):
        pane = self._mgr.GetPane(self.layers)
        state = pane.IsShown()^True
        self.mapToolBar.ToggleTool(self.layersTool.GetId(),state)
        self.MenuBar.Check(self.menuViewLayers.GetId(),state)
        if state:
            pane.Show()
        else:
            pane.Hide()
        self._mgr.Update()
            
    def toolbarIcons(self,evtName=None,evt=None,value=None):
        self.mapToolBar.ToggleWindowStyle(wx.TB_NOICONS)
        self.MenuBar.Check(self.menuViewIcons.GetId(), self.mapToolBar.HasFlag(wx.TB_NOICONS)^True)
    def toolbarText(self,evtName=None,evt=None,value=None):
        self.mapToolBar.ToggleWindowStyle(wx.TB_TEXT)
        self.MenuBar.Check(self.menuViewText.GetId(), self.mapToolBar.HasFlag(wx.TB_TEXT))
    def toggle_pan(self,evtName=None,evt=None,value=None):
        self.setTool('panTool')
    def toggle_zoom(self,evtName=None,evt=None,value=None):
        self.setTool('zoomTool')
    def toggle_select(self,evtName=None,evt=None,value=None):
        self.setTool('selectTool')
    def zoomExtent(self,evtName=None,evt=None,value=None):
        self.mapPanel.mapObj.zoom_to_world()
    def table_update(self,mdl,tag=None):
        mdl.layer.selection = mdl.selection
