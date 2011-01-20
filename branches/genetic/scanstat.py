
import math
import numpy as np
import pysal
import Tkinter as tk
import time    
    
if __name__ == '__main__':
    path='C:\Python25\pysal-1.0.0\pysal\cluster\\'
    shp=pysal.open(path+'Point.shp')
    
    size=0.02
    th=0.38

    # get the pointset
    i=0
    n=len(shp)
    data=np.ones((n,2))
    while i<n:
        data[i]=shp.get(i)
        i=i+1

    begin_time=time.clock()
    
    xmax=max(data[:,0])
    xmin=min(data[:,0])
    ymax=max(data[:,1])
    ymin=min(data[:,1])
    
    #visualizing
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
        x=sx*(data[i,0]-xmin)+100
        y=sx*(data[i,1]-ymin)+100
        canvas.create_oval(x-1,y-1,x+1,y+1,fill='black')
    canvas.pack()
    
    rmax=max(dx/2,dy/2)
    rmin=size
    
    x_size=int(dx/size)+1
    y_size=int(dy/size)+1
    clusterids=[]
    density=n/(dx*dy)
    totalCount=0
    llrMax=0
    for i in range(x_size):
        x=xmin+i*size
        for j in range(y_size):    
            y=ymin+j*size
            for k in range(int(rmax/rmin)):
                r=(k+1)*rmin
                count=0
                for iCount in range(n):
                    x0=data[iCount,0]
                    y0=data[iCount,1]
                    if (x0-x)**2+(y0-y)**2<r**2:
                        count=count+1
                    ec=density*(np.pi*r*r)
                    if count>ec:
                        llr=np.log((count/ec)**count)*((n-count)/(n-ec))**(n-count)
                        if llr>llrMax:
                            llrMax=llr
                    else:
                        llr=0
                    if llr>th:
                        #visualizing
                        x1=sx*(x-xmin)+100
                        y1=sx*(y-ymin)+100
                        r1=sx*r
                        clusterids.append(canvas.create_oval(x1-r1,y1-r1,x1+r1,y1+r1,outline='red'))
                    totalCount=totalCount+1
    print totalCount
    print llrMax
    end_time=time.clock()
    
   
    '''
    for i in range(n):
        a=setOfPoints.clId[i]
        print i,a
    ''' 

    
    print 'Run time: ',end_time-begin_time
