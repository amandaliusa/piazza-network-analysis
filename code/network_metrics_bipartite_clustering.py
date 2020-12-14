import xlrd 
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
from plfit import plfit
from pq_helper import bipartite_coef, get_dataframe, neighbors

'''
Script for analysis of bipartite clustering within pq network
Author: Amanda Li
'''
     
#----------------------------------------------------------------------
if __name__ == "__main__":
    path = "acm95a100a2018_anonymized_modified.xlsx"
    (p_nodes, q_nodes, links, mod_p_nodes) = get_dataframe(path)
    
    # Notice that status=0 p-nodes do not contribute to the average bipartite 
    # coefficients, since they have no neighbors. Furthermore, p-nodes that only
    # asked but did not answer questions also do not contribute to the average 
    # bipartite coefficients, since we only say that a p-node i and a q-node alpha are 
    # neighbors if there exists a link i --> alpha. We take these factors into account
    # when computing the average bipartite coefficient by scaling accordingly (see below).
    
    n = len(p_nodes)
    m = len(q_nodes)
    
    A = np.loadtxt(open("adjacency_matrix_all.csv", "rb"), delimiter=",")     
    
    # get neighbors
    p_N, q_N = neighbors(A, n, m)  
    
    # get common neighbors
    ATA = np.matmul(A.T, A) # p-nodes
    AAT = np.matmul(A, A.T) # q-nodes        
    p_CN = ATA[:n, :n]
    q_CN = AAT[n:, n:]    
        
    # bipartite clustering coefficients of q-nodes    
    q_CB, hn_q = bipartite_coef(p_CN, q_N, p_nodes['Out-Degree'])    
    average_q_CB_all = np.mean(q_CB)  
    average_q_CB = np.mean(q_CB) * 241 / hn_q # one q-node was not answered
    
    # bipartite clustering coefficients of p-nodes    
    p_CB, hn_p = bipartite_coef(q_CN, p_N, q_nodes['In-Degree'])    
    average_p_CB_all = np.mean(p_CB) # with all p-nodes
    average_p_CB = average_p_CB_all * 196 / hn_p # counting p-nodes with neighbors only
    
    
    