'''
Created on 2009-10-29

@author: Jing YAO
'''
from numpy import array
from scipy.cluster import vq

class Kmeans(object):
    '''
    K-means clustering
    (1) Select K points as the initial centroids
    (2) Repeat
    (3)     Form K clusters by assigning all points to the closet centroid
            Recompute the centroid of each cluster
    (4) Until The centroids do not change
    
    This class is to wrap the class "scipy.cluster.vq", including some customized functions as well.
    More details can be found at 
    http://docs.scipy.org/doc/scipy/reference/cluster.vq.html

    customized functions:
    (1) dic1(self)
    (2) dic2(self)
    '''


    def __init__(self, obs, k_or_guess, iter=10, thresh=1.0000000000000001e-05, minit='random', missing='warn'):
        '''
        Constructor
        Arguments:
            narrObs(ndarray): a group of observations, represented by an array of vectors
        '''
        self.obs=obs  # obs: the array of the observation vectors.
        self.k_or_guess=k_or_guess # k_or_guess: The number of clusters to form as well as the number of centroids to generate.
                          #Alternatively, passing a k by N array specifies the initial k centroids.    
        #arguments for function kmeans and kmeans2
        self.iter=iter    #Number of iterations of the k-means
        self.thresh=thresh #Terminates the k-means algorithm if the change in distortion since the last k-means iteration is less than thresh.
        self.minit=minit  #Method for initialization.
        self.missing=missing

    def whiten(self, obs):
        '''
        Normalize a group of observations on a per feature basis
        
        Arguments:
            obs(ndarray): Each row of the array is an observation. The columns are the features seen during each observation.
                          Example:
                          #   f0    f1    f2
                    obs = [[  1.,   1.,   1.],  #o0
                           [  2.,   2.,   2.],  #o1
                           [  3.,   3.,   3.],  #o2
                           [  4.,   4.,   4.]]) #o3
        
        Return:
            ndarray: Contains the values in obs scaled by the standard devation of each column        

        Example:
        >>> from numpy import array
        >>> features  = array([[ 1.9,2.3,1.7],[1.5,2.5,2.2],[ 0.8,0.6,1.7]])
        >>> mycls=Kmeans(features,2)
        >>> x=mycls.whiten(features)
        >>> print x
        >>> 
        [[ 4.17944278  2.69811351  7.21248917]
         [ 3.29956009  2.93273208  9.33380951]
         [ 1.75976538  0.7038557   7.21248917]]
        '''
        return vq.whiten(obs)
    
    def vq(self, obs, code_book):
        '''
        Vector Quantization: assign codes from a code book to observations.
        
        Arguments:
            obs(ndarray): Each row of the NxM array is an observation. 
                          The columns are the ¡°features¡± seen during each observation. 
                          The features must be whitened first using the whiten function 
                          or something equivalent.

            code_book(ndarray): The code book is usually generated using the k-means algorithm.
                                Each row of the array holds a different code, and the columns are 
                                the features of the code.
                                Example:
                                    #   f0    f1    f2   f3
                        code_book = [[  1.,   2.,   3.,   4.],  #c0
                                     [  1.,   2.,   3.,   4.],  #c1
                                     [  1.,   2.,   3.,   4.]]) #c2
        
        Return:
            code(ndarray): A length N array holding the code book index for each observation.
            dist(ndarray): The distortion (distance) between the observation and its nearest code        

        Example:
        >>> from numpy import array
        >>> features  = array([[ 1.9,2.3,1.7],[1.5,2.5,2.2],[ 0.8,0.6,1.7]])
        >>> mycls=Kmeans(features,2)
        >>> code_book = array([[1.,1.,1.], [2.,2.,2.]])
        >>> x=mycls.vq(features,code_book)
        >>> print x
        >>> 
        (array([1, 1, 0]), array([ 0.43588989,  0.73484692,  0.83066239]))

        ''' 
        return vq.vq(obs, code_book)
    
    def kmeans(self, obs, k_or_guess, iter=20, thresh=1e-5):
        '''
        Performs k-means on a set of observation vectors forming k clusters. 
        
        Arguments:
            obs(ndarray):Each row of the M by N array is an observation vector. 
                         The columns are the features seen during each observation. 
                         The features must be whitened first with the whiten function.

            k_or_guess(int or ndarray): The number of centroids to generate. 
                                      A code is assigned to each centroid, which is also the row index of the centroid in the code_book matrix generated.
                                     The initial k centroids are chosen by randomly selecting observations from the observation matrix. 
                                     Alternatively, passing a k by N array specifies the initial k centroids.
            iter(int): The number of times to run k-means, returning the codebook with the lowest distortion. 
                       This argument is ignored if initial centroids are specified with an array for the k_or_guess paramter. 
                       This parameter does not represent the number of iterations of the k-means algorithm.
            thresh(float): Terminates the k-means algorithm if the change in distortion since the last k-means iteration is less than thresh.
 
        Returns: 
            codebook(ndarray): A k by N array of k centroids. The i¡¯th centroid codebook[i] is represented with the code i. 
                               The centroids and codes generated represent the lowest distortion seen, not necessarily the globally minimal distortion.
            distortion(float): The distortion between the observations passed and the centroids generated.        
        
        Example:
        >>> from numpy import array
        >>> features  = array([[ 1.9,2.3],
        ...                    [ 1.5,2.5],
        ...                    [ 0.8,0.6],
        ...                    [ 0.4,1.8],
        ...                    [ 0.1,0.1],
        ...                    [ 0.2,1.8],
        ...                    [ 2.0,0.5],
        ...                    [ 0.3,1.5],
        ...                    [ 1.0,1.0]])
        >>> book = array((features[0],features[2]))
        >>> mycls=Kmeans(features,book)
        >>> obs=mycls.whiten(features)
        >>> x=mycls.kmeans(obs,book)
        >>> print x
        >>> 
        (array([[ 2.59540741,  2.23522819],
               [ 0.6728834 ,  1.43391997]]), 0.96294262717442791)
        '''
        return vq.kmeans(obs, k_or_guess, iter, thresh)
        
    def kmeans2(self, data, k, iter=10, thresh=1.0000000000000001e-05, minit='random', missing='warn'):
        '''
        Classify a set of observations into k clusters using the k-means algorithm. 
        
        Arguments:
            data(ndarray): A M by N array of M observations in N dimensions or a length M array of M one-dimensional observations.
            k(int or ndarray): The number of clusters to form as well as the number of centroids to generate. 
                               If minit initialization string is ¡®matrix¡¯, or if a ndarray is given instead, it is interpreted as initial cluster to use instead.
            iter(int): Number of iterations of the k-means algrithm to run. Note that this differs in meaning from the iters parameter to the kmeans function.
            thresh(float): (not used yet).
            minit(string): Method for initialization. Available methods are ¡®random¡¯, ¡®points¡¯, ¡®uniform¡¯, and ¡®matrix¡¯:
                           ¡®random¡¯: generate k centroids from a Gaussian with mean and variance estimated from the data.
                           ¡®points¡¯: choose k observations (rows) at random from data for the initial centroids.
                           ¡®uniform¡¯: generate k observations from the data from a uniform distribution defined by the data set (unsupported).
                           ¡®matrix¡¯: interpret the k parameter as a k by M (or length k array for one-dimensional data) array of initial centroids.
        Returns: 
            centroid(ndarray): A k by N array of centroids found at the last iteration of k-means.
            label(ndarray): label[i] is the code or index of the centroid the i¡¯th observation is closest to.

        Example:
        >>> from numpy import array
        >>> features  = array([[ 1.9,2.3],
        ...                    [ 1.5,2.5],
        ...                    [ 0.8,0.6],
        ...                    [ 0.4,1.8],
        ...                    [ 0.1,0.1],
        ...                    [ 0.2,1.8],
        ...                    [ 2.0,0.5],
        ...                    [ 0.3,1.5],
        ...                    [ 1.0,1.0]])
        >>> book = array((features[0],features[2]))
        >>> mycls=Kmeans(features,book)
        >>> obs=mycls.whiten(features)
        >>> x=mycls.kmeans(obs,book)
        >>> print x
        >>> 
        (array([[ 2.59540741,  2.23522819],
                [ 0.6728834 ,  1.43391997]]), array([0, 0, 1, 1, 1, 1, 0, 1, 1]))
        '''
        return vq.kmeans2(data, k, iter, thresh, minit, missing)
        
    def dic1(self):
        '''
        Using kmeans function, return a dictionary with key representing the index of the clusters, 
        and data(array) representing the index of the observation in each clusters.

        Example:
        >>> from numpy import array
        >>> features  = array([[ 1.9,2.3],
        ...                    [ 1.5,2.5],
        ...                    [ 0.8,0.6],
        ...                    [ 0.4,1.8],
        ...                    [ 0.1,0.1],
        ...                    [ 0.2,1.8],
        ...                    [ 2.0,0.5],
        ...                    [ 0.3,1.5],
        ...                    [ 1.0,1.0]])
        >>> book = array((features[0],features[2]))
        >>> mycls=Kmeans(features,book)
        >>> x=mycls.dic1()
        >>> print x
        >>> 
        {0: [0, 1, 6], 1: [2, 3, 4, 5, 7, 8]}
        '''
        newobs=self.whiten(self.obs)
        tp1=self.kmeans(newobs, self.k_or_guess, self.iter, self.thresh)
        cdbook=tp1[0]
        tp2=self.vq(newobs, cdbook)
        id=tp2[0]
        nobs=len(id)
        dic={}
        k=cdbook.ndim
        for i in range(k):
            dic[i]=[]
        for i in range(nobs):
            dic[id[i]].append(i)
        return dic
            
    def dic2(self):
        '''
        Using kmeans2 function, return a dictionary with key representing the index of the clusters, 
        and data(array) representing the index of the observation in each clusters.

        Example:
        >>> from numpy import array
        >>> features  = array([[ 1.9,2.3],
        ...                    [ 1.5,2.5],
        ...                    [ 0.8,0.6],
        ...                    [ 0.4,1.8],
        ...                    [ 0.1,0.1],
        ...                    [ 0.2,1.8],
        ...                    [ 2.0,0.5],
        ...                    [ 0.3,1.5],
        ...                    [ 1.0,1.0]])
        >>> book = array((features[0],features[2]))
        >>> mycls=Kmeans(features,book)
        >>> x=mycls.dic2()
        >>> print x
        >>> 
        {0: [0, 1, 6], 1: [2, 3, 4, 5, 7, 8]}
        '''
        newobs=self.whiten(self.obs)
        tp=self.kmeans2(newobs, self.k_or_guess, self.iter, self.thresh, self.minit, self.missing)
        id=tp[1]
        nobs=len(id)
        dic={}
        k=tp[0].ndim
        for i in range(k):
            dic[i]=[]
        for i in range(nobs):
            dic[id[i]].append(i)
        return dic

            
if __name__ == '__main__':
    features  = array([[ 1.9,2.3],[ 1.5,2.5],[ 0.8,0.6],[ 0.4,1.8],[ 0.1,0.1],[ 0.2,1.8],[ 2.0,0.5],[ 0.3,1.5],[ 1.0,1.0]])
    book = array((features[0],features[2]))
    mycls=Kmeans(features,book)
    x=mycls.dic2()
    print x
            
            
            
