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

#    def __init__(self, args, **kwargs):
#        super(Moran_scatter, self).__init__(args, **kwargs) 

    def __init__(self, figure, y):     

        '''
        Constructor
        '''
        self.figure = figure
        self.axes = self.figure.add_subplot(111)


#        N = mi.p_sim.size
#        x = np.arange(N)
#        
#        self.axes.scatter(x, mi.p_sim)
#        
#        line = np.ones(N)
#        limit5 = list(0.05*line)
#        self.axes.plot(x,limit5)

#        np.random.seed(2)
#        inc = 0.1
#        e1 = np.random.uniform(0,1, size=(500,))
#        e2 = np.random.uniform(0,1, size=(500,))
#        e3 = np.random.uniform(0,1 + inc, size=(500,))
#        e4 = np.random.uniform(0,1 + 2*inc, size=(500,))       
        
        treatments = [y] #[e1,e2,e3,e4]
        
        #self.axes = self.figure.add_subplot(111)
        pos = np.array(range(len(treatments)))+1
        bp = self.axes.boxplot( treatments, sym='k+', patch_artist=True,
                         positions=pos, bootstrap=5000 )
#        text_transform= mtransforms.blended_transform_factory(self.axes.transData,self.axes.transAxes)
        
        self.axes.set_xlabel('treatment')
        self.axes.set_ylabel('response')
        #self.axes.set_ylim(-0.2, 1.4)
#        self.figure.setp(bp['whiskers'], color='k',  linestyle='-' )
#        self.figure.setp(bp['fliers'], markersize=3.0)
        self.figure.subplots_adjust(right=0.99,top=0.99)






def main():
    ex = wx.App()
    Moran_scatter(None)
    ex.MainLoop()


if __name__=="__main__":
    main()
    
    

