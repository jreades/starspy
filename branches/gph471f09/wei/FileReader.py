from pysal import *
from pysal.cg.shapes import *

class SHPReader():
    '''read shapefile
    Class attributes: String filepath: the file path of shape file
                      List coordList: list for saving coordinates of the shapes in the shape file
                      '''
    def __init__(self,filepath="D:\\py_workplace\\drag and drop project\\California.shp"):
        '''construction function: initialize the instance of Class shpReader 
        input: the file path of shape file
        '''    
        self.filepath=filepath
        self.coordList=[]
        
    def readshp(self):
        '''read shapefile, transform longitude and latitude into canvas coordinates
        and save them into coordList
        '''
        #call pysal.open() to read shape file
        shp = pysal.open(self.filepath)
        
        #transform longitude and latitude into screen coordinates
        minxList=[]
        maxxList=[]
        minyList=[]
        maxyList=[]
                
        for i in range(len(shp)):
            ashp = shp.get(i)
            
            able=ashp.bounding_box.left
            abri=ashp.bounding_box.right
            ablo=ashp.bounding_box.lower
            abup=ashp.bounding_box.upper
            
            minxList.append(able)
            maxxList.append(abri)
            minyList.append(ablo)
            maxyList.append(abup)
        
        minX = min(minxList)    
        maxX = max(maxxList)
        minY = min(minyList)
        maxY = max(maxyList)
        scaleX = maxX-minX
        scaleY = maxY-minY
        
        #set self.coordList as the screen coordlist
        for i in range(len(shp)):
            j=0
            transCoor=[]
            coorList = [] 
            ashp = shp.get(i)
            
            for vert in ashp.vertices:
                for point in vert:
                    coorList.append(point)
    
            while j<len(coorList):
                transCoor.append(((coorList[j]-minX)*500)/scaleX)
                transCoor.append(((maxY-coorList[j+1])*500)/scaleY)
                j=j+2
            
            self.coordList.append(transCoor)
                                    
      
class DBFReader():
    '''read dbf file
    Class attribute: String filepath: the file path of dbf file
                     List attributeHeader: list for saving the fields' names in dbf file
                     List attributeList: list for saving the records in dbf file'''
    def __init__(self, filepath="D:\\py_workplace\\drag and drop project\\California.dbf"):
        '''construction function: initialize the instance of Class dbfReader 
        input: the file path of dbf file
        '''    
        self.filepath=filepath
        self.attributeHeader=[]
        self.attributeList=[]
        
    def readdbf(self):
        '''read dbf file, save the fields' names into attributeHeader
        and save the records into attributeList
        '''
        #call pysal.open() to read dbf file
        db=pysal.open(self.filepath)
        
        #save the records into attributeList
        for attr in db:
            self.attributeList.append(attr)
            
        #save the fields' names into attributeHeader
        for atnm in db.header:
            self.attributeHeader.append(atnm)
            
        

if __name__=='__main__':
    testshp=SHPReader()
    testshp.readshp()
    testshp.compute_bbox()
    print len(testshp.coordList)
    print testshp.bboxList
    print len(testshp.bboxList)
    testdbf=DBFReader()
    testdbf.readdbf()
    print testdbf.attributeHeader
    print testdbf.attributeList

