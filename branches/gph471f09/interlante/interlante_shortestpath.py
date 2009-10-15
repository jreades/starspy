	###LINDSEY INTERLANTE - GPH 471 EXERCISE #2###

# Initially, I defined the nodes and connections between the nodes as graph "conn". #
# The graph consists of eight nodes and each node's corresponding arcs, which are defined below as lists.# 

conn = {'0':['2','1'],'1':['0','3'],'2':['0','4','3'], '3':['1','2','5'],'4':['2','6','5'],'5':['3','4','7'],'6':['4','7'],'7':['5','6']}

nodes=['0','1','2','3','4','5','6','7']

# The shortest path function utilizes the connections (defined in conn above) and considers the beginning (beg) and end (end) of each path. # 
# This function is set to return the path as a list (in brackets []).#

def shortestpath(conn, beg, end, path=[]):
	path = path + [beg]
	if beg == end:
		return path
	shortest = None	
	for node in conn[beg]:
		if node not in path:
			newpath = shortestpath(conn, node, end, path)
			if newpath:
				if not shortest or len(newpath) < len(shortest):
					shortest = newpath
	return shortest

# This component of the code uses a for loop to determine the length of the shortest path between each pair of nodes. 
# It is formatted so that the output will look like this: "0->1 with shortest path length of 2," where 0 is the starting node (beg) 
# and 1 is the ending node (end) on this particular shortest path.#

for i in nodes:
	for j in nodes:
		if i !=j:
			s= i + "->" + j + " with shortest path length of " + str(len(shortestpath(conn,i,j)))
			print s

# This component of the code builds upon the previous code and identifies the length of the shortest path as well as the nodes that 
#are traversed for each combination. The output of this section looks like this: "['0', '1'] 0->1 with shortest path length of 2," 
#meaning that the shortest path between node 0 (beg) and 1 (end) touches two nodes (0 and 1) identified in the brackets. # 

for i in nodes:
	for j in nodes:
		if i !=j:
			print shortestpath(conn,i,j)
			s= i + "->" + j + " with shortest path length of " + str(len(shortestpath(conn,i,j)))
			print s