import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pq_helper import bipartite_coef, get_dataframe, neighbors, common_neighbors, remove_status_0

'''
Script for analysis of random model #2 for the pq network
Author: Amanda Li
'''

def model2(n, m, l):
    '''
    Function that takes a number of p-nodes, q-nodes, and links; generates a random 
    network; and returns the adjacency matrix for the network. Following the convention
    set in the notes, for p-node i and q-node alpha, we set A(i, alpha) = 1 if alpha --> i 
    and A(alpha, i) = 1 if i --> alpha.
    
    Inputs:
    n: number of p-nodes
    m: number of q-nodes
    l: number of p --> q links
    
    Outputs:
    A: (n+m, n+m) adjacency matrix
    '''
    
    A = np.zeros([n+m, n+m]) # adjacency matrix 
    
    # for each q-node alpha, choose one p-node i_alpha uniformly at random to ask the 
    # question: alpha --> i_alpha
    for alpha in range(m):
        i_alpha = np.random.randint(0, n-1) # asks: alpha --> i_alpha
        # create dyadic link
        A[i_alpha][n + alpha] = 1
    
    # generate l p --> q links
    for k in range(l):
        # choose q-node uniformly at random 
        beta = np.random.randint(0, m-1)
        
        # choose p-node uniformly at random from P \ A_beta
        j_beta = np.random.randint(0, n-1)
        while A[j_beta][n + beta] == 1 or A[n + beta][j_beta] == 1:
            j_beta = np.random.randint(0, n-1)
        
        # create new link from j_beta to beta and add j_beta to A_beta
        A[n + beta][j_beta] = 1
        
    return A
        
#----------------------------------------------------------------------
if __name__ == "__main__":
    
    path = 'acm95a100a2018_anonymized_modified.xlsx'
    (p_nodes, q_nodes, links, mod_p_nodes) = get_dataframe(path)  
    
    n = len(p_nodes) - 12 # remove instructor and TAs
    m = len(q_nodes)
    
    # count number of answers given by students only (P185 - P196 are instructor/TAs)
    l = 0
    for i in range(len(links)):
        if links['Start'][i][0] == 'P':
            if int(links['Start'][i][1:]) < 185:
                l += 1  
    
    N = 100
    cn_p = np.zeros([N, 1]) # not including status=0 p-nodes
    cn_q = np.zeros([N, 1])
    cb_p = np.zeros([N, 1])
    cb_q = np.zeros([N, 1])
    
    # generate N synthetic networks
    for i in range(N):
        # create adjacency matrices and lists of neighbors
        A = model2(n, m, l)
        p_N, q_N = neighbors(A, n, m)
        A_1, status0 = remove_status_0(A, n)
        
        # calculate common neighbors (use A_1 for status=1 p-nodes only)
        cn_pi, cn_qi = common_neighbors(A_1, n-status0, m)
        cn_p[i] = cn_pi
        cn_q[i] = cn_qi
        
        # calculate bipartite coefficients
        ATA = np.matmul(A.T, A) # p-nodes
        AAT = np.matmul(A, A.T) # q-nodes        
        p_CN = ATA[:n, :n]
        q_CN = AAT[n:, n:]
        
        p_out_degree = np.sum(A[n:, :n], axis=0)
        q_in_degree =  np.sum(A[n:, :n], axis=1)
        
        q_CB, hn_q = bipartite_coef(p_CN, q_N, p_out_degree)
        p_CB, hn_p = bipartite_coef(q_CN, p_N, q_in_degree)
        
        # count only nodes that have neighbors
        #cb_q[i] = np.mean(q_CB) * m / hn_q 
        #cb_p[i] = np.mean(p_CB) * n / hn_p
        
        # count all nodes 
        cb_q[i] = np.mean(q_CB) 
        cb_p[i] = np.mean(p_CB)        
       
    # calculate values from actual network with TAs/instructor removed
    A_act = np.loadtxt(open("adjacency_matrix_all.csv", "rb"), delimiter=",") 
    
    # remove (zero-indexed) rows and columns corresponding to TAs/instructor 
    A_act = np.delete(A_act, [i for i in range(184,195)], 0)
    A_act = np.delete(A_act, [i for i in range(184,195)], 1)
    
    p_N_act, q_N_act = neighbors(A_act, n, m)        
    
    # remove status=0 nodes
    A_act_1, status0_act = remove_status_0(A_act, n)    
    
    # calculate common neighbors    
    cn_p_act, cn_q_act = common_neighbors(A_act_1, n-status0_act, m)
       
    # calculate bipartite coefficients
    ATA_act = np.matmul(A_act.T, A_act) # p-nodes
    AAT_act = np.matmul(A_act, A_act.T) # q-nodes        
    p_CN_act = ATA_act[:n, :n]
    q_CN_act = AAT_act[n:, n:]
    
    p_out_degree_act = np.sum(A_act[n:, :n], axis=0)
    q_in_degree_act =  np.sum(A_act[n:, :n], axis=1)
    
    q_CB_act, hn_q_act = bipartite_coef(p_CN_act, q_N_act, p_out_degree_act)
    p_CB_act, hn_p_act = bipartite_coef(q_CN_act, p_N_act, q_in_degree_act)
    
    # count only nodes that have neighbors
    #cb_q_act = np.mean(q_CB_act) * m / hn_q_act
    #cb_p_act = np.mean(p_CB_act) * n / hn_p_act  
    
    # count all nodes
    cb_q_act = np.mean(q_CB_act) 
    cb_p_act = np.mean(p_CB_act) 
    
    # boxplots
    plt.figure()
    plt.hlines(cn_q_act, 0.5, 1.5)    
    plt.boxplot(cn_q)
    plt.ylabel('Average Number of Common Neighbors')
    plt.title('Average Number of Common Neighbors for q-nodes, N = {}'.format(N))  
    plt.legend(['True value'])
    
    plt.figure()
    plt.hlines(cn_p_act, 0.5, 1.5)    
    plt.boxplot(cn_p)
    plt.ylabel('Average Number of Common Neighbors')
    plt.title('Average Number of Common Neighbors for p-nodes, N = {}'.format(N))    
    plt.legend(['True value'])
    
    plt.figure()
    plt.hlines(cb_q_act, 0.5, 1.5)    
    plt.boxplot(cb_q)
    plt.ylabel('Average Bipartite Clustering Coefficient')
    plt.title('Average Bipartite Clustering Coefficient for q-nodes, N = {}'.format(N))
    plt.legend(['True value'])
    
    plt.figure()
    plt.hlines(cb_p_act, 0.5, 1.5)    
    plt.boxplot(cb_p)
    plt.ylabel('Average Bipartite Clustering Coefficient')
    plt.title('Average Bipartite Clustering Coefficient for p-nodes, N = {}'.format(N))    
    plt.legend(['True value'])
