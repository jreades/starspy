p =0
t = t+1

for poly in shp:
  c = poly.centroid
  c = list(c)
  data = db.next()
  table.append([p,c,data,t])
  p = p+1

