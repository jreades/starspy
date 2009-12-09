# This python script creates a user interface window that generates a lattice
# landscape based on user-specified parameters. 
#
# Written by Nicholas Malizia on December 8th, 2009.

import wx
import random

class MyFrame(wx.Frame):
   
    # This init function creates the skeleton of the GUI. 
    def __init__(self, parent):

        # A frame is created below. This is the window which houses the interface.
        wx.Frame.__init__(self, parent, -1, "Visualizing Spatial Dependence 2",
         size=(595,510))
       
        # This section creates a panel which holds a radiobox, or
        # a group of radio buttons. Placing it on a panel allows it to
        # move around more easily. 
        self.radiopanel = wx.Panel(self, -1, (10, 75), (200, 100))
        self.radiopanel.options = ['SAR', 'CAR', 'MA']
        self.radiopanel.radiobox = wx.RadioBox(self.radiopanel, -1,
            "Model",(5, 0), choices=self.radiopanel.options, style=wx.VERTICAL)
        self.radiopanel.radiobox.SetSelection(0)

        # This section creates a static box and puts a drop down box inside
        # where the user can specify a value for rho. The rholist gives a list
        # of all possible values for the user to select from. In contrast to the 
        # radio panel above, this is not placed on a panel but directly on the 
        # frame.
        rholist = ("-0.9", "-0.8", "-0.7", "-0.6", "-0.5", "-0.4", 
                    "-0.3", "-0.2", "-0.1", "0", "0.1", "0.2", "0.3",                               "0.4", "0.5", "0.6", "0.7", "0.8", "0.9")
        wx.StaticBox(self, -1, 'Rho', (15, 180), (80, 60))
        self.dependence = wx.ComboBox(self, -1, value=rholist[9], 
                        pos=(19, 205), size=(70, -1), 
                        choices=(rholist), style=wx.CB_READONLY)


        # This code creates the spin control and surrounding box used
        # to set the dimensions of the landscape. Again this is placed directly
        # on the frame.
        wx.StaticBox(self, -1, 'Dimension', (15, 10), (80, 55))
        self.dimensions = wx.SpinCtrl(self, -1, '', (20, 30), (60, -1))
        self.dimensions.SetRange(2, 20)
        self.dimensions.SetValue(5)

        
        # This code creates the two buttons in the frame.
        # See below for the functions "OnDraw" and "OnClose."
        # I found event management associated with buttons, the mouse, and 
        # widgets to be extremely simple in wxPython.        
        wx.Button(self, 1, 'Draw',(20, 260))
        wx.EVT_BUTTON (self, 1, self.OnDraw)
        wx.Button(self, 2, 'Quit', (20, 290))   
        wx.EVT_BUTTON (self, 2, self.OnClose)
        

        # This creates a panel on which the landscape is drawn.
        # I endowed it with a ToolTip that will only be 
        # active over only this panel. 
        self.drawpanel = wx.Panel(self, -1, (120, 10), (470, 470))
        self.drawpanel.SetBackgroundColour(wx.NullColor)
        self.drawpanel.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.drawpanel.SetToolTip(wx.ToolTip("I'm a ToolTip!"))
        
        
        # These variables are initialized for use in the next section
        # by the text panel.  
        
        model = ""
        rho = ""
        count = ""
        wcount = ""
        bcount = ""

        countlabel = ""
        wcountlabel = ""
        bcountlabel = ""
        modellabel = ""
        rholabel = ""


        # This section creates a panel on which text is written broadcasting 
        # the results of the landscape generation. 
        self.textpanel = wx.Panel(self, -1, (10, 340), (100, 150))
        self.textpanel.SetBackgroundColour(wx.NullColour)


        # This section writes text to describe the landscape that
        # was generated. 
        self.textpanel.model = wx.StaticText(self.textpanel, -1, model, 
            (56, 5))
        self.textpanel.rho = wx.StaticText(self.textpanel, -1, rho, 
            (43, 25))
        self.textpanel.count = wx.StaticText(self.textpanel, -1, count, 
            (54, 65))
        self.textpanel.wcount = wx.StaticText(self.textpanel, -1, wcount, 
            (52, 85))
        self.textpanel.bcount = wx.StaticText(self.textpanel, -1, bcount, 
            (51, 105))


        self.textpanel.modellabel = wx.StaticText(self.textpanel, -1, 
            modellabel, (10, 5))
        self.textpanel.rholabel = wx.StaticText(self.textpanel, -1,                         rholabel, (10, 25))
        self.textpanel.countlabel = wx.StaticText(self.textpanel, -1,                       countlabel, (10, 65))
        self.textpanel.wcountlabel = wx.StaticText(self.textpanel, -1,                      wcountlabel, (10, 85))
        self.textpanel.bcountlabel = wx.StaticText(self.textpanel, -1,                      bcountlabel, (10, 105))

        # This places the frame in the center of the screen. 
        self.Centre()


    # This function generates the landscape drawing and updates the 
    # appropriate text. 
    def OnDraw(self, event):
        dc = wx.PaintDC(self.drawpanel)
        dc.Clear()
        dc.BeginDrawing()
        dc.SetPen(wx.Pen("red",1))

        # This examines the input widgets and gets the new values for the
        # parameters of the landscape. 
        choice = self.radiopanel.radiobox.GetSelection()
        m = self.radiopanel.options[choice]
        rhotext = self.dependence.GetValue()
        
        # This determines the number of squares in the grid and then uses the
        # information to adjust the size of the squares relative to the
        # size of the size of the DC.
        n = self.dimensions.GetValue()

        h = (460 + n)/n
        w = (460 + n)/n

        black = 0
        white = 0
        
        # Sets the starting x value for drawing within the DC.
        x = 0
         
        # The loop which draws the squares on the squares on the DC.  
        for i in range (n):

            #Sets the starting y value for drawing within the DC. 
            y = 0

            for j in range (n):
                # Sets the background color randomly to black or white.
                c = random.randrange(2)
                if c == 1:
                    dc.SetBrush(wx.Brush('black'))
                    black = black + 1

                else:
                    dc.SetBrush(wx.Brush('white'))
                    white = white + 1

                # Sets the dimensions and position for the current square.
                dc.DrawRectangle(x, y, w, h)
                dc.EndDrawing()

                # Moves the drawing position for the square. 
                y = y + h -1

            x = x + w -1

        # This section writes the description of the new landscape. 
        self.textpanel.count.SetLabel(str(n**2))
        self.textpanel.wcount.SetLabel(str(white))
        self.textpanel.bcount.SetLabel(str(black))
        self.textpanel.model.SetLabel(m)
        self.textpanel.rho.SetLabel(str(rhotext))

        self.textpanel.countlabel.SetLabel("Count:")
        self.textpanel.wcountlabel.SetLabel("White:")
        self.textpanel.bcountlabel.SetLabel("Black:")
        self.textpanel.modellabel.SetLabel("Model:")
        self.textpanel.rholabel.SetLabel("Rho:")

 
    # This function gets the x, y coordinates when the mouse is right clicked.
    # I wanted to explore this more so that I could return the values of the 
    # polygon that was clicked on but I could not get this functioning properly.
    def OnRightDown(self, event):
        """right mouse button is pressed"""
        pt = event.GetPosition()
        print pt


    # This function closes the application.     
    def OnClose(self, event):
        self.Close(True)

 
 
app = wx.PySimpleApp()
frame = MyFrame(None)
frame.Show()
app.MainLoop()

