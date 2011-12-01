"""
This script is very similar to the readshapefile.py script except that it is used for adding more shapefiles to the table.
"""
p =0
t = t+1

for poly in shp:
  c = poly.centroid
  c = list(c)
  data = db.next()
  table.append([p,c,data,t])
  p = p+1

