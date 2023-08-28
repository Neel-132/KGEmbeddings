#!/usr/bin/env python
# coding: utf-8

# In[160]:


from Gprocess import roach as rch
import matplotlib.pyplot as plt
import tqdm as tqdm
from time import time

from gem.utils import graph_util
from gem.evaluation import visualize_embedding as viz
from gem.evaluation import evaluate_graph_reconstruction as gr

from gem.embedding.hope import HOPE
from argparse import ArgumentParser


# In[161]:


l = []
with open('train.txt') as data:
    for line in data:
        l.append(line)
triple = rch.split_raw_triple(l)
triple


# In[162]:


triple = rch.delete_edge(triple)


# In[163]:


for edge in triple:
    edge[1] = edge[1].strip()
triple


# In[164]:


key = rch.nodemap(triple)
key
keyinv = rch.mapback(key)


# In[165]:


ntriple = rch.preprocess(triple, key)
len(ntriple)


# In[ ]:


#adj = rch.getadjlist(ntriple, keyinv)
#adj


# In[106]:


'''with open('adjwn18.txt', 'w') as f:
    for key, value in adj.items(): 
        f.write('%s:%s\n' % (key, value))
    print("File written successfully")
    f.close()'''


# In[24]:


#len(adj)


# In[95]:


ntriple


# In[159]:


degreedist = rch.getdegreedist(ntriple)
degreedist


# In[108]:


sgraph = rch.getsubgraph(ntriple, [785, 1038, 60])


# In[109]:


sgkey = rch.nodemap(sgraph)
sgkeyinv = rch.mapback(sgkey)


# In[110]:


sgraph = rch.preprocess(sgraph, sgkey)


# In[111]:


len(sgraph)


# In[112]:


sgraph = rch.drop_duplicate_node(sgraph)


# In[113]:


with open('3hopsubgraphwn18.edgelist', 'w') as s:
    for item in sgraph:
        s.write('{} {}\n'.format(item[0], item[1]))
    print('File written successfully')
                 
s.close()


# In[ ]:


edge_f = "1hopsubgraphwn18.edgelist"
isDirected = True
G = graph_util.loadGraphFromEdgeListTxt(edge_f, directed=isDirected)
G = G.to_directed()


# In[ ]:


embedding = HOPE(d = 4, beta = 0.01)
print('Num nodes: %d, num edges: %d' % (G.number_of_nodes(), G.number_of_edges()))
Y = embedding.learn_embedding(graph=G, is_weighted=True, no_python=True)
t1 = time()
print(embedding.get_method_name()+':\n\tTraining time: %f' % (time() - t1))
MAP, prec_curv, err, err_baseline = gr.evaluateStaticGraphReconstruction(G, embedding, Y, None)
print(("\tMAP: {} \t precision curve: {}\n\n\n\n"+'-'*100).format(MAP, prec_curv[:5]))


# In[126]:


import pandas as pd
labels = []
for i in range(1, 5):
    labels.append("D{}".format(i))
    
df = pd.DataFrame(Y, columns = tuple(labels))


# In[127]:


df.to_csv("1hopsgemb.csv", index = False)

