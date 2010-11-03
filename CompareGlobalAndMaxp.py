'''
Created on Oct 21, 2010

@author: GeoDa Admin
'''
import pysal
import time
from pysal.common import copy
from GlobalMaxp_V3 import GlobalMaxp
from maxp_V2 import Maxp
import numpy as np

if __name__ == '__main__':
    
    import random
    import numpy as np
    random.seed(100)
    np.random.seed(100)
    w=pysal.lat2W(30,30)
    z=np.random.random_sample((w.n,2))
    p=np.random.random(w.n)*100
    p=np.ones((w.n,1),float)
    floor=3
    solution1=Maxp(w,z,floor,floor_variable=p,initial=100)
    solution2=GlobalMaxp(w,z,floor,floor_variable=p,initial=100)
    solution2.feasible = solution1.feasible
    solution2.p = solution1.p
    solution2.regions = copy.deepcopy(solution1.regions)
    solution2.area2region = copy.deepcopy(solution1.area2region)
    
    time0 = time.clock()
    solution1.swap()
    time1 = time.clock()
    print "The Number of Regions generated: ", solution1.p
    print "The final Within Sum of Squares is: ", solution1.objective_function()
    print "The previous Maxp Stuff took %.3f seconds to swap" % (time1 - time0)
    print ""
    
    time2 = time.clock()
    solution2.globalSwap()
    time3 = time.clock()
    print "The Number of Regions generated: ", solution2.p
    print "The final Within Sum of Squares is: ", solution2.objective_function()
    print "The Global Maxp Stuff took %.3f seconds to swap" % (time3 - time2)
    print ""
