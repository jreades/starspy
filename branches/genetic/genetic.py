import scipy.stats as STATS
import math
import numpy as np
import Tkinter as tk


    



def fitness(counts,radii,rates):
    """

    Arguments
    ---------
    counts: array like (nx1)
            observed counts in a cluster
    radii: array like (nx1)
            radii of clusters
    rates: array like (nx1)
           intensity rate per unit of area

    Returns
    -------
    ratio: array (nx1)
           ratio of cdf observed to cdf expected
    """
    ev=2*math.pi*radii * rates
    # get cumulative probabilities of expected
    cdf_e=STATS.poisson.cdf(ev,rates)
    cdf_o=STATS.poisson.cdf(counts,rates)
    # form ratio of cumulative prob observed over cumulative prop expected
    ratio=cdf_o/cdf_e
    return ratio

def mutate(population,pct=0.2,jigger=0.01):
    n=len(population.fitness)
    nm=int(np.floor(pct*n))
    ids=np.arange(n)
    rids=np.random.permutation(ids)[0:nm]
    for r in rids:
        mi=population.centroids[r]
        ri=population.radii[r]
        d=np.random.random((2,1))*(2*jigger)+(1-jigger)
        if r%2:
            radius=ri*d[0]
            x,y=mi
        else:
            radius=ri
            x=d[1]*mi[0]
            y=d[1]*mi[1]
        population.centroids[r][0]=x
        population.centroids[r][1]=y
        population.radii[r]=radius
    print nm
    return population 

def replace(population,pct=0.2):
    n=len(population.fitness)
    nm=int(np.floor(pct*n))
    print nm
    return population

def select(population):
    """
    implements roulette wheel selection
    """
    partsum=population.fitness/population.fitness.sum()
    flag=1
    n=len(population.fitness)
    while flag:
        j=np.random.randint(n)
        c=partsum[j]
        r=np.random.random()
        if r < c:
            flag=0
    return j

class Population:
    """
    Genetic population
    """
    def __init__(self,centroids,radii,rates,data):
        self.centroids=centroids
        self.radii=radii
        self.rates=rates
        self.counts=np.zeros_like(rates)
        self.data=data
        self._set_counts()
        self._set_fitness()

    def _set_counts(self):
        for point in self.data:
            x,y=point
            for i,centroid in enumerate(self.centroids):
                cx,cy=centroid
                dx=(x-cx)**2
                dy=(y-cy)**2
                if math.sqrt(dx+dy)<self.radii[i]:
                    self.counts[i]+=1

    def _set_fitness(self):
        self.fitness=fitness(self.counts,self.radii,self.rates)












class MAPEX:
    """
    Genetic algorithm for cluster detection
    
    References
    ----------

    Openshaw and Perree 1996


    Notes
    -----

    Not yet functional, only partially implemented
    
    """
    def __init__(self,points, generations=100, max_radius=0.01, sampling=0.05,
            crossover=0.6, survive=0.8, mutation=0.2):
        """

        Parameters
        ----------

        points:  array (nx2)
                 x and y coordinates

        generations: int
                     number of generations

        max_radius: float
                    percentage of the bounding box rectangle area to use for
                    circle radius maximum

        sampling: float
                  percentage of n to use as sample

        crossover: float
                  percentage of sample that should generate offspring
        survive: float
                 percentage of current generation (and offspring) that should
                 survive

        mutation: float
                  percentage of the current generation to mutate

        """
        self.points = points
        self.sampling=sampling
        self.max_radius=max_radius
        self.crossover=crossover
        self.survive=survive
        self.mutation=mutation
        self._solve()


    def _solve(self):
        n,k=self.points.shape
        ids=np.arange(n)


        # get mbr for entire point set
        minx,miny=self.points.min(axis=0)
        maxx,maxy=self.points.max(axis=0)
        self.mbr=[minx,miny,maxx,maxy]
        self.area=(maxx-minx)*(maxy-miny)

        top=tk.Tk()
        canvas=tk.Canvas(top,height=700,width=700)
        sx=500*1./(maxx-minx)

        for i in range(n):
            x=sx*(self.points[i,0]-minx)+100
            y=sx*(self.points[i,1]-miny)+100
            canvas.create_oval(x-1,y-1,x+1,y+1,fill='black')
        canvas.pack()

        # calculate intensity
        self.intensity = n *1. / ((maxy-miny) * (maxx-minx))

        # sample points for seeding
        ns=int(n*self.sampling)
        rids=np.random.permutation(ids)[0:ns]
        gen0=self.points[rids,:]
        self.ns=ns

        # generate random circles on these points
        counts=np.ones((ns,1))
        radii0=np.random.random((ns,1))*self.max_radius*self.area

        clusterids=[]
        for i,point in enumerate(gen0):
            x=sx*(point[0]-minx)+100
            y=sx*(point[1]-miny)+100
            r=sx*radii0[i]
            r=r[0]
            clusterids.append(canvas.create_oval(x-r,y-r,x+r,y+r,tags=("old")))



        # count number of other points inside each circle
        # should use binning here for large n problems
        r2=radii0*2
        nin=np.zeros((ns,1))
        for i in range(ns):
            for point in self.points:
                dx=point[0]-gen0[i][0]
                dy=point[1]-gen0[1][0]
                if dx*dx+dy*dy <= r2[i]:
                    nin[i]+=1
                
        # calculate fitness of each circle
        gen0fitness=self._fit(nin,gen0,radii0)

        # loop over generations
        gen=0
        self.gen0=gen0
        np0=np
        while gen < 100:

            # perform crossover and mutation on circles
            child_points, child_radii=self._cross_over(gen0,radii0)
            nc=len(child_points)
            npc=np.zeros((nc,1))
            cradii2=child_radii**2
            for i in range(nc):
                for point in self.points:
                    dx=child_points[i][0]-point[0]
                    dy=child_points[i][1]-point[1]
                    if dx*dx+dy*dy <=cradii2[i]:
                        npc[i]+=1
            # calculate fitness of children
            cfit=self._fit(npc,child_points,child_radii)


            # form new potential new generation
            gen1=np.vstack((gen0,child_points))
            radii1=np.vstack((radii0,child_radii))
            fitness=np.vstack((gen0fitness,cfit))
            ngen1=len(fitness)
            nsurvive=int(self.survive*ngen1)
            ids=np.argsort(fitness.flatten())
            nids=ids[-nsurvive:]
            gen1=gen1[nids,:]
            radii1=radii1[nids,:]

            # replace low fitness circles with new random circles
            nr=ngen1-len(gen1)
            radiir=np.random.random((nr,1))*self.max_radius
            rp=np.zeros((nr,2))
            rp[:,0]=np.random.random(nr)*(maxx-minx)+maxx
            rp[:,1]=np.random.random(nr)*(maxy-miny)+maxy
            gen0=np.vstack((gen1,rp))
            radii0=np.vstack((radii1,radiir))
            for id in clusterids:
                canvas.delete(id)
            clusterids=[]
            for i,point in enumerate(gen0):
                x=sx*(point[0]-minx)+100
                y=sx*(point[1]-miny)+100
                r=sx*radii0[i]
                r=r[0]
                clusterids.append(canvas.create_oval(x-r,y-r,x+r,y+r,tags=("old")))
            print len(clusterids),len(gen0)
            # mutate
            ngen=len(gen0)
            ids=range(ngen)
            np.random.shuffle(ids)
            ngen=int(ngen*self.mutation)
            for id in ids[0:ngen]:
                gen0[id,0]*=np.random.random()*(1.05-0.95)+0.95
                gen0[id,1]*=np.random.random()*(1.05-0.95)+0.95
                

            gen+=1
        for i,point in enumerate(gen0):
            x=sx*(point[0]-minx)+100
            y=sx*(point[1]-miny)+100
            r=sx*radii0[i]
            r=r[0]
            canvas.create_oval(x-r,y-r,x+r,y+r,tags=("old"))
        self.gen0=gen0
        self.radii=radii0

    def _fit(self,counts,centers,radii):
        """
        Calculates the fitness of a circle
        """
        ns=len(counts)
        lamb=self.intensity
        fitness=[ counts[i]-radii[i]**2 * math.pi * lamb for i in range(ns)]
        return fitness

    def _cross_over(self,gen,radii):
        """
        use a distance decay function for probabilities of crossing over pairs

        this is different from what is in the original algorithm.
        """
        n=len(gen)
        d=np.zeros((n,n))
        centers=gen
        rn=range(n)
        for i in rn:
            for j in rn:
                d[i,j]=(centers[i,0]-centers[j,0])**2 + (centers[i,1]-centers[j,1])**2
                d[j,i]=d[i,j]
        dmax=d.max()
        p=d/dmax
        ncross=int(self.crossover*n)
        nc=0
        ids=rn
        c_centers=np.zeros((ncross,2))
        c_radii=np.zeros((ncross,1))
        it=0
        while nc < ncross:
            ids=np.random.permutation(ids)
            i=ids[0]
            j=ids[1]
            r=np.random.random()
            if r < p[i,j]:
                c_centers[nc,0]=(centers[i,0]+centers[j,0])/2.
                c_centers[nc,1]=(centers[i,1]+centers[j,1])/2.
                c_radii[nc]=(radii[i]+radii[j])/2.
                r2=np.random.random()
                if r2 >0.5:
                    c_centers[nc]=centers[i]
                    c_radii[nc]=radii[j]
                else:
                    c_centers[nc]=centers[j]
                    c_radii[nc]=radii[i]
                nc+=1
            it+=1
        return (c_centers,c_radii)



if __name__ == '__main__':

    import numpy as np

    n=100

    x=np.random.random((n,2))*9.
    x[0:25,:]=np.random.random((25,2))*5.

    #solution=MAPEX(x)

    nc=np.floor(n*0.10)
    counts=np.arange(nc)
    counts.shape=(nc,1)
    rates=np.ones((nc,1))
    radii=np.random.random(int(nc))*(0.20*9)
    radii.shape=(nc,1)
    rates=rates*(n*1.)/100.
    ids=np.arange(n)
    ids=np.random.permutation(ids)
    rids=ids[0:int(nc)]
    centroids=x[rids,:]
    population=Population(centroids,radii,rates,x)
    gen=0
    nsize=len(population.fitness)
    new_population=population
    while gen<100:
        old_population=new_population
        centroids=np.zeros_like(centroids)
        radii=np.zeros_like(radii)
        off=0
        while off < nsize:
            # select mates
            i=select(old_population)
            j=select(old_population)
            # first offspring is average of parents
            pt1i=old_population.centroids[i]
            pt1j=old_population.centroids[j]
            pt1c=(pt1i+pt1j)/2.
            pt1radius=(old_population.radii[i]+old_population.radii[j])/2.
            centroids[off]=pt1c
            radii[off]=pt1radius
            off+=1
            if off < nsize:
                # second offspring is mix of one parent centroid and others radius
                pt2c=old_population.centroids[i]
                pt2radius=old_population.radii[j]
                if np.random.random()>0.5:
                    pt2c=old_population.centroids[j]
                    pt2radius=old_population.radii[i]
                centroids[off]=pt2c
                radii[off]=pt2radius
            off+=1
        new_population=Population(centroids,radii,rates,x)
        new_population=mutate(new_population)
        new_population=replace(new_population)
        gen+=1



