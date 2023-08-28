from tqdm import tqdm as tqdm
def split_raw_triple(raw_triple, ch = '\t'):
    ''' splits the raw triple to get the triple (nodes, edges, nodes) '''
    triple = []
    for el in raw_triple:
    	triple.append(el.split(ch))

    return triple


def nodemap(triple):
	''' enumerates each tuple of a graph '''

	key = {} # to store each encoding of a node
	i = 0

	for edge in triple:
		for j in range(len(edge)):
			if edge[j] in key: # if the node is already encoded then do nothing. If j is 1 implies edge[j] is an edge so we ignore
				continue
			
			else:
				key[edge[j]] = i # encode the node
				i += 1

	return key


def getdegreedist(nodes):
	''' gets the outdegree distribution of the entire graph '''

	degreedist = {}
	i = 0
	
	for node in nodes:
		if node[0] in degreedist:  
			degreedist[node[0]] += 1      # if node already in degree dictionary then increment its key value
		else:
			degreedist[node[0]] = 1
	
	return degreedist


def sort_degreedist(degreedist, reverse = False):
	''' sorts the degree distribution '''

	degreedistsorted = dict(sorted(degreedist.items(), key=lambda item: item[1], reverse = reverse))
	
	return degreedistsorted


def delete_edge(triple):
    ''' deletes the edge labels from the triple containing nodes and edges'''
    for el in triple:
        el.pop(1)
    return triple


def to_string_node(triple):
    for el in triple:
        for i in range(len(el)):
            el[i] = str(el[i])
    return triple


def getsubgraph(triple, nodes, adj = {}, hops = 1):
    ''' returns a subgraph corresponding to the nodes specified and the hops specified'''
    hop = hops
    sgraph = []
    if hops == 0:
        return []


    for el in nodes:
        for edge in triple:
            if edge[0] == el:
                sgraph.append(edge)
    else:
        while(hop > 1):
            for node in nodes:
                neighbours = []
                if node in adj:
                    for nd in adj[node]:
                        neighbours.append(nd)
                        for edge in triple:
                            if edge[0] == nd and edge not in sgraph:
                                sgraph.append(edge)
            nodes = neighbours
            hop -= 1


    return sgraph


def drop_duplicate_node(triple):
	''' drops a duplicate triple '''

	n_triple = []

	for el in triple:
		if el not in n_triple:
			n_triple.append(el)  #dropping the duplicates

	return n_triple


def preprocess(triple, key):
    ''' returns the node encoding for each node '''
    for el in triple:
        for j in range(len(el)):
            el[j] = key[el[j]]  # changes each node by its encoding
    return triple

def getadjlist(triple, key):
	'''returns the adjacency list of the graph'''
	adj = {} # to store the adjacency list
	key = tqdm(key)
	for node in key: 
 		adj_v = [] #to store the set of nodes adjacent to each node
 		for edges in triple:
 			if edges[0] == node:
 				adj_v.append(edges[1])
 		adj[node] = adj_v
	return adj

def mapback(key):
	''' maps back the node encoding to its node '''
	reverse_key = {}
	for node in key:
		reverse_key[key[node]] = node
	return reverse_key

#key = nodemap([['N', 'A'],['N', 'B'], ['B', 'C']])
#print(preprocess([['N', 'A'],['N', 'B'], ['B', 'C']], key))
#print(getdegreedist(preprocess([['N', 'A'],['N', 'B'], ['B', 'C']], key)))

