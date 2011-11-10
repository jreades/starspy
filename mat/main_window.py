'''
Created on Mar 6, 2011

@author: dhyou
'''

#from Tkinter import *
#import tkFileDialog

import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure


import wx
from moran_autocorrelation import *

class Project_GPH(wx.Frame):
  
    def __init__(self, *args, **kwargs):
        super(Project_GPH, self).__init__(*args, **kwargs) 
  
                
        self.initUI()
        
    def initUI(self):
      
#        self.parent.title("PySal Plots")
#        
#        menubar = Menu(self.parent)
#        self.parent.config(menu=menubar)
#        
#        fileMenu = Menu(menubar)
#        fileMenu.add_command(label="Open GAL", command=self.openGAL)
#        fileMenu.add_command(label="Open TXT", command=self.openTXT)
#        fileMenu.add_command(label="Exit", command=self.onExit)
#        menubar.add_cascade(label="File", menu=fileMenu)
#
#
#        plotMenu = Menu(menubar)
#        plotMenu.add_command(label="Moran's I Scatter", command=self.openGAL)
#        plotMenu.add_command(label="P-values", command=self.openTXT)
#        plotMenu.add_command(label="Box-Plot", command=self.onExit)
#        menubar.add_cascade(label="Plot", menu=plotMenu)

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fitem1 = fileMenu.Append(wx.ID_ANY, 'Open GAL', 'Open GAL')
        fitem2 = fileMenu.Append(wx.ID_ANY, 'Open TXT', 'Open Attribute')
        fitem3 = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')

        self.Bind(wx.EVT_MENU, self.openGAL, fitem1)
        self.Bind(wx.EVT_MENU, self.openTXT, fitem2)
        self.Bind(wx.EVT_MENU, self.onExit, fitem3)
        
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)


        main = wx.BoxSizer(wx.HORIZONTAL)
        
        panel = wx.Panel(self, -1)
        
        
        stat = wx.BoxSizer(wx.VERTICAL)
        st1 = wx.StaticText(panel, label="Moran's I: ")
        st2 = wx.StaticText(panel, label='Y mean: ')
        st3 = wx.StaticText(panel, label='Y Standard Deviation: ')
        st4 = wx.StaticText(panel, label='Number of points: ')
        stat.Add(st1, flag=wx.RIGHT, border=8)
        stat.Add(st2, flag=wx.RIGHT, border=8)
        stat.Add(st3, flag=wx.RIGHT, border=8)
        stat.Add(st4, flag=wx.RIGHT, border=8)
        
        main.Add(stat, flag=wx.LEFT|wx.EXPAND,border=10)
        
        
        infPanel = wx.Panel(panel, -1)
        figure = Figure(figsize=(6, 4), dpi=80)
        moran = Moran_scatter(figure)
        self.figure = moran.figure
        self.canvas = FigureCanvas(infPanel, -1, self.figure)
        
        plot = wx.BoxSizer(wx.VERTICAL)
        plot.Add(self.canvas, flag=wx.Left, border=10) 
        
        infPanel.SetSizer(plot)
        main.Add(infPanel, 0.6, wx.EXPAND | wx.RIGHT, 20)
        panel.SetSizer(main)

        self.SetSize((600, 400))
        self.SetTitle('PySal Plots')
        self.Centre()
        self.Show(True)
        

        

    def openGAL(self, e):
        print "111"
        #self.fileGAL = tkFileDialog.askopenfilename(filetypes = [('.gal files','.gal')], title = 'Open GAL',initialdir='./' )

    def openTXT(self, e):
        print "222"
        #self.fileTXT = tkFileDialog.askopenfilename(filetypes = [('.csv files','.txt'),('.csv files','.csv')], title = 'Open Comma Delimited',initialdir='./' )

    def onExit(self, e):
        self.Close()



def main():

    ex = wx.App()
    Project_GPH(None)
    ex.MainLoop() 


if __name__ == '__main__':
    main()
    
    

