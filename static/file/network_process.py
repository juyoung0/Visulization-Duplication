import argparse
import networkx as nx
import matplotlib
import os
import sys
import json
from networkx.drawing.nx_agraph import graphviz_layout
from networkx.drawing.nx_agraph import write_dot

parser = argparse.ArgumentParser(description='Get Gene List convert to Network Data and return (Degree, Betweenness Centrality, x-axis, y-axis)')
parser.add_argument('gene_list_file',type=str,help='Gene List file')
parser.add_argument('netw_file',type=str,help='Network file')
parser.add_argument('width',type=float,help='width')
parser.add_argument('height',type=float,help='height')
parser.add_argument('username',type=str,help='username')
parser.add_argument('project_name',type=str,help='project_name')
parser.add_argument('session_name',type=str,help='session_name')
parser.add_argument('session_ver',type=str,help='session_ver')
parser.add_argument('block_iden',type=str,help='block_iden')


args = parser.parse_args()

matplotlib.use('Agg')

gene_file = open(args.gene_list_file,'r') # Pass Gene List
gene_data = gene_file.read().splitlines()
net_file = open(args.netw_file,'r') # Pass Network Data
net_data = net_file.read().splitlines()

default_width = 800.0 # Default width
default_height = 600.0 # Default height
user_width = args.width # Get width as argument
user_height = args.height # Get Height as argument

user_G = nx.Graph()

net_list = []

for elem in net_data:
    tokens = elem.split(" ")
    if (tokens[0] in gene_data) and (tokens[1] in gene_data): # Find only in-geneList edges ( To find out-geneList edges, change and to or )
        user_G.add_node(tokens[0])
        user_G.add_node(tokens[1])
        user_G.add_edge(tokens[0],tokens[1],weight=int(tokens[2]))
        net_elem = {}
        net_elem['src'] = tokens[0]
        net_elem['tgt'] = tokens[1]
        net_elem['cs'] = int(tokens[2])
        net_list.append(net_elem)
#MST = nx.minimum_spanning_tree(user_G)

#print "Node number : " + str(user_G.number_of_nodes())
#print "Edge number : " + str(user_G.number_of_edges())

deg = nx.degree(user_G) # Get Node Degree
bc = nx.betweenness_centrality(user_G) # Get Node Betweenness Centrality

# Get positions of each layout

#pos = nx.circular_layout(user_G)
#l_name = "circular"
#pos = nx.fruchterman_reingold_layout(user_G)
#l_name = "fruchterman"
#pos = nx.random_layout(user_G)
#l_name = "random"
#pos = nx.shell_layout(user_G)
#l_name = "shell"
#pos = nx.spring_layout(user_G)
#l_name = "spring"
#pos = nx.spectral_layout(user_G)
#l_name = "spectral"
pos = graphviz_layout(user_G)
l_name = "graphviz"

node_list = nx.nodes(user_G) # Get nodes of Graph as List

node_output = []
# Caculate according to User Display
for elem in node_list:
    x = pos[elem][0]
    y = pos[elem][1]
    x = x*(user_width/default_width)
    y = y*(user_height/default_height)
    pos[elem] = (x,y)
    node_elem = {}
    node_elem['gene'] = elem
    node_elem['degree'] = user_G.degree(elem)
    node_elem['bc'] = float(bc[elem])
    node_elem['x'] = float(pos[elem][0])
    node_elem['y'] = float(pos[elem][1])
    node_output.append(node_elem)

"""
# Draw Graph in Image
nx.draw(user_G,pos)
nx.draw_networkx_labels(user_G,pos)
img_name = "path_" + l_name + ".png"
matplotlib.pyplot.savefig(img_name,dpi=300)
"""

os.chdir('..')
res_file_name = os.path.join(os.getcwd(), 'member', args.username, args.project_name, args.session_name, args.session_ver, args.block_iden, "result_node.txt")
res_file = open(res_file_name,'w')

# Write to File
#res_file.write("Name,Degree,BetweennessCentrality\n")#"Name,Degree,BetweennessCentrality,x-axis,y-axis\n")
res_file.write(json.dumps({'output':node_output}))#","+str(pos[elem][0])+","+str(pos[elem][1])+"\n")

net_file.close()
res_file.close()

edge_file_name = os.path.join(os.getcwd(), 'member', args.username, args.project_name, args.session_name, args.session_ver, args.block_iden, "result_edge.txt")
edge_file = open(edge_file_name,'w')
edge_file.write(json.dumps({'output':net_list}))
edge_file.close()
