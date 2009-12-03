'''
Created on 2009-10-29

@author: Jing YAO
'''
import random 
import pysal 
import numpy as num 
from operator import gt, lt 
import sys 
import copy
from components import check_contiguity


class AZP(object):
    '''
    Assumption: each zone has at least one neighbor, that is, the graph is of connectivity.
    
    Automatic Zoning Problem (AZP)
    Step 1: Start by generating a random zoning system of N small zones into M regions, M<N
    Step 2: Make a list of the M regions. 
    Step 3: Select and remove any region K at random from this list.
    Step 4: Identify a set of zones bordering on members of region K that could be moved 
            into region K without destroying the internal contiguity of the donor region(s)
    Step 5: Randomly select zones from this list until either there is a local improvement 
            in the current value of the objective function or a move that is equivalently 
            as good as the current best. Then make the move, update the list of candidate 
            zones, and return to step 4 or else repeat step 5 until the list is exhausted
    Step 6: When the list for region K is exhausted return to step 3, select another region, 
            and repeat steps 4-6
    Step 7: Repeat steps 2-6 until no further improving moves are made
    '''


    def __init__(self, w, z, iniCount, nIter=100):
        '''
        Arguments:
            w: spatial weights object
            z: array, n*m matrix of observations on m attributes across n zones.
            iniCount: int, the number of initial regions
            nIter: int, the number of iteration 
        '''
        self.w=w
        self.z=z
        self.iniCount=iniCount
        self.n=z.shape[0] #n rows--n zones
        self.m=z.shape[1] #m attributes
        #initialize
        self.iniSolution()        
        self.zoneTOregion()        
        curfobj=self.objective_function()
        self.cur_regions=copy.copy(self.regions)
        self.cur_zone2region=copy.copy(self.zone2region)
        self.wss=[]
        for i in range(nIter):
            self.iniSolution()
            self.zoneTOregion()
            fobj=self.objective_function()
            # find the optimal solution
            if fobj<curfobj:
                self.wss.append(fobj)
                self.cur_regions=copy.copy(self.regions)
                self.cur_zone2region=copy.copy(self.zone2region)
                curfobj=fobj
        self.regions=copy.copy(self.cur_regions)
        self.zone2region=copy.copy(self.cur_zone2region)                
        
    def iniSolution(self):
        '''
        step1: randomly select iniCount zones as seeds
        step2: randomly select a seed/region
        step3: form a region with the seed and all its first order neighbors
        step4: repeat step2-3 until all seeds are visited
        step5: if there are no zones remained, done! Otherwise, repeat step2-4.       
        '''
        nCluster=self.iniCount 
        remains=range(0,self.n) #the zones to be inserted into regions       
        regions=[[] for i in range(nCluster)] #list of lists
        seeds=random.sample(range(0,self.n),nCluster) #randomly select nCluster zones as a seeds
        for i in range(nCluster):  #initialize regions
            regions[i].append(seeds[i])
            remains.remove(seeds[i]) #those seeds have been in regions
            
        while len(remains)!=0:  #insert other zones into those regions
            for i in range(nCluster):                
                neighbors=copy.copy(self.getNeighbors(i, regions)) #neighbors of ith region                
                neighbors=[neig for neig in neighbors if neig in remains]                
                if len(neighbors)!=0:  #add all the neighbors into the ith region
                    regions[i].extend(neighbors)
                    remains=[elem for elem in remains if elem not in neighbors]#delete neighbors from remains                    
                    if len(remains)==0:
                        break
                    
        self.regions=copy.copy(regions)
        self.zone2region={}
        for r,region in enumerate(regions):
            for zone in region:
                self.zone2region[zone]=r
                
    def getNeighbors(self, idRegion, regions=None):
        '''
        Given a region, represented by a list including the index of original zones in the region,
        return a list of neighbors represented by the index of the neighbor zones.
        
        Arguments:
            idRegion: int, the index of the region whose neighbor are to be found
            regions: List, a list of lists, each list is a region, including the indexes of areas in that region.
            
        Return:
            L: list, including indexes of neighbor areas.
        '''
        if not regions:
            regions=self.regions
        
        neigh=[]
        members=regions[idRegion]                     
        for member in members:                         
            candidates=self.w.neighbors[member]                         
            candidates=[candidate for candidate in candidates if candidate not in members]                         
            candidates=[candidate for candidate in candidates if candidate not in neigh]                         
            neigh.extend(candidates) 
        
        return neigh
        
    def objective_function(self,solution=None):         
        # solution is a list of lists of region ids [[1,7,2],[0,4,3],...] such         
        # that the first region has areas 1,7,2 the second region 0,4,3 and so         
        # on. solution does not have to be exhaustive         
        if not solution:             
            solution=self.regions         
        wss=0         
        for region in solution:             
            m=self.z[region,:]             
            var=m.var(axis=0)             
            wss+=sum(num.transpose(var))*len(region)         
        return wss 
    
    def zoneTOregion(self):
        '''
        Main function implements AZP algorithm 
        '''
        
        flag=True        
        while flag:
            nmove=0 
            #Step 1: Start by generating a random zoning system of N small zones into M regions, M<N
            #Step 2: Make a list of the M regions. 
            mRegions=range(0,self.iniCount)
            #Step 3: Select and remove any region K at random from this list.
            while len(mRegions)!=0: # change to loop
                # generate a random integer in[0, nRegions]
                # kRegion: the id of the region to be removed            
                temp1=random.sample(mRegions,1) #randomly select a region from mRegions
                kRegion=temp1[0]                              
                mRegions.remove(kRegion)  # remove region k from list mRegions
                #Step 4: Identify a set of zones bordering on members of region K that could be moved 
                #into region K without destroying the internal contiguity of the donor region(s)
                kneighbors=copy.copy(self.getNeighbors(kRegion))
                #Step 5: Randomly select zones from this list until either there is a local improvement 
                #   in the current value of the objective function or a move that is equivalently 
                #as good as the current best. Then make the move, update the list of candidate 
                #zones, and return to step 4 or else repeat step 5 until the list is exhausted
                while len(kneighbors)!=0: # change to loop # if len(kneighbors)==0, go to step 3
                    temp2=random.sample(kneighbors,1)#random.randint(0, nNeighbors) # select a neighbor
                    idNeighbor=temp2[0]                                 
                    k=self.zone2region[idNeighbor] # original region the neighbor zone belongs to                
                    kzones=copy.copy(self.regions[k])                    
                    tag=check_contiguity(self.w, kzones,idNeighbor)                    
                    kneighbors.remove(idNeighbor) #remove selected neighbor    
                    
                    if tag:  # the remaining zones in zone k are contiguous
                        #remove the neighbor from the original region
                        #calculate the objective function
                        cur_in=self.regions[kRegion]
                        cur_out=self.regions[self.zone2region[idNeighbor]]
                        current=self.objective_function([cur_in,cur_out])
                        new_in=copy.copy(cur_in)
                        new_out=copy.copy(cur_out)
                        new_in.append(idNeighbor)
                        new_out.remove(idNeighbor)
                        new=self.objective_function([new_in,new_out])
                        change=new-current 
                        if change<0:  # move this neighbor to this region
                            # extend the neighbor list
                            old_region=self.zone2region[idNeighbor]
                            self.regions[old_region].remove(idNeighbor)
                            self.zone2region[idNeighbor]=kRegion
                            self.regions[kRegion].append(idNeighbor) 
                            kneighbors=self.getNeighbors(kRegion)#update the list of neighbors
                            nmove=nmove+1
            #Step 6: When the list for region K is exhausted return to step 3, select another region, 
                     #and repeat steps 4-6
            #Step 7: Repeat steps 2-6 until no further improving moves are made
            if nmove==0:
                flag=False

if __name__ == '__main__':
    w=pysal.weights.weights.lat2gal(5,5)         
    z=num.random.random_sample((w.n,2))         
    nCount=5
    azp=AZP(w,z,nCount)
    
    print azp.regions
    
    
