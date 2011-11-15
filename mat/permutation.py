import pysal
import numpy as np
w = pysal.open("C:/Users/Daehyun You/workspace/Project/stl.gal").read()
f = pysal.open("C:/Users/Daehyun You/workspace/Project/stl_hom.txt")
y = np.array(f.by_col['HR8893'])
mi = pysal.Moran(y,  w,permutations=9999)

import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


# the histogram of the data
n, bins, patches = plt.hist(mi.sim, 50, normed=1, facecolor='green', alpha=0.9)

# add a 'best fit' line
y = mlab.normpdf(bins, mi.EI_sim, mi.sim.std())
l = plt.plot(bins, y, 'r--', linewidth=1)
l2 = plt.plot(mi.I*np.ones(20), max(n)*np.array(range(20))/19, 'b', linewidth =2)

plt.xlabel('permutation')
plt.ylabel('density')
plt.title(r"Permutation of Moran's I")
plt.grid(True)

plt.show()


###http://pysal.org/1.2/library/esda/moran.html 
