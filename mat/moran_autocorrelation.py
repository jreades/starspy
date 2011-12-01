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


class Moran_scatter: #(wx.Frame):

#    def __init__(self, args, **kwargs):
#        super(Moran_scatter, self).__init__(args, **kwargs) 

    def __init__(self, figure, gal, y1):     

        '''
        Constructor
        '''
        #read_data = open("C:/Users/Daehyun You/workspace/Project/stl_hom.txt", "r")
#        read_data = open(comma, "r")
#        read_data.readline()
#        read_data.readline()
#        
#        ch = []
#        for line in read_data:
#            temp = line.split(",")
#            ch.append(float(temp[3]))

#        y = np.array(ch)
#        ymean = y.mean()
#        ystd = y.std()
#        z = (y - ymean)/ystd
#        
#        read_data.close()
        
        
        ymean = y1.mean()
        ystd = y1.std()
        z = (y1 - ymean)/ystd
        
        #read_gal = open("C:/Users/Daehyun You/workspace/Project/stl.gal", "r")
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
        
#        self.canvas = FigureCanvas(self, -1, self.figure)

        
#        figure(1)
#        scatter(z,wz,c='r')
#        
#        slope, yint = self.LineFit(z,wz)
#        regression = slope*z + yint
#        figure(1)
#        self.axes.plot(z,regression)
#        show()


#        self.sizer = wx.BoxSizer(wx.VERTICAL)
#        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
#        self.SetSizer(self.sizer)
#        self.Fit()
#
#
##        panel = wx.Panel(self)
##        
##        panel.SetSizer(self.sizer)
#        self.SetSize((600, 400))
#        self.SetTitle('PySal Plots')
#        self.Centre()
#        self.Show(True)
        

    def LineFit(self,x,y):
        ''' Returns slope and y-intercept of linear fit to (x,y) data set'''
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
    
    

