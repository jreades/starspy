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
import json
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

        #defaults 
        defaults = {'pos':wx.DefaultPosition, 'size':wx.DefaultSize, 'shell':{'pos':wx.DefaultPosition,'size':wx.DefaultSize}}
        #read prefs...
        paths = wx.StandardPaths.Get()
        pth = os.path.join(paths.GetUserDataDir(),'stars.config')
        if os.path.exists(pth):
            config = open(pth,'r')
            try:
                d = json.load(config)
                defaults.update(d)
                #print "Config loaded:",defaults
            except ValueError:
                print "bad config file, consider removing"

        mapview_xrc.xrcMapFrame.__init__(self,parent)
        self.SetPosition(defaults['pos'])
        self.SetSize(defaults['size'])


        self._mgr = wx.aui.AuiManager(self)

        shell = wx.Frame(self,pos=defaults['shell']['pos'], size=defaults['shell']['size'])
        shell.Bind(wx.EVT_CLOSE,self.shell)
        shell.SetTitle("STARS -- Console")
        sh = Shell(shell) 
        self.__shell = shell

        #Add Map Panel and Layers Control
        self.model = MapModel()
        self.model.addListener(self.able)
        self.mapPanel = wxMapPanel(self,self.model)
        self.layers = LayersControl(self,self.mapPanel.mapObj,size=(150,400))

        #AUI Setup
        self._mgr.AddPane(self.mapPanel, wx.CENTER)
        self._mgr.AddPane(self.layers, wx.aui.AuiPaneInfo().Name('layers').Caption('Layers').Left().MaximizeButton().Hide() )
        self._mgr.Update()
        self.toggleLayers()

        self.tools = {}
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
        self.setTool('panTool',False)

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
        d['menuLayerRemove'] = self.removeLayer

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
            self.mapMenuBar.EnableTop(self.mapMenuBar.FindMenu('Layer'),True)
            self.ToolBar.EnableTool(self.tableTool.GetId(),True)
            self.menuViewTable.Enable(True)
        else:
            self.mapMenuBar.EnableTop(self.mapMenuBar.FindMenu('Layer'),False)
            self.ToolBar.EnableTool(self.tableTool.GetId(),False)
            self.menuViewTable.Enable(False)
    def onCopy(self,evtName=None,evt=None,value=None):
        """ Copies the current display buffer to the Clipboard """
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.BitmapDataObject(self.mapPanel.buffer))
            wx.TheClipboard.Close()
        else:
            wx.Bell()
            print "Could not open the clipboard?"
    def open(self,evtName=None,evt=None,value=None):
        dlg = wx.FileDialog(self,"Open Shapefile", wildcard="ESRI ShapeFile (*.shp)|*.shp", style=wx.FD_MULTIPLE|wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            for pth in dlg.GetPaths():
                #pth = dlg.GetPath()
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
            self.setTool('selectTool',True)
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
        if self.model.selected_layer:
            layer = self.model.selected_layer
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
    def removeLayer(self,evtName=None,evt=None,value=None):
        print evtName,self.model.selected_layer
        if evtName == 'OnMenu' and self.model.selected_layer:
            print "remove layer"
            self.model.removeLayer(self.model.selected_layer)
            
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
    def OnClose(self,evt):
        paths = wx.StandardPaths.Get()
        pth = paths.GetUserDataDir()
        if not os.path.exists(pth):
            os.mkdir(pth)
        config = open(os.path.join(pth,'stars.config'),'w')
        json.dump({
            "pos":self.GetPosition().Get(), 
            "size":self.GetSize().Get(),
            "shell": {
                "pos": self.__shell.GetPosition().Get(),
                "size": self.__shell.GetSize().Get()
            }
        },config)
        config.close()
        self.Destroy()
