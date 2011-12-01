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

#    def __init__(self, args, **kwargs):
#        super(Moran_scatter, self).__init__(args, **kwargs) 

    def __init__(self, figure, mi):     

        '''
        Constructor
        '''
        self.figure = figure
        self.axes = self.figure.add_subplot(111)
	self.axes.set_xlabel('x Values')
	self.axes.set_ylabel('P Values')


        N = mi.p_sim.size
        x = np.arange(N)
        
        self.axes.scatter(x, mi.p_sim)
        
        line = np.ones(N)
        limit5 = list(0.05*line)
        self.axes.plot(x,limit5)


def main():
    ex = wx.App()
    Moran_scatter(None)
    ex.MainLoop()


if __name__=="__main__":
    main()
    
    

