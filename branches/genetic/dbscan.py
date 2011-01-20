
import math
import numpy as np
import pysal
import Tkinter as tk
import time    

class Point:
    def __init__(self,pos,dataId,clId):
        self.pos=pos
        self.dataId=dataId
        self.clId=clId

class Seeds:
    def __init__(self,data,dataId,clId):
        self.data=data
        n=len(data)
        self.size=n
        self.dataId=dataId
        self.clId=clId
        
    def get(self,i):
        point=Point(self.data[i],self.dataId[i],self.clId[i])
        return point
        
    def delete(self,point):
        n=point.dataId
        self.data=np.delete(self.data,n,0)
        self.dataId=np.delete(self.dataId,n,0)
        self.clId=np.delete(self.clId,n,0)
        self.size=self.size-1
    
    def append(self,point):
        self.data=np.vstack((self.data,point.pos))
        self.dataId=np.hstack((self.dataId,point.dataId))
        self.clId=np.hstack((self.clId,point.clId))
        self.size=self.size+1
        
class SetOfPoints:
    def __init__(self,data):
        self.data=data
        n=len(data)
        self.size=n
        self.clId=np.zeros(n)-1
        self.dataId=np.empty(n)
        for i in range(n):
            self.dataId[i]=i
    
    def get(self,i):
        point=Point(self.data[i],self.dataId[i],self.clId[i])
        return point
    
    def regionQuery(self,point,Eps):
        data_seeds=np.empty((0,2))
        dataId_seeds=np.empty(0)
        clId_seeds=np.empty(0)
        for i in range(n):
            if Distance(point.pos,self.data[i])<Eps:
                data_seeds=np.vstack((data_seeds,self.data[i]))
                dataId_seeds=np.hstack((dataId_seeds,self.dataId[i]))
                clId_seeds=np.hstack((clId_seeds,self.clId[i]))
        seeds=Seeds(data_seeds,dataId_seeds,clId_seeds)
        return seeds
    
    def changeClIds(self,seeds,s_clId):
        for i in seeds.dataId:
            self.clId[i]=s_clId
                
def ExpandCluster(setofPoints,point,ClId,Eps,MinPts):
    seeds=setOfPoints.regionQuery(point,Eps)
    if seeds.size<MinPts:
        setOfPoints.clId[point.dataId]=0
        return 0
    else:
        setOfPoints.changeClIds(seeds,ClId)
        seeds.delete(point)
        while seeds.size>0:
            currentP=seeds.get(0)
            result=setOfPoints.regionQuery(currentP,Eps)
            if result.size>=MinPts:
                for i in range(result.size):
                    resultP=result.get(i)
                    if resultP.clId in [-1,0]:
                        if resultP.clId==-1:
                            seeds.append(resultP)
                        setOfPoints.clId[resultP.dataId]=ClId
            seeds.delete(currentP)
        return 1 
                        
def Distance(pos1,pos2):
    distance=0
    n=len(pos1)
    for i in range(n):
        distance=distance+(pos1[i]-pos2[i])**2
    distance=distance**0.5
    return distance
    
if __name__ == '__main__':
    path='C:\Python25\pysal-1.0.0\pysal\cluster\\'
    shp=pysal.open(path+'Point.shp')
    
    Eps=0.03
    MinPts=4

    # get the pointset
    i=0
    n=len(shp)
    data=np.ones((n,2))
    while i<n:
        data[i]=shp.get(i)
        i=i+1
    
    setOfPoints=SetOfPoints(data) 

    begin_time=time.clock()
    
    ClusterId=1
    for i in range(n):
        point=setOfPoints.get(i)
        if point.clId==-1:    
            if ExpandCluster(setOfPoints,point,ClusterId,Eps,MinPts):
                ClusterId=ClusterId+1
                 
    end_time=time.clock()
    
    #visualizing
    xmax=max(data[:,0])
    xmin=min(data[:,0])
    ymax=max(data[:,1])
    ymin=min(data[:,1])

    top=tk.Tk()
    dy=ymax-ymin
    dx=xmax-xmin
    if dy>dx:
        h0=1200
        w0=1000/dy*dx+200
        sx=1000*1./dy
    else:
        w0=1200
        h0=1000/dx*dy+200
        sx=1000*1./dx
    canvas=tk.Canvas(top,height=h0,width=w0)
    for i in range(n):
        x=sx*(setOfPoints.data[i,0]-xmin)+100
        y=sx*(setOfPoints.data[i,1]-ymin)+100
        if setOfPoints.clId[i]>0:
            canvas.create_oval(x-3,y-3,x+3,y+3,fill='red')
        else:
            canvas.create_oval(x-3,y-3,x+3,y+3,fill='black')    
    canvas.pack()

    
    '''
    for i in range(n):
        a=setOfPoints.clId[i]
        print i,a
    ''' 

    
    print 'Run time: ',end_time-begin_time
