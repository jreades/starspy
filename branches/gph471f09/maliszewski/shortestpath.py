g={0: [2, 1], 1: [0, 3], 2: [0, 4, 3], 3: [1, 2, 5], 4: [2, 6, 5], 5: [3, 4, 7], 6: [4, 7], 7: [5, 6]}
def shortestpath(g, d={}, p={}, q={}):
#create distance holding matrix
    for i in range(0,len(g)):
        d[i,i] = 0
        for j in range(0, len(g)):
            d.setdefault((i,j), 999999)
            for k in g[i]:
                d[i,k] = 1
#create intermediate node matrix
    for i in range(0, len(g)):
        for j in range(0, len(g)):
            p[i,j] = -1
#Find shortest length between all nodes
    for i in range(0,len(g)):
        for j in range(0,len(g)):
            for k in range(0,len(g)):
                if d[i,k] + d[k,j] < d[i,j]:
                    p[i,j] = k
                    d[i,j]=d[i,k] + d[k,j]
#create path holding matrix
    for i in range(0, len(g)):
        for j in range(0, len(g)):
            q[i,j] = -1
#write i,j values with no intermediate nodes
    for i in range(0,len(g)):
        for j in range(0,len(g)):
            if p[i,j] < 0:
                q[i,j]= i,j
#find and write shortest path from i to j with all intermediate nodes
    for k in range(1,len(g)):            
        for i in range(0,len(g)):
            for j in range(0,len(g)):
                if p[i,j] >= 0:
                    l=p[i,j]
                    if p[i,l]<0:
                        if p[l,j]<0:
                            q[i,j]=q[i,l],q[l,j]
                            p[i,j]=-1
#return shortest path matrix (q) and shortest length matrix (d)
    return q,d

                
    
