#add the angle constraint based on cluster_ga_origin_6.py

import math
import numpy as np
import pysal
import Tkinter as tk
import time
Fitness_Th=50
Num_Th=10

def ellipse(x,y,x0,y0,r1,r2,a):
    u=x*np.cos(a)+y*np.sin(a)-x0*np.cos(a)-y0*np.sin(a)
    v=y*np.cos(a)-x*np.sin(a)-y0*np.cos(a)+x0*np.sin(a)
    s=(u/r1)**2+(v/r2)**2
    return s

def ellipse2(x0,y0,r1,r2,theta,alpha):
    x=x0+r1*np.cos(alpha)*np.cos(theta)-r2*np.sin(alpha)*np.sin(theta)
    y=y0+r1*np.cos(theta)*np.sin(alpha)-r2*np.sin(theta)*np.cos(alpha)
    return x,y
    
def lnfactorial(n):
    n=int(n)
    if n==0:
        return 1
    else:
        x=0
        for i in range(n-1):
            x=x+np.log(i+1)
        return x

def fitness(counts,radii,square,n):
    ic=len(counts)
    x=np.empty(ic)
    ratio=np.empty(ic)
    for i in range(ic):
        x[i]=n/square*(np.pi*radii[i][0]*radii[i][1])
        if counts[i]<x[i]:
            ratio[i]=0
        else:  
            ratio[i]=-x[i]+counts[i]*np.log(x[i])-lnfactorial(counts[i])
            ratio[i]=np.exp(ratio[i])
            ratio[i]=max(0,np.log(1/ratio[i]))
    return ratio

def fitness2(count,square0,square,n):
    x=n/square*square0
    if count<x:
        ratio=0
    else:  
        ratio=-x+count*np.log(x)-lnfactorial(count)
        ratio=np.exp(ratio)
        ratio=max(0,np.log(1/ratio))
    return ratio 

# select the first n biggest fitness
def select(population,n):
    nc=len(population.centroids)
    cen=np.empty((nc,2))
    rad=np.empty((nc,2))
    ang=np.empty(nc)
    fit=np.empty(nc)
    count=np.empty(nc)
    for i in range(nc):
        cen[i]=population.centroids[i]
        rad[i]=population.radii[i]
        fit[i]=population.fitness[i]
        ang[i]=population.angles[i]
        count[i]=population.counts[i]
    centroid2=np.empty((n,2))
    radii2=np.empty((n,2))
    fit2=np.empty(n)
    ang2=np.empty(n)
    count2=np.empty(n)
    fmax=max(fit)
    fmin=min(fit)
    i=0
    while i<n:
        j=0
        while fit[j]<fmax:
            j+=1
        centroid2[i]=cen[j]
        radii2[i]=rad[j]
        ang2[i]=ang[j]
        fit2[i]=fit[j]
        count2[i]=count[j]
        fit[j]=fmin
        fmax=max(fit)
        i+=1
    return centroid2,radii2,ang2,fit2,count2

def notfar(centroids,radii,i,j):
    x1=centroids[i][0]
    x2=centroids[j][0]
    y1=centroids[i][1]
    y2=centroids[j][1]
    r1=radii[i]
    r2=radii[j]
    if np.sqrt(((x1-x2)/(r1[0]+r2[0]))**2+((y1-y2)/(r1[1]+r2[1]))**2)<=3:
        return 1
    else:
        return 0


def create_random(n,xmax,xmin,ymax,ymin):
    centroids=np.random.random((n,2))
    centroids[:,0]=centroids[:,0]*(xmax-xmin)+xmin
    centroids[:,1]=centroids[:,1]*(ymax-ymin)+ymin
    rmax=min(ymax-ymin,xmax-xmin)/4
    radii=np.random.random((n,2))*rmax
    angle=np.random.random(n)*np.pi
    return centroids,radii,angle

def create_children(centroids,radii,angle,n):
    cen=np.empty((n,2))
    rad=np.empty((n,2))
    ang=np.empty((n))
    m=len(centroids)
    for i in range(n):
        x=int(np.random.random()*m)
        y=int(np.random.random()*m)
        while notfar(centroids,radii,x,y)==0:
            x=int(np.random.random()*m)
            y=int(np.random.random()*m)         
        cen[i]=(centroids[x]+centroids[y])/2
        rad[i]=(radii[x]+radii[y])/2
        ang[i]=(angle[x]+angle[y])/2
    return cen,rad,ang
        
def mutate(centroids,radii,angle,n,xmax,xmin,ymax,ymin):
    m=len(centroids)
    m_protect=int(m*0.1)
    for i in range(n):
        x=m_protect+int(np.random.random()*(m-m_protect))        
        r0=np.random.random(3)
        th=min(xmax-xmin,ymax-ymin)/4
        if r0[0]<1/3:
            centroids[x][0]=centroids[x][0]+min((np.random.random()-0.5)*5*radii[x][0],th)
            centroids[x][1]=centroids[x][1]+min((np.random.random()-0.5)*5*radii[x][1],th)
        if r0[1]<1/3:
            radii[x]=radii[x]*(np.random.random(2)*2.7+0.3)
        if r0[2]<1/3:
            angle[x]=angle[x]+np.random.random()*np.pi/2
            if angle[x]>np.pi:
                angle[x]=angle[x]-np.pi
            elif angle[x]<0:
                angle[x]=angle[x]+np.pi            
    return centroids,radii,angle

def test_intersect(cen1,rad1,ang1,cen2,rad2,ang2):
    # 0: no contact
    # 1: circle 1 is included in circle 2
    # 2: circle 2 is included in circle 1
    # 3: intersect
    angle=0
    x1,y1=ellipse2(cen1[0],cen1[1],rad1[0],rad1[1],angle*np.pi/180.,ang1)
    a=ellipse(x1,y1,cen2[0],cen2[1],rad2[0],rad2[1],ang2)
    if a <= 1:
        while angle<360 and a<=1:
            angle+=1
            x1,y1=ellipse2(cen1[0],cen1[1],rad1[0],rad1[1],angle*np.pi/180.,ang1)
            a=ellipse(x1,y1,cen2[0],cen2[1],rad2[0],rad2[1],ang2)
        if angle>=360:
            return 1
        else:
            return 3
    else:
        while angle<360 and a>1:
            angle+=1
            x1,y1=ellipse2(cen1[0],cen1[1],rad1[0],rad1[1],angle*np.pi/180.,ang1)
            a=ellipse(x1,y1,cen2[0],cen2[1],rad2[0],rad2[1],ang2)
        if angle>=360:
            a=ellipse(cen1[0],cen1[1],cen2[0],cen2[1],rad1[0],rad1[1],ang1)
            if a<=1:
                return 2
            else:
                return 0
        else:
            return 3
    
def notcontain(cen1,rad1,ang1,cen2,rad2,ang2,data,square,n):
    count1=0
    count2=0
    x1,y1=cen1
    x2,y2=cen2
    rx1,ry1=rad1
    rx2,ry2=rad2
    for point in data:
        x,y=point
        if ellipse(x,y,x1,y1,rx1,ry1,ang1)<=1:
            count1+=1
        if ellipse(x,y,x2,y2,rx2,ry2,ang2)<=1:
            count2+=1
    count=count2-count1
    square0=np.pi*(rx2*ry2-rx1*ry1)
    fit=fitness2(count,square0,square,n)
    return fit

def intersect(cen1,rad1,ang1,cen2,rad2,ang2,data,square,n):
    xmax=min(cen1[0]-rad1[0],cen2[0]-rad2[0])
    ymax=min(cen1[1]-rad1[1],cen2[1]-rad2[1])
    xmin=max(cen1[0]+rad1[0],cen2[0]+rad2[0])
    ymin=max(cen1[1]+rad1[1],cen2[1]+rad2[1])   
    angle=0
    while angle<360:
        angle+=1
        x1,y1=ellipse2(cen1[0],cen1[1],rad1[0],rad1[1],angle*np.pi/180.,ang1)
        x2,y2=ellipse2(cen2[0],cen2[1],rad2[0],rad2[1],angle*np.pi/180.,ang2)
        if ellipse(x1,y1,cen2[0],cen2[1],rad2[0],rad2[1],ang2)<=1:
            if x1>xmax:
                xmax=x1
            if x1<xmin:
                xmin=x1
            if y1>ymax:
                ymax=y1
            if y1<ymin:
                ymin=y1
        if ellipse(x2,y2,cen1[0],cen1[1],rad1[0],rad1[1],ang1)<=1:        
            if x2>xmax:
                xmax=x2
            if x2<xmin:
                xmin=x2
            if y2>ymax:
                ymax=y2
            if y2<ymin:
                ymin=y2
    centroid=np.empty(2)
    centroid[0]=(xmax+xmin)/2
    centroid[1]=(ymax+ymin)/2
    radii=np.empty(2)
    radii[0]=(xmax-xmin)/2
    radii[1]=(ymax-ymin)/2
    ang=(ang1+ang2)/2
    count=0
    for point in data:
        x,y=point
        x0,y0=centroid
        rx,ry=radii
        if ellipse(x,y,x0,y0,rx,ry,ang)<=1:
            count+=1
    square0=np.pi*rx*ry
    fit=fitness2(count,square0,square,n)
    return fit,centroid,radii,ang



def union(cen1,rad1,ang1,cen2,rad2,ang2,data,square,n):
    xmax=max(cen1[0]+rad1[0],cen2[0]+rad2[0])
    ymax=max(cen1[1]+rad1[1],cen2[1]+rad2[1])
    xmin=min(cen1[0]-rad1[0],cen2[0]-rad2[0])
    ymin=min(cen1[1]-rad1[1],cen2[1]-rad2[1])   
    centroid=np.empty(2)
    centroid[0]=(xmax+xmin)/2
    centroid[1]=(ymax+ymin)/2
    radii=np.empty(2)
    radii[0]=(xmax-xmin)/2
    radii[1]=(ymax-ymin)/2
    ang=0
    count=0
    for point in data:
        x,y=point
        x0,y0=centroid    
        rx,ry=radii
        if ellipse(x,y,x0,y0,rx,ry,ang)<=1:
            count+=1
    square0=np.pi*rx*ry
    fit=fitness2(count,square0,square,n)
    return fit,centroid,radii,ang
    
def relocate(cen,rad,ang,fit,population,xmax,xmin,ymax,ymin):
    centroids=population.centroids
    radii=population.radii
    angles=population.angles
    for i in range(len(centroids)):
        x,y=centroids[i]
        rx,ry=radii[i]
        if ellipse(x,y,cen[0],cen[1],rx,ry,ang)<1:
            centroids[i],radii[i],angles[i]=create_random(1,xmax,xmin,ymax,ymin)
    return centroids,radii,angles
    
def addbanned(population_banned,cen_g,rad_g,ang_g,fit_g,data,square,n):
    #print population_banned.centroids
    #print population_banned.radii
    #print cen_g,rad_g,fit_g
    centroid_banned=population_banned.centroids
    radii_banned=population_banned.radii
    angle_banned=population_banned.angles
    fit_banned=population_banned.fitness

    cen_add=np.empty(2)
    rad_add=np.empty(2)
    fit_add=-1000
    j=0
    flag=0
    while j < len(centroid_banned):
        cen_l=centroid_banned[j]
        rad_l=radii_banned[j]
        ang_l=angle_banned[j]
        fit_l=fit_banned[j]
        case=test_intersect(cen_g,rad_g,ang_g,cen_l,rad_l,ang_l)
        # if g doesn't intersect any ellipse in the banned list, add g.
        if case>0:
            flag=1
            # g is contained in l:
            if case==1: 
                # if the area in l, but not in g, is lower than the minimum accepted fitness value, add g and remove l.
                fit=notcontain(cen_g,rad_g,ang_g,cen_l,rad_l,ang_l,data,square,n)
                if fit<Fitness_Th:
                    centroid_banned=np.delete(centroid_banned,j,0)
                    radii_banned=np.delete(radii_banned,j,0)
                    angle_banned=np.delete(angle_banned,j)
                    fit_banned=np.delete(fit_banned,j)
                    j=j-1
                    if fit_g>fit_add:
                        cen_add=cen_g
                        rad_add=rad_g
                        ang_add=ang_g
                        fit_add=fit_g
            # l is contained in g
            elif case==2:
                # if the area in g, but not in l, meets the minimum accepted fitness value, add g and remove l.
                fit=notcontain(cen_l,rad_l,ang_l,cen_g,rad_g,ang_g,data,square,n)
                if fit>Fitness_Th:
                    centroid_banned=np.delete(centroid_banned,j,0)
                    radii_banned=np.delete(radii_banned,j,0)
                    angle_banned=np.delete(angle_banned,j)
                    fit_banned=np.delete(fit_banned,j)
                    j=j-1
                    if fit_g>fit_add:
                        cen_add=cen_g
                        rad_add=rad_g
                        ang_add=ang_g
                        fit_add=fit_g
            # l intersects g
            elif case==3:
                # create ellipses approximating the intersection of l and g
                fit_int,cen_int,rad_int,ang_int=intersect(cen_g,rad_g,ang_g,cen_l,rad_l,ang_l,data,square,n)
                # if the intersection is better than both l and g, add the intersection, and remove l
                if fit_int>fit_g and fit_int>fit_l:
                    centroid_banned=np.delete(centroid_banned,j,0)
                    radii_banned=np.delete(radii_banned,j,0)
                    angle_banned=np.delete(angle_banned,j)
                    fit_banned=np.delete(fit_banned,j)
                    j=j-1
                    if fit_int>fit_add:
                        cen_add=cen_int
                        rad_add=rad_int
                        ang_add=ang_int
                        fit_add=fit_int
                # if g is better than the intersection and the intersection is better than l, add g and remove l
                elif fit_g>fit_int and fit_g>fit_l:
                    centroid_banned=np.delete(centroid_banned,j,0)
                    radii_banned=np.delete(radii_banned,j,0)
                    angle_banned=np.delete(angle_banned,j)
                    fit_banned=np.delete(fit_banned,j)
                    j=j-1
                    if fit_g>fit_add:
                        cen_add=cen_g
                        rad_add=rad_g
                        ang_add=ang_g
                        fit_add=fit_g
                # if both l and are better than the intersection, compare l and g with the union
                elif fit_g>fit_int and fit_l>fit_int:
                    fit_uni,cen_uni,rad_uni,ang_uni=union(cen_g,rad_g,ang_g,cen_l,rad_l,ang_l,data,square,n)
                    # if the union is better than g and l, add the union and remove l.
                    if fit_uni>fit_g and fit_uni>fit_l:
                        centroid_banned=np.delete(centroid_banned,j,0)
                        radii_banned=np.delete(radii_banned,j,0)
                        angle_banned=np.delete(angle_banned,j)
                        fit_banned=np.delete(fit_banned,j)
                        j=j-1
                        if fit_uni>fit_add:
                            cen_add=cen_uni
                            rad_add=rad_uni
                            ang_add=ang_uni
                            fit_add=fit_uni 
                    else:
                    #otherwise: add g
                        centroid_banned=np.delete(centroid_banned,j,0)
                        radii_banned=np.delete(radii_banned,j,0)
                        angle_banned=np.delete(angle_banned,j)
                        fit_banned=np.delete(fit_banned,j)
                        j=j-1
                        if fit_g>fit_add:
                            cen_add=cen_g
                            rad_add=rad_g
                            ang_add=ang_g
                            fit_add=fit_g
        j=j+1
    # if g doesn't intersect any ellipse in the banned list, add g
    if flag==0:
        centroid_banned=np.vstack((centroid_banned,cen_g))
        radii_banned=np.vstack((radii_banned,rad_g))
        angle_banned=np.hstack((angle_banned,ang_g))
    elif fit_add<>-1000:
        centroid_banned=np.vstack((centroid_banned,cen_add))
        radii_banned=np.vstack((radii_banned,rad_add))
        angle_banned=np.hstack((angle_banned,ang_add))
    population_banned2=Population(centroid_banned,radii_banned,angle_banned,data,square)
    #print population_banned2.centroids
    #print population_banned2.radii
    return population_banned2

def drawpoints(pos,xmax,xmin,ymax,ymin):
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
    canvas=tk.Canvas(top,height=h0,width=w0)
    for i in range(n):
        x=sx*(pos[i,0]-xmin)+100
        y=sx*(pos[i,1]-ymin)+100
        canvas.create_oval(x-1,y-1,x+1,y+1,fill='black')
    canvas.pack()
    return canvas

def drawellipse(population_banned,canvas,xmax,xmin,ymax,ymin,color):
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
    for i in range(len(population_banned.centroids)):
        x0=population_banned.centroids[i][0]
        y0=population_banned.centroids[i][1]
        a0=population_banned.angles[i]
        r0=population_banned.radii[i]
        x=sx*(x0-xmin)+100
        y=sx*(y0-ymin)+100
        r=sx*r0
        for j in range(360):
            a=j/360.*2*np.pi
            x2,y2=ellipse2(x,y,r[0],r[1],a,a0)
            clusterids.append(canvas.create_oval(x2-1,y2-1,x2+1,y2+1,outline=color))
        print population_banned.counts[i]
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


    # get the bound of points
    xmax=max(pos[:,0])
    xmin=min(pos[:,0])
    ymax=max(pos[:,1])
    ymin=min(pos[:,1])

    square=(ymax-ymin)*(xmax-xmin)

    #visualizing
    top=tk.Tk()
    canvas=drawpoints(pos,xmax,xmin,ymax,ymin)
    clusterids=[]
    
    # Initialize the population with random ellipses
    nc=np.int(n*0.1)
    counts=np.arange(nc)
    centroids,radii,angles=create_random(nc,xmax,xmin,ymax,ymin)
    population=Population(centroids,radii,angles,pos,square)
    gen=0
    new_population=population
    nb=0

    # While the halting condition is not met
    while gen<50:
        old_population=new_population
        # Place the best-fit ellipses into the next generation
        centroids,radii,angles,fit,count=select(new_population,int(0.3*nc))

        # Add random ellipses to the next generation
        cenr,radr,angr=create_random(int(0.2*nc),xmax,xmin,ymax,ymin)
        centroids=np.vstack((centroids,cenr))
        radii=np.vstack((radii,radr))
        angles=np.hstack((angles,angr))
        ncc=nc-len(centroids)
        

        # Create children until the geneartion is full
        cenc,radc,angc=create_children(centroids,radii,angles,ncc)
        centroids=np.vstack((centroids,cenc))
        radii=np.vstack((radii,radc))
        angles=np.hstack((angles,angc))
        # Mutate some of the ellipses
        n_mu=int(len(centroids)/5)
        centroids,radii,angles=mutate(centroids,radii,angles,n_mu,xmax,xmin,ymax,ymin)
        new_population=Population(centroids,radii,angles,pos,square)

        # Add the best ellipse to the banned list
        if gen>=5 and gen/2==gen/2.:
            cen,rad,ang,fit,count=select(new_population,1)
            print ang[0],count[0],fit[0]  #,count[0]
            if fit[0]>Fitness_Th and count[0]>Num_Th:
                if nb==0:
                    population_banned=Population(cen,rad,ang,pos,square)
                    nb+=1
                else:
                    #add the best one into the banned list
                    population_banned=addbanned(population_banned,cen[0],rad[0],ang[0],fit[0],pos,square,n)
                    #relocate the centroids
                    centroids,radii,angles=relocate(cen[0],rad[0],ang[0],fit[0],new_population,xmax,xmin,ymax,ymin)
                    new_population=Population(centroids,radii,angles,pos,square)
                    # visualizing 
                    nb=len(population_banned.centroids)
                    drawellipse(population_banned,canvas,xmax,xmin,ymax,ymin,'blue')
            
        # Disperse the ellipses if converged early
        fmed=np.median(new_population.fitness)
        fmax=max(new_population.fitness)
        if fmax-fmed<fmax*0.01:
            centroids,radii,angles=create_random(nc,xmax,xmin,ymax,ymin)
            new_population=Population(centroids,radii,angles,pos,square)
        gen+=1
    if nb>0:
        #visualizing
        canvas.destroy()
        canvas=drawpoints(pos,xmax,xmin,ymax,ymin)
        drawellipse(population_banned,canvas,xmax,xmin,ymax,ymin,'red') 
        
        for i in range(len(population_banned.centroids)):
            print population_banned.centroids[i], population_banned.radii[i], population_banned.angles[i],population_banned.fitness[i]
            
    end_time=time.clock()
    print 'Run time: ',end_time-begin_time  
