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

for i in table:
    print i
