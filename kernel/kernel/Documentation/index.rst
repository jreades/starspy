.. Kernel documentation master file, created by
   sphinx-quickstart on Sat Dec 03 16:52:49 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Kernel's documentation!
==================================

Contents:

.. toctree::
   :maxdepth: 2

.. module:: Kernel
.. class:: Kernel(points[list], bandwidth, resolution)
   :synopsis: Describes the functions housed within Kernel class

This class houses the centralized functions for KDE.  Included are functions that take an input list in the following format: [x1,y1,x2,y2,...,xn,yn] and run a kernel density estimation calculation over these input points.

The following variables are instantiated and stored in the __init__function: these are the input points, the x-coordinates and y-coordinates of the input data, the bandwidth, and the resolution of the output coordinates in question.  Defaults are provided, but can be edited by the user.

The user must input the following when calling this module:

A) Points: a list of points at which observations are made in the format [x1, y1, x2, y2, ..... xn, yn] where n is the total number of observations.
B) Bandwidth: corresponds to the distance over which an observed point affects the grid points around it
C) Resolution: This directly corresponds to the number of grid points at which the user would like to see the output.

"""
Example of inputs needed:
    points = [11, 22, 23, 33, 33, 44, 45, 55]
    b = 2
    r = 10
Will be needed to call:
    k = Kernel(points, b, r)

.. function:: PrepLists()
Preplists take the input list from the user and splits the x- and y- values into separate lists.  Since coordinate pairs create a 2-dimensional output, the x- and y-values will need to be evaluated separately, then combined again near the final step of the kernel calculation.

After this step, the function finds the minimum bounding coordinates of the coverage area, then adds the bandwidth distance as a buffer.  Within this region, effects from the kernel smoothing function are possible.

This sets up the output grid functionality.  The maximum and minimum range values are divided into equal parts by the input resolution value.  This creates an x,y grid, where output kernel values will be returned in the calculation functions.  The values outputgrid_x, and outputgrid_y are stored as the variable names, where each pairing of x,y values will later have a kernel value attached to it.

Users also have the option - in later functions - to access a kernel value at a specific point, so long as that point falls within the bounding coordinates of the output grid.

Values returned from this function are the xvals, yvals, outputgrid_x, and outputgrid_y.

-----
Example:
    points = [11, 22, 23, 33, 33, 44, 45, 55]
    b = 2
    r = 10

    k = Kernel(points, b, r)
    k.preplists()

    This k.preplists() command would create an input xvals of [11,23,33,45] and an input yvals of [22,33,44,55].  In xy space, this would correspond to [(11,22), (23,33), (33,44), and (45,55)]  
    The bandwidth above is '2', so the output x grid would have bounding coordinates of 9 (11-2), and 47 (45+2).  The output y grid would have bounding coordinates of 20 (22-2) and 57 (55+2).  Within this minimum bounding rectangle of (9,20) and (47,57) would contain any possible results of any following kernel function.  The x- and y- grids would be parsed into 10 equal parts, per the resolution, and these become the outputgrid_x and outputgrid_y lists.  These values are returned from the Preplists function to pass into the kernel calculation functions, along with the xvals and yvals variables.

.. function:: calculate(xi, mu, sig, method)

    The calculate function offers three kernel density estimation models: 1) Gaussian (normal distribution), 2) Triangular, and 3) Uniform kernels.  Each conditional statement in the function will calculate a kernel height differently, but each will use: "xi", which is the value for each location from the outputgrid_x or outputgrid_y lists: "mu" which corresponds to each location from the xvals and yvals lists: and "sig", which is the bandwidth value.  The 'method' argument is a numerical key, accessed by later functions to alert the calculate() function to the appropriate condition.

.. function:: gaussian()
   This function applies a normal distribution smoothing function around each xlist or ylist location, then locates each requested x- and y- location in the output grids, and calculates the cumulative height of all gaussian kernel heights at each output grid coordinate pair.  Total height will be the sum of the number of input points' effect, expressed in the 'rows' variable.

   The x- and y- values are evaluated separately, then multiplied to generate a Gaussian kernel height at each output grid location.  Returned from this function is 'r': each coordinate pair in the output grid and its associated kernel height, which is the 'gaus_kernel' variable.

.. function:: gaussian_point(xpoint, ypoint)
   A user must input a desired x- and y- coordinate to call this function, and that point must be within the output grid area in order to impacted by kernel smoothing functions.  If not the case, the function prompts the user to re-enter a valid coordinate pair.
   If passed, then this function works exactly like the gaussian() function, but uses the specific x- and y- points instead of the output grid x- and y- coordinates.  Returned from this function is 'r': the requested coordinate pair and its kernel height, which is the 'gaus_kernel' variable.

.. function:: triangular()
   This function applies a triangular smoothing function around each xlist or ylist location, then locates each requested x- and y- location in the output grids, and calculates the cumulative height of all gaussian kernel heights that originate at all input points over each output grid coordinate pair.  Total height will be the sum of the number of input points' effect, expressed in the 'rows' variable.

   The x- and y- values are evaluated separately, then multiplied to generate a Triangular kernel height at each output grid location.  Returned from this function is 'r': each coordinate pair in the output grid and its associated kernel height, which is the 'tri_kernel' variable.

.. function:: triangular_point(xpoint, ypoint)
   A user must input a desired x- and y- coordinate to call this function, and that point must be within the output grid area in order to impacted by kernel smoothing functions.  If not the case, the function prompts the user to re-enter a valid coordinate pair.
   If passed, then this function works exactly like the triangular() function, but uses the specific x- and y- points instead of the output grid x- and y- coordinates.  Returned from this function is 'r': the requested coordinate pair and its kernel height, which is the 'tri_kernel' variable.

.. function:: uniform()
   This function applies a uniform distribution smoothing function around each xlist or ylist location, then locates each requested x- and y- location in the output grids, and calculates the cumulative height of all uniform kernel heights that originate at all input points over each output grid coordinate pair.  Total height will be the sum of the number of input points' effect, expressed in the 'rows' variable.

   The x- and y- values are evaluated separately, then multiplied to generate a uniform kernel height at each output grid location.  Returned from this function is 'r': each coordinate pair in the output grid and its associated kernel height, which is 'uni_kernel'.

.. function:: uniform_point(xpoint, ypoint)
   A user must input a desired x- and y- coordinate to call this function, and that point must be within the output grid area in order to impacted by kernel smoothing functions.  If not the case, the function prompts the user to re-enter a valid coordinate pair.
   If passed, then this function works exactly like the uniform() function, but uses the specific x- and y- points instead of the output grid x- and y- coordinates.  Returned from this function is 'r': the requested coordinate pair and its kernel height, which is 'uni_kernel'.

Building on the example from earlier, calling the Gaussian function:

    points = [11, 22, 23, 33, 33, 44, 45, 55]
    b = 2
    r = 10

    k = Kernel(points, b, r)
    k.preplists()

    print 'The x-coordinate, y-coordinate, and gaussian kernel values are:', k.gaussian()

Will return an array of 100 x,y coordinate pairs and 100 associated kernel values, starting with
"(9.0, 20.0, 0.01463745789778124), (9.0, 24.111111111111111, 0.013826330006026441), (9.0, 28.222222222222221, 0.0015821466424731905)...(47.0, 52.888888888888886, 0.013826330006026415), (47.0, 57.0, 0.01463745789778124)"

Calling the k.gaussian_point() function using the input x1=30,y1=50 will generate the following result:

"The gaussian kernel value at a specific point is: [ 0.00100357]"



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

