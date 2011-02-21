import random
from stars.visualization.layers import BaseLayer, PointLayer, PolygonLayer
from stars.visualization.mapModels import MapModel
import pysal
import wx
import wxLayers

class wxMapPanel(wx.Panel):
    """ Display a MapModel in a wxPanel """
    def __init__(self, parent, mapObj):
        wx.Panel.__init__(self,parent,style=wx.WANTS_CHARS,size=mapObj.pixel_size)
        self.mapObj = mapObj
        self.Bind(wx.EVT_SIZE, self.onSize)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.mapObj.addListener(self._mapListener)
        self.layers = {}
        self._updateLayers()
        self.pan_offset = 0,0
        self.background = (255,255,255,255)
        self.trns = 0
        w,h = self.GetSize()
        self.buffer = wx.EmptyBitmapRGBA(w,h,alpha=self.trns)
    def _updateLayers(self):
        for layer in self.mapObj.layers:
            if layer not in self.layers:
                self.layers[layer] = [wxLayers.wxLayers[layer.type](layer),None,None]
    def _mapListener(self,mdl,tag=''):
        #print mdl,tag
        if tag and "selection:" in tag:
            lid = int(tag.split(':')[1])
            self.layers[self.mapObj.layers[lid]][2] = None
            self.draw()
        elif tag and "classification:" in tag:
            lid = int(tag.split(':')[1])
            self.layers[self.mapObj.layers[lid]][1] = None
            self.draw()
        elif tag == 'extent' or tag == 'offset' or tag == 'size':
            for layer in self.layers:
                self.layers[layer][1] = None
                self.layers[layer][2] = None
            self.draw()
        elif tag == 'layers':
            self._updateLayers()
            self.mapObj.zoom_to_world()
    def onSize(self,evt):
        w,h = self.GetSize()
        self.buffer = wx.EmptyBitmapRGBA(w,h,alpha=self.trns)
        self.mapObj.pixel_size = (w,h)
        #print evt
    def onPaint(self,evt):
        pdc = wx.PaintDC(self)
        pdc.Clear()
        self.draw()
    def cacheLayer(self,layer):
        wxLayer = self.layers[layer][0]
        bitmap = wxLayer.draw(self.mapObj)
        self.layers[layer][1] = bitmap
        return bitmap
    def cacheLayerSelectin(self,layer):
        wxLayer = self.layers[layer][0]
        sbitmap = wxLayer.draw_selection(self.mapObj)
        self.layers[layer][2] = sbitmap
        return sbitmap
    def drawBoxOutline(self,pt1=None,pt2=None):
        self.draw()
        if pt1 and pt2:
            cdc = wx.ClientDC(self)
            cdc.SetBrush(wx.Brush(wx.Colour(255,255,255,128)))
            cdc.SetPen(wx.Pen(wx.Colour(0,0,0,255)))
            x = min(pt1[0],pt2[0])
            y = min(pt1[1],pt2[1])
            w = max(pt1[0],pt2[0]) - x
            h = max(pt1[1],pt2[1]) - y
            cdc.DrawRectangle(x,y,w,h)
    def draw(self):
        dc = wx.MemoryDC()
        dc.SelectObject(self.buffer)
        dc.SetBackground(wx.Brush(wx.Colour(*self.background)))
        dc.Clear()
        px,py = self.pan_offset
        for layer in self.mapObj.layers:
            bitmap = self.layers[layer][1]
            if not bitmap:
                bitmap = self.cacheLayer(layer)
            sbitmap = self.layers[layer][2]
            if not sbitmap:
                sbitmap = self.cacheLayerSelectin(layer)
            dc.DrawBitmap(bitmap,px,py)
            dc.DrawBitmap(sbitmap,px,py)
        # double buffered to prevent screen flicker on windows.
        dc.SelectObject(wx.NullBitmap)
        cdc = wx.ClientDC(self)
        cdc.DrawBitmap(self.buffer,0,0)
    def addControl(self,control):
        control.setMap(self)
        self.Bind(control.evtType,control.onEvent)
    def pan(self,dx,dy):
        #px,py = self.pan_offset
        #px+=dx
        #py+=dy
        #self.pan_offset = px,py
        #self.draw()
        self.mapObj.pan(dx,dy)

if __name__=="__main__":
    from wxMapTools import panTool,randomSelction,zoomWorld,zoomTool,randomClassification,randomPalette
    import pysal
    import numpy
    import random
    stl = pysal.open('../../examples/stl_hom/stl_hom.shp').read()
    usa = pysal.open('../../examples/usa/usa.shp').read()
    polys = PolygonLayer(stl)
    pts = PointLayer([p.centroid for p in stl])
    #mapObj = MapModel([PolygonLayer(usa),polys,pts])
    mapObj = MapModel([polys,pts])
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
            self.mapPanel = wxMapPanel(self.frame,mapObj)
            tools = [panTool(),zoomTool(),randomSelction(),randomClassification(),randomPalette(),zoomWorld()]
            for tool in tools:
                self.mapPanel.addControl(tool)
            self.frame.Show()
            #tools[0].disable() #disable the panTool
            return True
    app = myApp(redirect=False)
    app.MainLoop()
