import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pq_helper import get_dataframe

'''
Script for analysis of random model #2 for the one-mode
projection of the pq network
Author: Amanda Li
'''

#----------------------------------------------------------------------
if __name__ == "__main__":
    
    path = 'acm95a100a2018_anonymized_modified.xlsx'
    (p_nodes, q_nodes, links, mod_p_nodes) = get_dataframe(path)    
    
    n = 184 # number of students 
    m = 263 # number of links in real network (see projections_p.py)
    
    N = 100
    n_cycles = []
    cycle_dict = {}
    
    for i in range(2, 21):
        cycle_dict[i] = []
    
    for i in range(N):
        A = np.zeros([n, n]) # adjacency matrix
        
        for j in range(m):
            # choose two nodes at random and create link
            a = np.random.randint(0, n-1)  
            b = np.random.randint(0, n-1)  
            while a == b:
                b = np.random.randint(0, n-1) 
            A[a][b] = 1
        
        # create graph and find number of cycles 
        G = nx.from_numpy_matrix(A, create_using=nx.DiGraph()) 
        cycles = list(nx.simple_cycles(G))
        n_cycles.append(len(cycles))
        
        cycle_lengths = {}
        
        for cycle in cycles:
            if len(cycle) not in cycle_lengths:
                cycle_lengths[len(cycle)] = 1
            else:
                cycle_lengths[len(cycle)] += 1  
        
        # count cycles of various lengths 
        for i in range(2, 21):
            try:
                cycle_dict[i].append(cycle_lengths[i])
            except:
                cycle_dict[i].append(0)                
    
    # cycle lengths from actual network (see projections_p.py)
    actual_cycles = {15: 297, 17: 166, 16: 276, 19: 42, 13: 331, 14: 296, 18: 76, 12: 318, 11: 229, 20: 14, 10: 175, 9: 137, 7: 67, 6: 40, 8: 90, 5: 20, 4: 9, 2: 8, 3: 6}
    
    # plot against actual network values 
    plt.figure()
    plt.hlines(2597, 0, 2)    
    plt.boxplot(n_cycles)
    plt.ylabel('Number of Cycles')
    plt.title('Number of Cycles in Random Graph')
    plt.legend(['True value'])  
    plt.savefig('Figures/One-Mode Projections/Random_model')
    
    for i in range(2, 21):
        plt.figure()
        plt.hlines(actual_cycles[i], 0, 2)    
        plt.boxplot(cycle_dict[i])
        plt.ylabel('Number of {}-Cycles'.format(i))
        plt.title('Number of {}-Cycles in Random Graph'.format(i))
        plt.legend(['True value'])        
        plt.savefig('Figures/One-Mode Projections/{}-cycles'.format(i))
    