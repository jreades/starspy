import wx
from wx.py.shell import Shell
import mapview_xrc
import stars
from stars.visualization.wxStars import wxMapPanel
from stars.visualization.wxStars import wxMapTools
from stars.visualization.mapModels import MapModel
from stars.visualization import layers
from tableViewer import TableViewer
import pysal
DEBUG = True

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
        shell = wx.Frame(self)
        shell.Bind(wx.EVT_CLOSE,self.shell)
        shell.SetTitle("Stars -- Console")
        sh = Shell(shell) 
        
        self.__shell = shell
        self.__tables = []
        self.tools = {}

        #Add Map Panel
        self.model = MapModel()
        self.mapPanel = wxMapPanel(self,self.model)
        sizer = self.mapPanelHolder.GetContainingSizer()
        sizer.Replace(self.mapPanelHolder,self.mapPanel)
        sizer.Layout()
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
        selectTool = wxMapTools.rectangleTool_Persistent()
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
            print pth
            shp = pysal.open(pth)
            if shp.type == pysal.cg.Polygon:
                layer = layers.PolygonLayer(shp.read())
            elif shp.type == pysal.cg.Point:
                layer = layers.PointLayer(shp.read())
            else:
                print "Unsupported Layer"
                return
            dbf = pysal.open(pth[:-4]+'.dbf')
            tbl = TableViewer(self,dbf)
            tbl.model.addListener(self.table_update)
            self.__tables.append(tbl)

            tbl.model.layer = layer
            layer.dbf = dbf
            self.model.addLayer(layer)
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
        if not self.__tables:
            state = False
        else:
            tbl = self.__tables[-1]
            state = tbl.IsShown()^True
            if state:
                tbl.Show()
            else:
                tbl.Hide()
        self.mapToolBar.ToggleTool(self.tableTool.GetId(),state)
        self.MenuBar.Check(self.menuViewTable.GetId(),state)
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
