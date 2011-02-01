'''
Created on Jan 28, 2011

@author: Xing Kang
'''
#!/usr/bin/env python

try:
    import numpy as N
    import numpy.random as RandomArray
    haveNumpy = True
    #print "Using numpy, version:", N.__version__
except ImportError:
            # numpy isn't there
            haveNumpy = False
            errorText = (
            "The FloatCanvas requires the numpy module, version 1.* \n\n"
            "You can get info about it at:\n"
            "http://numpy.scipy.org/\n\n"
            )
      
#---------------------------------------------------------------------------
import wx
from wx.lib.floatcanvas import NavCanvas, FloatCanvas, Resources
import wx.lib.colourdb
import time, random

class FloatCanvasView(wx.Frame):
    
    def __init__(self, parent, id, title, position, size):
        wx.Frame.__init__(self, parent, id, title, position, size)
        self.CreateStatusBar()      # Where Amazing Happens
        
        self.Canvas = FloatCanvas.FloatCanvas(self, Debug = 0, BackgroundColor='Light Grey')
        # Below is a wrapper for the FloatCanvas with a toolbar and a button "Zoom To Fit"
        # NC = NavCanvas.NavCanvas(self, Debug = 0, BackgroundColor='Light Grey')
        
        ## getting all the colors for random objects
        wx.lib.colourdb.updateColourDB()
        self.colors = wx.lib.colourdb.getColourList()
        
        wx.GetApp().Yield(True)
        
        self.drawRandomGraphics()

        self.Canvas.ZoomToBB()

    def drawPoint(self, xy, color, diameter):
        self.Canvas.AddPoint(xy, Color=color, Diameter=diameter)
        
    def drawLine(self, points, width=1.0, color='Black'):
        self.Canvas.AddLine(points, LineWidth=width, LineColor=color)
    
    def drawPolygon(self, points, width=1.0, lineColor='Black', fillColor='Red', fillStyle='Solid'):
        self.Canvas.AddPolygon(points, LineWidth=width, LineColor=lineColor, FillColor=fillColor, FillStyle=fillStyle)
    
    def drawRandomGraphics(self):
        Canvas = self.Canvas
        colors = self.colors
        Range = (-20, 20)
        
        # Canvas.InitAll()
        
        # Polygons
        for i in range(3):
            points = []
            for j in range(random.randint(2,6)):
                point = (random.uniform(Range[0],Range[1]),random.uniform(Range[0],Range[1]))
                points.append(point)
            lw = random.randint(1,6)
            cf = random.randint(0,len(colors)-1)
            cl = random.randint(0,len(colors)-1)
            self.drawPolygon(points, lw, colors[cl], colors[cf])

        # Lines
        for i in range(5):
            points = []
            for j in range(random.randint(2,10)):
                point = (random.randint(Range[0],Range[1]),random.randint(Range[0],Range[1]))
                points.append(point)
            lw = random.randint(1,10)
            cf = random.randint(0,len(colors)-1)
            cl = random.randint(0,len(colors)-1)
            self.drawLine(points, lw, colors[cl])

        # Points
        for i in range(5):
            xy = (random.uniform(Range[0],Range[1]),random.uniform(Range[0],Range[1]))
            D = random.randint(1,50)
            cf = random.randint(0,len(colors)-1)
            self.drawPoint(xy, colors[cf], D)
        
class ViewApp(wx.App):
    
    def __init__(self, *args, **kwargs):
        wx.App.__init__(self, *args, **kwargs)
        
    def OnInit(self):
        wx.InitAllImageHandlers()
        view = FloatCanvasView(None, -1, 'Paint by FloatCanvas', wx.DefaultPosition, (640, 480))
        self.SetTopWindow(view)
        view.Show()
        
        return True

if __name__ == '__main__':
    app = ViewApp(False)
    app.MainLoop()