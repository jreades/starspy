'''
Created on Mar 6, 2011

@author: dhyou
'''
import sys,math,random,time
from copy import deepcopy 
import numpy as np


import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
import wx


class Moran_pvalue: #(wx.Frame):


 

    def __init__(self, figure, mi):     

        '''
        Receive a figure object and local moran's value from main_window
        Draw the scatter plot to show p-avlues with 5% line
        p-values are obtained from the PySal function of moran.p_sim 
        '''
        self.figure = figure
        self.axes = self.figure.add_subplot(111)
	self.axes.set_xlabel('x Values')
	self.axes.set_ylabel('P Values')


        N = mi.p_sim.size
        x = np.arange(N)
        
        color = []
        for i in range(N):
            if mi.p_sim[i] < 0.05:
                color.append(100)
            else:
                color.append(10)
        
        
        self.axes.scatter(x, mi.p_sim, c=color)
        
        self.axes.set_xlabel('x Values')
        self.axes.set_ylabel('P Values')
        self.axes.set_xlim(-5,N+5)
        
        line = np.ones(N)
        limit5 = list(0.05*line)
        self.axes.plot(x,limit5,linewidth=2.0)


def main():
    ex = wx.App()
    Moran_scatter(None)
    ex.MainLoop()


if __name__=="__main__":
    main()
    
    

