def shortestPathComputing(graph = {0: [2, 1], 1: [0, 3], 2: [0, 4, 3], 3: [1, 2, 5], 4: [2, 6, 5], 5: [3, 4, 7], 6: [4, 7], 7: [5, 6]}):    
    """return a list of tuple([path], length) for all the graph's nodes
    Argument: a dictionary representing the graph"""
    Max = 9999
    node_list = graph.keys()
    Node_Num = len(node_list)
    weight = 1

    dis = [[Max for j in range(Node_Num)] for i in range(Node_Num)]
    path = [[[] for j in range(Node_Num)] for i in range(Node_Num)]
    pre_node = [[-1 for j in range(Node_Num)] for i in range(Node_Num)]
    for key in node_list:
        dis[key][key] = 0
        path[key][key].append(key)
        for value in graph[key]:            
            dis[key][value] = weight            
            path[key][value].append(key)
            path[key][value].append(value)
            
    unsolved_set = []

    for key in node_list:
        unsolved_set.extend(node_list[node_list.index(key)+1:])
        if not unsolved_set:
            break
        static_us = unsolved_set[:]
        for i in range(len(static_us)):
            short_length = min(dis[key][un_node] for un_node in unsolved_set)
            for un_node in unsolved_set:
                if dis[key][un_node] == short_length:
                    short_node = un_node
            if short_length == Max:
                break
            dis[key][short_node] = short_length
            unsolved_set.remove(short_node)
            for un_node in unsolved_set:
                if dis[key][un_node] > (dis[key][short_node] + dis[short_node][un_node]):
                    dis[key][un_node] = (dis[key][short_node] + dis[short_node][un_node])
                    pre_node[key][un_node] = short_node
        
        del unsolved_set[:]
        s = []
        
        for i in range(Node_Num):
            if not (pre_node[key][i] == -1):
                j = i
                while not (pre_node[key][j] == -1):
                    s.append(pre_node[key][j])
                    j = pre_node[key][j]
                s.reverse()
                path[key][i].append(key)
                path[key][i].extend(s)
                path[key][i].append(i)
                s = []

    for i in node_list:
        for j in node_list:
            if dis[i][j] > dis[j][i]:
                dis[i][j] = dis[j][i]
            if path[i][j] and (not path[j][i]):
                path[j][i] = path[i][j][:]
                path[j][i].reverse()
      #      print "The shortest path between node %d and node %d is %d" %(i, j, dis[i][j])
    
    result = []
    for i in node_list:
        for j in node_list:
            tuple = (path[i][j], dis[i][j])
            result.append(tuple)

    return result

result = shortestPathComputing()
print result
 
