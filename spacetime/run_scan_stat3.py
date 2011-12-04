"""
This is the script that is used to create a table from all of the needed shapefiles. The first shapefile needs to be added using the readshapefile script and all subsiquent files are added using the addshp.py script. Any number of files may be added by repeating lines 11-13 as is seen in lines 15-17.
"""

import pysal

shp = pysal.open('Shapefiles/Arizona_Counties_1990.shp')
db = pysal.open('Shapefiles/Arizona_Counties_1990.dbf')
execfile('readshapefile.py')

shp = pysal.open('Shapefiles/Arizona_Counties_2000.shp')
db = pysal.open('Shapefiles/Arizona_Counties_2000.dbf')
execfile('addshp.py')

shp = pysal.open('Shapefiles/Arizona_Counties_2010.shp')
db = pysal.open('Shapefiles/Arizona_Counties_2010.dbf')
execfile('addshp.py')

"""for i in table:
    print i
"""
"""
This script takes a shapefile that is specified in the execshp.py file, calculates that centroid, assigns an id starting at 0 and then creates a table that includes the point id, the centroid, the data from the shapes dbf and the time period which always starts at 1.
"""


table = []
p = 0
t = 1

for poly in shp:
    c = poly.centroid
    c = list(c)
    data = db.next()
    table.append([p,c,data,t])
    p = p+1

"""
This script is very similar to the readshapefile.py script except that it is used for adding more shapefiles to the table.
"""
"""

p =0
t = t+1

for poly in shp:
    c = poly.centroid
    c = list(c)
    data = db.next()
    table.append([p,c,data,t])
    p = p+1
"""
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
    x1 = point[1][0]
    y1 = point[1][1]
    for other in table:
        x2 = other[1][0]
        y2 = other[1][1]
        dist = sqrt((x2-x1)**2 + (y2-y1)**2)
        distances.append([point[0], dist, other[0]])
    distances.sort()

    for i in distances:
        print i
"""
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


point_num = 1
relationship_table = []
for point in distances:
    neighbors = []
    if point[0] == point_num:
        neighbors.append(point[2])
    point_num += 1
    relationship_table.append(neighbors)
"""

"""Need input table and distance table for inputs"""

"""import calc_total_ratio"""



total_pop_total = 0.0
for i in table:
    total_pop_total =+ table[2][3]

total_w = 0.0
for i in table:
    total_w =+ i[2][4]

outside_total_ratio = total_w / total_pop_total

import warnings
warnings.filterwarnings("ignore", " ", category = 'exceptions.OverflowError')



likelihood_ratios = []
for i in distances:
    for j in table:
        if i[2] == j[0]:
            nz = float(j[2][4])
            mz = float(j[2][3]) * outside_total_ratio
            bigN = total_pop_total
            hyp_test = "Accept Null"
            if nz > mz:
                hyp_test = "Reject Null"
            likeratio = ((nz/mz)**nz)*(((bigN-nz)/(bigN-mz))**(bigN-nz))
            likelihood_ratios.append([i[0], i[2], likeratio, hyp_test ])

for i in likelihood_ratios:
    print i











if __name__ == '__main__':
    import doctest
    doctest.testmod()
