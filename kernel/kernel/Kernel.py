"This code calculates the kernel density function values at a series of points"
"The user must input:"
"   A) Points: a list of points at which observations are made in the format [x1, y1, x2, y2, ..... xn, yn] where n is the total number of observations."
"   B) Bandwidth: corresponds to the distance over which an observed point affects the grid points around it"
"   C) Resolution: This directly corresponds to the number of grid points at which the user would like to see the output"

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
            
            outpoints_x = numpy.linspace(lowx, highx, self.resolution)
            outpoints_y = numpy.linspace(lowy, highy, self.resolution)
            outputgrid_x = [0]
            outputgrid_y = [0]
            for i in outpoints_x:
                for j in outpoints_y:
                    outputgrid_x.append(i)
                    outputgrid_y.append(j)
            outputgrid_x.pop(0)
            outputgrid_y.pop(0)

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
        def calculate(self,xi,mu,sig,method):
            if method == 1:   #This corresponds to the Gaussian method
                constant = 1 / (numpy.sqrt(2*numpy.pi * sig*sig))
                exponent = (xi-mu)**2
                exponent /= 2*sig*sig
                returnval = constant * numpy.exp(-exponent)

            elif method == 2:   #This corresponds to the Triangular method
                if (mu-sig) <= xi and (mu+sig) >= xi:
                    z = abs(mu-xi)
                    returnval = (sig-z)/sig
                else:
                    returnval = 0
            
            elif method == 3:    #This corresponds to the Uniform method
                if (mu-sig) <= xi and (mu+sig) >= xi:
                    returnval = 1
                else:
                    returnval = 0

            return returnval

        #Calculate Gaussian Kernel in an output grid
        def gaussian(self):
            x = numpy.array(self.xvals) #Pass x-values into array
            X = numpy.array(self.outputgrid_x) #Set x linespace
            rows = len(self.points)/2
            f = numpy.zeros((rows,X.shape[0]))
            for i,Xi in enumerate(X):
                for j, xj in enumerate(x):
                    f[j,i] = self.calculate(Xi,xj,self.bandwidth,1)
            kernx = numpy.sum(f, axis = 0)        

            y = numpy.array(self.yvals) #Pass y-values into array
            Y = numpy.array(self.outputgrid_y) #Set y linespace
            g = numpy.zeros((rows,Y.shape[0]))
            for i,Yi in enumerate(Y):
                for j, yj in enumerate(y):
                    g[j,i] = self.calculate(Yi,yj,self.bandwidth,1)
            kerny = numpy.sum(g, axis = 0)        

            gaus_kernel = kernx * kerny #Calculate 2-dimensional kernel
            
            r = zip(self.outputgrid_x, self.outputgrid_y, gaus_kernel)
            return r
        
        #Calculate Gaussian Kernel at one user-provided point
        def gaussian_point(self, xpoint, ypoint):
            if xpoint < min(self.outputgrid_x) or xpoint > max(self.outputgrid_x) or ypoint < min(self.outputgrid_y) or ypoint > max(self.outputgrid_y):
                r = "The point you provided lies outside the area of influence of the input points"
            else:    
                x = numpy.array(self.xvals) #Pass input x-values into array
                X = xpoint
                rows = len(self.points)/2
                f = numpy.zeros((rows,1))
                for j, xj in enumerate(x):
                    f[j] = self.calculate(X,xj,self.bandwidth,1)
                kernx = numpy.sum(f, axis = 0)        

                y = numpy.array(self.yvals) #Pass y-values into array
                Y = ypoint
                g = numpy.zeros((rows,1))
                for j, yj in enumerate(y):
                    g[j] = self.calculate(Y,yj,self.bandwidth,1)
                kerny = numpy.sum(g, axis = 0)        

                gaus_kernel = kernx * kerny #Calculate 2-dimensional kernel
            
                r = gaus_kernel

            return r
            
            
        #Calculate Triangular Kernel in an output grid
        def triangular(self):
            x = numpy.array(self.xvals) #Pass x-values into array
            X = numpy.array(self.outputgrid_x) #Set x linespace
            rows = len(self.points)/2
            f = numpy.zeros((rows,X.shape[0]))
            for i,Xi in enumerate(X):
                for j, xj in enumerate(x):
                    f[j,i] = self.calculate(Xi,xj,self.bandwidth,2)
            kernx = numpy.sum(f, axis = 0)        

            y = numpy.array(self.yvals) #Pass y-values into array
            Y = numpy.array(self.outputgrid_y) #Set y linespace
            g = numpy.zeros((rows,Y.shape[0]))
            for i,Yi in enumerate(Y):
                for j, yj in enumerate(y):
                    g[j,i] = self.calculate(Yi,yj,self.bandwidth,2)
            kerny = numpy.sum(g, axis = 0)        

            tri_kernel = kernx * kerny #Calculate 2-dimensional kernel
            
            r = zip(self.outputgrid_x, self.outputgrid_y, tri_kernel)
            return r
           
        #Calculate Triangular Kernel at one user-provided point
        def triangular_point(self, xpoint, ypoint):
            if xpoint < min(self.outputgrid_x) or xpoint > max(self.outputgrid_x) or ypoint < min(self.outputgrid_y) or ypoint > max(self.outputgrid_y):
                r = "The point you provided lies outside the area of influence of the input points"
            else:    
                x = numpy.array(self.xvals) #Pass input x-values into array
                X = xpoint
                rows = len(self.points)/2
                f = numpy.zeros((rows,1))
                for j, xj in enumerate(x):
                    f[j] = self.calculate(X,xj,self.bandwidth,2)
                kernx = numpy.sum(f, axis = 0)        

                y = numpy.array(self.yvals) #Pass y-values into array
                Y = ypoint
                g = numpy.zeros((rows,1))
                for j, yj in enumerate(y):
                    g[j] = self.calculate(Y,yj,self.bandwidth,2)
                kerny = numpy.sum(g, axis = 0)        

                tri_kernel = kernx * kerny #Calculate 2-dimensional kernel
            
                r = tri_kernel

            return r
           
        #Calculate Uniform Kernel in an output grid
        def uniform(self):
            x = numpy.array(self.xvals) #Pass x-values into array
            X = numpy.array(self.outputgrid_x) #Set x linespace
            rows = len(self.points)/2
            f = numpy.zeros((rows,X.shape[0]))
            for i,Xi in enumerate(X):
                for j, xj in enumerate(x):
                    f[j,i] = self.calculate(Xi,xj,self.bandwidth,3)
            kernx = numpy.sum(f, axis = 0)        

            y = numpy.array(self.yvals) #Pass y-values into array
            Y = numpy.array(self.outputgrid_y) #Set y linespace
            g = numpy.zeros((rows,Y.shape[0]))
            for i,Yi in enumerate(Y):
                for j, yj in enumerate(y):
                    g[j,i] = self.calculate(Yi,yj,self.bandwidth,3)
            kerny = numpy.sum(g, axis = 0)        

            uni_kernel = kernx * kerny #Calculate 2-dimensional kernel
            
            r = zip(self.outputgrid_x, self.outputgrid_y, uni_kernel)
            return r
            
        #Calculate Uniform Kernel at one user-provided point
        def uniform_point(self, xpoint, ypoint):
            if xpoint < min(self.outputgrid_x) or xpoint > max(self.outputgrid_x) or ypoint < min(self.outputgrid_y) or ypoint > max(self.outputgrid_y):
                r = "The point you provided lies outside the area of influence of the input points"
            else:    
                x = numpy.array(self.xvals) #Pass input x-values into array
                X = xpoint
                rows = len(self.points)/2
                f = numpy.zeros((rows,1))
                for j, xj in enumerate(x):
                    f[j] = self.calculate(X,xj,self.bandwidth,3)
                kernx = numpy.sum(f, axis = 0)        

                y = numpy.array(self.yvals) #Pass y-values into array
                Y = ypoint
                g = numpy.zeros((rows,1))
                for j, yj in enumerate(y):
                    g[j] = self.calculate(Y,yj,self.bandwidth,3)
                kerny = numpy.sum(g, axis = 0)        

                uni_kernel = kernx * kerny #Calculate 2-dimensional kernel
            
                r = uni_kernel

            return r
            

if __name__ == '__main__':

    points = [11, 22, 23, 33, 33, 44, 45, 55]
    b = 2
    r = 10

    k = Kernel(points, b, r)
    k.preplists()

   # print 'The input/output grid coordinate pairs are', k.preplists()
    print 'The x-coordinate, y-coordinate, and gaussian kernel values are:', k.gaussian()
    print 'The x-coordinate, y-coordinate, and triangular kernel values are:', k.triangular()
    print 'The x-coordinate, y-coordinate, and uniform kernel values are:', k.uniform()

    x1 = 30
    y1 = 50
    x2 = 67
    y2 = 19

    print 'The gaussian kernel value at a specific point is:', k.gaussian_point(x1, y1)
    print 'When the specified point is outside the boundary you get:', k.gaussian_point(x2, y2)
