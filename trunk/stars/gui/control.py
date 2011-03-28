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
import pysal
import numpy
import os
import json
DEBUG = True

COLOR_SAMPLE_WIDTH = 20
COLOR_SAMPLE_HEIGHT = 20

class StatusTool(wxCanvasTools.wxCanvasControl):
    def __init__(self,wx_status_bar,status_field,enabled=True):
        self.status = wx_status_bar
        self.field = status_field
        wxCanvasTools.wxCanvasControl.__init__(self,enabled)
    def _onEvent(self,evt):
        x,y = self.canvas.model.pixel_to_world(*evt.Position)
        self.status.SetStatusText("%f, %f"%(x,y),self.field)

class layerPropFrame(mapview_xrc.xrcLayerPropFrame):
    def __init__(self,parent,layer):
        stars.remapEvtsToDispatcher(self,self.evtDispatch)
        mapview_xrc.xrcLayerPropFrame.__init__(self,parent)

        self.Bind(wx.EVT_CLOSE,self.close)

        self.layer = layer
        #layer.addListener(self.update)
        self.update(layer)

        self.dispatch = d = {}
        d['classificationApply'] = self.run
    def evtDispatch(self,evtName,evt):
        evtName,widgetName = evtName.rsplit('_',1)
        if widgetName in self.dispatch:
            self.dispatch[widgetName](evtName,evt)
        else:
            if DEBUG: print "not implemented:", evtName,widgetName
    def update(self,mdl):
        self.classificationAttribute.SetItems(mdl.data_table.header)
        self.classificationAttribute.Select(0)
        self.classificationMethod.SetItems(pysal.esda.mapclassify.kmethods.keys())
        self.classificationMethod.Select(0)
        self.classificationClasses.SetItems(map(str,range(3,11)))
        self.classificationClasses.Select(2)
    def run(self,evtName=None,evt=None,value=None):
        y = self.layer.data_table.by_col(self.classificationAttribute.GetStringSelection())
        y = numpy.array(y)
        k = int(self.classificationClasses.GetStringSelection())
        meth = pysal.esda.mapclassify.kmethods[self.classificationMethod.GetStringSelection()]
        self.layer.classification = meth(y,k)
    def close(self,evt):
        self.Hide()
        
class mapFrame(mapview_xrc.xrcMapFrame):
    def __init__(self,parent=None):
        stars.remapEvtsToDispatcher(self,self.evtDispatch)
        mapview_xrc.xrcMapFrame.__init__(self,parent)
        # localize layerMenu.
        self.layerMenu = self.mapMenuBar.Menus[self.mapMenuBar.FindMenu('Layer')][0]

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
        # restore defaults
        self.SetPosition(defaults['pos'])
        self.SetSize(defaults['size'])
        # setup shell
        shell = wx.Frame(self,pos=defaults['shell']['pos'], size=defaults['shell']['size'])
        shell.Bind(wx.EVT_CLOSE,self.shell)
        shell.SetTitle("STARS -- Console")
        sh = Shell(shell) 
        self.__shell = shell

        #Setup Map Panel and Layers Control
        self.model = MapModel()
        #self.model.addPath('/Users/charlie/Documents/data/stl_hom/stl_hom.shp')
        self.model.addListener(self.able)
        self.mapCanvas = wxCanvas(self,self.model)
        self.layers = LayersControl(self,self.mapCanvas.model,size=(150,400))

        #Add a plot Canvas
        #x = self.model.layers[0].data_table.by_col('HR8893')
        #y = self.model.layers[0].data_table.by_col('PE87')
        #somePoints = map(pysal.cg.Point,zip(x,y))
        #for i,pt in enumerate(somePoints):
        #    pt.id = i+1
        
        #plotLayer = layers.ScatterLayer(somePoints)
        #self.plot = CanvasModel([plotLayer])
        #self.plotCanvas= wxCanvas(self,self.plot)
        #self.plotCanvas.addControl(wxCanvasTools.selectTool())
        
        #def custom_linker(src, tag):
        #    layers = [plotLayer, self.model.layers[0]]
        #    targets = [x for x in layers if x != src]
        #    for target in targets:
        #        target.selection = src.selection
        #plotLayer.addListener(custom_linker)
        #self.model.layers[0].addListener(custom_linker)
            

        # initialize the Advanced User Interface (AUI) manager.
        self._mgr = wx.aui.AuiManager(self)
        # Setup AUI Panes
        self._mgr.AddPane(self.mapCanvas, wx.CENTER)
        #self._mgr.AddPane(self.plotCanvas, wx.LEFT)
        #self._mgr.AddPane(self.mapCanvas, wx.aui.AuiPaneInfo().Name('mapView').Caption('Map View 1').Left().MaximizeButton().Show() )
        self._mgr.AddPane(self.layers, wx.aui.AuiPaneInfo().Name('layers').Caption('Layers').Left().MaximizeButton().Hide() )
        #self._mgr.AddPane(self.ToolBar, wx.aui.AuiPaneInfo().Name('toolbar1').Caption('ToolBar').ToolbarPane().Top() )
        self._mgr.Update()
        self.toggleLayers()

        # Setup Tools
        self.tools = {}
        #setup status tool
        statusTool = StatusTool(self.status,3)
        self.mapCanvas.addControl(statusTool)
        #setup pan tool
        panTool = wxCanvasTools.panTool()
        self.mapCanvas.addControl(panTool)
        self.tools['panTool'] = panTool,self.panTool.GetId(),self.menuToolPan.GetId()
        #setup zoom tool
        zoomTool = wxCanvasTools.zoomTool()
        self.mapCanvas.addControl(zoomTool)
        self.tools['zoomTool'] = zoomTool,self.zoomTool.GetId(),self.menuToolZoom.GetId()
        #setup select tool
        selectTool = wxCanvasTools.selectTool()
        selectTool.disableBrushing()
        self.mapCanvas.addControl(selectTool)
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
        d['menuLayerZoom'] = self.zoomLayer
        d['menuLayerSelectable'] = self.layerSelectable
        d['menuLayerProps'] = self.layerProps

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
            self.MenuBar.Check(self.menuLayerSelectable.GetId(),self.model.selected_layer.is_selectable)
        else:
            self.mapMenuBar.EnableTop(self.mapMenuBar.FindMenu('Layer'),False)
            self.ToolBar.EnableTool(self.tableTool.GetId(),False)
            self.menuViewTable.Enable(False)
            self.MenuBar.Check(self.menuLayerSelectable.GetId(),False)
    def onCopy(self,evtName=None,evt=None,value=None):
        """ Copies the current display buffer to the Clipboard """
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.BitmapDataObject(self.mapCanvas.buffer))
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
        if evtName == 'OnMenu' and self.model.selected_layer:
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
        self.mapCanvas.model.zoom_to_world()
    def zoomLayer(self,evtName=None,evt=None,value=None):
        self.model.extent = self.model.selected_layer.extent
    def layerSelectable(self,evtName=None,evt=None,value=None):
        if evtName == 'OnMenu':
            state = self.model.selected_layer.is_selectable^True
            self.model.selected_layer.is_selectable = state
    def layerProps(self,evtName=None,evt=None,value=None):
        if evtName == 'OnMenu' and self.model.selected_layer:
            layer = self.model.selected_layer
            if not hasattr(layer,'propsView'):
                print "Create Props View"
                layer.propsView = layerPropFrame(self,layer)
            layer.propsView.Show()
            layer.propsView.Raise()
            
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
