"""
wxLayers

wxLayers implement drawing of stars layers in wx
"""
import wx
import numpy
import stars.visualization.layers as layers
from stars.visualization.transforms import WorldToViewTransform
from kernelDensityTime import KernelDensity
from pysal.cg import bbcommon, get_rectangle_rectangle_intersection

class wxPointLayer:
    def __init__(self,layer):
        if not isinstance(layer,layers.PointLayer):
            raise TypeError, "Layer must be instance of PointLayer"
        self.layer = layer
        self.trns = 0
        self.radius = 5
    def draw_set(self,gc,matrix,ids):
        #NOTE: This is w,h not Radius!
        r = self.radius#*transform.scale #see option 2 below
        radius = r/2.0
        data = self.layer.data
        for i in ids:
            pt = data[i]
            ### Two options for drawing points.
            ### First is to Draw with an Ellipse
            x,y = matrix.TransformPoint(*pt)
            gc.DrawEllipse(x-radius,y-radius,r,r)
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
            cs = self.layer.colors
            #cs = {0:(255,0,0)}
        for i,cls in enumerate(cl.classes):
            r,g,b,a = cs[i]
            gc.SetBrush( gc.CreateBrush(wx.Brush(wx.Colour(r,g,b,a))) )
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
        #gc.SetBrush( gc.CreateBrush(wx.Brush(wx.Colour(255,255,0,255), style=wx.CROSSDIAG_HATCH)) )
        gc.SetBrush( gc.CreateBrush(wx.Brush(wx.Colour(255,255,0,255))) )
        matrix = gc.CreateMatrix()
        matrix.Scale(1./transform.scale,1./-transform.scale) #first transform is applied last
        matrix.Translate(*transform.offset)                   #last transform is applied first
        gc = self.draw_set(gc,matrix,self.layer.selection)
        return buff
class wxScatterLayer(wxPointLayer):
    def __init__(self,layer):
        if not isinstance(layer,layers.ScatterLayer):
            raise TypeError, "Layer must be instance of ScatterLayer"
        self.layer = layer
        self.trns = 0
        self.radius = 5
    def draw(self,transform):
        buff = wxPointLayer.draw(self,transform)
        dc = wx.MemoryDC()
        dc.SelectObject(buff)
        ox,oy = transform.world_to_pixel(0,0)
        left,lower,right,upper = transform.extent
        lx,oy = transform.world_to_pixel(left,0)
        rx,oy = transform.world_to_pixel(right,0)
        ox,uy = transform.world_to_pixel(0,upper)
        ox,ly = transform.world_to_pixel(0,lower)

        dc.DrawLine(lx,oy,rx,oy)
        dc.DrawLine(ox,ly,ox,uy)
        for i in range(20): #just a sample of how to draw an ticks, need to draw them using real Majors/Minors.
            dc.DrawLine(ox+(i*20), oy-2, ox+(i*20), oy+2)
            dc.DrawLine(ox-(i*20), oy-2, ox-(i*20), oy+2)
            dc.DrawLine(ox-2, oy+(i*20), ox+2, oy+(i*20))
            dc.DrawLine(ox-2, oy-(i*20), ox+2, oy-(i*20))

        return buff
class wxPolygonLayer:
    def __init__(self,layer):
        if not isinstance(layer,layers.PolygonLayer):
            raise TypeError, "Layer must be instance of PolygonLayer"
        self.layer = layer
        self.trns = 0
    def draw_set(self,pth,ids):
        window = self.transform.extent
        data = self.layer.data
        inside = set([x.id-1 for x in self.layer.locator.overlapping(window)])
        to_draw = inside.intersection(set(ids))
        for i in to_draw:
            poly = data[i]
            # only draw the polygon if it's inside the view window.
            # for very large shapefiles and small view windows, it would be fast to query an rtree.
            #if bbcommon(window,poly.bounding_box):
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
        self.transform = transform
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
            #cs = {0:(255,0,0)}
            cs = self.layer.colors
        for i,cls in enumerate(cl.classes):
            r,g,b,a = cs[i]
            pth = gc.CreatePath()
            pth = self.draw_set(pth,cls)
            pth.Transform(matrix)
            gc.SetBrush( gc.CreateBrush(wx.Brush(wx.Colour(r,g,b,a))) )
            gc.FillPath(pth)
            gc.StrokePath(pth)
        return buff
    def draw_selection(self,transform):
        self.transform = transform
        w,h = transform.pixel_size
        buff = wx.EmptyBitmapRGBA(w,h,alpha=self.trns)
        dc = wx.MemoryDC()
        dc.SelectObject(buff)
        gc = wx.GraphicsContext.Create(dc)
        gc.SetPen( gc.CreatePen(wx.Pen(wx.Colour(0,0,0,255),1)) )
        gc.SetBrush( gc.CreateBrush(wx.Brush(wx.Colour(255,255,0,255), style=wx.CROSSDIAG_HATCH)) )
        matrix = gc.CreateMatrix()
        matrix.Scale(1./transform.scale,1./-transform.scale) #first transform is applied last
        matrix.Translate(*transform.offset)                   #last transform is applied first
        pth = gc.CreatePath()
        pth = self.draw_set(pth,self.layer.selection)
        pth.Transform(matrix)
        gc.FillPath(pth)
        gc.StrokePath(pth)
        return buff
class wxKernelDensityLayer:
    def __init__(self,layer):
        if not isinstance(layer,layers.KernelDensityLayer):
            raise TypeError, "Layer must be instance of KernelDensityLayer"
        self.layer = layer
        self.trns = 0
    def draw_selection(self,transform):
        w,h = transform.pixel_size
        buff = wx.EmptyBitmapRGBA(w,h,alpha=self.trns)
        return buff
    def draw(self,transform):
        kd = self.layer.data

        raster = kd.raster
        img = numpy.zeros((kd.rows,kd.cols,3),numpy.uint8)
        scaled = (raster-raster.min())/(raster.max()-raster.min())
        img[:,:,0] = (scaled*255).astype("B") #red
        img[:,:,2] = ((1+(scaled*-1))*255).astype("B") #blue
        image = wx.EmptyImage(kd.cols,kd.rows)
        image.SetData(img.tostring())
        bitmap = image.ConvertToBitmap()

        w,h = transform.pixel_size
        buff = wx.EmptyBitmapRGBA(w,h,alpha=self.trns)
        dc = wx.MemoryDC()
        dc.SelectObject(buff)
        gc = wx.GraphicsContext.Create(dc)
        gc.Scale(1./transform.scale,1./-transform.scale)
        gc.Translate(*transform.offset)
        left,lower,right,upper = kd.extent
        gc.DrawBitmap(bitmap,left,lower,right-left,upper-lower)
        return buff
class wxCachedPolygonLayer:
    """
    This is a cached layer.
    Each draw is cahced in a buffer. On the next draw, assuming only the scale has changed...
        only the difference between the extents of the old buffer and the new request are drawn.
    """
    def __init__(self,layer):
        if not isinstance(layer,layers.PolygonLayer):
            raise TypeError, "Layer must be instance of PolygonLayer"
        self.cache = {}
        self.cache2 = {} #selection cache, this need to be a little smarter.
        self.layer = layer
        self.trns = 0
    def draw_set(self,pth,ids):
        window = self.transform.extent
        data = self.layer.data
        inside = set([x.id-1 for x in self.layer.locator.overlapping(window)])
        to_draw = inside.intersection(set(ids))
        #print "\tdrawing %d polygons"%len(to_draw)
        for i in to_draw:
            poly = data[i]
            # only draw the polygon if it's inside the view window.
            # for very large shapefiles and small view windows, it would be fast to query an rtree.
            #if bbcommon(window,poly.bounding_box):
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
        """ pre-draw function, calc what needs to be drawn """
        if self.cache:
            oldT = self.cache['transform']
            if (oldT.scale != transform.scale) or not bbcommon(oldT.extent,transform.extent):
                #bad cache, clear it.
               self.cache = {}
            else: # We have a Good cache!
                w,h = transform.pixel_size
                buff = wx.EmptyBitmapRGBA(w,h,alpha=self.trns)
                dc = wx.MemoryDC()
                dc.SelectObject(buff)
                common = get_rectangle_rectangle_intersection(transform.extent,oldT.extent)
                x,y = oldT.world_to_pixel(common.left,common.upper)
                X,Y = oldT.world_to_pixel(common.right,common.lower)
                #print x,y,X,Y
                cw, ch = X-x, Y-y
                dest_x,dest_y = transform.world_to_pixel(common.left,common.upper)
                dc_temp = wx.MemoryDC()
                dc_temp.SelectObject(self.cache['buff'])
                dc.Blit(dest_x,dest_y,cw,ch, dc_temp, x, y)
                dc_temp.SelectObject(wx.NullBitmap)

                region = wx.Region(0,0,w,h)
                region.Subtract(dest_x,dest_y,cw,ch)
                ri = wx.RegionIterator(region)
                while not ri.Rect.Empty:
                    #print "part:", ri.Rect
                    px,py,w,h = ri.Rect
                    pX,pY = px+w, py+h
                    left,upper = transform.pixel_to_world(px,py)
                    right,lower = transform.pixel_to_world(pX,pY)
                    part = self.draw_post(WorldToViewTransform([left,lower,right,upper],w,h))
                    dc_temp.SelectObject(part)
                    dc.Blit(px,py,w,h, dc_temp, 0, 0)
                    ri.Next()
                #del dc_temp
                #dc.SelectObject(wx.NullBitmap)
                #del dc
                self.cache['buff'] = buff
                self.cache['transform'] = transform.copy()
                return buff
        if not self.cache: #populate a new cache.
            self.cache['transform'] = transform.copy()
            buff = self.draw_post(transform)
            self.cache['buff'] = buff #populat the initial cache
            return buff
            
    def draw_post(self,transform):
        self.transform = transform
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
            #cs = {0:(255,0,0)}
            cs = self.layer.colors
        for i,cls in enumerate(cl.classes):
            r,g,b,a = cs[i]
            pth = gc.CreatePath()
            pth = self.draw_set(pth,cls)
            pth.Transform(matrix)
            gc.SetBrush( gc.CreateBrush(wx.Brush(wx.Colour(r,g,b,a))) )
            gc.FillPath(pth)
            gc.StrokePath(pth)
        return buff
    def draw_selection(self,transform):
        self.transform = transform
        w,h = transform.pixel_size
        buff = wx.EmptyBitmapRGBA(w,h,alpha=self.trns)
        dc = wx.MemoryDC()
        dc.SelectObject(buff)
        gc = wx.GraphicsContext.Create(dc)
        gc.SetPen( gc.CreatePen(wx.Pen(wx.Colour(0,0,0,255),1)) )
        gc.SetBrush( gc.CreateBrush(wx.Brush(wx.Colour(255,255,0,255), style=wx.CROSSDIAG_HATCH)) )
        matrix = gc.CreateMatrix()
        matrix.Scale(1./transform.scale,1./-transform.scale) #first transform is applied last
        matrix.Translate(*transform.offset)                   #last transform is applied first
        pth = gc.CreatePath()
        pth = self.draw_set(pth,self.layer.selection)
        pth.Transform(matrix)
        gc.FillPath(pth)
        gc.StrokePath(pth)
        return buff

wxLayers = {'PolygonLayer':wxPolygonLayer,'PointLayer':wxPointLayer,'KernelDensityLayer':wxKernelDensityLayer, 'ScatterLayer':wxScatterLayer}
