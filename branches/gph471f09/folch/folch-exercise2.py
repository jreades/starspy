class NodePair:
    '''
    A class to hold the output from the shortest path and shortest length
    algorithms below.
    '''
    def __init__(self, pair, length):
        self.pair = pair
        self.length = length


def findLengths(graph):
    '''
    Input:
    graph (dictionary): dictionary where the key is node ID and the value is
                        a list of node IDs that are directly connected to
                        the key node (assumes no nodes linking back to
                        themselves, an undirected graph, all points are
                        reachable from all other points)

    Returns:
    List of instances of the NodePair class.  Each instance contains the node
    pair and the length of the shortest path between those nodes.
    '''
    n = len(graph)
    # build sparse adjacency matrix
    a = {}         #adjacency matrix
    for i in graph:
        for j in graph[i]:
            a[tuple(set([i,j]))] = 1
    c = a.copy()   #connectivity matrix
    # build up all the candidate node pairs still needing to be connected
    tester = {}
    for i in xrange(n):
        for j in xrange(i+1, n):
            if (i,j) not in a:
                tester[(i,j)] = 0
    
    m = 1  #node pair length
    # loop over the candidate pairs until each has a length
    while tester:
        m += 1
        popDict = {}
        for pair in tester:
            i,j = pair
            for k in xrange(n):
                if tuple(set([i,k])) in c and tuple(set([k,j])) in a:
                    popDict[pair] = m
                    break
        c.update(popDict)
        map(tester.pop, popDict.keys())
    pairs = [NodePair(i, c[i]) for i in c]
    return pairs, max(c.values())
        

def findPaths(pairs, maxLen):
    '''
    Input:
    pairs (list): list of instances of the NodePair class (note: this is an 
                  output from findLengths function)
    maxLen (integer): the maximum shortest path length (note: this is an
                      output from findLengths function)
    
    Returns:
    List of instances from the NodePair class.  Each instance contains the node
    pair and a list of nodes connecting i to j (including i and j).  Note:
    other shortest paths besides the one returned may exist.
    '''
    # build up a nested dictionary of the form [nodeID]:{[length]:set(nodeIDs)}
    # the inner set is all the nodes that are the defined length away from the
    # outer key 
    connections = dict([(i, {}) for i in range(len(pairs))])
    for i in connections:
        connections[i] = dict([(j, set([])) for j in range(1, maxLen+1)])
    for pair in pairs:
        i,j = pair.pair
        connections[i][pair.length].add(j)
        connections[j][pair.length].add(i)

    # find the shortest path by manipulating sets of connected nodes
    for pair in pairs:
        i,j = pair.pair
        path = [i]
        for testLen in xrange(pair.length-1, 0, -1):
            sharedNodes = connections[i][1].intersection(connections[j][testLen])
            i = sharedNodes.pop()
            path.append(i)
        path.append(j)
        pair.path = path
    return pairs
            

if __name__ == "__main__":
    g={0: [2, 1], 1: [0, 3], 2: [0, 4, 3], 3: [1, 2, 5], 4: [2, 6, 5], 5: [3, 4, 7], 6: [4, 7], 7: [5, 6]}
    pairs, maxLen = findLengths(g)
    pairs = findPaths(pairs, maxLen)
    for i in pairs:
        print 'Pair: %s, Length: %d, Path: %s' %(i.pair, i.length, i.path)

