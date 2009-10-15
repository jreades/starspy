# define the dictionary which describes the graph

g = {0: [2, 1], 1: [0, 3], 2: [0, 4, 3], 3: [1, 2, 5], 4: [2, 6, 5], 5: [3, 4, 7], 6: [4, 7], 7: [5, 6]}

# write the function to find the shortest path between two points in the graph

def shortest_path (g, start, end, path = []):
	path = path + [start]
	if start == end:
		return path
	shortest = None
	for node in g[start]:
		if node not in path:
			newpath = shortest_path (g, node, end, path)
			if newpath:
				if not shortest or len(newpath) < len(shortest):
					shortest = newpath
	return shortest
	
# write two nested while statements in order to repeat through the function
# for every pair of points in the graph

i = 0
while i < 8:
	j = 0
	while j < 7:
		print shortest_path (g, i, j)
		print len (shortest_path (g, i, j))  # length of path is one less 
		j = j + 1
	print shortest_path (g, i, j)
	print len (shortest_path (g, i, j)) 
	i = i + 1
