

import pysal
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

class Moran_histogram:
  
      def __init__(self, figure, mi):
    	 self.figure = figure
    	 self.axes = self.figure.add_subplot(111)
	 #mi = pysal.Moran(y,  w, permutations=9999)




         # the histogram of the data
         n, bins, patches = self.axes.hist(mi.sim, 50, normed=1, facecolor='green', alpha=0.9)

         # add a 'best fit' line
         y = mlab.normpdf(bins, mi.EI_sim, mi.sim.std())
         l = self.axes.plot(bins, y, 'r--', linewidth=1)
         l2 = self.axes.plot(mi.I*np.ones(20), max(n)*np.array(range(20))/19, 'b', linewidth =2)

         self.axes.set_xlabel('Permutation')
         self.axes.set_ylabel('Density')
         # plt.title(r"Permutation of Moran's I")
         #self.axes.grid(True)

         #plt.show()


def main():
    ex = wx.App()
    Moran_histogram(None)
    ex.MainLoop()




if __name__=="__main__":
    main()





