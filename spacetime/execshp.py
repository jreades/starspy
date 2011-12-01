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

for i in table:
    print i
