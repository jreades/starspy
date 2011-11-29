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

import numpy as np
import pysal
import os
import wx
from moran_autocorrelation import *
from moran_pvalue import *
from moran_boxplot import *
from moran_permutation_11_16 import *
from draw_shape import *

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

        self.w = None
        self.galpath = ""
        self.mi = None
        self.localmi = None

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fitem1 = fileMenu.Append(wx.ID_ANY, 'Open GAL', 'Open GAL')
        fitem2 = fileMenu.Append(wx.ID_ANY, 'Open Shapefile', 'Open Shapefile (.shp)')
        fitem3 = fileMenu.Append(wx.ID_ANY, 'Open TXT', 'Open Attribute')
        fitem4 = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')

        self.Bind(wx.EVT_MENU, self.openGAL, fitem1)
        self.Bind(wx.EVT_MENU, self.openSHP, fitem2)
        self.Bind(wx.EVT_MENU, self.openTXT, fitem3)
        self.Bind(wx.EVT_MENU, self.onExit, fitem4)

        
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


        #main = wx.BoxSizer(wx.HORIZONTAL)
        main = wx.GridBagSizer(1, 3)
        
        panel = wx.Panel(self, -1)
        
        
        stat = wx.BoxSizer(wx.VERTICAL)
        
        self.ch1 = wx.ComboBox(panel, size=(150, -1), style=wx.CB_READONLY)
        self.Bind(wx.EVT_COMBOBOX, self.calPysal, self.ch1)
        st1 = wx.StaticText(panel, label="Moran's I: ")
        st2 = wx.StaticText(panel, label='Y mean: ')
        st3 = wx.StaticText(panel, label='Y Standard Deviation: ')
        st4 = wx.StaticText(panel, label='Number of points: ')
        stat.Add(self.ch1, flag=wx.LEFT, border=8)
        stat.Add(st1, flag=wx.LEFT, border=8)
        stat.Add(st2, flag=wx.LEFT, border=8)
        stat.Add(st3, flag=wx.LEFT, border=8)
        stat.Add(st4, flag=wx.LEFT, border=8)
        
        
        
        
        self.infPanel = wx.Panel(panel, -1)
        figure = Figure(figsize=(4, 4), dpi=100)
#        moran = Moran_scatter(figure)
#        self.figure = moran.figure
        self.figure = figure
        self.canvas = FigureCanvas(self.infPanel, -1, self.figure)
        
        plot = wx.BoxSizer(wx.VERTICAL)
        plot.Add(self.canvas, flag=wx.Left, border=10) 
             
        self.infPanel.SetSizer(plot)
        
        

        self.shpPanel = wx.Panel(panel,size=(400,400))
        
        
        main.Add(self.shpPanel, pos=(0,0), flag=wx.RIGHT) # | wx.RIGHT, 600)
        main.Add(self.infPanel, pos=(0,1), flag=wx.EXPAND|wx.RIGHT,border=10)
        main.Add(stat, pos=(0,2), flag=wx.LEFT|wx.EXPAND,border=10)
        
        
        
        panel.SetSizer(main)

        self.SetSize((1100, 480))
        self.SetTitle('PySal Plots')
        self.Centre()
        self.Show(True)
        
        
    def showScatter(self,e):
        if self.mi <> None:            
            figure = Figure(figsize=(4, 4), dpi=100)
            moran = Moran_scatter(figure, self.galpath, self.y)
            self.figure = moran.figure
            self.canvas = FigureCanvas(self.infPanel, -1, self.figure)        
 
    def showPvalue(self,e):
        if self.localmi <> None:
            figure = Figure(figsize=(4, 4), dpi=100)
            moran = Moran_pvalue(figure, self.localmi)
            self.figure = moran.figure
            self.canvas = FigureCanvas(self.infPanel, -1, self.figure)   
            
    def showBoxplot(self,e):
        if self.localmi <> None:
            figure = Figure(figsize=(4, 4), dpi=100)
            moran = Moran_boxplot(figure, self.y)
            self.figure = moran.figure
            self.canvas = FigureCanvas(self.infPanel, -1, self.figure)       

    def showHistogram(self,e):
        if self.mi<> None:
            figure = Figure(figsize=(4, 4), dpi=100)
            moran = Moran_histogram(figure,self.mi)
            self.figure = moran.figure
            self.canvas = FigureCanvas(self.infPanel, -1, self.figure)

    def openSHP(self, e):
        wildcard = "Shape File(.shp)|*.shp"
        dlg = wx.FileDialog(self,"Choose a shape file",os.getcwd(),"",wildcard,wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.shapepath = dlg.GetPath()
            print "%s" %(self.shapepath)
            
            if issubclass(type(self.shapepath),basestring):              
                geo = pysal.open(self.shapepath,'r')          
            self.geo = geo          
    #        if issubclass(type(w),basestring):             
    #            w = pysal.open(w,'r').read()          
    #        self.w = w       
            self.shpPanel = WeightsMap(self,self.geo,self.w) 
            
            fname = self.shapepath.replace(".shp",".dbf")
            self.db = pysal.open(fname,'r')
            self.ch1.AppendItems(self.db.header)
            
        
        dlg.Destroy()


    def openGAL(self, e):
        dlg = wx.FileDialog(self,"Choose .gal file",os.getcwd(),"","*.gal",wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.galpath = dlg.GetPath()
            print "%s" %(self.galpath)
            self.w = pysal.open(self.galpath).read()
            print "self.w"
            print self.w
            
        dlg.Destroy()
        #self.openPysal()
        #self.fileGAL = tkFileDialog.askopenfilename(filetypes = [('.gal files','.gal')], title = 'Open GAL',initialdir='./' )

    def openTXT(self, e):
        wildcard = "Comma Delimited File(.txt)|*.txt|Comma Delimited File(.csv)|*.csv"
        dlg = wx.FileDialog(self,"Choose a comma delimited file",os.getcwd(),"",wildcard,wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            commapath = dlg.GetPath()
            print "%s" %(commapath)
            
            self.db = pysal.open(commapath)
            self.ch1.AppendItems(self.db.header)
            
            
        dlg.Destroy()
        #self.openPysal()
        #self.fileTXT = tkFileDialog.askopenfilename(filetypes = [('.csv files','.txt'),('.csv files','.csv')], title = 'Open Comma Delimited',initialdir='./' )

    def calPysal(self, e):
        i = self.ch1.GetSelection()
        if i > -1 and self.w <> None:
            cname = str(self.ch1.GetString(i))
            self.y = np.array(self.db.by_col[cname])
                
            print "y-values"
            print self.y
#            self.w = pysal.open(self.galpath).read()
            
            self.mi = pysal.Moran(self.y, self.w)
            self.localmi = pysal.Moran_Local(self.y, self.w)
            print self.mi.I
            print self.mi.EI
            print self.mi.p_norm

    def onExit(self, e):
        self.Close()



def main():

    ex = wx.App()
    Project_GPH(None)
    ex.MainLoop() 


if __name__ == '__main__':
    main()
    
    

