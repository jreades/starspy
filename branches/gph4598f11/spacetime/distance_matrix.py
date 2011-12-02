"""
This script finds the Euclidean distance between each pair of points,
and organizes them in a matrix.

Input should be a list that contains a list for each point:
    [point_num, weight, x, y]

Output should be a list that contains a list for each point pair
"""

from math import sqrt
import numpy as np

#Input table : table = [point_num, weight, x-coord, y-coord, total_pop]
distances = []

for point in table:
    x1 = point[2]
    y1 = point[3]
    for other in table:
        x2 = other[2]
        y2 = other[3]
        dist = sqrt((x2-x1)**2 + (y2-y1)**2)
        distances.append([point[0], dist, other[0]])
distances.sort()

d = np.array(distances)
nd = {}
pop = []
cpop = []
for i in range(len(table)):
    pop.append(table[i][4])
    for k in distances[i]:
        nd[i+1] = d[d[:,0] == i+1][:,2].tolist()
for i in range(len(table)):
    temp = []
    for p in range(len(table)):
        temp.append(pop[int(nd[i+1][p])-1])
    cpop.append(temp)

"""
point_num = 1
relationship_table = []
for point in distances:
    neighbors = []
    if point[0] == point_num:
        neighbors.append(point[2])
    point_num += 1
    relationship_table.append(neighbors)
"""
