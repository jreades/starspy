"This is the first attempt at making this work"

import numpy

class Kernel:
        def __init__(self, points, bandwidth=2, resolution=10):
            self.points = points
            self.bandwidth = bandwidth
            self.resolution = resolution
            self.xvals = []
            self.yvals = []

        def preplists(self):

            #Start by separating the input points into x and y values
            coords = self.points
            #points_array = numpy.array(points)
            loop = [0]
            for i in range((len(coords))/2):
                    loop.append(i*2)
            loop.pop(0)
            loop.pop(0)
            x1 = coords[0]
            xvals = [x1]
            y1 = coords[1]
            yvals = [y1]
            for i in loop:
                    x = coords[i]
                    y = coords[i+1]
                    xvals.append(x)
                    yvals.append(y)

            #Find the extents of the bounding rectangle
            lowx = min(xvals) - self.bandwidth
            highx = max(xvals) + self.bandwidth
            lowy = min(yvals) - self.bandwidth
            highy = max(yvals) + self.bandwidth

            #Create a set of output x and y values (for the output grid)
            
            outputgrid_x = numpy.linspace(lowx, highx, self.resolution)
            outputgrid_y = numpy.linspace(lowy, highy, self.resolution)

            #Zips the x, y values for the output grid together to create
	    #coordinate pairs.  We may not need this, but we can append
	    #z-values later if we want	
            #r = zip(outputgrid_x, outputgrid_y)
            
            self.outputgrid_x = outputgrid_x
            self.outputgrid_y = outputgrid_y
            self.xvals = xvals
            self.yvals = yvals

            return outputgrid_x, outputgrid_y, xvals, yvals
            
        #Function for Gaussian calculation
        def normd(self,xi,mu,sig):
            constant = 1 / (numpy.sqrt(2*numpy.pi * sig*sig))
            exponent = (xi-mu)**2
            exponent /= 2*sig*sig
            return constant * numpy.exp(-exponent)

        #Calculate Gaussin Kernel
        def gaussian(self):
            x = numpy.array(self.xvals) #Pass x-values into array
            X = self.outputgrid_x #Set x linespace
            rows = len(self.points)/2
            f = numpy.zeros((rows,X.shape[0]))
            for i,Xi in enumerate(X):
                for j, xj in enumerate(x):
                    f[j,i] = self.normd(Xi,xj,self.bandwidth)
            kernx = numpy.sum(f, axis = 0)        

            y = numpy.array(self.yvals) #Pass y-values into array
            Y = self.outputgrid_y #Set y linespace
            g = numpy.zeros((rows,Y.shape[0]))
            for i,Yi in enumerate(Y):
                for j, yj in enumerate(y):
                    g[j,i] = self.normd(Yi,yj,self.bandwidth)
            kerny = numpy.sum(g, axis = 0)        

            gaus_kernel = kernx * kerny #Calculate 2-dimensional kernel
            
            r = zip(self.outputgrid_x, self.outputgrid_y, gaus_kernel)
            return r
                    
            #Now we just need to find the kernel value at each output grid x,y    

if __name__ == '__main__':

    points = [11, 22, 23, 33, 33, 44, 45, 55]
    b = 2
    r = 10

    k = Kernel(points, b, r)
    k.preplists()
    #test1 = k.gaussian()
    #print test1

   # print 'The input/output grid coordinate pairs are', k.preplists()
    print 'The x-coordinate, y-coordinate, and gaussian kernel values are:', k.gaussian()
