import random
from stars.visualization.layers import BaseLayer, PointLayer, PolygonLayer, KernelDensityLayer
import pysal
import wx
import wxLayers

class wxCanvasPanel(wx.Panel):
    """ Display a CanvasModel in a wxPanel """
    def __init__(self, parent, model):
        wx.Panel.__init__(self,parent,style=wx.WANTS_CHARS,size=model.pixel_size)
        self.model = model
        self.Bind(wx.EVT_SIZE, self.onSize)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.model.addListener(self._mapListener)
        self.layers = {}
        self._updateLayers()
        self.background = (255,255,255,255)
        self.trns = 0
        w,h = self.GetSize()
        self.buffer = wx.EmptyBitmapRGBA(w,h,alpha=self.trns)
        self.boxoutline = None
    def _updateLayers(self):
        for layer in self.model.layers:
            if layer not in self.layers:
                self.layers[layer] = [wxLayers.wxLayers[layer.type](layer),None,None]
    def _mapListener(self,mdl,tag=''):
        #print mdl,tag
        if tag and "selection:" in tag:
            lid = int(tag.split(':')[1])
            self.layers[self.model.layers[lid]][2] = None
            self.draw()
        elif tag and "classification:" in tag:
            lid = int(tag.split(':')[1])
            self.layers[self.model.layers[lid]][1] = None
            self.draw()
        elif tag == 'extent' or tag == 'offset' or tag == 'size':
            for layer in self.layers:
                self.layers[layer][1] = None
                self.layers[layer][2] = None
            self.draw()
        elif tag == 'layers':
            self._updateLayers()
            self.draw()
        elif tag and 'data' in tag:
            print "update KDE"
            lid = int(tag.split(':')[1])
            self.layers[self.model.layers[lid]][1] = None
            self.draw()
    def onSize(self,evt):
        w,h = self.GetSize()
        self.buffer = wx.EmptyBitmapRGBA(w,h,alpha=self.trns)
        self.model.pixel_size = (w,h)
        #print evt
    def onPaint(self,evt):
        pdc = wx.PaintDC(self)
        pdc.Clear()
        self.draw()
    def cacheLayer(self,layer):
        wxLayer = self.layers[layer][0]
        bitmap = wxLayer.draw(self.model)
        self.layers[layer][1] = bitmap
        return bitmap
    def cacheLayerSelectin(self,layer):
        wxLayer = self.layers[layer][0]
        sbitmap = wxLayer.draw_selection(self.model)
        self.layers[layer][2] = sbitmap
        return sbitmap
    def drawBoxOutline(self,pt1=None,pt2=None):
        if pt1 and pt2:
            x = min(pt1[0],pt2[0])
            y = min(pt1[1],pt2[1])
            w = max(pt1[0],pt2[0]) - x
            h = max(pt1[1],pt2[1]) - y
            self.boxoutline = x,y,w,h
        else:
            self.boxoutline = None
        self.draw()
    def draw(self):
        if not self.layers:
            return
        dc = wx.MemoryDC()
        dc.SelectObject(self.buffer)
        dc.SetBackground(wx.Brush(wx.Colour(*self.background)))
        dc.Clear()
        for layer in self.model.layers[::-1]: #draw the top layer last
            bitmap = self.layers[layer][1]
            if not bitmap:
                bitmap = self.cacheLayer(layer)
            sbitmap = self.layers[layer][2]
            if not sbitmap:
                sbitmap = self.cacheLayerSelectin(layer)
            dc.DrawBitmap(bitmap,0,0)
            dc.DrawBitmap(sbitmap,0,0)
        # double buffered to prevent screen flicker on windows.
        dc.SelectObject(wx.NullBitmap)
        cdc = wx.ClientDC(self)
        cdc.DrawBitmap(self.buffer,0,0)
        if self.boxoutline:
            cdc.SetBrush(wx.Brush(wx.Colour(255,255,255,128)))
            cdc.SetPen(wx.Pen(wx.Colour(0,0,0,255)))
            cdc.DrawRectangle(*self.boxoutline)
    def addControl(self,control):
        control.setCanvas(self)
        if type(control.evtType) == wx._core.PyEventBinder:
            self.Bind(control.evtType,control.onEvent)
        else:
            for evt in control.evtType:
                self.Bind(evt, control.onEvent)
    def pan(self,dx,dy):
        self.model.pan(dx,dy)

if __name__=="__main__":
    from stars.visualization.mapModels import MapModel
    from wxMapTools import panTool,randomSelction,zoomWorld,zoomTool2,randomClassification,randomPalette,animateKD,rectangleTool_Persistent
    import pysal
    import numpy
    import random
    stl = pysal.open('../../examples/stl_hom/stl_hom.shp').read()
    usa = pysal.open('../../examples/usa/usa.shp').read()
    polys = PolygonLayer(stl)
    pts = PointLayer([p.centroid for p in stl])
    #pts = pysal.open('/Users/charlie/Documents/data/pittsburgh/pitthom.shp','r').read()
    #pts = pysal.open('/Users/charlie/Documents/Work/NIJ/Target1/Mesa Data/Mesa_ResBurgAllYears_withGrids/Mesa_ResBurgAllYears_withGrids.shp','r').read()
    #model = MapModel([PolygonLayer(usa),polys,pts])
    model = MapModel([polys,pts])
    #model = MapModel([KernelDensityLayer(pts),PointLayer(pts)])
    #model = MapModel([KernelDensityLayer(pts),PointLayer(pts)])
    #polys.selection = range(0,len(polys),4)
    data = [random.random() for i in range(len(polys))]
    data = numpy.array(data)
    cl = pysal.esda.mapclassify.Natural_Breaks(data,k=5)
    polys.classification = cl
    colors = dict([(i,[random.randint(0,255) for i in range(3)]) for i in range(5)])
    polys.colors = colors

    class myApp(wx.App):
        def OnInit(self):
            self.frame = wx.Frame(None,size=(500,500))
            self.mapPanel = wxCanvasPanel(self.frame,model)
            #tools = [panTool(),zoomTool2(),randomSelction(),randomClassification(),randomPalette(),zoomWorld(),animateKD()]
            tools = [rectangleTool_Persistent()]
            for tool in tools:
                self.mapPanel.addControl(tool)
            self.frame.Show()
            #tools[0].disable() #disable the panTool
            return True
    app = myApp(redirect=False)
    app.MainLoop()
