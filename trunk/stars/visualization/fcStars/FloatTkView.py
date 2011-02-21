'''
Created on Feb 3, 2011

@author: Xing Kang
'''

BG='gray'
LEGEND_WIDTH=50
BUFFER=0.05
LINE_COLORS='blue','green','red','yellow','cyan','magenta','purple'

import projections
import wx
from wx.lib.floatcanvas import NavCanvas, FloatCanvas, Resources
import wx.lib.colourdb
import time, random

class FloatView(wx.Frame):
    
    def __init__(self, parent, id, title, position, size, dynamic_Size=True):
        wx.Frame.__init__(self, parent, id, title, position, size)
        
        self.master = parent
        self.width, self.height = size
        
        height = self.height
        width = self.width
        if dynamic_Size:
            w = min(self.GetMaxSize())
            w /= 2.0
            width = w
            height = w
        
        self.canvas = FloatCanvas.FloatCanvas(self, size=(width, height), BackgroundColor=BG, Debug=0)
        canSize = self.canvas.GetSizeTuple()
        self.width, self.height = canSize
        self.title = title
        
        self.Bind(wx.EVT_SIZING, self.onSizing)
        if self.master:
            self.master.SetTitle(title)
        
        self.makeMenu()
        
    def onSizing(self):
        pass
    
    def makeMenu(self):
        menuBar = wx.MenuBar()
        self.menuBar = menuBar
        
        self.fileMenu()
        self.legendMenu()
        
        self.SetMenuBar(menuBar)
        
    def fileMenu(self):
        menu = wx.Menu()
        fItem = wx.MenuItem(menu, -1, '&Save', 'Click to save file')
        menu.AppendItem(fItem)
        
        menu.AppendSeparator()
        
        fItem1 = wx.MenuItem(menu, -1, '&Quit', 'Quit the program')
        self.Bind(wx.EVT_MENU, self.quit, fItem1)
        menu.AppendItem(fItem1)
        
        self.menuBar.Append(menu, "&File")

    def legendMenu(self):
        menu1 = wx.Menu()
        lItem = wx.MenuItem(menu1, -1, 'Show Legend', 'Click to see legend')
        menu1.AppendItem(lItem)
        
        lItem1 = wx.MenuItem(menu1, -1, 'Hide Legend', 'Click to invisible legend')
        menu1.AppendItem(lItem1)
        
        self.menuBar.Append(menu1, "&Legend")
    
    def quit(self, event):
        return self.Destroy()

if __name__ == '__main__':
    app = wx.PySimpleApp()
    view = FloatView(None, -1, 'New Frame', wx.DefaultPosition, (1024, 768))
    app.SetTopWindow(view)
    view.Show()
    app.MainLoop()