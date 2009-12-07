from shapely.geometry import Polygon

    
def rectangleIntersectPolygon(rect,poly): 
    '''judge whether a rectangle intersect a polygon
    input: List rect: the rectangle's coordinate list, like [0,0,1,1]
           List poly: the polygon's coordinate list, like [0,0,1,0,1,1,0,1,0,0]
    output: Boolean bool: the boolean value for indicating whether the rectangle intersect the polygon
    '''
    #tranform rectangle's coordinate list into polygon's coordinate list
    if len(rect)==4:
        rect=transformRectangelToPolygon(rect)
    
    i=0
    j=0
    rectPoList=[]
    polyPoList=[]
    
    #change the data format of the two coordinate lists, like from [0,0,1,0,1,1,0,1,0,0] to [[(0,0),(1,0),(1,1),(0,1),(0,0)] 
    while i<len(rect):
        po1=(rect[i],rect[i+1])
        rectPoList.append(po1)
        i=i+2        
       
    while j<len(poly):
        po2=(poly[j],poly[j+1])
        polyPoList.append(po2)
        j=j+2
    
    #initialize the instance of Class Polygon in package shapely
    rectReal=Polygon(tuple(rectPoList))
    polyReal=Polygon(tuple(polyPoList)) 
    
    #call intersects() in shapely to judge whether they two intersects
    if rectReal.intersects(polyReal):
        return True
    else:
        return False
    
def transformRectangelToPolygon(rect):
    '''tranform the rectangle's coordinate list format into a polygon's coordinate list format
    input: List rect: the rectangle's coordinate list, like [0,0,1,1]
    output: List poly: the transformed coordinate list, like [0,0,1,0,1,1,0,1,0,0]
    '''
    return [rect[0],rect[1],rect[0],rect[3],rect[2],rect[3],rect[2],rect[1]]



if __name__=='__main__':
    print polygonIntersectPolygon([0,0,1,1],[0,0,1,0,1,1,0,1,0,0])
    