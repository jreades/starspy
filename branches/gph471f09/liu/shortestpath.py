### short.py

### Yin Liu   yin.liu.1@asu.edu


graph = {0:[2,1],1:[0,3],2:[0,4,3],3:[1,2,5,],4:[2,6,5],5:[3,4,7],6:[4,7],7:[5,6]}

	
def short(G={}):
	"""Returns the shortest steps and path from each vertex to each other.

	Arguments:
		G = {}, represents a graph; 
			the keys keys represent each vertex while the values represent the linking neighbors to each vertex.
	"""
	
	ans=[]
	keys = G.keys()
	
	for st in keys:
		anst=[]
		pack=[]
		neigh=[]
		t=0

		for i in keys:
			t = t+1
			anst.append([st,i,-1,str(st)])
					
		anst[st][2]=0
		t = t-1
		pack.append([G.get(st),anst[st][3]])
		
		while t != 0:
			neigh = pack
			pack = []
			for num in range(len(neigh)):
				pp = neigh[num][1]    # pp records the previours path
				
				for item in range(len(neigh[num][0])):	
					end = neigh[num][0][item]
					if anst[end][2] == -1:
						anst[end][2]=anst[st][2]+1
						anst[end][3]=pp + " - "+str(end)
						t = t-1
						pack.append([G.get(end),anst[end][3]])
			anst[st][2]=anst[st][2]+1
		anst[st][2] = 0
		ans.extend(anst)
	
	for i in range(len(ans)):
		result = "Start:"+str(ans[i][0])+" End:"+str(ans[i][1])+" -- "+"Length:"+str(ans[i][2]) + " Path:"+str(ans[i][3])
		print result

