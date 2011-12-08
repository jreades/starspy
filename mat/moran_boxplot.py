'''
Created on Mar 6, 2011

@author: dhyou
'''
import sys,math,random,time
from copy import deepcopy 
import numpy as np
#from numpy.random import *


import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
import wx


class Moran_boxplot: #(wx.Frame):


 

    def __init__(self, figure, y):     

        '''
        Receive a figure object and the selected variable from main_window
        Draw a box-plot to show outliers. 
        '''
        self.figure = figure
        self.axes = self.figure.add_subplot(111)




        











       
        
        treatments = [y] 
        

        pos = np.array(range(len(treatments)))+1
        bp = self.axes.boxplot( treatments, sym='k+', patch_artist=True,
                         positions=pos, bootstrap=5000 )

        
        self.axes.set_xlabel('Treatment')
        self.axes.set_ylabel('Response')



        self.figure.subplots_adjust(right=0.95,top=0.95)






def main():
    ex = wx.App()
    Moran_scatter(None)
    ex.MainLoop()


if __name__=="__main__":
    main()
    
    

