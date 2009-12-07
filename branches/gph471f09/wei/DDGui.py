from Tkinter import *
from FileReader import *
from ComputeGeometry import *



class View():
    '''the class for all gui operation
    class attributes: TK root: gui root
                      Dictionary cList: coordinate dictionary for saving all the shapes' coordinates in input shape file
                      Dictionary attrList: attribute dictionary for saving all the shapes' attributes in input dbf file
                      Canvas mapCav: canvas for displaying map
                      Canvas tsCav: canvas for displaying time series
                      Double firstX: the TopLeft vertex' X coordinate of the rectangle for selecting polygon in the map 
                      Double firstY: the TopLeft vertex' Y coordinate of the rectangle for selecting polygon in the map
                      Double lastX: the BottomRight vertex' X coordinate of the rectangle for selecting polygon in the map
                      Double lastY: the BottomRight vertex' Y coordinate of the rectangle for selecting polygon in the map
                      List selectedPolyID: list for saving the selected polygons' ID
                      '''
    def __init__(self,root,mapCav,tsCav,mapFilePath="D:\\py_workplace\\drag and drop project\\California.shp", dbfFilePath="D:\\py_workplace\\drag and drop project\\California.dbf"):
        '''construction function: initialize the instance of Class View 
        input: gui root
               cavas for map
               canvas for time series
               shape file path
               dbf file path
        '''       
        #initialize cList by the input shape file
        self.cList={}   
        shp = SHPReader(mapFilePath)
        shp.readshp()
        for i in range(len(shp.coordList)):
            self.cList[i] = shp.coordList[i]  
            
        #initialize attrList by the input dbf file
        self.attrList={}
        dbf = DBFReader(dbfFilePath)
        dbf.readdbf()
        for j in range(len(dbf.attributeList)):
            self.attrList[j] = dbf.attributeList[j] 
            
        #initialize other attributes of the instance    
        self.root = root    
        self.mapCav = mapCav
        self.tsCav = tsCav
        self.firstX=0
        self.firstY=0
        self.lastX=0
        self.lastY=0
        self.selectedPolyID=[]
        
        #bind the widgets with events
        self.mapCav.bind('<Button-1>', self.mouseLeftClick)
        self.mapCav.bind('<ButtonRelease-1>', self.mouseLeftRelease)
        self.mapCav.bind('<B1-Motion>', self.mouseMove)
        self.tsCav.bind('<Enter>', self.mouseEnterInTS)
        
        
    def drawMap(self):
        '''draw the polygons on the mapCav, according to the coordinates saved in cList
        '''
        for c in self.cList.values():
            self.mapCav.create_polygon(tuple(c),fill='green',outline='black',tags='initialMap')
            
    def mouseLeftClick(self,event):
        '''response function for mouse left click event on the mapCav:
        mainly to assign the event's coordinates to firstX and firstY 
        '''
        if self.selectedPolyID:
            self.mapCav.config(cursor='right_side')            
        else:            
            self.mapCav.delete('selector')
            self.mapCav.delete('selectedPoly')
            self.firstX=event.x
            self.firstY=event.y
        
    def mouseMove(self,event):
        '''response function for mouse move event on the mapCav:
        mainly to move the selected rectangle
        '''
        if not self.selectedPolyID:
            self.mapCav.delete('movingRectangle')
            self.mapCav.create_rectangle((self.firstX,self.firstY,event.x,event.y), outline='black',tags=('movingRectangle'))
        else:
            self.mapCav.delete('selector')
            dx=(self.lastX-self.firstX)/2
            dy=(self.lastY-self.firstY)/2
            self.mapCav.delete('draggingRectangle') 
            self.mapCav.create_rectangle((event.x-dx,event.y-dy,event.x+dx,event.y+dy), outline='black',tags=('draggingRectangle'))
       
    def mouseLeftRelease(self,event):
        '''response function for mouse left release event on the mapCav:
        mainly to create the selected rectangle, save the selected polygons' ID in the selectedPolyID
        and highlight the selected polygons
        '''        
        if not self.selectedPolyID:
            # create the selected rectangle
            self.mapCav.delete('movingRectangle')
            self.lastX=event.x
            self.lastY=event.y
            self.mapCav.create_rectangle((self.firstX,self.firstY,self.lastX,self.lastY), outline='black',tags=('selector'))
            
            #save the selected polygons' ID in the selectedPolyID
            rect = [self.firstX,self.firstY,self.lastX,self.lastY]
            for key,pol in self.cList.items():
                if rectangleIntersectPolygon(rect,pol):
                    self.selectedPolyID.append(key)
            
            #highlight the selected polygons
            for k,po in self.cList.items():
                if k in self.selectedPolyID:
                    self.mapCav.create_polygon(tuple(po),fill='red',outline='yellow',tags=('selectedPoly'))
                    
            self.mapCav.tag_raise('selector')
            
    def drawTimeSeries(self):
        '''draw time curve for the sum of selected polygons' hospitalization values on the tsCav, 
        according to the polygons' ID saved in selectedPolyID
        '''
        self.drawCoordinates()
        sum_901=0
        sum_915=0
        sum_926=0
        if self.selectedPolyID:
            #if the selectedPolyID is not empty, display the sum of selected polygons' hospitalization values
            for poly in self.selectedPolyID:
                sum_901=sum_901+self.attrList[poly][8]
                sum_915=sum_915+self.attrList[poly][7]
                sum_926=sum_926+self.attrList[poly][9]
            self.selectedPolyID=[]
        else:
            #if the selectedPolyID is empty, display the sum of all polygons' hospitalization values
            for attr in self.attrList.values():
                sum_901=sum_901+attr[8]
                sum_915=sum_915+attr[7]
                sum_926=sum_926+attr[9]
                
        print sum_901
        print sum_915
        print sum_926
        
        #transform the actual value into the corresponding canvas coordinates
        transform_sum901=370-(sum_901/10)
        transform_sum915=370-(sum_915/10)
        transform_sum926=370-(sum_926/10)        

        #draw time curve        
        self.tsCav.create_line((90,transform_sum901,170,transform_sum915),arrow='none', tags=('tsLine'))
        self.tsCav.create_line((170,transform_sum915,250,transform_sum926),arrow='none', tags=('tsLine'))
        self.tsCav.create_oval((90-2,transform_sum901-2,90+2,transform_sum901+2),fill='red', tags=('tsLine'))
        self.tsCav.create_oval((170-2,transform_sum915-2,170+2,transform_sum915+2),fill='red', tags=('tsLine'))
        self.tsCav.create_oval((250-2,transform_sum926-2,250+2,transform_sum926+2),fill='red', tags=('tsLine'))
    
    def drawCoordinates(self):
        '''draw the x axis representing time period, 
        y axis representing hospitalization value
        '''
        #draw x and y axis
        self.tsCav.create_line((50,400,300,400),arrow='last')
        self.tsCav.create_line((50,400,50,50),arrow='last')
        self.tsCav.create_text((330,410),text='Date(month/day)')
        self.tsCav.create_text((50,40),text='Hospitalization')
        #draw x scale
        self.tsCav.create_line((90,400,90,395),arrow='none')
        self.tsCav.create_text((90,410),text='9/01')
        self.tsCav.create_line((170,400,170,395),arrow='none')
        self.tsCav.create_text((170,410),text='9/15')
        self.tsCav.create_line((250,400,250,395),arrow='none')
        self.tsCav.create_text((250,410),text='9/26')
        #draw y scale
        self.tsCav.create_line((50,370,55,370),arrow='none')
        self.tsCav.create_text((40,370),text='0')
        self.tsCav.create_line((50,320,55,320),arrow='none')
        self.tsCav.create_text((40,320),text='500')        
        self.tsCav.create_line((50,270,55,270),arrow='none')
        self.tsCav.create_text((40,270),text='1000')
        self.tsCav.create_line((50,220,55,220),arrow='none')
        self.tsCav.create_text((40,220),text='1500')
        self.tsCav.create_line((50,170,55,170),arrow='none')
        self.tsCav.create_text((40,170),text='2000')
        self.tsCav.create_line((50,120,55,120),arrow='none')
        self.tsCav.create_text((40,120),text='2500')
        self.tsCav.create_line((50,70,55,70),arrow='none')
        self.tsCav.create_text((40,70),text='3000')        
       
    def mouseEnterInTS(self, event):
        '''response function for mouse enter event on the tsCav:
        mainly to redraw the time curve according to the new selected polygons
        '''      
        self.tsCav.focus_set()
        self.tsCav.delete('tsLine')
        self.drawTimeSeries()
        print "enter TS"
        

        
    
if __name__=='__main__':
    #construct the root window 
    root = Tk()
    root.title('H1N1 Hospitalization Map and Time Seires')  
    
    #construct the canvas for map and time series
    cav_map = Canvas(root,bg='white')
    cav_timeSeries = Canvas(root,bg='white')
    cav_map.config(height = 500, width=500) 
    cav_timeSeries.config(height = 500, width=380) 
    
    #construct the instance of View using root and two canvases
    viewRoot = View(root,cav_map,cav_timeSeries)  
    viewRoot.drawMap()
    viewRoot.drawTimeSeries()
    root.geometry('900x510+25+30')

    cav_map.pack(fill=Y, expand=1,side=LEFT)
    cav_timeSeries.pack(fill=Y, expand=1, side=RIGHT)
 
    root.mainloop()





        

    