#genearate points randomly

import math
import numpy as np
import pysal
import Tkinter as tk
import time
Fitness_Th=30
Num_Th=10

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
        x[i]=n/3*2/square*(np.pi*radii[i][0]*radii[i][1])
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
    fit=np.empty(nc)
    count=np.empty(nc)
    for i in range(nc):
        cen[i]=population.centroids[i]
        rad[i]=population.radii[i]
        fit[i]=population.fitness[i]
        count[i]=population.counts[i]
    centroid2=np.empty((n,2))
    radii2=np.empty((n,2))
    fit2=np.empty(n)
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
        fit2[i]=fit[j]
        count2[i]=count[j]
        fit[j]=fmin
        fmax=max(fit)
        i+=1
    return centroid2,radii2,fit2,count2

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
    return centroids,radii

def create_children(centroids,radii,n):
    cen=np.empty((n,2))
    rad=np.empty((n,2))
    m=len(centroids)
    for i in range(n):
        x=int(np.random.random()*m)
        y=int(np.random.random()*m)
        while notfar(centroids,radii,x,y)==0:
            x=int(np.random.random()*m)
            y=int(np.random.random()*m)         
        cen[i]=(centroids[x]+centroids[y])/2
        rad[i]=(radii[x]+radii[y])/2
    return cen,rad
        
def mutate(centroids,radii,n,xmax,xmin,ymax,ymin):
    m=len(centroids)
    m_protect=int(m*0.1)
    for i in range(n):
        x=m_protect+int(np.random.random()*(m-m_protect))        
        r0=np.random.random()
        th=min(xmax-xmin,ymax-ymin)/4
        if r0>0.5:
            centroids[x][0]=centroids[x][0]+min((np.random.random()-0.5)*5*radii[x][0],th)
            centroids[x][1]=centroids[x][1]+min((np.random.random()-0.5)*5*radii[x][1],th)
        else:
            radii[x]=radii[x]*(np.random.random(2)*2.7+0.3)
    return centroids,radii

def test_intersect(cen1,rad1,cen2,rad2):
    # 0: no contact
    # 1: circle 1 is included in circle 2
    # 2: circle 2 is included in circle 1
    # 3: intersect
    angle=0
    x1=cen1[0]+rad1[0]*np.cos(angle*np.pi/180)
    y1=cen1[1]+rad1[1]*np.sin(angle*np.pi/180)
    a=(x1-cen2[0])**2/rad2[0]**2+(y1-cen2[1])**2/rad2[1]**2
    if a <= 1:
        while angle<360 and a<=1:
            angle+=1
            x1=cen1[0]+rad1[0]*np.cos(angle*np.pi/180)
            y1=cen1[1]+rad1[1]*np.sin(angle*np.pi/180)
            a=(x1-cen2[0])**2/rad2[0]**2+(y1-cen2[1])**2/rad2[1]**2
        if angle>=360:
            return 1
        else:
            return 3
    else:
        while angle<360 and a>1:
            angle+=1
            x1=cen1[0]+rad1[0]*np.cos(angle*np.pi/180)
            y1=cen1[1]+rad1[1]*np.sin(angle*np.pi/180)
            a=(x1-cen2[0])**2/rad2[0]**2+(y1-cen2[1])**2/rad2[1]**2
        if angle>=360:
            if (cen2[0]-cen1[0])**2/rad1[0]**2+(cen2[1]-cen1[1])**2/rad1[1]**2<=1:
                return 2
            else:
                return 0
        else:
            return 3
    
def notcontain(cen1,rad1,cen2,rad2,data,square,n):
    count1=0
    count2=0
    x1,y1=cen1
    x2,y2=cen2
    rx1,ry1=rad1
    rx2,ry2=rad2
    for point in data:
        x,y=point
        if ((x-x1)/rx1)**2+((y-y1)/ry1)**2<=1:
            count1+=1
        if ((x-x2)/rx2)**2+((y-y2)/ry2)**2<=1:
            count2+=1
    count=count2-count1
    square0=np.pi*(rx2*ry2-rx1*ry1)
    fit=fitness2(count,square0,square,n/3*2)
    return fit

def intersect(cen1,rad1,cen2,rad2,data,square,n):
    xmax=min(cen1[0]-rad1[0],cen2[0]-rad2[0])
    ymax=min(cen1[1]-rad1[1],cen2[1]-rad2[1])
    xmin=max(cen1[0]+rad1[0],cen2[0]+rad2[0])
    ymin=max(cen1[1]+rad1[1],cen2[1]+rad2[1])   
    angle=0
    while angle<360:
        angle+=1
        x1=cen1[0]+rad1[0]*np.cos(angle*np.pi/180)
        y1=cen1[1]+rad1[1]*np.sin(angle*np.pi/180)
        x2=cen2[0]+rad2[0]*np.cos(angle*np.pi/180)
        y2=cen2[1]+rad2[1]*np.sin(angle*np.pi/180)
        if (x1-cen2[0])**2/rad2[0]**2+(y1-cen2[1])**2/rad2[1]**2<=1:
            if x1>xmax:
                xmax=x1
            if x1<xmin:
                xmin=x1
            if y1>ymax:
                ymax=y1
            if y1<ymin:
                ymin=y1
        if (x2-cen1[0])**2/rad1[0]**2+(y2-cen1[1])**2/rad1[1]**2<=1:        
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
    
    count=0
    for point in data:
        x,y=point
        x0,y0=centroid
        dx=(x-x0)
        dy=(y-y0)    
        rx,ry=radii
        if (dx/rx)**2+(dy/ry)**2<=1:
            count+=1
    square0=np.pi*rx*ry
    fit=fitness2(count,square0,square,n/3*2)
    return fit,centroid,radii



def union(cen1,rad1,cen2,rad2,data,square,n):
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
    
    count=0
    for point in data:
        x,y=point
        x0,y0=centroid
        dx=(x-x0)
        dy=(y-y0)    
        rx,ry=radii
        if (dx/rx)**2+(dy/ry)**2<=1:
            count+=1
    square0=np.pi*rx*ry
    fit=fitness2(count,square0,square,n/3*2)
    return fit,centroid,radii
    
def relocate(cen,rad,fit,population,xmax,xmin,ymax,ymin):
    centroids=population.centroids
    radii=population.radii
    for i in range(len(centroids)):
        x,y=centroids[i]
        rx,ry=radii[i]
        if (cen[0]-x)**2/rx**2-(cen[1]-y)**2/ry**2<1:
            centroids[i],radii[i]=create_random(1,xmax,xmin,ymax,ymin)
    return centroids,radii
    
def addbanned(population_banned,cen_g,rad_g,fit_g,data,square,n):
    #print population_banned.centroids
    #print population_banned.radii
    #print cen_g,rad_g,fit_g
    centroid_banned=population_banned.centroids
    radii_banned=population_banned.radii
    fit_banned=population_banned.fitness

    cen_add=np.empty(2)
    rad_add=np.empty(2)
    fit_add=-1000
    j=0
    flag=0
    while j < len(centroid_banned):
        cen_l=centroid_banned[j]
        rad_l=radii_banned[j]
        fit_l=fit_banned[j]
        case=test_intersect(cen_g,rad_g,cen_l,rad_l)
        # if g doesn't intersect any ellipse in the banned list, add g.
        if case>0:
            flag=1
            # g is contained in l:
            if case==1: 
                # if the area in l, but not in g, is lower than the minimum accepted fitness value, add g and remove l.
                fit=notcontain(cen_g,rad_g,cen_l,rad_l,data,square,n)
                if fit<Fitness_Th:
                    centroid_banned=np.delete(centroid_banned,j,0)
                    radii_banned=np.delete(radii_banned,j,0)
                    fit_banned=np.delete(fit_banned,j)
                    j=j-1
                    if fit_g>fit_add:
                        cen_add=cen_g
                        rad_add=rad_g
                        fit_add=fit_g
            # l is contained in g
            elif case==2:
                # if the area in g, but not in l, meets the minimum accepted fitness value, add g and remove l.
                fit=notcontain(cen_l,rad_l,cen_g,rad_g,data,square,n)
                if fit>Fitness_Th:
                    centroid_banned=np.delete(centroid_banned,j,0)
                    radii_banned=np.delete(radii_banned,j,0)
                    fit_banned=np.delete(fit_banned,j)
                    j=j-1
                    if fit_g>fit_add:
                        cen_add=cen_g
                        rad_add=rad_g
                        fit_add=fit_g
            # l intersects g
            elif case==3:
                # create ellipses approximating the intersection of l and g
                fit_int,cen_int,rad_int=intersect(cen_g,rad_g,cen_l,rad_l,data,square,n)
                # if the intersection is better than both l and g, add the intersection, and remove l
                if fit_int>fit_g and fit_int>fit_l:
                    centroid_banned=np.delete(centroid_banned,j,0)
                    radii_banned=np.delete(radii_banned,j,0)
                    fit_banned=np.delete(fit_banned,j)
                    j=j-1
                    if fit_int>fit_add:
                        cen_add=cen_int
                        rad_add=rad_int
                        fit_add=fit_int
                # if g is better than the intersection and the intersection is better than l, add g and remove l
                elif fit_g>fit_int and fit_g>fit_l:
                    centroid_banned=np.delete(centroid_banned,j,0)
                    radii_banned=np.delete(radii_banned,j,0)
                    fit_banned=np.delete(fit_banned,j)
                    j=j-1
                    if fit_g>fit_add:
                        cen_add=cen_g
                        rad_add=rad_g
                        fit_add=fit_g
                # if both l and are better than the intersection, compare l and g with the union
                elif fit_g>fit_int and fit_l>fit_int:
                    fit_uni,cen_uni,rad_uni=union(cen_g,rad_g,cen_l,rad_l,data,square,n)
                    # if the union is better than g and l, add the union and remove l.
                    if fit_uni>fit_g and fit_uni>fit_l:
                        centroid_banned=np.delete(centroid_banned,j,0)
                        radii_banned=np.delete(radii_banned,j,0)
                        fit_banned=np.delete(fit_banned,j)
                        j=j-1
                        if fit_uni>fit_add:
                            cen_add=cen_uni
                            rad_add=rad_uni
                            fit_add=fit_uni 
                    else:
                    #otherwise: add g
                        centroid_banned=np.delete(centroid_banned,j,0)
                        radii_banned=np.delete(radii_banned,j,0)
                        fit_banned=np.delete(fit_banned,j)
                        j=j-1
                        if fit_g>fit_add:
                            cen_add=cen_g
                            rad_add=rad_g
                            fit_add=fit_g
        j=j+1
    # if g doesn't intersect any ellipse in the banned list, add g
    if flag==0:
        centroid_banned=np.vstack((centroid_banned,cen_g))
        radii_banned=np.vstack((radii_banned,rad_g))
    elif fit_add<>-1000:
        centroid_banned=np.vstack((centroid_banned,cen_add))
        radii_banned=np.vstack((radii_banned,rad_add))
    population_banned2=Population(centroid_banned,radii_banned,data,square)
    #print population_banned2.centroids
    #print population_banned2.radii
    return population_banned2

class Population:
    def __init__(self,centroids,radii,data,square):
        self.centroids=centroids
        self.radii=radii
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
                if (dx/rx)**2+(dy/ry)**2<=1:
                    self.counts[i]+=1
    def _set_fitness(self):
        self.fitness=fitness(self.counts,self.radii,self.square,len(self.data))

if __name__ == '__main__':
    
    begin_time=time.clock()
    
    # get the pointset
    xmax=100.
    xmin=0.
    ymax=100.
    ymin=0.
    i=0
    n=500
    pos=np.ones((n,2))
    while i<n/3*2:
        pos[i][0]=xmin+np.random.random()*(xmax-xmin)
        pos[i][1]=ymin+np.random.random()*(ymax-ymin)
        i=i+1
    while i<n/6*5:
        pos[i][0]=xmin+(xmax-xmin)/8+np.random.random()*(xmax-xmin)/6
        pos[i][1]=ymin+(ymax-ymin)/6+np.random.random()*(ymax-ymin)/8
        i=i+1
    while i<n:
        pos[i][0]=xmin+(xmax-xmin)/8*6+np.random.random()*(xmax-xmin)/12
        pos[i][1]=ymin+(ymax-ymin)/7*3+np.random.random()*(ymax-ymin)/4
        i=i+1    
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
    clusterids=[]
    
    # Initialize the population with random ellipses
    nc=np.int(n*0.1)
    counts=np.arange(nc)
    centroids,radii=create_random(nc,xmax,xmin,ymax,ymin)
    population=Population(centroids,radii,pos,square)
    gen=0
    new_population=population
    nb=0

    # While the halting condition is not met
    while gen<50:
        old_population=new_population
        # Place the best-fit ellipses into the next generation
        centroids,radii,fit,count=select(new_population,int(0.3*nc))

        # Add random ellipses to the next generation
        cenr,radr=create_random(int(0.2*nc),xmax,xmin,ymax,ymin)
        centroids=np.vstack((centroids,cenr))
        radii=np.vstack((radii,radr))
        ncc=nc-len(centroids)

        # Create children until the geneartion is full
        cenc,radc=create_children(centroids,radii,ncc)
        centroids=np.vstack((centroids,cenc))
        radii=np.vstack((radii,radc))

        # Mutate some of the ellipses
        n_mu=int(len(centroids)/5)
        centroids,radii=mutate(centroids,radii,n_mu,xmax,xmin,ymax,ymin)
        new_population=Population(centroids,radii,pos,square)

        # Add the best ellipse to the banned list
        if gen>=5 and gen/2==gen/2.:
            cen,rad,fit,count=select(new_population,1)
            print fit[0]  #,count[0]
            if fit[0]>Fitness_Th and count[0]>Num_Th:
                if nb==0:
                    population_banned=Population(cen,rad,pos,square)
                    nb+=1
                else:
                    #add the best one into the banned list
                    population_banned=addbanned(population_banned,cen[0],rad[0],fit[0],pos,square,n)
                    #relocate the centroids
                    centroids,radii=relocate(cen[0],rad[0],fit[0],new_population,xmax,xmin,ymax,ymin)
                    new_population=Population(centroids,radii,pos,square)
                    # visualizing 
                    nb=len(population_banned.centroids)
                    for i in range(nb):
                        x0=population_banned.centroids[i][0]
                        y0=population_banned.centroids[i][1]
                        r0=population_banned.radii[i]
                        x=sx*(x0-xmin)+100
                        y=sx*(y0-ymin)+100
                        r=sx*r0
                        clusterids.append(canvas.create_oval(x-r[0],y-r[1],x+r[0],y+r[1],outline='blue'))
            
        # Disperse the ellipses if converged early
        fmed=np.median(new_population.fitness)
        fmax=max(new_population.fitness)
        if fmax-fmed<fmax*0.01:
            centroids,radii=create_random(nc,xmax,xmin,ymax,ymin)
            new_population=Population(centroids,radii,pos,square)
        gen+=1
    if nb>0:
        #visualizing
        canvas.destroy()
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
        
        for i in range(len(population_banned.centroids)):
            x0=population_banned.centroids[i][0]
            y0=population_banned.centroids[i][1]
            r0=population_banned.radii[i]
            x=sx*(x0-xmin)+100
            y=sx*(y0-ymin)+100
            r=sx*r0
            clusterids.append(canvas.create_oval(x-r[0],y-r[1],x+r[0],y+r[1],outline='red'))
        
        #print population_banned.centroids
        #print population_banned.radii
    end_time=time.clock()
    print 'Run time: ',end_time-begin_time  
