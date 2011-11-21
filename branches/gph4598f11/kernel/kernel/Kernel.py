"This is the first attempt at making this work"

import numpy

class Kernel:
    def __init__(self, points, values, bandwidth):
        self.points = points
        self.values = values
        self.bandwidth = bandwidth
    
    points_array = numpy.array(points)
    dimension = points_array.ndim
    if dimension == 1:
        print "Points has one dimension"
    elif dimension == 2:
        print "Coordinate Pairs"
    else:
        print "Error - too many dimensions in points"

    def Hello(self):
        print "Hello from the Kernel Team"

if __name__ == '__main__':

    points = [1, 2, 3, 4]
    values = [6, 7, 8, 9]
    bandwidth = 2

    k = Kernel(points, values, bandwidth)
    k.Hello()
