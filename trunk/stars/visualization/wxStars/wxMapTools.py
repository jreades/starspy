import pysal
import numpy
import random
import wx

class wxMapControl(object):
    """ Base class for MapControls, aka Tools """
    evtType = wx.EVT_MOUSE_EVENTS
    def __init__(self,enabled=True):
        self._enabled = True
    def enable(self):
        self._enabled = True
    @property
    def enabled(self):
        return self._enabled
    def disable(self):
        self._enabled = False
    def setMap(self,mapObj):
        self.mapObj = mapObj
    def onEvent(self,evt):
        if self._enabled:
            self._onEvent(evt)
            evt.Skip()
class panTool(wxMapControl):
    """
    Mouse tool for panning the map Canvas.
    When Active,
        clicking and draging will pan the map.
    """
    def __init__(self):
        wxMapControl.__init__(self)
        self._prev_position = None
    def _onEvent(self,evt):
        if evt.Dragging() and evt.LeftIsDown():
            if self._prev_position:
                x,y = self._prev_position
                X,Y = evt.Position
                px,py = (X-x),(Y-y)
                self.mapObj.pan(px,py)
        if evt.LeftDown(): #state changed to left down
            self.mapObj.CaptureMouse() #capture mouse events even when it leaves the frame.
        if evt.LeftUp():
            if self.mapObj.HasCapture():
                self.mapObj.ReleaseMouse()
        self._prev_position = evt.Position
class zoomTool(wxMapControl):
    """
    Mouse tool for zooming the map Canvas.
    When Active,
        clicking and draging will draw a zoom box.
        on release the map extent will be set to the extent of the box.
    """
    def __init__(self):
        wxMapControl.__init__(self)
        self._prev_position = None
        self.__start = None
        self.__end = None
    def _onEvent(self,evt):
        if evt.Dragging() and evt.RightIsDown():
            if self.__start:
                self.mapObj.drawBoxOutline(self.__start,evt.Position)
        if evt.RightDown(): #state changed to left down
            self.mapObj.CaptureMouse() #capture mouse events even when it leaves the frame.
            self.__start = evt.Position
            self.__end = None
        if evt.RightUp():
            if self.mapObj.HasCapture():
                self.mapObj.ReleaseMouse()
            self.__end = evt.Position
            transform = self.mapObj.mapObj
            dx,dy = self.mapObj.pan_offset
            x,y = self.__start
            x-=dx
            y-=dy
            X,Y = self.__end
            X-=dx
            Y-=dy
            x,y = transform.pixel_to_world(x,y)
            X,Y = transform.pixel_to_world(X,Y)
            left = min(x,X)
            right = max(x,X)
            lower = min(y,Y)
            upper = max(y,Y)
            self.mapObj.mapObj.extent = [left,lower,right,upper]
class randomSelction(wxMapControl):
    """
    For Demo Purposes only.
    
    Keyboard tool for selecting random regions in each layer.
    When Active,
        When the 'R' Key is pressed n (default 10) random regions will be selected in each layer.
    """
    evtType = wx.EVT_CHAR
    def __init__(self,n=10):
        wxMapControl.__init__(self)
        self.n = n
    def _onEvent(self,evt):
        if chr(evt.GetKeyCode()).lower() == 'r':
            for layer in self.mapObj.layers:
                layer.selection = random.sample(range(len(layer)),self.n)
class randomClassification(wxMapControl):
    """
    For Demo Purposes only.
    
    Keyboard tool for randomly classifing the map.
    When Active,
        When the 'C' Key is pressed a random classification (with k classes, default 5) will be applied in each layer.
    """
    evtType = wx.EVT_CHAR
    def __init__(self,k=5):
        wxMapControl.__init__(self)
        self.k = k
    def _onEvent(self,evt):
        if chr(evt.GetKeyCode()).lower() == 'c':
            for layer in self.mapObj.layers:
                n = len(layer.data)
                data = numpy.array([random.random() for i in range(n)])
                layer.classification = pysal.esda.mapclassify.Natural_Breaks(data,k=self.k)
class randomPalette(wxMapControl):
    """
    For Demo Purposes only.
    
    Keyboard tool for randomly assigning a color Palette.
    When Active,
        When the 'P' Key is pressed a random Palette (with k classes, default 5) will be applied to each layer.
    """
    evtType = wx.EVT_CHAR
    def __init__(self,k=5):
        wxMapControl.__init__(self)
        self.k = k
    def _onEvent(self,evt):
        if chr(evt.GetKeyCode()).lower() == 'p':
            for layer in self.mapObj.layers:
                layer.colors = dict([(i,[random.randint(0,255) for i in range(3)]) for i in range(5)])
class zoomWorld(wxMapControl):
    """
    Keyboard tool for zooming the full extent of the map.
    When Active,
        When the 'Z' Key is pressed the map extent will be set the full extent of the layers.
    """
    evtType = wx.EVT_CHAR
    def _onEvent(self,evt):
        if chr(evt.GetKeyCode()).lower() == 'z':
            self.mapObj.pan_offset = 0,0
            self.mapObj.mapObj.zoom_to_world()
