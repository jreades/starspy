import tempfile
f = tempfile.NamedTemporaryFile(suffix = '.shp'); fname = f.name; f.close()
import pysal
i = pysal.open('shapefile.shp', 'r')
o = pysal.open(fname, 'w')
for shp in i:
    o.write(shp)
o.close()
open('shapefile.shp','rb').read() == open(fname,'rb').read()
open('shapefile.shx','rb').read() == open(fname[:-1]+'x','rb').read()
import os
os.remove(fname); os.remove(fname.replace('.shp','.shx'))
