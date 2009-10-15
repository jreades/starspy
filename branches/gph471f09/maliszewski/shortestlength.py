#dictionary holding values where the key is the id of the node, and the values of the key are the first order neighbors. In other words, node ‘0’ is connected to nodes ‘2’ and ‘1’, while node ‘4’ is connected to nodes ‘2’, ‘6’, and ‘5’. Assume all first order connections are of the same length (i.e., an unweighted graph).
g={0: [2, 1], 1: [0, 3], 2: [0, 4, 3], 3: [1, 2, 5], 4: [2, 6, 5], 5: [3, 4, 7], 6: [4, 7], 7: [5, 6]}
#create function to find shortest length
def shortestlength(g, d={}):
#create distance holding matrix
    for i in range(0,len(g)):
        d[i,i] = 0
        for j in range(0, len(g)):
            d.setdefault((i,j), 999999)
            for k in g[i]:
                d[i,k] = 1
#Find shortest length between all nodes
    for i in range(0,len(g)):
        for j in range(0,len(g)):
            for k in range(0,len(g)):
                d[i,j] = min(d[i,j], d[i,k] + d[k,j])
    return d


            

            
            
            
            
            
