'''
Created on 2009-11-11

@author: Jing YAO
'''
import random 
import pysal 
import numpy as num
import sys 
import copy
from components import check_contiguity


class MAXp(object):
    '''
    Assumption: each area has at least one neighbor, that is, the graph is of connectivity.
    
    The max-p-region problem is a special case of const rained clustering where
    a finite number of geographical areas, n, are aggregated into the maximum
    number of regions, p, such that each region satisfies the following const raints:
    
    1. The areas within a region must be geographically connected. This
    const raint is commonly known as the spatial cont iguity constraint.
    
    2. The regional value of a predefined attribute must be greater than or
    equal to a minimum predefined threshold value. This regional value
    is obtained by adding up the areal values of the att ribute of the areas
    assigned to each region.

    3. Each area must be assigned to one and only one region.
    
    4. Each region must contain at least one area.
    '''
    
    def __init__(self, w, z, constrain_value, constrain_attribute, nIter=100):
        '''        
        Arguments:
            w: spatial weights object
            z: array, n*m matrix of observations on m attributes across n areas.                  
            constrain_value: float, a threshold value for a variable that has to be obtained
            in each region.
            constrain_attribute: list, n*1 vector, it is the attribute variable whose value at regional
            level is constrained to be greater than or equal to a predefined
            threshold value (constrain_value).
            nIter: int, the number of iteration
        '''
        self.w=w
        self.z=z
        self.nobs=self.w.n #nobs: int, the number of observations
        self.cons_val=constrain_value
        self.cons_attr=constrain_attribute
        p=0
        solution=[]
        
        for i in range(nIter):
            self.iniSolution()            
            if self.p==p:
                solution.append(self.regions)
            if self.p>p:
                p=copy.copy(self.p)
                solution=copy.copy([self.regions])
        
        # local search phase: find the optimal local move
        self.wss=[]
        curfobj=999999
        for idelem, elem in enumerate(solution):
            # result of construction phase
            self.regions=copy.copy(elem)
            self.p=len(self.regions)
            for r, region in enumerate(self.regions):
                for area in region:
                    self.area2region[area]=r
            # local search
            self.areaTOregion()            
            for r, region in enumerate(self.regions):
                for area in region:
                    self.area2region[area]=r 
            fobj=self.objective_function()                
            #self.wss.append(fobj)
            if fobj<curfobj:
                self.wss.append(fobj)
                self.cur_regions=copy.copy(self.regions)
                self.cur_area2region=copy.copy(self.area2region)
                curfobj=fobj
        # the final result
        self.regions=copy.copy(self.cur_regions)
        self.area2region=copy.copy(self.cur_area2region)
        self.p=len(self.regions)        
        
    def iniSolution(self):
        '''
        step1: selecting at random an unassigned area i as the "seed" of a growing region 
        (Gk). If there is no seed area, go to step5.
        
        step2: If the constrained attribute value of the selected area(Li) is greater than 
        or equal to the regional threshold value (threshold), the area becomes a region 
        by itself, go to step1; otherwise, go to step3.   
        
        step3: find all the neighbors of seed area. if there is no neighbors, go to step1.
         
        step4: one neighboring unassigned area is added to the growing region.
        The area to be added is determined by ordering the candidate areas (C) with 
        respect to an adaptive greedy function g(.). the candidate area with the lowest 
        greedy function value is assigned to the growing region Gk. go to step2.       
        
        step5: if there is no remaining area, done. if remaining areas cannot grow a new
        region, go to step6.
        
        step6: assign remaining areas to one of the existing regions.
        '''
        self.p=0 # number of regions
        nLoop=0
        while nLoop<=100:
            nLoop+=1
            remains=range(self.nobs) # remaining unassigned areas  
            regions=[]
            enclaves=[] # including regions that cannot satisfy the constraints
            while len(remains)!=0:
                temp1=random.sample(remains,1) #randomly select an area as the seed
                idseed=temp1[0]  #id of seed area
                remains.remove(idseed)
                region=[idseed] #the growing region with seed
                flag=True  #mark whether a region is formed
                while flag:
                    if self.check_constrain(region):
                        flag=False
                        regions.append(region)  # if satisfy the constraint attribute value, done
                    else:
                        candidates=[]  # neighbors of the growing region
                        for area in region:
                            neighbors=self.w.neighbors[area]
                            neighbors=[neigh for neigh in neighbors if neigh in remains]
                            neighbors=[neigh for neigh in neighbors if neigh not in region]
                            candidates.extend(neighbors)
                        if len(candidates)==0: # the growing region has no neighbors
                            enclaves.extend(region)
                            flag=False
                        else:
                            # choose the best neighbor based on greedy function
                            id_bestNeighbor=self.get_BestNeighbor(candidates, region)
                            region.append(id_bestNeighbor) # add the best neighbor
                            remains.remove(id_bestNeighbor) # update remaining areas
        
            # if no initial solution has been found, try again                
            if len(regions)!=0:
                # assign areas in enclaves into formed regions
                self.p=len(regions)
                while len(enclaves)!=0:
                    temp2=random.sample(enclaves,1) #randomly select an area to be assigned to regions
                    idEnclave=temp2[0]
                    # find all the neighbor regions; if no neighbor regions, leave it in enclaves
                    idregion=[] # id of candidate regions
                    for i in range(self.p):
                        temp_Neighbors=self.getNeighbors(i, regions) # neighbors of ith region
                        if idEnclave in temp_Neighbors: # area is the neighbor of ith region
                            idregion.append(i)
                    # assign the area to a neighboring region based on greedy function
                    if len(idregion)!=0:
                        tag=9999999
                        for j in idregion:
                            temp=self.greedy_function(idEnclave, regions[j])
                            if temp < tag:
                                tag=temp
                                id_bestRegion=j
                        # assign the enclave to the best neighboring region
                        regions[id_bestRegion].append(idEnclave)
                        enclaves.remove(idEnclave)
                           
                # set final regions
                self.regions=copy.copy(regions)
                self.area2region={}
                for r,region in enumerate(regions):
                    for area in region:
                        self.area2region[area]=r
                
    
    def get_BestNeighbor(self, neighbors, region):
        '''
        For given region, select the best neighbor in neighbors to be moved based on greedy function.
        
        Arguments:
            neighbors: list, including indexes of areas on the border of the region
            region: list, including indexes of areas in the region
            
        Return:
            n: integer, index of the area to be moved
        '''
        tag=9999999
        idNeighbor=-1
        for i in neighbors:
            temp=self.greedy_function(i, region)
            if temp < tag:
                tag=temp
                idNeighbor=i
        
        return idNeighbor                        
            
    def check_constrain(self, region):
        '''
        check value of constrained attribute
        
        Arguments:
            region: list, including indexes of areas in the region
            
        Return:
            True or False: boolean, if satisfying constrain value return True, otherwise, return False
        '''        
        fsum=0
        for i in region:
            fsum=fsum+self.cons_attr[i]
        
        if fsum >= self.cons_val:
            return True
        else:
            return False
        
    def greedy_function(self, idarea, region):
        '''
        The greedy function measures the benefit of selecting each candidate.
        
        Arguments:
            idarea: int, index of the area to be moved
            region: list, including the indexes of the areas in this region. It is the 
                    recipient region.
        
        Return:
            f: float, 
        '''
        ncol=self.z.shape[1] #ncol: the number of attributes       
        
        varea=self.z[idarea] #vector of the area
        fsum=0
        for index in region:
            voldarea=self.z[index]
            for j in range(ncol):
                fsum=fsum+num.power((varea[j]-voldarea[j]),2)
        
        return fsum
    
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
    
    def get_optimalNeighbors(self, idRegion):
        '''
        Given a candidate region in local move, return all the neighbors that keep both
        contiguity and constraint value.
        
        Arguments:
            idRegion: index of region
            
        Return:
            L: list, list including indexes of desired neighbors that can be added into the region. 
        '''
        # get all the neighbors
        neighbors=copy.copy(self.getNeighbors(idRegion))
        
        # find all the candidate neighbors
        candidate=[]
        for neigh in neighbors:
            id_neiRegion=self.area2region[neigh]           
            n2r=copy.copy(self.regions[id_neiRegion])
            temp_n2r=copy.copy(n2r)
            if check_contiguity(self.w, n2r, neigh):  # this function will remove neigh from n2r
                temp_n2r.remove(neigh)
                if self.check_constrain(temp_n2r):
                    candidate.append(neigh)
        return candidate
    
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
    
    def areaTOregion(self):
        '''
        Main function implements MAXP algorithm 
        
        Step1. Start with a initial feasible solution from the construction phase. This
        solution , with its respective global heterogeneity value, will have the
        status of current solution.
        
        Step2. Generate a list of all potential feasible neighboring solutions from the
        current solution. This list is known as the candidate list of moves.
        
        Step3. Evaluate each candidate by calculating its impact in the global heterogeneity
        value
        
        Step4. Choose the best admissible candidate and perform the move.
        
        Step5. The algorithm stops if the aspirational criteria have not been improved
        during a predefined number of iterations (conv) ; otherwise go to step2.
        '''
        flag=True        
        while flag:
            nmove=0            
            #Step 1: Start by generating a random zoning system of N small zones into M regions, M<N
            #Step 2: Make a list of the M regions. 
            mRegions=range(self.p)
            #Step 3: Select and remove any region K at random from this list.
            while len(mRegions)!=0: # change to loop
                # generate a random integer in[0, nRegions]
                # kRegion: the id of the region to be removed            
                temp1=random.sample(mRegions,1) #randomly select a region from mRegions
                kRegion=temp1[0]               
                mRegions.remove(kRegion)  # remove region k from list mRegions
                #Step 4: Identify a set of zones bordering on members of region K that could be moved 
                #into region K without destroying the internal contiguity of the donor region(s)
                # and keep the constraint value of the donor region
                kneighbors=copy.copy(self.get_optimalNeighbors(kRegion))
                #Step 5: Find the neighbor leading to a optimal local improvement 
                #   in the current value of the objective function or a move that is equivalently 
                #as good as the current best. Then make the move, update the list of candidate 
                #zones, and return to step 4 or else repeat step 5 until no possible neighbors can be found
                while len(kneighbors)!=0: # change to loop # if len(kneighbors)==0, go to step 3
                    # find the neighbor leading to the best move
                    id_bestArea=-1
                    tag=0.0
                    for idNeighbor in kneighbors:
                        #remove the neighbor from the original region
                        #calculate the objective function
                        cur_in=self.regions[kRegion]
                        cur_out=self.regions[self.area2region[idNeighbor]]
                        current=self.objective_function([cur_in,cur_out])
                        new_in=copy.copy(cur_in)
                        new_out=copy.copy(cur_out)
                        new_in.append(idNeighbor)
                        new_out.remove(idNeighbor)
                        new=self.objective_function([new_in,new_out])
                        change=new-current 
                        if change<tag: 
                            id_bestArea=idNeighbor
                            tag=change

                    # move the best neighbor
                    if id_bestArea>=0:
                        old_region=self.area2region[idNeighbor]
                        self.regions[old_region].remove(idNeighbor)
                        self.area2region[idNeighbor]=kRegion
                        self.regions[kRegion].append(idNeighbor) 
                        #update the list of neighbors
                        kneighbors=copy.copy(self.get_optimalNeighbors(kRegion))
                        nmove=nmove+1
                    else:
                        kneighbors=copy.copy([])
                    
            #Step 6: When no further possible move for region K,return to step 3, select another region, 
                     #and repeat steps 4-6
            #Step 7: Repeat steps 2-6 until no further improving moves are made
            if nmove==0:
                flag=False
        
if __name__ == '__main__':
    w=pysal.weights.weights.lat2gal(5,5)         
    z=num.random.random_sample((w.n,2)) 
    p=num.ones((w.n,1),float)
    floor=3
    s=MAXp(w,z,floor,p,5)
   
    print s.regions
    print s.p
    print s.wss

''' 
z is a 3*3 matrix
>>>[[5, 8, 2], [1, 0, 3], [7, 6, 4]]
>>>3
>>>[0.60811056002989328, 0.58105974630405288]
'''

'''
z is a 5*5 matrix
>>>[[22, 23, 18], [19, 24, 14, 9, 4], [12, 17, 16], [21, 20, 15, 10, 11], [8, 13, 7], [2, 3, 1], [6, 5, 0]]
>>>7
>>>[2.1090952102975153, 1.788088110187168, 1.7825748044896392]
'''