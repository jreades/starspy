import numpy


class Kernel():

    """Centralized Kernel functions
   
    Parameters
    ----------

    point_array : multitype
                  x,y coordinate pairs with a z-attribute value
    bandwidth   : float or array-like (optional)
                  the bandwidth :math:`h_i` for the kernel. 
    fixed       : binary
                  If true then :math:`h_i=h \\forall i`. If false then
                  bandwidth is adaptive across observations.
    function    : string {'triangular','uniform','quadratic','epanechnikov',
                  'quartic','bisquare','gaussian'}
                  kernel function defined as follows with 

                  .. math::

                      z_{i,j} = d_{i,j}/h_i

                  triangular 

                  .. math::

                      K(z) = (1 - |z|) \ if |z| \le 1

                  uniform 

                  .. math::

                      K(z) = |z| \ if |z| \le 1

                  quadratic 

                  .. math::

                      K(z) = (3/4)(1-z^2) \ if |z| \le 1

                  epanechnikov

                  .. math::

                      K(z) = (1-z^2) \ if |z| \le 1

                  quartic

                  .. math::

                      K(z) = (15/16)(1-z^2)^2 \ if |z| \le 1
                 
                  bisquare

                  .. math::

                      K(z) = (1-z^2)^2 \ if |z| \le 1

                  gaussian

                  .. math::

                      K(z) = (2\pi)^{(-1/2)} exp(-z^2 / 2)
	"""

	def triangular(data, attributes, bandwidth):
		bw = self.bandwith #Bandwidth set from user
		z = [] #This will be the matrix passed into the kernel function
		zs = z #Kernel z-scores after function has been applied
		#What I still can't figure out is how to take an input data array, evaluate its attributes (such as # of events), then create an output matrix.  once we do this, we can then run the kernel function over this array or matrix and should have an output.  Thoughts?
		kernel=[1-z for z in zs]

	def uniform(data, attributes, bandwidth):
		bw = self.bandwith
		z = []
		zs = z
		kernel=z

	def quadratic(data, attributes, bandwidth):
		bw = self.bandwidth
		z = []
		zs = z
		kernel=[(3./4)*(1-z**2) for z in zs]

	def epanechnikov(data, attributes, bandwdith):
		bw = self.bandwidth
		z = []
		zs = z
		kernel=[(1-z**2) for z in zs]

	def quartic(data, attributes, bandwidth):
		bw = self.bandwidth
		z = []
		zs = z
		kernel=[(15./16)*(1-z**2)**2 for z in zs]

	def bisquare(data, attributes, bandwidth):
		z = []
		zs = z
		bw = self.bandwidth
		kernel=[(1-z**2)**2 for z in zs]

	def gaussian(data, attributes, bandwidth):
		z = []
		zs = z
		bw = self.bandwidth
		c=np.pi*2
            	c=c**(-0.5)
            	kernel=[c*np.exp(-(z**2)/2.) for z in zs]
		



