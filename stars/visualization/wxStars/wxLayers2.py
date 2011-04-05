import wx
import numpy
import stars.visualization.layers as layers
from stars.visualization.transforms import WorldToViewTransform
from kernelDensityTime import KernelDensity
from pysal.cg import bbcommon, get_rectangle_rectangle_intersection

class wxTimeSeriesPlot:
    def __init__(self,layer):
        if not isinstance(layer,layers.TimeSeriesPlot):
            raise TypeError, "Layer must be instance of TimeSeriesPlot"
        self.layer = layer
        self.trns = 0
    def draw(self,transform):
        w,h = transform.pixel_size
        buff = wx.EmptyBitmapRGBA(w,h,alpha=self.trns)
        dc = wx.MemoryDC()
        dc.SelectObject(buff)
        sx,sy = 1./transform.scale,1./-transform.scale
        ox,oy = transform.offset

        #draw axis
        x0,y0 = (0 + ox) * sx, (0 + oy) * sy   #origin
        dc.DrawLine(0,y0,w,y0)
        dc.DrawLine(x0,0,x0,h)

        gc = wx.GraphicsContext.Create(dc)
        #gc.SetPen( gc.CreatePen(wx.Pen(wx.Colour(0,0,0,255),1)) )
        gc.SetPen( gc.CreatePen(wx.Pen(wx.Colour(175,175,175,255),1)) )
        #gc.Scale(1./transform.scale,1./-transform.scale) #first transform is applied last
        #gc.Translate(*transform.offset)                   #last transform is applied first

        y_by_t = self.layer.data
        series,periods = y_by_t.shape
        #norm = (y_by_t - y_by_t.mean(0)) / y_by_t.std(0)
        t = numpy.array(range(periods))
        t = (t + ox) * sx
        norm = (y_by_t + oy) * sy
        for s in range(series):
            pts = zip(t,norm[s,:])
            gc.StrokeLines(pts)
        return buff
    def draw_selection(self,transform):
        w,h = transform.pixel_size
        buff = wx.EmptyBitmapRGBA(w,h,alpha=self.trns)
        dc = wx.MemoryDC()
        dc.SelectObject(buff)
        sx,sy = 1./transform.scale,1./-transform.scale
        ox,oy = transform.offset
        #draw time selection
        dc.SetPen(wx.Pen(wx.Colour(255,0,0,255),1))
        t = (self.layer._t + ox) * sx
        dc.DrawLine(t,0,t,h)

        gc = wx.GraphicsContext.Create(dc)
        gc.SetPen( gc.CreatePen(wx.Pen(wx.Colour(0,0,0,255),2)) )
        #gc.Scale(1./transform.scale,1./-transform.scale) #first transform is applied last
        #gc.Translate(*transform.offset)                   #last transform is applied first

        y_by_t = self.layer.data
        sel = list(self.layer.selection)
        sel.sort()
        y_by_t = y_by_t[sel,:]
        series,periods = y_by_t.shape
        #norm = (y_by_t - y_by_t.mean(0)) / y_by_t.std(0)
        t = numpy.array(range(periods))
        t = (t + ox) * sx
        norm = (y_by_t + oy) * sy
        for s in range(series):
            pts = zip(t,norm[s,:])
            gc.StrokeLines(pts)
        return buff
