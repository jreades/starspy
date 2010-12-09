# modification of the mutation step based on cluster_ga11

import math
import numpy as np
import pysal
import Tkinter as tk
import time

Th_cluster=200

def ellipse(x,y,x0,y0,r1,r2,a):
    u=x*np.cos(a)+y*np.sin(a)-x0*np.cos(a)-y0*np.sin(a)
    v=y*np.cos(a)-x*np.sin(a)-y0*np.cos(a)+x0*np.sin(a)
    s=(u/r1)**2+(v/r2)**2
    return s

def ellipse2(x0,y0,r1,r2,theta,alpha):
    x=x0+r1*np.cos(alpha)*np.cos(theta)-r2*np.sin(alpha)*np.sin(theta)
    y=y0+r1*np.cos(theta)*np.sin(alpha)+r2*np.sin(theta)*np.cos(alpha)
    return x,y

def fitness(counts,radii,square,n):
    ratio=counts/(math.pi*radii[:,0]*radii[:,1]/square)**0.5
    return ratio

def cross1(population,x,y,data):
    centroid=(population.centroids[x]+population.centroids[y])/2
    radii0=(population.radii[x]+population.radii[y])/2
    if abs(population.angles[x]-population.angles[y])<np.pi/2:
        angle=(population.angles[x]+population.angles[y])/2
    else:
        angle=(population.angles[x]+population.angles[y]-np.pi)/2
        if angle<0:
            angle=angle+np.pi
    return centroid, radii0, angle

def cross2(population,x,y,data):
    centroid=population.centroids[x]
    radii0=population.radii[y]
    if abs(population.angles[x]-population.angles[y])<np.pi/2:
        angle=(population.angles[x]+population.angles[y])/2
    else:
        angle=(population.angles[x]+population.angles[y]-np.pi)/2
        if angle<0:
            angle=angle+np.pi
    return centroid, radii0, angle

def mutate(population,x,data,xmax,xmin,ymax,ymin):
    centroid=population.centroids[x]
    radii0=population.radii[x]
    angle=population.angles[x]
    fitness=population.fitness[x]
    rmax=min(ymax-ymin,xmax-xmin)/4
    if fitness<50:
        centroid[0]=centroid[0]+(np.random.random()-0.5)*(xmax-xmin)/2
        centroid[1]=centroid[1]+(np.random.random()-0.5)*(ymax-ymin)/2
        radii0=np.random.random(2)*rmax
    elif fitness<150:
        centroid[0]=centroid[0]+(np.random.random()-0.5)*radii0[0]*3
        centroid[1]=centroid[1]+(np.random.random()-0.5)*radii0[1]*3
        radii0[0]=radii0[0]*(np.random.random()*2.7+0.3)
        radii0[1]=radii0[1]*(np.random.random()*2.7+0.3)
        angle=np.random.random()*np.pi
    else:
        r=np.random.random()
        if r<0.3:
            centroid[0]=centroid[0]+(np.random.random()-0.5)*radii0[0]
            centroid[1]=centroid[1]+(np.random.random()-0.5)*radii0[1]       
        elif r<0.5:
            radii0[0]=radii0[0]*(np.random.random()+0.5)
        elif r<0.7:
            radii0[1]=radii0[1]*(np.random.random()+0.5)
        else:
            angle=angle+np.random.random()*np.pi/2-np.pi/4
            if angle>np.pi:
                angle=angle-np.pi
            elif angle<0:
                angle=angle+np.pi
    return centroid,radii0,angle

def intabu(c0,r0,a,ct,rt,nt):
    flag=0
    for i in np.arange(nt):
        dcx=c0[0]-ct[i][0]
        dcy=c0[1]-ct[i][1]
        rx=r0[0]+rt[i][0]
        ry=r0[1]+rt[i][1]
        if ellipse(c0[0],c0[1],ct[i][0],ct[i][1],rx,ry,a)<1:
            flag=1
    return flag

def notfar(population,i,j):
    x1=population.centroids[i][0]
    x2=population.centroids[j][0]
    y1=population.centroids[i][1]
    y2=population.centroids[j][1]
    r1=population.radii[i]
    r2=population.radii[j]
    if np.sqrt(((x1-x2)/(r1[0]+r2[0]))**2+((y1-y2)/(r1[1]+r2[1]))**2)<=3:
        return 1
    else:
        return 0

def select(population,nc,data):
    centroids=population.centroids
    radii=population.radii
    angles=population.angles
    fitness=population.fitness

    centroid2=np.empty((nc,2))
    radii2=np.empty((nc,2))
    angle2=np.empty((nc))
    
    fmax=max(fitness)
    fmin=min(fitness)
    i=0
    while i<nc:
        j=0
        while fitness[j]<fmax:
            j+=1
        centroid2[i]=centroids[j]
        radii2[i]=radii[j]
        angle2[i]=angles[j]
        fitness[j]=fmin
        fmax=max(fitness)
        i+=1
    new_population=Population(centroid2,radii2,angle2,data,square)
    return new_population

def create_random(n,xmax,xmin,ymax,ymin):
    centroids=np.random.random((n,2))
    centroids[:,0]=centroids[:,0]*(xmax-xmin)+xmin
    centroids[:,1]=centroids[:,1]*(ymax-ymin)+ymin
    rmax=min(ymax-ymin,xmax-xmin)/4
    radii=np.random.random((n,2))*rmax
    angle=np.zeros(n)
    return centroids,radii,angle

def create_random2(xmax,xmin,ymax,ymin):
    cen=np.random.random(2)
    cen[0]=cen[0]*(xmax-xmin)+xmin
    cen[1]=cen[1]*(ymax-ymin)+ymin
    rad=np.random.random(2)*rmax
    ang=0
    return cen,rad,ang  
        
def drawellipse(cen,r0,a0,canvas,xmax,xmin,ymax,ymin,color):
    dy=ymax-ymin
    dx=xmax-xmin
    if dy>dx:
        h0=1200
        w0=1000./dy*dx+200
        sx=1000*1./dy
    else:
        w0=1200
        h0=1000./dx*dy+200
        sx=1000*1./dx
    clusterids=[]
    x0=cen[0]
    y0=cen[1]
    r=sx*r0
    x1,y1=ellipse2(x0,y0,r0[0],r0[1],0,a0)
    print 'visualized radius:', r
    for j in range(361):
        a=j/360.*2*np.pi
        x2,y2=ellipse2(x0,y0,r0[0],r0[1],a,a0)
        x12=sx*(x1-xmin)+100
        y12=sx*(y1-ymin)+100
        x22=sx*(x2-xmin)+100
        y22=sx*(y2-ymin)+100            
        clusterids.append(canvas.create_line(x12,y12,x22,y22,fill=color))
        x1=x2
        y1=y2
    return clusterids


class Population:
    def __init__(self,centroids,radii,angles,data,square):
        self.centroids=centroids
        self.radii=radii
        self.angles=angles
        self.counts=np.zeros(len(centroids))
        self.data=data
        self.square=square
        self._set_counts()
        self._set_fitness()

    def _set_counts(self):
        for point in self.data:
            x,y=point
            for i,centroid in enumerate(self.centroids):
                cx,cy=centroid
                dx=(x-cx)
                dy=(y-cy)
                rx,ry=self.radii[i]
                a=self.angles[i]
                if ellipse(x,y,cx,cy,rx,ry,a)<=1:
                    self.counts[i]+=1
    def _set_fitness(self):
        self.fitness=fitness(self.counts,self.radii,self.square,len(self.data))
        
if __name__ == '__main__':
    path='C:\Python25\pysal-1.0.0\pysal\cluster\\'
    shp=pysal.open(path+'Point.shp')

    begin_time=time.clock()


    # get the pointset
    i=0
    n=len(shp)
    pos=np.ones((n,2))
    while i<n:
        pos[i]=shp.get(i)
        i=i+1
    pos0=pos

    # get the bound of points
    xmax=max(pos[:,0])
    xmin=min(pos[:,0])
    ymax=max(pos[:,1])
    ymin=min(pos[:,1])

    square=(ymax-ymin)*(xmax-xmin)

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
        x=sx*(pos[i,0]-xmin)+100
        y=sx*(pos[i,1]-ymin)+100
        canvas.create_oval(x-1,y-1,x+1,y+1,fill='black')
    canvas.pack()


    # generate the circles with random centroids and radiums
    nc=np.floor(n*0.1)
    rmax=min(ymax-ymin,xmax-xmin)/4
    centroids,radii,angles=create_random(nc,xmax,xmin,ymax,ymin)
    population=Population(centroids,radii,angles,pos,square)
    gen=0
    new_population=population
    fsum1=population.fitness.sum()
    fsum0=fsum1-100
    print fsum1
    #print population.centroids

    nc_detected=0
    centroids_detected=np.empty((50,2))
    radii_detected=np.empty((50,2))
    angle_detected=np.empty((50))
    flag=1
    
    while flag==1:
        while gen<50 and (fsum1-fsum0)/abs(fsum0)>0.003:
            fsum0=fsum1
            old_population=new_population        

            centroids=old_population.centroids
            radii=old_population.radii
            angles=old_population.angles
            i=0
            #cross
            for i in range(nc):
                x1=int(np.random.random()*nc)
                x2=int(np.random.random()*nc)
                while x1==x2 or notfar(old_population,x1,x2)==0:
                    x1=int(np.random.random()*nc)
                    x2=int(np.random.random()*nc)                   
                r=np.random.random()
                if r>0.5:
                    cen,rad,ang=cross1(old_population,x1,x2,pos)
                    while intabu(cen,rad,ang,centroids_detected,radii_detected,nc_detected):
                        cen,rad,ang=create_random2(xmax,xmin,ymax,ymin)
                else:
                    cen,rad,ang=cross2(old_population,x1,x2,pos)
                    while intabu(cen,rad,ang,centroids_detected,radii_detected,nc_detected):
                        cen,rad,ang=create_random2(xmax,xmin,ymax,ymin)
                centroids=np.vstack((centroids,cen))
                radii=np.vstack((radii,rad))
                angles=np.hstack((angles,ang))
                i=i+1
            #mutate
            for i in range(2*nc):
                x=int(np.random.random()*nc) 
                cen,rad,ang=mutate(old_population,x,pos,xmax,xmin,ymax,ymin)
                while intabu(cen,rad,ang,centroids_detected,radii_detected,nc_detected):
                    cen,rad,ang=create_random2(xmax,xmin,ymax,ymin)
                centroids=np.vstack((centroids,cen))
                radii=np.vstack((radii,rad))
                angles=np.hstack((angles,ang))
                i=i+1
            population=Population(centroids,radii,angles,pos,square)
            new_population=select(population,nc,pos)
            fsum1=new_population.fitness.sum()
            print fsum1
            gen+=1
        print 'generation:', gen
        #print new_population.centroids
        #print new_population.radii


        clusterids=[]
        fmax=0
        for i,point in enumerate(new_population.centroids):
            x=sx*(point[0]-xmin)+100
            y=sx*(point[1]-ymin)+100
            r=sx*new_population.radii[i]
            if new_population.fitness[i]>fmax:
                i_fmax=i
                fmax=new_population.fitness[i]
            #clusterids.append(canvas.create_oval(x-r,y-r,x+r,y+r,outline='blue'))
        cen=new_population.centroids[i]
        rad=new_population.radii[i]
        f0=new_population.fitness[i]
        ang=new_population.angles[i]
        c0=new_population.counts[i]
        
        #threshold of fitness
        if f0>Th_cluster and c0>10 and intabu(cen,rad,ang,centroids_detected,radii_detected,nc_detected)==0:
            
            print 'Cluster ',nc_detected+1
            print 'Pos: (',cen[0],',',cen[1],')'
            print 'radius: ',rad[0],',',rad[1]
            print 'Angle: ',ang
            print 'Counts: ',c0
            print 'Fitness: ',f0
            #visualizing
            drawellipse(cen,rad,ang,canvas,xmax,xmin,ymax,ymin,'red')
            
            #add the solution/tabu
            centroids_detected[nc_detected][0]=cen[0]
            centroids_detected[nc_detected][1]=cen[1]
            radii_detected[nc_detected]=rad
            angle_detected[nc_detected]=ang
            nc_detected+=1
            # delect the points in the detected cluster
            pos2=np.empty((0,2))
            for i in range(len(pos)):
                x=pos[i][0]
                y=pos[i][1]
                if ellipse(x,y,cen[0],cen[1],rad[0],rad[1],ang)>1:
                    pos2=np.vstack((pos2,pos[i]))
            pos=pos2
            
            # generate the circles with random centroids and radiums
            centroids,radii,angles=create_random(nc,xmax,xmin,ymax,ymin)
            population=Population(centroids,radii,angles,pos,square)
            gen=0
            new_population=population
            fsum1=population.fitness.sum()
            fsum0=fsum1-100            
        else:
            flag=0
            
        end_time=time.clock()
    print 'Run time: ',end_time-begin_time
    
    #ratio test
    