'''
Created on Mar 6, 2011

@author: dhyou
'''
import sys,math,random,time
from copy import deepcopy 
import numpy as np
#from pylab import *


import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
import wx


class Moran_scatter:


    def __init__(self, figure, gal, y1):
             

        '''
        Read the data from GAL file and calculate x and y value
        Draw the scatter plot to show autocorrelation with a linear line 
        '''
        
        ymean = y1.mean()
        ystd = y1.std()
        z = (y1 - ymean)/ystd
        
        read_gal = open(gal, "r")
        numNode = int(read_gal.readline())
        
        wz = []
        zi = list(z)
        for i in range(numNode):
            loc, num = read_gal.readline().split(" ")
            loc = int(loc)
            num = int(num)
            
            wzi = 0
            temp = read_gal.readline().split(" ")
            for k in temp:
                index = int(k)-1
                wzi += zi[index]/num

            wz.append(wzi)          
            
        
        wz = np.array(wz)
        print z
        print wz
        
        read_gal.close()


        self.figure = figure
        self.axes = self.figure.add_subplot(111)
	    
        
        self.axes.set_xlabel('Zi')
        self.axes.set_ylabel('Wij*Zj')


        self.axes.scatter(z,wz)

        
        slope, yint = self.LineFit(z,wz)
        regression = slope*z + yint
        self.axes.plot(z,regression)
        self.axes.plot(z,0*wz)
        self.axes.plot(0*z, wz)

        
        

    def LineFit(self,x,y):
        """
        Returns slope and y-intercept of linear fit to (x,y) data set
        """
        xavg = x.mean()
        slope = (y*(x-xavg)).sum()/(x*(x-xavg)).sum()
        yint = y.mean()-slope*xavg
        return slope, yint



def main():
    ex = wx.App()
    Moran_scatter(None)
    ex.MainLoop()



if __name__=="__main__":
    main()
    
    

