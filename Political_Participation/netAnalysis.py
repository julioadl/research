import sys
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

#Load file
name_file = sys.argv[1]
csv = pd.read_csv(name_file)
#Take screen names and mentions
sn = list(csv.screen_name)
mentions = list(csv.Mentions)
no_of_nodes = len(sn)
#Build dictionary by loading keys
netDict1 = {}
for i in sn:
	netDict1[i] = []

#Extend with other mentiosn
for i in range(no_of_nodes):
	#Except na's
	try:
		#Split out mentions
		out_mentions = mentions[i].split(',')
		#Extend into initial dict
		netDict1[sn[i]].extend(out_mentions)
	except:
		pass

#Eliminate duplicates
netDict2 = {}
for i in netDict1:
	netDict2[i] = list(set(netDict1[i]))

#PAss into networkx format
#Note that create_using allows to make it directed graph
net = nx.from_dict_of_lists(netDict2, create_using=nx.DiGraph())
#Obtain degree
deg = net.degree()
#Obtain in_degree
in_deg = net.in_degree()
#Out degree
out_deg = net.out_degree()
#Calculate betweeness
betweenness = nx.betweenness_centrality(net)
#Calculate eigenvector
eigenvector = nx.eigenvector_centrality_numpy(net)
#Join all these measures into Data Frames
degree = pd.DataFrame({'node':deg.keys(), 'degree': deg.values()})
indegree = pd.DataFrame({'node':in_deg.keys(), 'indegree': in_deg.values()})
outdegree = pd.DataFrame({'node':out_deg.keys(), 'outdegree': out_deg.values()})
between = pd.DataFrame({'node':betweenness.keys(), 'betweenness': betweenness.values()})
eigen = pd.DataFrame({'node':eigenvector.keys(), 'eigenvector': eigenvector.values()})
#join into a single data frame
dta = degree.merge(indegree)
dta = dta.merge(indegree)
dta = dta.merge(outdegree)
dta = dta.merge(between)
dta = dta.merge(eigen)
#Save 
dta.to_csv('netstats.csv')
layout = nx.spring_layout(net, k=1)
nx.draw_networkx(net, node_size=25, with_labels=False, pos=layout, alpha=0.5, width=0.5)
plt.show()