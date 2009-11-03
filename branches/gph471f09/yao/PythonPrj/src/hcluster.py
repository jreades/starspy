'''
Created on 2009-10-31

@author: Jing YAO
'''
from numpy import array

from scipy.cluster import hierarchy

from scipy.spatial import distance

#import matplotlib

class HCluster(object):
    '''
    Hierarchical clustering
    (1) Compute the proximity matrix
    (2) Let each data point be a cluster
    (3) Repeat
    (4)        Merge the two closest clusters
    (5)        Update the proximity matrix
    (6) Until only a single cluster remains
    
    This class is to wrap the class "scipy.cluster.hierarchy", including some customized functions as well.
    More details can be found at 
    http://docs.scipy.org/doc/scipy/reference/cluster.hierarchy.html

    customized functions:
    (1) allClusters(self, Z)
    (2) getChildren(self, Z, index)
    (3) expandClusters(self, Z
    (4) kClusters(self, Z, k)
    (5) kClusters2(self, Z, k)
    (5) compareLists(self, L1, L2)
    (6) minCluster(self, Z, L)
    (7) obsToClusters(self, Z, L)

    '''


    def __init__(self,data):
        '''
        Arguments:
            data : ndarray, the n by m matrix representing original observations.
        
                
        '''
        self.obs=data
    
    #These functions cut hierarchical clusterings into flat clusterings or 
    #find the roots of the forest formed by a cut by providing the flat cluster ids 
    #of each observation.

    #(1)fcluster: forms flat clusters from hierarchical clusters. 
    #(2)fclusterdata: forms flat clusters directly from data. 
    #(3)leaders: singleton root nodes for flat cluster. 
    
    def fcluster(self, Z, t, criterion='inconsistent', depth=2, R=None, monocrit=None):
        '''
        Forms flat clusters from the hierarchical clustering defined by the linkage matrix Z. 
        The threshold t is a required parameter.
        
        Arguments: 
            Z : ndarray The hierarchical clustering encoded with the matrix returned by the linkage function.
            t : double The threshold to apply when forming flat clusters.
            criterion : string (optional) The criterion to use in forming flat clusters. 
                This can be any of the following values:
                'inconsistent': If a cluster node and all its decendents have an inconsistent value less than 
                    or equal to t then all its leaf descendents belong to the same flat cluster. 
                    When no non-singleton cluster meets this criterion, every node is assigned to its own cluster. 
                    (Default)
                'distance': Forms flat clusters so that the original observations in each flat cluster have no 
                    greater a cophenetic distance than t.
                'maxclust': Finds a minimum threshold r so that the cophenetic distance between any two original 
                    observations in the same flat cluster is no more than r and no more than t flat clusters are formed.
                'monocrit': Forms a flat cluster from a cluster node c with index i when monocrit[j] <= t.
                 'maxclust_monocrit': Forms a flat cluster from a non-singleton cluster node c when monocrit[i] <= r 
                     for all cluster indices i below and including c. r is minimized such that no more than t flat 
                     clusters are formed. monocrit must be monotonic. 
            depth : int (optional) The maximum depth to perform the inconsistency calculation. It has no meaning 
                for the other criteria. (default=2) 
            R : ndarray (optional) The inconsistency matrix to use for the 'inconsistent' criterion. 
                This matrix is computed if not provided. 
            monocrit : ndarray (optional) A (n-1) numpy vector of doubles. monocrit[i] is the statistics upon which 
                non-singleton i is thresholded. 
        Returns: 
            T : ndarray A vector of length n. T[i] is the flat cluster number to which original observation i belongs.

        Example:
            >>> features  = array([[ 1.9,2.3],
            ...                    [ 1.5,2.5],
            ...                    [ 0.8,0.6],
            ...                    [ 0.4,1.8],
            ...                    [ 0.1,0.1],
            ...                    [ 0.2,1.8],
            ...                    [ 2.0,0.5],
            ...                    [ 0.3,1.5],
            ...                    [ 1.0,1.0]])
            >>> mycls=HCluster(features)
            >>> x=mycls.pdist(features)
            >>> y=mycls.linkage(x)    
            >>> rs=mycls.fclusterdata(y,0.4)
            >>> print rs
            >>>
            wrong![1 1 3 2 4 2 5 2 3]
        '''
        return hierarchy.fcluster(Z, t, criterion, depth, R, monocrit)
    
    def fclusterdata(self, X, t, criterion='inconsistent', metric='euclidean', depth=2, method='single', R=None):
        '''
        Clusters the original observations in the n by m data matrix X (n observations in m dimensions), 
        using the euclidean distance metric to calculate distances between original observations, performs 
        hierarchical clustering using the single linkage algorithm, and forms flat clusters using the
        inconsistency method with t as the cut-off threshold.
         
        Arguments: 
            X : ndarray n by m data matrix with n observations in m dimensions. 
            t : double The threshold to apply when forming flat clusters. 
            criterion : string Specifies the criterion for forming flat clusters. 
                Valid values are 'inconsistent', 'distance', or 'maxclust' cluster formation algorithms. 
                See fcluster for descriptions. 
            method : string The linkage method to use (single, complete, average, weighted, median centroid, ward). 
                See linkage for more information. 
            metric : string The distance metric for calculating pairwise distances. 
                See distance.pdist for descriptions and linkage to verify compatibility with the linkage method. 
            t : double The cut-off threshold for the cluster function or the maximum number of clusters 
                (criterion='maxclust'). 
            depth : int The maximum depth for the inconsistency calculation. See inconsistent for more information. 
            R : ndarray The inconsistency matrix. It will be computed if necessary if it is not passed. 
 
        Returns:
            T : ndarray A vector of length n. T[i] is the flat cluster number to which original observation i belongs.   

        Example:
            >>> features  = array([[ 1.9,2.3],
            ...                    [ 1.5,2.5],
            ...                    [ 0.8,0.6],
            ...                    [ 0.4,1.8],
            ...                    [ 0.1,0.1],
            ...                    [ 0.2,1.8],
            ...                    [ 2.0,0.5],
            ...                    [ 0.3,1.5],
            ...                    [ 1.0,1.0]])
            >>> mycls=HCluster(features)
            >>> x=mycls.pdist(features)
            >>> y=mycls.linkage(x)    
            >>> rs=mycls.fclusterdata(features,0.8)
            >>> print rs
            >>>
            [1 1 3 2 4 2 5 2 3]
        '''
        return hierarchy.fclusterdata(X, t, criterion, metric, depth, method, R)
    
    def leaders(self, Z, T):
        '''
        Returns the root nodes in a hierarchical clustering corresponding to a cut defined by a flat cluster 
        assignment vector T. 
        
        Arguments: 
            Z : ndarray, The hierarchical clustering encoded as a matrix. See linkage for more information.
            T : ndarray, The flat cluster assignment vector. 

        Returns: (L, M)
            L : ndarray, The leader linkage node id's stored as a k-element 1D array where k is the number 
                of flat clusters found in T.
            M : ndarray, The leader linkage node id's stored as a k-element 1D array where k is the number 
                of flat clusters found in T. This allows the set of flat cluster ids to be any arbitrary set
                of k integers.
        '''
        return hierarchy.leaders(Z, T)
    
    #These are routines for agglomerative clustering.

    #(1)linkage: agglomeratively clusters original observations. 
    #(2)single: the single/min/nearest algorithm. (alias) 
    #(3)complete: the complete/max/farthest algorithm. (alias) 
    #(4)average: the average/UPGMA algorithm. (alias) 
    #(5)weighted: the weighted/WPGMA algorithm. (alias) 
    #(6)centroid: the centroid/UPGMC algorithm. (alias) 
    #(7)median: the median/WPGMC algorithm. (alias) 
    #(8)ward: the Ward/incremental algorithm. (alias) 
    
    def linkage(self,y, method='single', metric='euclidean'):
        '''
        Performs hierarchical/agglomerative clustering on the condensed distance matrix y. 
        
        Arguments:
            y : ndarray, A condensed or redundant distance matrix. A condensed distance matrix is a flat array 
                containing the upper triangular of the distance matrix. This is the form that pdist returns. 
                Alternatively, a collection of m observation vectors in n dimensions may be passed as an m by n array.
            method : string, The linkage algorithm to use. The Linkage Methods can be 'single', 'complete', 'average',
                'weighted', 'centroid', 'median', 'ward'.
            metric : string, The distance metric to use. See the distance.pdist function for a list of valid 
                distance metrics.

        Returns: 
            Z : ndarray, The hierarchical clustering encoded as a linkage matrix.

        Example:
            >>> features  = array([[ 1.9,2.3],
            ...                    [ 1.5,2.5],
            ...                    [ 0.8,0.6],
            ...                    [ 0.4,1.8],
            ...                    [ 0.1,0.1],
            ...                    [ 0.2,1.8],
            ...                    [ 2.0,0.5],
            ...                    [ 0.3,1.5],
            ...                    [ 1.0,1.0]])
            >>> mycls=HCluster(features)
            >>> x=mycls.pdist(features)
            >>> y=mycls.linkage(x)    
            >>> print y
            >>>
            [[  3.           5.           0.2          2.        ]
             [  7.           9.           0.31622777   3.        ]
             [  2.           8.           0.4472136    2.        ]
             [  0.           1.           0.4472136    2.        ]
             [ 10.          11.           0.86023253   5.        ]
             [  4.          13.           0.86023253   6.        ]
             [  6.          14.           1.11803399   7.        ]
             [ 12.          15.           1.30384048   9.        ]]            
        '''
        return hierarchy.linkage(y, method, metric)
    
    def single(self, y):
        '''
        Performs single/min/nearest linkage on the condensed distance matrix y. See linkage for more information on the return structure and algorithm.

        Arguments:
            y : ndarray, The upper triangular of the distance matrix. The result of pdist is returned in this form.
 
        Returns: 
            Z : ndarray, The linkage matrix.
        '''
        return hierarchy.single(y)
    
    def complete(self, y):
        '''
        Performs complete complete/max/farthest point linkage on the condensed distance matrix y.
        
        Arguments:
            y : ndarray, The upper triangular of the distance matrix. 
                The result of pdist is returned in this form.
 
        Returns:
            Z : ndarray, A linkage matrix containing the hierarchical clustering. 
        '''   
        return hierarchy.complete(y)
    
    def average(self, y):
        '''
        Performs average/UPGMA linkage on the condensed distance matrix y. 
        
        Arguments:
            y : ndarray, The upper triangular of the distance matrix. 
                The result of pdist is returned in this form.
 
        Returns:
            Z : ndarray, A linkage matrix containing the hierarchical clustering. 
        '''
        return hierarchy.average(y)
    
    def weighted(self, y):
        '''
        Performs weighted/WPGMA linkage on the condensed distance matrix y.
        
        Arguments:
            y : ndarray, The upper triangular of the distance matrix. The result of pdist is returned in this form.
 
        Returns: 
            Z : ndarray, A linkage matrix containing the hierarchical clustering. 
                See the linkage function documentation for more information on its structure.
        '''
        return hierarchy.weighted(y)
    
    def centroid(self, y): 
        '''
        Performs centroid/UPGMC linkage. 
        
        Arguments:
            y : ndarray, A condensed or redundant distance matrix. 
                A condensed distance matrix is a flat array containing the upper triangular of the distance matrix. 
                Alternatively, a collection of m observation vectors in n dimensions may be passed as a m by n array.
 
        Returns:
            Z : ndarray, A linkage matrix containing the hierarchical clustering. 
        '''
        return hierarchy.centroid(y)
    
    def median(self, y):
        '''
        Performs median/WPGMC linkage. See linkage for more information on the return structure and algorithm.
        
        Arguments:
            Q : ndarray, A condensed or redundant distance matrix. A condensed distance matrix is a flat array 
                containing the upper triangular of the distance matrix. This is the form that pdist returns. 
                Alternatively, a collection of m observation vectors in n dimensions may be passed as a m by n array.
 
        Returns: 
            Z : ndarray, The hierarchical clustering encoded as a linkage matrix.
        '''
        return hierarchy.median(y) 

    def ward(self, y):
        '''
        Arguments:
            Q : ndarray, A condensed or redundant distance matrix. 
                A condensed distance matrix is a flat array containing the upper triangular of the distance matrix. This is the form that pdist returns. Alternatively, a collection of m observation vectors in n dimensions may be passed as a m by n array.
 
        Returns: 
            Z : ndarray, The hierarchical clustering encoded as a linkage matrix.
        '''
        return hierarchy.ward(y)     
        
    #These routines compute statistics on hierarchies.

    #(1)cophenet: computes the cophenetic distance between leaves. 
    #(2)from_mlab_linkage: converts a linkage produced by MATLAB(TM). 
    #(3)inconsistent: the inconsistency coefficients for cluster. 
    #(4)maxinconsts: the maximum inconsistency coefficient for each cluster. 
    #(5)maxdists: the maximum distance for each cluster. 
    #(6)maxRstat: the maximum specific statistic for each cluster. 
    #(7)to_mlab_linkage: converts a linkage to one MATLAB(TM) can understand. 
    
    def cophenet(self, Z, Y=None):
        '''
        Calculates the cophenetic distances between each observation in the 
        hierarchical clustering defined by the linkage Z.
        
        Arguments:
            Z : ndarray The hierarchical clustering encoded as an array 
                (see linkage function). 
            Y : ndarray (optional) Calculates the cophenetic correlation coefficient c 
                of a hierarchical clustering defined by the linkage matrix Z of a set of n observations in m dimensions. 
                Y is the condensed distance matrix from which Z was generated. 
        
        Returns: 
            (c, {d}) - c : ndarray, The cophentic correlation distance (if y is passed).
            d : ndarray, The cophenetic distance matrix in condensed form. 
                The  ijth entry is the cophenetic distance between original observations i and j. 
        '''
        return hierarchy.cophenet(Z, Y)
    
    def from_mlab_linkage(self, Z):
        '''
        Converts a linkage matrix generated by MATLAB(TM) to a new linkage matrix compatible with this module.
        
        Arguments: 
            Z : ndarray, A linkage matrix generated by MATLAB(TM)
 
        Returns: 
            ZS : ndarray, A linkage matrix compatible with this library.
        '''
        return hierarchy.from_mlab_linkage(Z)
    
    def inconsistent(self, Z, d=2):
        '''
        Calculates inconsistency statistics on a linkage.
        
        Arguments: 
            d : int, The number of links up to d levels below each non-singleton cluster
            Z : ndarray,The  by 4 matrix encoding the linkage (hierarchical clustering). 
                See linkage documentation for more information on its form.
 
        Returns: 
            R : ndarray, A  by 5 matrix where the i'th row contains the link statistics for
                the non-singleton cluster i. 
        '''
        return hierarchy.from_mlab_linkage(Z)
    
    def maxinconsts(self, Z, R):
        '''
        Returns the maximum inconsistency coefficient for each non-singleton cluster and its descendents.

        Arguments: 
            Z : ndarray, The hierarchical clustering encoded as a matrix. See linkage for more information.
            R : ndarray, The inconsistency matrix.
 
        Returns: 
            MI : ndarray, A monotonic (n-1)-sized numpy array of doubles.
        '''
        return hierarchy.maxinconsts(Z, R)
    
    def maxdists(self, Z):
        '''
        Returns the maximum distance between any cluster for each non-singleton cluster.

        Arguments: 
        Z : ndarray, The hierarchical clustering encoded as a matrix. See linkage for more information.
 
        Returns: 
            MD : ndarray, A (n-1) sized numpy array of doubles; MD[i] represents the maximum distance 
            between any cluster (including singletons) below and including the node with index i. 
            More specifically, MD[i] = Z[Q(i)-n, 2].max() where Q(i) is the set of all node indices 
            below and including node i. 
        '''
        return hierarchy.maxdists(Z)
    
    def maxRstat(self, Z, R, i):
        '''
        Returns the maximum statistic for each non-singleton cluster and its descendents.

        Arguments: 
            Z : ndarray, The hierarchical clustering encoded as a matrix. 
            R : ndarray, The inconsistency matrix.
            i : int, The column of R to use as the statistic.
 
    Returns: 
        MR : ndarray Calculates the maximum statistic for the i'th column of the inconsistency matrix R 
            for each non-singleton cluster node. MR[j] is the maximum over R[Q(j)-n, i] where Q(j) 
            the set of all node ids corresponding to nodes below and including j. 
        '''
        return hierarchy.maxRstat(Z, R, i)
    
    def to_mlab_linkage(self, Z):
        '''
        Converts a linkage matrix Z generated by the linkage function of this module to a MATLAB(TM) 
        compatible one. The return linkage matrix has the last column removed and the cluster indices 
        are converted to 1..N indexing.
        
        Arguments: 
            Z : ndarray, A linkage matrix generated by this library.
 
        Returns: 
            ZM : ndarray, A linkage matrix compatible with MATLAB(TM)'s hierarchical clustering functions.
        ''' 
        return hierarchy.to_mlab_linkage(Z)



    
    #Routines for visualizing flat clusters.

    #(1)dendrogram: visualizes linkages (requires matplotlib). 
    
    def dendrogram(self,Z, p=30, truncate_mode=None, color_threshold=None, get_leaves=True, orientation='top', labels=None, count_sort=False, distance_sort=False, show_leaf_counts=True, no_plot=False, no_labels=False, color_list=None, leaf_font_size=None, leaf_rotation=None, leaf_label_func=None, no_leaves=False, show_contracted=False, link_color_func=None):
        '''
        Plots the hiearchical clustering defined by the linkage Z as a dendrogram. 
        The dendrogram illustrates how each cluster is composed by drawing a U-shaped 
        link between a non-singleton cluster and its children.   
        
        Arguments: 
            Z : ndarray, The linkage matrix encoding the hierarchical clustering to render 
                as a dendrogram.            
            truncate_mode : string, Truncation is used to condense the dendrogram. There are several modes:
            None/none: no truncation is performed (Default) 
            lastp: the last p non-singleton formed in the linkage are the only non-leaf nodes in the linkage; 
                    they correspond to to rows Z[n-p-2:end] in Z. All other non-singleton clusters are contracted 
                    into leaf nodes.
            mlab: This corresponds to MATLAB(TM) behavior. (not implemented yet)
            level/mtica: no more than p levels of the dendrogram tree are displayed. This corresponds to 
                Mathematica(TM) behavior.
            p : int, The p parameter for truncate_mode. 
            color_threshold : double, For brevity, let t be the color_threshold. Colors all the descendent links below a 
                cluster node k the same color if k is the first node below the cut threshold t. All links connecting 
                nodes with distances greater than or equal to the threshold are colored blue. If t is less than or equal 
                to zero, all nodes are colored blue. If color_threshold is None or default, corresponding with MATLAB(TM) 
                behavior, the threshold is set to 0.7*max(Z[:,2]).
            get_leaves : bool, Includes a list R['leaves']=H in the result dictionary. 
            orientation : string, The direction to plot the dendrogram, which can be any of the following strings
            top: plots the root at the top, and plot descendent links going downwards. (default).
            bottom: plots the root at the bottom, and plot descendent links going upwards.
            left: plots the root at the left, and plot descendent links going right.
            right: plots the root at the right, and plot descendent links going left.
            labels : ndarray, By default labels is None so the index of the original observation is used to label the 
                leaf nodes.
            count_sort : string/bool, For each node n, the order (visually, from left-to-right) n's two descendent links 
                are plotted is determined by this parameter, which can be any of the following values:
                False: nothing is done. 
                ascending/True: the child with the minimum number of original objects in its cluster is plotted first.
                descendent: the child with the maximum number of original objects in its cluster is plotted first.
            Note distance_sort and count_sort cannot both be True.
            distance_sort : string/bool, For each node n, the order (visually, from left-to-right) n's two descendent 
                links are plotted is determined by this parameter, which can be any of the following values:
                False: nothing is done. 
                ascending/True: the child with the minimum distance between its direct descendents is plotted first.
                descending: the child with the maximum distance between its direct descendents is plotted first.
            show_leaf_counts : bool, When True, leaf nodes representing k>1 original observation are labeled with the 
                number of observations they contain in parentheses.
            no_plot : bool, When True, the final rendering is not performed. This is useful if only the data structures 
                computed for the rendering are needed or if matplotlib is not available.
            no_labels : bool, When True, no labels appear next to the leaf nodes in the rendering of the dendrogram.
            leaf_label_rotation : double, Specifies the angle (in degrees) to rotate the leaf labels. When unspecified, 
                the rotation based on the number of nodes in the dendrogram. (Default=0)
            leaf_font_size : int, Specifies the font size (in points) of the leaf labels. When unspecified, the size based 
                on the number of nodes in the dendrogram.
            leaf_label_func : lambda or function, When leaf_label_func is a callable function, for each leaf with cluster 
                index k<2n-1. The function is expected to return a string with the label for the leaf. Indices k<n 
                correspond to original observations while indices k>=n correspond to non-singleton clusters.
            show_contracted : bool, When True the heights of non-singleton nodes contracted into a leaf node are plotted
                as crosses along the link connecting that leaf node. This really is only useful when truncation is used 
                (see truncate_mode parameter).
            link_color_func : lambda/function When a callable function, link_color_function is called with each 
                non-singleton id corresponding to each U-shaped link it will paint. The function is expected to return 
                the color to paint the link, encoded as a matplotlib color string code.

        Returns: 
            R : dict A, dictionary of data structures computed to render the dendrogram. 
                It has the following keys:
                icoord: a list of lists [I1, I2, ..., Ip] where Ik is a list of 4 independent 
                        variable coordinates corresponding to the line that represents the 
                        k th link painted.
                dcoord: a list of lists [I2, I2, ..., Ip] where Ik is a list of 4 independent
                         variable coordinates corresponding to the line that represents the 
                         k th link painted.
                ivl: a list of labels corresponding to the leaf nodes. 
                leaves: for each i, H[i] == j, cluster node j appears in the i th position in the 
                        left-to-right traversal of the leaves, where j<2n-1 and i<n. If j is less than n, the 
                        ith leaf node corresponds to an original observation. Otherwise, it corresponds to 
                        a non-singleton cluster.
        Example:
            >>> features  = array([[ 1.9,2.3],
            ...                    [ 1.5,2.5],
            ...                    [ 0.8,0.6],
            ...                    [ 0.4,1.8],
            ...                    [ 0.1,0.1],
            ...                    [ 0.2,1.8],
            ...                    [ 2.0,0.5],
            ...                    [ 0.3,1.5],
            ...                    [ 1.0,1.0]])
            >>> mycls=HCluster(features)
            >>> x=mycls.pdist(features)
            >>> y=mycls.linkage(x)
            >>> rs=mycls.dendrogram(y)
            >>> for key, data in rs.items():
            >>>     print key, data
            >>> 
            ivl ['0', '1', '6', '4', '7', '3', '5', '2', '8']
            dcoord [[0.0, 0.44721359549995793, 0.44721359549995793, 0.0], [0.0, 0.20000000000000001, 0.20000000000000001,
            0.0], [0.0, 0.31622776601683794, 0.31622776601683794, 0.20000000000000001], [0.0, 0.44721359549995793,
            0.44721359549995793, 0.0], [0.31622776601683794, 0.86023252670426265, 0.86023252670426265, 0.44721359549995793],
            [0.0, 0.86023252670426276, 0.86023252670426276, 0.86023252670426265], [0.0, 1.1180339887498949,
            1.1180339887498949, 0.86023252670426276], [0.44721359549995793, 1.3038404810405297, 1.3038404810405297,
            1.1180339887498949]]
            leaves [0, 1, 6, 4, 7, 3, 5, 2, 8]
            color_list ['g', 'r', 'r', 'r', 'r', 'r', 'b', 'b']
            icoord [[5.0, 5.0, 15.0, 15.0], [55.0, 55.0, 65.0, 65.0], [45.0, 45.0, 60.0, 60.0], [75.0, 75.0, 85.0, 85.0],
            [52.5, 52.5, 80.0, 80.0], [35.0, 35.0, 66.25, 66.25], [25.0, 25.0, 50.625, 50.625], [10.0, 10.0, 37.8125,
            37.8125]]
        
        '''
        return hierarchy.dendrogram(Z, p, truncate_mode, color_threshold, get_leaves, orientation, labels, count_sort, distance_sort, show_leaf_counts, no_plot, no_labels, color_list, leaf_font_size, leaf_rotation, leaf_label_func, no_leaves, show_contracted, link_color_func)

    def set_link_color_palette(self, palette):  
        '''
        Changes the list of matplotlib color codes to use when coloring links with the dendrogram 
        color_threshold feature.

        Arguments: 
            palette : A list of matplotlib color codes. The order of the color codes is the order in which 
                the colors are cycled through when color thresholding in the dendrogram.
        '''
        return hierarchy.set_link_color_palette(palette) 

    
    
    #These are data structures and routines for representing hierarchies as tree objects.

    #(1)ClusterNode: represents cluster nodes in a cluster hierarchy. 
    #(2)leaves_list: a left-to-right traversal of the leaves. 
    #(3)to_tree: represents a linkage matrix as a tree object. 
    
    def ClusterNode(self, id, left=None, right=None, dist=0, count=1):
        '''
        A tree node class for representing a cluster. Leaf nodes correspond to original 
        observations, while non-leaf nodes correspond to non-singleton clusters.
        '''
        return hierarchy.ClusterNode(id, left, right, dist, count)
    
    def leaves_list(self,Z):
        '''
        Returns a list of leaf node ids (corresponding to observation vector index) as they appear 
        in the tree from left to right. Z is a linkage matrix.

        Arguments: 
            Z : ndarray, The hierarchical clustering encoded as a matrix. See linkage for more information.
 
        Returns: 
            L : ndarray, The list of leaf node ids.
        '''
        return hierarchy.leaves_list(Z) 
    
    def to_tree(self, Z, rd=False):
        '''
        Converts a hierarchical clustering encoded in the matrix Z (by linkage) into an easy-to-use tree object. The reference r to the root ClusterNode object is returned.

        Arguments:
            Z : ndarray The linkage matrix in proper form (see the linkage function documentation). 
            r : bool When False, a reference to the root ClusterNode object is returned. Otherwise, 
                a tuple (r,d) is returned. r is a reference to the root node while d is a dictionary mapping 
                cluster ids to ClusterNode references. If a cluster id is less than n, 
                then it corresponds to a singleton cluster (leaf node). See linkage for more information 
                on the assignment of cluster ids to clusters. 
 
        Returns: 
            L : list The pre-order traversal 
        '''
        return hierarchy.to_tree(Z, rd)
    
    #These are predicates for checking the validity of linkage and inconsistency matrices as well as for checking isomorphism of two flat cluster assignments.

    #(1)is_valid_im: checks for a valid inconsistency matrix. 
    #(2)is_valid_linkage: checks for a valid hierarchical clustering. 
    #(3)is_isomorphic: checks if two flat clusterings are isomorphic. 
    #(4)is_monotonic: checks if a linkage is monotonic. 
    #(5)correspond: checks whether a condensed distance matrix corresponds with a linkage 
    #(6)num_obs_linkage: the number of observations corresponding to a linkage matrix.
    
    def is_isomorphic(self, T1, T2):
        '''
        Determines if two different cluster assignments T1 and T2 are equivalent.

        Arguments: 
            T1 : ndarray An assignment of singleton cluster ids to flat cluster ids. 
            T2 : ndarray An assignment of singleton cluster ids to flat cluster ids. 
            
        Returns: 
            b : boolean Whether the flat cluster assignments T1 and T2 are equivalent 
        '''
        return hierarchy.is_isomorphic(T1, T2) 
    
    def is_monotonic(self, Z):
        '''
        Returns True if the linkage passed is monotonic. The linkage is monotonic if for every cluster s and t joined,
        the distance between them is no less than the distance between any previously joined clusters.

        Arguments: 
            Z : ndarray The linkage matrix to check for monotonicity.
             
        Returns: 
            b : bool A boolean indicating whether the linkage is monotonic.  
        ''' 
        return hierarchy.is_monotonic(Z)
    
    def is_valid_im(self, R, warning=False, throw=False, name=None):
        '''
        Returns True if the inconsistency matrix passed is valid. 

        Arguments: 
            R : ndarray The inconsistency matrix to check for validity. 
            warning : bool When True, issues a Python warning if the linkage matrix passed is invalid. 
            throw : bool When True, throws a Python exception if the linkage matrix passed is invalid. 
            name : string This string refers to the variable name of the invalid linkage matrix. 
 
        Returns: 
            b : bool True iff the inconsistency matrix is valid.  
        '''
        return hierarchy.is_valid_im(R, warning, throw, name)
    
    def is_valid_linkage(self, Z, warning=False, throw=False, name=None):
        '''
        Checks the validity of a linkage matrix. A linkage matrix is valid if it is a two dimensional 
        nd-array (type double) with n rows and 4 columns. 
        
        Arguments: 
            warning : bool When True, issues a Python warning if the linkage matrix passed is invalid. 
            throw : bool When True, throws a Python exception if the linkage matrix passed is invalid. 
            name : string This string refers to the variable name of the invalid linkage matrix. 
 
        Returns: 
            b : bool, True iff the inconsistency matrix is valid.
        '''
        return hierarchy.is_valid_linkage(Z, warning, throw, name)
    
    def correspond(self, Z, Y):
        '''
        Checks if a linkage matrix Z and condensed distance matrix Y could possibly 
        correspond to one another.

        Arguments:
            Z : ndarray, The linkage matrix to check for correspondance.
            Y : ndarray, The condensed distance matrix to check for correspondance.
 
        Returns: 
            b : bool, A boolean indicating whether the linkage matrix and 
                distance matrix could possibly correspond to one another.
        '''
        return hierarchy.correspond(Z, Y)
    
    def num_obs_linkage(self, Z):
        '''
        Returns the number of original observations of the linkage matrix passed.

        Arguments: 
            Z : ndarray, The linkage matrix on which to perform the operation.
 
        Returns: 
            n : int, The number of original observations in the linkage.
        '''
        return hierarchy.num_obs_linkage(Z)

    def pdist(self, X, metric='euclidean', p=2, V=None, VI=None):
        '''
        Computes the pairwise distances between m original observations in n-dimensional space.
        Returns a condensed distance matrix Y. For each  and  (where ),
        the metric dist(u=X[i], v=X[j]) is computed and stored in the :math:`ij`th entry.

        Arguments: 
            X : ndarray, An m by n array of m original observations in an n-dimensional space.
            metric : string or function, The distance metric to use. The distance function can be 'braycurtis',
                    'canberra', 'chebyshev', 'cityblock', 'correlation', 'cosine', 'dice', 'euclidean', 'hamming',
                    'jaccard', 'kulsinski', 'mahalanobis', 'matching', 'minkowski', 'rogerstanimoto', 'russellrao',
                    'seuclidean', 'sokalmichener', 'sokalsneath', 'sqeuclidean', 'yule'.
            w : ndarray, The weight vector (for weighted Minkowski).
            p : double, The p-norm to apply (for Minkowski, weighted and unweighted)
            V : ndarray, The variance vector (for standardized Euclidean).
            VI : ndarray, The inverse of the covariance matrix (for Mahalanobis).
 
        Returns:
            Y : ndarray, A condensed distance matrix.

        Example:
            >>> features  = array([[ 1.9,2.3],
            ...                    [ 1.5,2.5],
            ...                    [ 0.8,0.6],
            ...                    [ 0.4,1.8],
            ...                    [ 0.1,0.1],
            ...                    [ 0.2,1.8],
            ...                    [ 2.0,0.5],
            ...                    [ 0.3,1.5],
            ...                    [ 1.0,1.0]])
            >>> mycls=HCluster(features)
            >>> x=mycls.pdist(features)
            >>> print x
            >>> 
            [ 0.4472136   2.02484567  1.58113883  2.84253408  1.77200451  1.80277564
              1.78885438  1.58113883  2.02484567  1.30384048  2.7784888   1.47648231
              2.06155281  1.56204994  1.58113883  1.26491106  0.86023253  1.34164079
              1.20415946  1.02956301  0.4472136   1.72626765  0.2         2.06155281
              0.31622777  1.          1.70293864  1.94164878  1.41421356  1.27279221
              2.22036033  0.31622777  1.13137085  1.97230829  1.11803399  0.86023253]
        '''
        return distance.pdist(X, metric, p, V, VI)

    #These are customized fuctions.

    def allClusters(self, Z):
        '''
        Return a dictionary, in which keys are index of all the clusters, values are the two
        subclusters belonging to the cluster. There are 2n-1 clusters,
        so the range of index is 0 to 2n-2.

        Arguments: 
            Z : ndarray, The linkage matrix on which to perform the operation.
 
        Returns: 
            L : dictionary.

        Example:
            >>> features  = array([[ 1.9,2.3],
            ...                    [ 1.5,2.5],
            ...                    [ 0.8,0.6],
            ...                    [ 0.4,1.8],
            ...                    [ 0.1,0.1],
            ...                    [ 0.2,1.8],
            ...                    [ 2.0,0.5],
            ...                    [ 0.3,1.5],
            ...                    [ 1.0,1.0]])
            >>> mycls=HCluster(features)
            >>> x=mycls.pdist(features)
            >>> y=mycls.linkage(x)    
            >>> rs=mycls.allClusters(y)
            >>> print rs
            >>> 
            {0: [0], 1: [1], 2: [2], 3: [3], 4: [4], 5: [5], 6: [6], 7: [7], 8: [8], 9: [3, 5],
            10: [7, 9], 11: [2, 8], 12: [0, 1], 13: [10, 11], 14: [4, 13], 15: [6, 14],
            16: [12, 15]}    
        '''
        n=self.num_obs_linkage(Z) #n: number of original observations
        dic={}
        for i in range(2*n-1):
            dic[i]=[]
            if i<n:
                dic[i].append(int(i))  # if index of cluster < n, then the value is index itself.
        for i in range(n-1):
            dic[n+i].append(int(Z[i][0]))
            dic[n+i].append(int(Z[i][1]))
        return dic

    def getChildren(self, Z, index):
        '''
        Given index of a cluster, return a list of all the index of the original observations
        included in this cluster.

        Arguments: 
            Z : ndarray, The linkage matrix on which to perform the operation.
 
        Returns: 
            L : list.

        Example:
            >>> features  = array([[ 1.9,2.3],
            ...                    [ 1.5,2.5],
            ...                    [ 0.8,0.6],
            ...                    [ 0.4,1.8],
            ...                    [ 0.1,0.1],
            ...                    [ 0.2,1.8],
            ...                    [ 2.0,0.5],
            ...                    [ 0.3,1.5],
            ...                    [ 1.0,1.0]])
            >>> mycls=HCluster(features)
            >>> x=mycls.pdist(features)
            >>> y=mycls.linkage(x)    
            >>> rs=mycls.getChildren(y, 10)
            >>> print rs
            >>> 
            [7, 3, 5]
            
        '''
        d=self.allClusters(Z)
        n=self.num_obs_linkage(Z)
        L=[]
        if index<n:
            L.extend(d[index])
            return L
        else:
            temp=d[index]
            id1=temp[0]
            id2=temp[1]
            L.extend(self.getChildren(Z, id1))
            L.extend(self.getChildren(Z, id2))
            return L

    def expandClusters(self, Z):
        '''
        Return a list of list, with 2n-1 rows, the index of each row corresponding the index of
        each cluster. Each row contains all the original observations in that cluster.

        Arguments: 
            Z : ndarray, The linkage matrix on which to perform the operation.
 
        Returns: 
            L : list.

        Example:
            >>> features  = array([[ 1.9,2.3],
            ...                    [ 1.5,2.5],
            ...                    [ 0.8,0.6],
            ...                    [ 0.4,1.8],
            ...                    [ 0.1,0.1],
            ...                    [ 0.2,1.8],
            ...                    [ 2.0,0.5],
            ...                    [ 0.3,1.5],
            ...                    [ 1.0,1.0]])
            >>> mycls=HCluster(features)
            >>> x=mycls.pdist(features)
            >>> y=mycls.linkage(x)    
            >>> rs=mycls.expandClusters(y)
            >>> print rs
            >>> 
            [[0], [1], [2], [3], [4], [5], [6], [7], [8], [3, 5], [7, 3, 5], [2, 8], [0, 1],
            [7, 3, 5, 2, 8], [4, 7, 3, 5, 2, 8], [6, 4, 7, 3, 5, 2, 8],
            [0, 1, 6, 4, 7, 3, 5, 2, 8]]       
        '''
        L=[]
        n=self.num_obs_linkage(Z)
        d=self.allClusters(Z)
        for i in range(2*n-1):
            temp=[]            
            if i<n:
                temp.append(int(i))                
            else:
                temp=self.getChildren(Z,i)
            L.append(temp)
        return L

    def kClusters(self, Z, k):
        '''
        Return a dictionary. Each of key is the index of the cluster, values are lists
        containing the index of original observations in that cluster.

        Arguments: 
            Z : ndarray, The linkage matrix on which to perform the operation.
            k : int, the desired number of clusters
 
        Returns: 
            D : dictionary.

        Example:
            >>> features  = array([[ 1.9,2.3],
            ...                    [ 1.5,2.5],
            ...                    [ 0.8,0.6],
            ...                    [ 0.4,1.8],
            ...                    [ 0.1,0.1],
            ...                    [ 0.2,1.8],
            ...                    [ 2.0,0.5],
            ...                    [ 0.3,1.5],
            ...                    [ 1.0,1.0]])
            >>> mycls=HCluster(features)
            >>> x=mycls.pdist(features)
            >>> y=mycls.linkage(x)    
            >>> rs=mycls.kClusters(y,5)
            >>> print rs
            >>> 
            {4: [4], 10: [7, 3, 5], 11: [2, 8], 12: [0, 1], 6: [6]}
        '''
        D={}
        n=self.num_obs_linkage(Z)
        if k==1:
            temp=self.getChildren(Z, 2*n-2)
            D[2*n-2]=temp
        else:
            temp=[]
            for i in range(k-1): #get the index of the clusters
                x1=Z[n-2-i][0]
                x2=Z[n-2-i][1]
                temp.append(min(x1,x2))
                if k-len(temp)==1:
                    temp.append(max(x1,x2))
            nkeys=len(temp)
            for i in range(nkeys):
                D[int(temp[i])]=self.getChildren(Z,temp[i])
        return D

    def kClusters2(self, Z, k):
        '''
        If we need k clusters in the hierachy clustering, this function will return a list of k indexes of those clusters.

        Arguments: 
            Z : ndarray, The linkage matrix on which to perform the operation.
            k : int, the desired number of clusters
            
        Returns: 
            L : list.

        Example:
            >>> features  = array([[ 1.9,2.3],
            ...                    [ 1.5,2.5],
            ...                    [ 0.8,0.6],
            ...                    [ 0.4,1.8],
            ...                    [ 0.1,0.1],
            ...                    [ 0.2,1.8],
            ...                    [ 2.0,0.5],
            ...                    [ 0.3,1.5],
            ...                    [ 1.0,1.0]])
            >>> mycls=HCluster(features)
            >>> x=mycls.pdist(features)
            >>> y=mycls.linkage(x)    
            >>> rs=mycls.kClusters2(y,5)
            >>> print rs
            >>> 
            [12, 6, 4, 10, 11]
        '''
        L=[]
        n=self.num_obs_linkage(Z)
        temp=[]
        if k==1:
            L.append(2*n-2)
        else:
            for i in range(k-1): #get the index of the clusters
                x1=Z[n-2-i][0]
                x2=Z[n-2-i][1]
                L.append(int(min(x1,x2)))
                if k-len(L)==1:
                    L.append(int(max(x1,x2)))
        return L

    def compareLists(self, L1, L2):
        '''
        If L2 contains every elements in L1, return True, otherwise, return False.
        
        Arguments: 
            L1 : list
            L2 : list
 
        Returns: 
            rs : bool

        Example:
            >>> features  = array([[ 1.9,2.3],
            ...                    [ 1.5,2.5],
            ...                    [ 0.8,0.6],
            ...                    [ 0.4,1.8],
            ...                    [ 0.1,0.1],
            ...                    [ 0.2,1.8],
            ...                    [ 2.0,0.5],
            ...                    [ 0.3,1.5],
            ...                    [ 1.0,1.0]])
            >>> mycls=HCluster(features)
            >>> l=[2,3]
            >>> m=[2,3,4]
            >>> print mycls.compareLists(l,m)
            >>> 
            True
        '''
        nlen=len(L1)
        for i in range(nlen):
            if not L1[i] in L2:
                return False
        return True

    def minCluster(self, Z, L):
        '''
        Return the smallest cluster that contains the original observations in L.

        Arguments: 
            Z : ndarray, The linkage matrix on which to perform the operation.
            L : list, including the indexes of orignial obeservations
 
        Returns: 
            indexCls : the index of the cluster that contains all the original observations in L.  

        Example:
            >>> features  = array([[ 1.9,2.3],
            ...                    [ 1.5,2.5],
            ...                    [ 0.8,0.6],
            ...                    [ 0.4,1.8],
            ...                    [ 0.1,0.1],
            ...                    [ 0.2,1.8],
            ...                    [ 2.0,0.5],
            ...                    [ 0.3,1.5],
            ...                    [ 1.0,1.0]])
            >>> mycls=HCluster(features)
            >>> x=mycls.pdist(features)
            >>> y=mycls.linkage(x)
            >>> l=[2,4]    
            >>> print mycls.minCluster(y, l)
            >>> 
            14
        '''
        arr=self.expandClusters(Z)
        n=len(arr)
        for i in range(n):
            if self.compareLists(L, arr[i]):
                return i
        

    def obsToClusters(self, Z, L):
        '''
        Given a list L of indexes of orignial obeservations, return an alternative in which the number
        of clusters is largest that can be acquired.

        Arguments: 
            Z : ndarray, The linkage matrix on which to perform the operation.
            L : list, including the indexes of orignial obeservations
 
        Returns: 
            indexL : a list including numbers of clusters corresponding to various alternatives of clustering.
                    with this number and function kClusters(), one desired solution of clustering can be attained. 

        Example:
            >>> features  = array([[ 1.9,2.3],
            ...                    [ 1.5,2.5],
            ...                    [ 0.8,0.6],
            ...                    [ 0.4,1.8],
            ...                    [ 0.1,0.1],
            ...                    [ 0.2,1.8],
            ...                    [ 2.0,0.5],
            ...                    [ 0.3,1.5],
            ...                    [ 1.0,1.0]])
            >>> mycls=HCluster(features)
            >>> x=mycls.pdist(features)
            >>> y=mycls.linkage(x)
            >>> l=[2,4]
            >>> print mycls.obsToClusters(y, l)
            >>> 
            3
        '''
        idCluster=self.minCluster(Z, L)
        n=self.num_obs_linkage(Z)
        for i in range(1, 2*n-2):
            temp=self.kClusters2(Z, i)
            if idCluster in temp:
                return i
        
if __name__ == '__main__':
    features = array([[ 1.9,2.3],[ 1.5,2.5],[ 0.8,0.6],[ 0.4,1.8],[ 0.1,0.1],[ 0.2,1.8],[ 2.0,0.5],[ 0.3,1.5],[ 1.0,1.0]])
    mycls=HCluster(features)
    x=mycls.pdist(features)
    y=mycls.linkage(x)    
    #rs=mycls.kClusters2(y,5)
    #print rs
    l=[0,6]
    #m=[2,5,4]
    print mycls.obsToClusters(y, l)
    


    
