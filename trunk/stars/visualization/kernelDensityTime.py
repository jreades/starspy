""" 
Yet Another Kernel Density Implementation in Python

This one supports updating the raster one event at a time, to allow for time series visualization.
"""

from sys import stdout
import pysal
import numpy
from math import exp,pi,ceil,floor,sqrt
try:
    from osgeo import gdal, gdal_array
    from osgeo.gdalconst import GDT_Float64
except ImportError:
    import gdal, gdal_array
    from gdalconst import GDT_Float64

def triangular(z):
    return 1 - abs(z)

def uniform(z):
    return abs(z)

def quadratic(z):
    return 0.75*(1 - z*z)

def quartic(z):
    return (15*1.0/16)*(1-z*z)*(1-z*z)

def gaussian(z):
    return sqrt(2*pi)*exp(-0.5*z*z)

class KernelDensity:
    """
    Kernel Density Estimation
    
    ptGeoObj -- PySAL Point Geo Object -- pysal.open('points.shp','r')
    cellSize -- int -- In Map Units.
    bandwidth -- float -- In Map Units.

    """
    def __init__(self, extent, cellSize, bandwidth, kernel='quadratic', extent_buffer=0):
        left, lower, right, upper = extent
        left,lower = left-extent_buffer,lower-extent_buffer
        right,upper = right+extent_buffer,upper+extent_buffer
        self.extent = pysal.cg.Rectangle(left,lower,right,upper)
        self.cellSize = cellSize
        self.bandwidth = bandwidth
        self.kernel = quadratic
        if kernel not in ['triangular', 'uniform', 'quadratic', 'quartic', 'gaussian']:
            raise 'Unsupported Kernel Type'
        else:
            self.kernel = eval(kernel)
        self._raster = numpy.zeros((self.rows,self.cols))
        self.bw = bandwidth
        self.cellSize = float(cellSize)
        self.grid_lower = lower+(cellSize/2.0)
        maxRow = self.rows-1
        self.grid_upper = self.grid_lower + (maxRow*self.cellSize)
        self.grid_left = left+(self.cellSize/2.0)
        self._n = 0
    def update(self,X,Y,invert=False):
        self._n += 1
        cellSize = self.cellSize
        radius = self.bandwidth / cellSize
        float_i = (Y-self.grid_lower) / cellSize
        #float_i = (self.grid_upper-Y) / cellSize
        i = int(floor(float_i - radius))
        i = i if i >= 0 else 0
        I = int(floor(float_i + radius))
        I = I if I < self.rows else self.rows-1

        float_j = (X-self.grid_left) / cellSize
        j = int(floor(float_j - radius))
        j = j if j >= 0 else 0
        J = int(floor(float_j + radius))
        J = J if J < self.cols else self.cols-1
        #print
        #print "update rows[%d:%d], cols[%d:%d]"%(i,I,j,J)
        for row in xrange(i,I+1):
            for col in xrange(j,J+1):
                x = self.grid_left+(col*cellSize)
                y = self.grid_lower+(row*cellSize)
                #y = self.grid_upper-(row*cellSize)
                d = ((x-X)**2 + (y-Y)**2) ** (0.5)
                if d <= self.bw:
                    z = d/self.bw
                    if invert:
                        self._raster[row,col] -= self.kernel(z)
                    else:
                        #print "update[%d,%d]"%(row,col)
                        self._raster[row,col] += self.kernel(z)
    @property
    def raster(self):
        return self._raster / (self._n*self.bw)
    @property
    def cols(self):
        return int(ceil(self.extent.width / float(self.cellSize)))
    @property
    def rows(self):
        return int(ceil(self.extent.height / self.cellSize))
    def erdasImage(self, outfilename):
        mpValue = self.mpValue
        mpArray = self.mpArray
        driver = gdal.GetDriverByName('HFA')
        out = driver.Create(outfilename, self.cols, self.rows, 1, GDT_Float64)
        if mpValue and hasattr(mpValue, 'value'):
            mpValue.value = 1
            mpArray.value = "The output image file is created."
        try:
            out.SetGeoTransform([self.extent.left, self.extent.width/self.cols, 0, self.extent.lower, 0, self.extent.height/self.rows])
            gdal_array.BandWriteArray(out.GetRasterBand(1), self.raster)
            mpValue.value = 100
            mpArray.value = "The output image file is successfully written."
            return True
        except:
            mpValue.value = 100
            mpArray.value = "Image writing failed."
            return False
    def asciiTable(self):
        mpValue = self.mpValue
        mpArray = self.mpArray
        tot = float(self.rows)
        s = "ncols %d\n"%self.cols
        s+= "nrows %d\n"%self.rows
        s+= "xllcorner %f\n"%self.extent.left
        s+= "yllcorner %f\n"%self.extent.lower
        s+= "cellsize %f\n"%self.cellSize
        s+= "nodata_value -1\n"
        c = 0
        for i in xrange(self.rows-1,-1,-1):
            for j in xrange(self.cols):
                s+="%f "%self.raster[i,j]
            s+="\n"
            if mpValue and hasattr(mpValue,'value'):
                c += 1
                mpValue.value = int(round((c/tot)*100))
            if mpArray and hasattr(mpArray,'value'):
                mpArray.value = "Saving... %d of %d rows remaining"%(i,tot)
            else:
                stdout.write('\r%f%% Complete.'%(100*(c/tot)))
                stdout.flush()
        return s

if __name__=='__main__':
    def draw(kd):
        img = numpy.zeros((kd.rows,kd.cols,3),numpy.uint8)
        raster = kd.raster
        scaled = (raster-raster.min())/(raster.max()-raster.min())
        img[:,:,0] = (scaled*255).astype("B") #red
        img[:,:,2] = ((1+(scaled*-1))*255).astype("B") #blue
        return Image.fromarray(img)
    import time
    import datetime
    from PIL import Image,ImageDraw
    t0 = time.clock()
    #shp = pysal.open('/Users/charlie/Documents/data/pittsburgh/pitthom.shp','r')
    shp = pysal.open('/Users/charlie/Documents/Work/NIJ/Target1/Mesa Data/Mesa_ResBurgAllYears_withGrids/Mesa_ResBurgAllYears_withGrids.shp','r')
    dbf = pysal.open('/Users/charlie/Documents/Work/NIJ/Target1/Mesa Data/Mesa_ResBurgAllYears_withGrids/Mesa_ResBurgAllYears_withGrids.dbf','r')
    dates = dbf.by_col("REPORT_DAT")
    data = dict([(date,set()) for date in dates])
    for date,point in zip(dates,shp):
        data[date].add(point)
    dates.sort()
    extent = [shp.header.get(x) for x in ['BBOX Xmin', 'BBOX Ymin', 'BBOX Xmax', 'BBOX Ymax']]
    kd = KernelDensity(extent,400,3500)
    #open('kd_ascii.txt','w').write(kd.asciiTable())
    start = dates[0]
    cur = start
    step = datetime.timedelta(days=1)
    window = datetime.timedelta(days=120)
    window = None
    end = dates[-1]
    #for i,date in enumerate(dates):
    i = 0
    while cur <= end:
        if cur in data:
            evts = data[cur]
            if window:
                clear = cur-window
                if clear in data:
                    for rx,ry in data[clear]:
                        kd.update(rx,ry,True)
            for x,y in evts:
                kd.update(x,y)
        img = draw(kd)
        d = ImageDraw.Draw(img)
        if window:
            d.text((0,0),clear.isoformat()+" through "+cur.isoformat())        
        else:
            d.text((0,0),cur.isoformat())        
        del d
        img.save("kd/kd_%d.png"%i)
        i+=1
        cur+=step
    print time.clock()-t0

