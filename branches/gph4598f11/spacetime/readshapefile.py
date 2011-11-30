import pysal
shp = pysal.open('Shapefiles/Arizona_Counties_2010.shp', 'r')
db = pysal.open('Shapefiles/Arizona_Counties_2010.dbf')
table = []
p =0

for poly in shp:
  c = poly.centroid
  c = list(c)
  data = db.next()
  table.append([p,c,data])
  p = p+1

for i in table:
    print i
