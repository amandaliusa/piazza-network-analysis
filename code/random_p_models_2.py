import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.distributions.empirical_distribution import ECDF
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
    
    N = 1000
    
    parameter_values = [0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000]
    
    # create DataFrame to store results
    alphas = [[i]*8 for i in parameter_values]
    d = {'alpha': [j for i in alphas for j in i], 'beta': parameter_values*8}
    df = pd.DataFrame(data=d)
    avg_cycles = []
    max_cycles = []
    
    #https://arxiv.org/pdf/cond-mat/0012181.pdf
    
    for alpha in parameter_values:
        for beta in parameter_values:
            n_cycles = []
    
            for iteration in range(N):
                # initialize adjacency matrix
                A = np.zeros([n, n]) 
                
                for link in range(m):
                    # get in-degrees and out-degrees of nodes
                    k_in = A.sum(axis=0)
                    k_out = A.sum(axis=1)
                    
                    # get vector of probabilities for each node (normalized)
                    p_a = k_out + alpha
                    p_a /= p_a.sum()
                    p_b = k_in + beta
                    p_b /= p_b.sum()  
                    
                    # choose source node
                    a = np.random.choice([k for k in range(n)], p=p_a)  
                    
                    # choose (different) sink node
                    b = np.random.choice([k for k in range(n)], p=p_b) 
                    while a == b:
                        b = np.random.choice([k for k in range(n)], p=p_b) 
                    
                    # create link between source and sink
                    A[a][b] = 1
                
                # create graph and find number of cycles 
                G = nx.from_numpy_matrix(A, create_using=nx.DiGraph()) 
                cycles = list(nx.simple_cycles(G))
                n_cycles.append(len(cycles))             
           
            # get average and maximum number of cycles
            max_cycles.append(np.max(n_cycles))
            avg_cycles.append(np.mean(n_cycles))
            print(f'alpha: {alpha}, beta: {beta}, avg cycles: {np.mean(n_cycles)}')
    
    # add avg and max cycles to dataframe
    df['maximum cycles'] = max_cycles
    df['average cycles'] = avg_cycles
    
    ## save dataframe
    df.to_csv('random_cycles.csv')
    
    ## cycle lengths from actual network (see projections_p.py)
    #actual_cycles = {15: 297, 17: 166, 16: 276, 19: 42, 13: 331, 14: 296, 18: 76, 12: 318, 11: 229, 20: 14, 10: 175, 9: 137, 7: 67, 6: 40, 8: 90, 5: 20, 4: 9, 2: 8, 3: 6}
    
    alpha = 100
    beta = 100
    n_cycles = []
    
    for iteration in range(N):
        # initialize adjacency matrix
        A = np.zeros([n, n]) 
        
        for link in range(m):
            # get in-degrees and out-degrees of nodes
            k_in = A.sum(axis=0)
            k_out = A.sum(axis=1)
            
            # get vector of probabilities for each node (normalized)
            p_a = k_out + alpha
            p_a /= p_a.sum()
            p_b = k_in + beta
            p_b /= p_b.sum()  
            
            # choose source node
            a = np.random.choice([k for k in range(n)], p=p_a)  
            
            # choose (different) sink node
            b = np.random.choice([k for k in range(n)], p=p_b) 
            while a == b:
                b = np.random.choice([k for k in range(n)], p=p_b) 
            
            # create link between source and sink
            A[a][b] = 1
        
        # create graph and find number of cycles 
        G = nx.from_numpy_matrix(A, create_using=nx.DiGraph()) 
        cycles = list(nx.simple_cycles(G))
        n_cycles.append(len(cycles))             
   
    # plot ecdf
    ecdf = ECDF(n_cycles)
    plt.figure()
    plt.plot(ecdf.x,ecdf.y)   
    plt.xlabel("number of cycles")
    plt.ylabel("ECDF")
    plt.title("ECDF of number of cycles (alpha = beta = 100)")
    
    # boxplots
    plt.figure()
    plt.boxplot(n_cycles)   
    plt.xlabel("number of cycles")
    plt.title("Number of cycles (alpha = beta = 100)") 
    
    plt.figure()
    plt.boxplot(n_cycles, showfliers=False)   
    plt.xlabel("number of cycles")
    plt.title("Number of cycles (alpha = beta = 100) w/out outliers")    

