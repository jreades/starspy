"""
This script finds the Euclidean distance between each pair of points,
and organizes them in a matrix.

Input should be a list that contains a list for each point:
    [point_num, weight, x, y]

Output should be a list that contains a list for each point pair
"""

from math import sqrt

#Input table : table = [point_num, weight, x-coord, y-coord]
distances = []

for point in table:
    x1 = point[2]
    y1 = point[3]
    for other in table:
        x2 = other[2]
        y2 = other[3]
        dist = sqrt((x2-x1)**2 + (y2-y1)**2)
        distances.append([point[0], other[0], dist])
