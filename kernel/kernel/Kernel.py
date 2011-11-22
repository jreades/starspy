"This is the first attempt at making this work"

import numpy

class Kernel:
        def __init__(self, points, bandwidth=2, resolution=10):
            self.points = points
            self.bandwidth = bandwidth
            self.resolution = resolution

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
            xspacing = int((highx - lowx)/self.resolution)

            outputgrid_x = []
            outputgrid_x.append(lowx)

            for i in range(lowx, highx, self.resolution):
                xx = i + xspacing
                outputgrid_x.append(xx)

            yspacing = int((highy - lowy)/self.resolution)

            outputgrid_y = []
            outputgrid_y = [lowy]

            for i in range(lowy, highy, self.resolution):
                yy = i + yspacing
                outputgrid_y.append(yy)

            #Zips the x, y values for the output grid together to create
	    #coordinate pairs.  We may not need this, but we can append
	    #z-values later if we want	
            r = zip(outputgrid_x, outputgrid_y)

            return r
 

    #Now we just need to find the kernel value at each output grid x,y    

if __name__ == '__main__':

    points = [11, 22, 23, 33, 33, 44, 45, 55]
    b = 2
    r = 10

    k = Kernel(points, b, r)
    print 'The input x values are', #xvals
    print 'The input y values are', #yvals
    print 'The output grid x values are', #outputgrid_x
    print 'The output grid y values are', #outputgrid_y
    print 'The output grid coordinate pairs are', k.preplists()
