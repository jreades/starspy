def shortestPathLength(graph = {0: [2, 1], 1: [0, 3], 2: [0, 4, 3], 3: [1, 2, 5], 4: [2, 6, 5], 5: [3, 4, 7], 6: [4, 7], 7: [5, 6]}):    
    """return a list[[distance]] for the shortest path length between any two nodes in the graph
    Argument:a dictionary representing the graph"""
    Max = 9999
    node_list = graph.keys()
    Node_Num = len(node_list)
    weight = 1

    dis = [[Max for j in range(Node_Num)] for i in range(Node_Num)]
    for key in node_list:
        for value in graph[key]:
            dis[key][key] = 0
            dis[key][value] = weight
            
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
        
        del unsolved_set[:]

    for i in node_list:
        for j in node_list:
            if dis[i][j] > dis[j][i]:
                dis[i][j] = dis[j][i]

    return dis

dis = shortestPathLength()
print dis
            
