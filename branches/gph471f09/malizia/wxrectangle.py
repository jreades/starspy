# This script was written to time the speed of wxPython in drawing
# a large number of random rectangles. 
#
# Written by Nicholas Malizia on December 8, 2009.


import random
import wx
import time
 
start = time.clock()

# A panel class used to draw the rectangles on.
class MyPanel(wx.Panel):

    def __init__(self, parent, id):
        # Create a panel.
        wx.Panel.__init__(self, parent, id)
        self.SetBackgroundColour("white")
 
        # Start the paint event for DrawRectangle()
        self.Bind(wx.EVT_PAINT, self.OnPaint)
 
    def OnPaint(self, evt):
        # Creates the device context for painting. 
        self.dc = wx.PaintDC(self)
        self.dc.Clear()
        self.dc.BeginDrawing()
        self.dc.SetPen(wx.Pen("BLACK",1))
       
         # A loop used to draw a few colorful rectangles...
        for k in range(300):
            self.dc.SetBrush(wx.Brush("blue"))

            # Set random x, y, w, h for rectangle.
            w = random.randint(10, width1/2)
            h = random.randint(10, height1/2)
            x = random.randint(0, width1 - w)
            y = random.randint(0, height1 - h)
            self.dc.DrawRectangle(x, y, w, h)
            self.dc.EndDrawing()

        # Free up the device context.
        del self.dc
 
# Sets the size of the panel.
height1 = 350
width1 = 400
 
app = wx.PySimpleApp()
# create a window/frame, no parent, -1 is default ID
frame = wx.Frame(None, -1, "wxPython Frame", size = (width1, height1))
# call the derived class, -1 is default ID
MyPanel(frame,-1)
# show the frame
frame.Show(True)

elapsed = (time.clock() - start)
print elapsed

# start the event loop
app.MainLoop()

