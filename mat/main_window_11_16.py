

#import numpy as np
#import pysal
#import os
#import wx

import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

import numpy as np
import pysal
import os
import wx
from moran_autocorrelation_11_16 import *
from moran_pvalue_11_16 import *
from moran_boxplot_11_16 import *
from moran_permutation_11_16 import *

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

        self.commapath = ""
        self.galpath = ""
        self.mi = None
        self.localmi = None

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fitem1 = fileMenu.Append(wx.ID_ANY, 'Open GAL', 'Open GAL')
        fitem2 = fileMenu.Append(wx.ID_ANY, 'Open TXT', 'Open Attribute')
        fitem3 = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')

        self.Bind(wx.EVT_MENU, self.openGAL, fitem1)
        self.Bind(wx.EVT_MENU, self.openTXT, fitem2)
        self.Bind(wx.EVT_MENU, self.onExit, fitem3)
        
        menubar.Append(fileMenu, '&File')
        
        plotMenu = wx.Menu()
        plot1 = plotMenu.Append(wx.ID_ANY, "Moran's I Scatter", "Show Moran's I Scatter Plot")
        plot2 = plotMenu.Append(wx.ID_ANY, "Moran's I p-values", "Show Moran's I p-values")
        plot3 = plotMenu.Append(wx.ID_EXIT, "Box-Plot", "Show Box-Plot")
	plot4 = plotMenu.Append(wx.ID_ANY, "Permutation of Moran's I", "Show Histogram of Moran's I")

        self.Bind(wx.EVT_MENU, self.showScatter, plot1)
        self.Bind(wx.EVT_MENU, self.showPvalue, plot2)
        self.Bind(wx.EVT_MENU, self.showBoxplot, plot3)
	self.Bind(wx.EVT_MENU, self.showHistogram, plot4)
        
        menubar.Append(plotMenu, '&Plots')
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
        
        
        self.infPanel = wx.Panel(panel, -1)
        figure = Figure(figsize=(6, 4), dpi=80)
#        moran = Moran_scatter(figure)
#        self.figure = moran.figure
        self.figure = figure
        self.canvas = FigureCanvas(self.infPanel, -1, self.figure)
        
        plot = wx.BoxSizer(wx.VERTICAL)
        plot.Add(self.canvas, flag=wx.Left, border=10) 
        
        self.infPanel.SetSizer(plot)
        main.Add(self.infPanel, 0.6, wx.EXPAND | wx.RIGHT, 20)
        panel.SetSizer(main)

        self.SetSize((600, 400))
        self.SetTitle('PySal Plots')
        self.Centre()
        self.Show(True)
        
        
    def showScatter(self,e):
        if self.mi <> None:            
            figure = Figure(figsize=(6, 4), dpi=80)
            moran = Moran_scatter(figure, self.commapath, self.galpath)
            self.figure = moran.figure
            self.canvas = FigureCanvas(self.infPanel, -1, self.figure)        
 
    def showPvalue(self,e):
        if self.localmi <> None:
            figure = Figure(figsize=(6, 4), dpi=80)
            moran = Moran_pvalue(figure, self.localmi)
            self.figure = moran.figure
            self.canvas = FigureCanvas(self.infPanel, -1, self.figure)   
            
    def showBoxplot(self,e):
        if self.localmi <> None:
            figure = Figure(figsize=(6, 4), dpi=80)
            moran = Moran_boxplot(figure, self.y)
            self.figure = moran.figure
            self.canvas = FigureCanvas(self.infPanel, -2, self.figure)   
    
    def showHistogram(self,e):
	if self.mi<> None:
	    figure = Figure(figsize=(6, 4), dpi=80)
	    moran = Moran_histogram(figure,self.mi)
            self.figure = moran.figure
            self.canvas = FigureCanvas(self.infPanel, -1, self.figure)
        
    def openPysal(self):

        if len(self.commapath) > 0 and len(self.galpath) > 0:
            f = pysal.open(self.commapath)
            self.y = np.array(f.by_col['HR8893'])
            print "y-values"
            print self.y
            w = pysal.open(self.galpath).read()
            
            self.mi = pysal.Moran(self.y,w,permutations=9999)
            self.localmi = pysal.Moran_Local(self.y,w)
            print self.mi.I
            print self.mi.EI
            print self.mi.p_norm

    def openGAL(self, e):
        dlg = wx.FileDialog(self,"Choose .gal file",os.getcwd(),"","*.gal",wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.galpath = dlg.GetPath()
            print "%s" %(self.galpath)
            
        dlg.Destroy()
        self.openPysal()
        #self.fileGAL = tkFileDialog.askopenfilename(filetypes = [('.gal files','.gal')], title = 'Open GAL',initialdir='./' )

    def openTXT(self, e):
        wildcard = "Comma Delimited File(.txt)|*.txt|Comma Delimited File(.csv)|*.csv"
        dlg = wx.FileDialog(self,"Choose a comma delimited file",os.getcwd(),"",wildcard,wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.commapath = dlg.GetPath()
            print "%s" %(self.commapath)
            
        dlg.Destroy()
        self.openPysal()
        #self.fileTXT = tkFileDialog.askopenfilename(filetypes = [('.csv files','.txt'),('.csv files','.csv')], title = 'Open Comma Delimited',initialdir='./' )

    def onExit(self, e):
        self.Close()



def main():

    ex = wx.App()
    Project_GPH(None)
    ex.MainLoop() 


if __name__ == '__main__':
    main()
    
    

