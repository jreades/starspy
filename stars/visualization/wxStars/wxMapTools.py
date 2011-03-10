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
class rectangleTool(wxMapControl):
    """
    A Generic Rectangle Tool.

    When Active,
        clicking and draging will draw a box.
        on release the tool's 'onRectangle' method will be called.
    """
    def __init__(self):
        wxMapControl.__init__(self)
        self.__start = None
        self.__end = None
    def _onEvent(self,evt):
        if evt.Dragging() and evt.LeftIsDown():
            if self.__start:
                self.mapObj.drawBoxOutline(self.__start,evt.Position)
        if evt.LeftDown(): #state changed to left down
            self.mapObj.CaptureMouse() #capture mouse events even when it leaves the frame.
            self.__start = evt.Position
            self.__end = None
        elif evt.LeftUp():
            if self.mapObj.HasCapture():
                self.mapObj.ReleaseMouse()
            self.__end = evt.Position
            transform = self.mapObj.mapObj
            x,y = self.__start
            X,Y = self.__end
            x,y = transform.pixel_to_world(x,y)
            X,Y = transform.pixel_to_world(X,Y)
            left = min(x,X)
            right = max(x,X)
            lower = min(y,Y)
            upper = max(y,Y)
            self.onRectangle([left,lower,right,upper])
    def onRectangle(self,rect):
        """ Called when the user releases the Mouse Button
        rect -- list -- [left, lower, right, upper] in World Coordinates
        """
        print "onRectangle(%r)"%rect
class rectangleTool2(wxMapControl):
    """
    A Generic Rectangle Tool, bound to the right mouse button.

    When Active,
        clicking and draging will draw a box.
        on release the tool's 'onRectangle' method will be called.
    """
    def __init__(self):
        wxMapControl.__init__(self)
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
        elif evt.RightUp():
            if self.mapObj.HasCapture():
                self.mapObj.ReleaseMouse()
            self.__end = evt.Position
            transform = self.mapObj.mapObj
            x,y = self.__start
            X,Y = self.__end
            x,y = transform.pixel_to_world(x,y)
            X,Y = transform.pixel_to_world(X,Y)
            left = min(x,X)
            right = max(x,X)
            lower = min(y,Y)
            upper = max(y,Y)
            self.onRectangle([left,lower,right,upper])
    def onRectangle(self,rect):
        """ Called when the user releases the Mouse Button
        rect -- list -- [left, lower, right, upper] in World Coordinates
        """
        print "onRectangle(%r)"%rect
class rectangleTool_Persistent(wxMapControl):
    """
    A Generic Rectangle Tool, where the rectangle persists after button release

    When Active,
        clicking and draging will draw a box.
        on release the tool's 'onRectangle' method will be called,
            repeatedly as the mouse is moved.
        right click to cancel.
    """
    evtType = [wx.EVT_MOUSE_EVENTS,wx.EVT_CHAR]
    def __init__(self):
        wxMapControl.__init__(self)
        self.__start = None
        self.__end = None
        self.__brushing = True
    def _onEvent(self,evt):
        evt_type = evt.GetEventType()
        if evt_type == wx.EVT_CHAR.typeId:
            self.onChar(evt)
        elif evt_type in wx.EVT_MOUSE_EVENTS.evtType:
            self.onMouse(evt)
    def onChar(self,evt):
        if evt.GetKeyCode() == wx.WXK_ESCAPE:
            self.__start = None
            self.__end = None
            if self.mapObj.HasCapture():
                self.mapObj.ReleaseMouse()
            self.mapObj.drawBoxOutline()
    def isBrushing(self):
        return self.__brushing
    def enableBrushing(self):
        self.__brushing = True
        self.__start = None
        self.__end = None
    def disableBrushing(self):
        self.__brushing = False
        self.__start = None
        self.__end = None
    def onMouse(self,evt):
        if evt.LeftDown(): #state changed to left down
            self.mapObj.CaptureMouse() #capture mouse events even when it leaves the frame.
            self.__start = evt.Position
            self.__end = None
        elif evt.Dragging() and evt.LeftIsDown():
            self.__end = evt.Position
            self.action(*evt.Position)
        elif evt.LeftUp():
            self.__end = evt.Position
            self.action(*evt.Position)
            if not self.__brushing:
                self.mapObj.drawBoxOutline()
        elif evt.RightDown() or (self.__start == self.__end and self.mapObj.boxoutline): #single click with no movement.
            self.__start = None
            self.__end = None
            if self.mapObj.HasCapture():
                self.mapObj.ReleaseMouse()
            self.mapObj.drawBoxOutline()
        elif self.__start and self.__end and self.__brushing:
            if not self.mapObj.HasCapture():
                self.mapObj.CaptureMouse()
            x,y = evt.Position
            self.action(x,y)
    def action(self,x,y):
        if self.__start and self.__end:
            w,h = (self.__start[0]-self.__end[0], self.__start[1]-self.__end[1])
            X,Y = x+w,y+h
            self.mapObj.drawBoxOutline((x,y),(X,Y))
            transform = self.mapObj.mapObj
            x,y = transform.pixel_to_world(x,y)
            if self.__start == self.__end: #single click.
                return self.onPoint(x,y)
            X,Y = transform.pixel_to_world(X,Y)
            left = min(x,X)
            right = max(x,X)
            lower = min(y,Y)
            upper = max(y,Y)
            self.onRectangle([left,lower,right,upper])

    def onRectangle(self,rect):
        """
        Called as the user draws a rectangle and/or moves a rectangle
        rect -- list -- [left, lower, right, upper] in World Coordinates
        """
        print "onRectangle(%r)"%rect
    def onPoint(self,x,y):
        print "onPoint(%f,%f)"%(x,y)
class selectTool(rectangleTool_Persistent):
    in_rect = False
    def onRectangle(self,rect):
        self.in_rect = True
        rect = pysal.cg.Rectangle(*rect)
        for layer in self.mapObj.mapObj.layers:
            if layer.is_selectable and layer.locator:
                rs = layer.locator.overlapping(rect)
                rs = [x.id-1 for x in rs]
                layer.selection = rs
    def onPoint(self,x,y):
        print "onPoint(%f,%f)"%(x,y)
        if self.in_rect and self.isBrushing():
            self.in_rect = False # keep the current selection.
        else:
            rect = pysal.cg.Rectangle(x,y,x,y)
            for layer in self.mapObj.mapObj.layers:
                if layer.is_selectable and layer.locator:
                    rs = layer.locator.overlapping(rect)
                    rs = [x.id-1 for x in rs]
                    layer.selection = rs
            
class zoomTool(rectangleTool):
    """
    Mouse tool for zooming the map Canvas.
    When Active,
        clicking and draging will draw a zoom box.
        on release the map extent will be set to the extent of the box.
    """
    def onRectangle(self,rect):
        self.mapObj.drawBoxOutline() # Clear the zoom box
        self.mapObj.mapObj.extent = rect #[left,lower,right,upper]
class zoomTool2(rectangleTool2):
    """
    Same as zoomTool, but bound to the right mouse button.
    Mouse tool for zooming the map Canvas.
    When Active,
        clicking and draging will draw a zoom box.
        on release the map extent will be set to the extent of the box.
    """
    def onRectangle(self,rect):
        self.mapObj.drawBoxOutline() # Clear the zoom box
        self.mapObj.mapObj.extent = rect #[left,lower,right,upper]
class animateKD(wxMapControl):
    """
    For Demo Purposes only.
    
    Keyboard tool for animating KernelDensity layers.
    When Active,
        When the 'A' Key is pressed first KernelDensity Layer found will be animated.
    """
    evtType = wx.EVT_CHAR
    def __init__(self):
        wxMapControl.__init__(self)
        self.step = 0
    def _onEvent(self,evt):
        if chr(evt.GetKeyCode()).lower() == 'a':
            for layer in self.mapObj.layers:
                if layer.type == "KernelDensityLayer":
                    if self.step == 0:
                        layer.animate()
                        self.step = layer.animate2()
                    else:
                        self.step = layer.animate2()
                    break
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
