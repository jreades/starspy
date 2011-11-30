shp = pysal.open('Arizona_Counties_2010.shp', 'r')
db = pysal.open('Arizona_Counties_2010.dbf')
table = []
p =0

for poly in shp:
  c = poly.centroid
  data = db.next()
  table.append([p,c,data])
  p = p+1
