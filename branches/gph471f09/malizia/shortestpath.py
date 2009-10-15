#Nicholas Malizia
#Geovisualization Assignment 2
#This program finds the shortest path from one node on a network to another.

#This defines the network in use. The network must be in the form of
#a dictionary for the program to work properly. 
network={0: [2, 1],
         1: [0, 3],
         2: [0, 4, 3],
         3: [1, 2, 5],
         4: [2, 6, 5],
         5: [3, 4, 7],
         6: [4, 7],
         7: [5, 6]}

#This is the part of the code that defines a function to find the shortest path between two nodes:
def shortest_path(network, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    shortest = None
    for node in network[start]:
        if node not in path:
            newpath = shortest_path(network, node, end, path)
            if newpath <> None:
                if shortest == None:
                    shortest = newpath
                if len(newpath) < len(shortest):
                    shortest = newpath
    return shortest


#This creates a dictionary to store the distance information
distances={}

#Here is the loop that cycles through all combinations of nodes and finds the shortest path:
for i in network:
    for j in network:
        path = shortest_path(network, i, j)
        key = (i,j)
        length = len(path)-1
        distances[key]=path,length

#Finally, we print the resulting dictionary.
#This dictionary is structured such that the key is a tuple containing (start, end)
#The value is a tuple containing the path (list) and its distance (integer). 
print distances

