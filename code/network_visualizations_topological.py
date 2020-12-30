import networkx as nx
import xlrd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pq_helper import get_dataframe

'''
Script for creating topological visualization of pq network
Author: Amanda Li
'''

#----------------------------------------------------------------------
if __name__ == "__main__":
    
    path = 'acm95a100a2018_anonymized_modified.xlsx'
    (p_nodes, q_nodes, links, mod_p_nodes) = get_dataframe(path)    
    
    # https://networkx.github.io/documentation/stable/tutorial.html  
    # https://networkx.github.io/documentation/stable/reference/drawing.html
    
    status1 = [] # list of status 1 p-nodes
    for item in links['Start']:
        if (item[0] == 'P') and (item not in status1):
            status1.append(item)
    for item in links['End']:
        if (item[0] == 'P') and (item not in status1):
            status1.append(item)  
    
    # read in adjacency matrix (which accounts for status 1 nodes only)
    book = pd.ExcelFile("adjacency_matrix_with_headers.xlsx")
    df = book.parse()    
    
    # create directed graph from adjacency matrix
    G = nx.from_numpy_matrix(df.values.transpose(), create_using=nx.DiGraph())
    G2 = nx.from_numpy_matrix(df.values.transpose(), create_using=nx.Graph()) 
    # use nx.connected_components(G2) to see components
    
    new_labels = {}
    
    for i in range(96): # relabel p-nodes
        new_labels[i] = status1[i]
    for j in range(96, 337): # label q-nodes 
        new_labels[j] = 'Q' + str(j - 95)
        
    nx.relabel_nodes(G, new_labels, copy=False)
    
    node_shape = {}
    for node in G.nodes():
        if node[0] == 'P':
            node_shape[node] = 'o'
        else:
            node_shape[node] = 's'
    
    nx.set_node_attributes(G, node_shape, 'shape')   
    
    edge_color = {}
    for edge in G.edges():
        if edge[0][0] == 'P':
            edge_color[edge] = 'blue'
        else:
            edge_color[edge] = 'red'
    
    nx.set_edge_attributes(G, edge_color, 'color') 
    
    # adjust k to change how closely nodes are distributed in image
    nodePos = nx.layout.spring_layout(G, k=0.3, iterations=20)
    nodeShapes = ['o', 's']
    edgeColors = ['blue', 'red']
    
    plt.figure()
    # draw nodes
    for shape in nodeShapes:
        if shape == 'o':
            node_label = 'p-nodes'
        else:
            node_label = 'q-nodes'
        nx.draw_networkx_nodes(G, nodePos, node_shape=shape, 
                               nodelist=[sNode[0] for sNode in filter(lambda x: x[1]['shape']==shape, G.nodes(data = True))], 
                               node_size=25, node_color='black', label=node_label)
    
    # draw edges
    for color in edgeColors:
        nx.draw_networkx_edges(G, nodePos, edge_color=color, 
                               edgelist=[sEdge for sEdge in filter(lambda x: x[2]['color']==color, G.edges(data = True))])    
    
    plt.title('Topological Visualization of PQ Network')
    plt.legend()
    #nx.draw_networkx(G, with_labels=True, node_size=100)
    
    # Note: Q135 doesn't have any links

    
    
    