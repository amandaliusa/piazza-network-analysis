import networkx as nx
import xlrd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pq_helper import get_dataframe

'''
Script for creating temporal visualization of the pq network
Author: Amanda Li
'''   

#----------------------------------------------------------------------
if __name__ == "__main__":
    
    path = 'acm95a100a2018_anonymized_modified.xlsx'
    (p_nodes, q_nodes, links, mod_p_nodes) = get_dataframe(path)    
    
    ordered_nodes = []
    ordered_edges = []
    duplicate_nodes = {} # store number of times a p-node has participated
    
    # iterate through all links
    for i in range(len(links['ID'])):
        start = links['Start'][i]
        end = links['End'][i]
        
        if start[0] == 'P': # [P answers Q]; always add new p-node but never new q-node
            
            # if p-node has not participated before
            if start not in duplicate_nodes:
                duplicate_nodes[start] = 0
            
            # add new p-node
            count = duplicate_nodes[start]
            duplicate_nodes[start] += 1
            start += '_' + str(count+1) # update start of link
            ordered_nodes.append(start)           
            
        else: # [Q asked by P]; always add new q-node and new p-node 
            
            # add new q-node
            ordered_nodes.append(start)
            
            # if p-node has not participated before
            if end not in duplicate_nodes:
                duplicate_nodes[end] = 0
            
            # add new p-node
            count = duplicate_nodes[end]
            duplicate_nodes[end] += 1            
            end += '_' + str(count+1) # specify end of link
            ordered_nodes.append(end)           
         
        # add edge corresponding to link 
        ordered_edges.append((start, end))   
    
    q = 1
    p = 2
    times = [0] * 910
    data = [0] * 910
    
    time = 1
    for i in range(len(ordered_nodes)):
        if ordered_nodes[i][0] == 'Q': # question is asked
            data[i] = q    # add q-node 
        else: 
            data[i] = p
            # check if p-node follows a q-node (person asks question)
            if ordered_nodes[i-1][0] == 'Q':
                time -= 1 # add p-node at same time as previous q-node
                
        times[i] = time # add node at current timestep
        time += 1
    
    # plot and label nodes
    fig, ax = plt.subplots()
    ax.scatter(times, data)
    for i, txt in enumerate(ordered_nodes):
        ax.annotate(txt, (times[i], data[i]))
    
    # plot links
    for edge in ordered_edges:
        from_node = edge[0]
        to_node = edge[1]
        
        f = ordered_nodes.index(from_node)
        t = ordered_nodes.index(to_node)
        
        # edges from q-node to p-node are red, from p-node to q-node are blue
        if from_node[0] == 'Q':
            color = 'red'
        else:
            color = 'blue'        
        
        plt.arrow(times[f], data[f], times[t] - times[f], data[t] - data[f], 
                  length_includes_head=True, color=color, head_width=0.006, head_length=0.01)
        plt.title('Temporal Visualization of PQ Network')
        plt.xlabel('Network Time')