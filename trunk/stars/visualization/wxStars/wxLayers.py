"""
wxLayers

wxLayers implement drawing of stars layers in wx
"""
import wx
import stars.visualization.layers as layers

class wxPointLayer:
    def __init__(self,layer):
        if not isinstance(layer,layers.PointLayer):
            raise TypeError, "Layer must be instance of PointLayer"
        self.layer = layer
        self.trns = 0
        self.radius = 5
    def draw_set(self,gc,matrix,ids):
        r = self.radius#*transform.scale #see option 2 below
        data = self.layer.data
        for i in ids:
            pt = data[i]
            ### Two options for drawing points.
            ### First is to Draw with an Ellipse
            x,y = matrix.TransformPoint(*pt)
            gc.DrawEllipse(x,y,r,r)
            ### Second is to Draw with a Graphics Path,
            ### It seems that you need to create a new Path Each time
            ### Otherwise the lines are drawn funny.
            ### Make sure you scale the radius above is you use the 2nd option.
            #x,y = pt
            #pth = gc.CreatePath()
            #pth.AddCircle(x,y,r)
            #pth.CloseSubpath()
            #pth.Transform(matrix)
            #gc.FillPath(pth)
            #gc.StrokePath(pth)
        return gc
    def draw(self,transform):
        w,h = transform.pixel_size
        buff = wx.EmptyBitmapRGBA(w,h,alpha=self.trns)
        dc = wx.MemoryDC()
        dc.SelectObject(buff)
        gc = wx.GraphicsContext.Create(dc)
        gc.SetPen( gc.CreatePen(wx.Pen(wx.Colour(0,0,0,255),1)) )
        matrix = gc.CreateMatrix()
        matrix.Scale(1./transform.scale,1./-transform.scale) #first transform is applied last
        matrix.Translate(*transform.offset)                   #last transform is applied first
        if self.layer.classification and self.layer.colors:
            cl = self.layer.classification
            cs = self.layer.colors
        else:
            class EmptyCL:
                classes = [range(len(self.layer.data))]
            cl = EmptyCL()
            cs = {0:(255,0,0)}
        for i,cls in enumerate(cl.classes):
            r,g,b = cs[i]
            gc.SetBrush( gc.CreateBrush(wx.Brush(wx.Colour(r,g,b,255))) )
            gc = self.draw_set(gc,matrix,cls)
        return buff
    def draw_selection(self,transform):
        w,h = transform.pixel_size
        r = self.radius#*transform.scale #see option 2 below
        buff = wx.EmptyBitmapRGBA(w,h,alpha=self.trns)
        dc = wx.MemoryDC()
        dc.SelectObject(buff)
        gc = wx.GraphicsContext.Create(dc)
        gc.SetPen( gc.CreatePen(wx.Pen(wx.Colour(0,0,0,255),1)) )
        gc.SetBrush( gc.CreateBrush(wx.Brush(wx.Colour(255,255,0,255))) )
        matrix = gc.CreateMatrix()
        matrix.Scale(1./transform.scale,1./-transform.scale) #first transform is applied last
        matrix.Translate(*transform.offset)                   #last transform is applied first
        gc = self.draw_set(gc,matrix,self.layer.selection)
        return buff
class wxPolygonLayer:
    def __init__(self,layer):
        if not isinstance(layer,layers.PolygonLayer):
            raise TypeError, "Layer must be instance of PolygonLayer"
        self.layer = layer
        self.trns = 0
    def draw_set(self,pth,ids):
        data = self.layer.data
        for i in ids:
            poly = data[i]
            parts = poly.parts
            if poly.holes[0]:
                parts = parts + poly.holes
            for part in parts:
                x,y = part[0]
                pth.MoveToPoint(x,y)
                for x,y in part[1:]:
                    pth.AddLineToPoint(x,y)
                pth.CloseSubpath()
        return pth
    def draw(self,transform):
        w,h = transform.pixel_size
        buff = wx.EmptyBitmapRGBA(w,h,alpha=self.trns)
        dc = wx.MemoryDC()
        dc.SelectObject(buff)
        gc = wx.GraphicsContext.Create(dc)
        gc.SetPen( gc.CreatePen(wx.Pen(wx.Colour(0,0,0,255),1)) )
        matrix = gc.CreateMatrix()
        matrix.Scale(1./transform.scale,1./-transform.scale) #first transform is applied last
        matrix.Translate(*transform.offset)                   #last transform is applied first
        if self.layer.classification and self.layer.colors:
            cl = self.layer.classification
            cs = self.layer.colors
        else:
            class EmptyCL:
                classes = [range(len(self.layer.data))]
            cl = EmptyCL()
            cs = {0:(255,0,0)}
        for i,cls in enumerate(cl.classes):
            r,g,b = cs[i]
            pth = gc.CreatePath()
            pth = self.draw_set(pth,cls)
            pth.Transform(matrix)
            gc.SetBrush( gc.CreateBrush(wx.Brush(wx.Colour(r,g,b,255))) )
            gc.FillPath(pth)
            gc.StrokePath(pth)
        return buff
    def draw_selection(self,transform):
        w,h = transform.pixel_size
        buff = wx.EmptyBitmapRGBA(w,h,alpha=self.trns)
        dc = wx.MemoryDC()
        dc.SelectObject(buff)
        gc = wx.GraphicsContext.Create(dc)
        gc.SetPen( gc.CreatePen(wx.Pen(wx.Colour(0,0,0,255),1)) )
        gc.SetBrush( gc.CreateBrush(wx.Brush(wx.Colour(255,255,0,255))) )
        matrix = gc.CreateMatrix()
        matrix.Scale(1./transform.scale,1./-transform.scale) #first transform is applied last
        matrix.Translate(*transform.offset)                   #last transform is applied first
        pth = gc.CreatePath()
        pth = self.draw_set(pth,self.layer.selection)
        pth.Transform(matrix)
        gc.FillPath(pth)
        gc.StrokePath(pth)
        return buff

wxLayers = {'PolygonLayer':wxPolygonLayer,'PointLayer':wxPointLayer}
