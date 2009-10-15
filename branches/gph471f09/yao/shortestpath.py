def GtoGraph(g,N):
    """
    tranfer a graph to a 2d distance matrix represented by tuple.
    """
    dist=[]  
    for i in range(N):  #inite dist to be a symmetric matrix with diagonal elements 0,other elements 9999
        dist.append([])
        for j in range(N):            
            if j==i:
                dist[i].append(0)
            else:
                dist[i].append(9999)             
    
    endv=[]
    for key,value in g.items():  #get actual path information from graph
        endv=value
        nlen=len(endv)
        for i in range(nlen):
            vvalue=endv[i]
            dist[key][vvalue]=1   #set actural length of path

    cost=[]
    for i in range(N):
        p=tuple(dist[i])
        cost.append(p)
    cost=tuple(cost)
            
    return cost

def ShortestPath(N, cost):
        """
        This function returns the actual shortest paths along with their lengths.
        I---the infinite distance
        dist---the shortest distance matrix
        gpath---the variable to be returned. It's a list matrix including dictionaries with key indicating lengths and
                values indicating actual shortest paths.
        v0---the start vertex of the path
        final---indicate whether the shortest path to vertex final[i] has been found
        path---record the vertex before current vertex in the shortest path.
        fullpath---the actual shortest paths along with their lengths from v0 to the other vertexes. 
        
        """
        I=99999
              
        gpath=[]
        for v0 in range(N): 
            final=[0]*N
            final[v0]= 1  #the shortest distance from v0 to v0 is 0"""
            path=[I]*N  #record the vertex before current vertex in the shortest path."""
            ipath=[]
            
            dist=[]
            for i in range(N):  #initiate the dist list
                p=[]
                for j in range(N):
                    p.append(cost[i][j])    
                dist.append(p)
            
            for i in range(N):
                if dist[v0][i]<I:
                    path[i]=v0  #initiate the path"""
                    
            for i in range(N):
                minDist=I 
                
                for w in range(N):    #find the shortest distance from vertex v0 to vertex v"""                
                    if ((final[w]==0) and (dist[v0][w]< minDist)):
                        minDist=dist[v0][w]
                        v=w
                final[v]=1  #the vertex v has been visited, i.e.,the shortest distance from v0 to v has been found """
            
                for w in range(N):
                    if ((final[w]==0) and (dist[v0][v] + cost[v][w] < dist[v0][w])):
                        dist[v0][w]=dist[v0][v] + cost[v][w]  #change the distance from v0 to w through v"""
                        path[w]=v     #v is the previous vertex in the shortest path from v0 to w"""

        
            fullpath=[]
            for i in range(N):
                allpath={}  #a dictionary:the key indicates the shortest distances, the value indicates the actual paths"""
                ipath=[]    #store the vertexs in the paths from v0 to i inversely"""
                ipath.append(i) #the last vertex in the path is i itself"""
                x=path[i]
                while (x!=v0 and x<I):
                    ipath.append(x)  #append the vertexes in the path from back to front"""
                    y=path[x]
                    x=y
                temp=[]
                temp.append(v0)  #the first vertex in the path is v0"""
                nCount=len(ipath)
                for j in range(nCount):  #add the vertexes in the path from v0 to vertex i"""
                    temp.append(ipath[nCount-j-1])
                if i==v0:
                    allpath[0]=temp
                else:
                    allpath[len(temp)-1]=temp
                fullpath.append(allpath)
            gpath.append(fullpath)
         
        return gpath
             


N=8
I=99999
g={0: [2, 1], 1: [0, 3], 2: [0, 4, 3], 3: [1, 2, 5], 4: [2, 6, 5], 5: [3, 4, 7], 6: [4, 7], 7: [5, 6]}
cost=GtoGraph(g,N)
G=ShortestPath(N,cost)
for i in range(N):
    print G[i] 
