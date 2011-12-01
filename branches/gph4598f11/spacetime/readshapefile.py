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
