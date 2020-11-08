import pandas as pd
import numpy as np

def get_dataframe(path):
    '''
    Takes the path to the spreadsheet file of anonymized data and reads the file as a dataframe. 
    Returns a dataframe for each sheet of the spreadsheet.
    
    Input:
    path: path to file to be read
    
    Outputs:
    p_nodes: dataframe corresponding to 'P_nodes' sheet
    q_nodes: dataframe corresponding to 'Q_nodes' sheet
    links: dataframe corresponding to 'Links' sheet
    mod_p_nodes: dataframe corresponding to 'P-Nodes-Modified' sheet
    '''
    
    book = pd.ExcelFile(path)
    p_nodes = book.parse('P-Nodes')
    q_nodes = book.parse('Q-Nodes')
    links = book.parse('Links')
    mod_p_nodes = book.parse('P-Nodes-Modified')
    return (p_nodes, q_nodes, links, mod_p_nodes) 

def neighbors(A, n, m):
    '''
    Takes an adjacency matrix and its number of p-nodes and q-nodes and determines the
    neighbors of all p-nodes and q-nodes.
    
    Inputs:
    A: (n+m, n+m) adjacency matrix with first n rows and columns corresponding to p-nodes 
    and last m rows and columns corresponding to q-nodes
    n: number of p-nodes
    m: number of q-nodes
    
    Outputs:
    p_N: a length n array of lists containing the ID numbers of the q-nodes that are
    neighbors to each p-node
    q_N: a length m array of lists containing the ID numbers of the p-nodes that are
    neighbors to each q-node
    '''
    
    p_N = [[] for i in range(n)]
    q_N = [[] for i in range(m)]
    
    # use 1-indexing to be consistent with previous work on bipartite clustering
    for i in range(1, n+1):
        for alpha in range(1, m+1): 
            # a p-node i and a q-node alpha are neighbors if i --> alpha
            if A[n+alpha-1][i-1] == 1: 
                p_N[i-1].append(alpha)
                q_N[alpha-1].append(i)
                
    return p_N, q_N

def bipartite_coef(CN, N, df):
    '''
    Calculates the bipartite clustering coefficients for either p-nodes or q-nodes, 
    as well as the number of the other type of node that has neighbors. 
    
    Inputs:
    CN: matrix of common neighbors for p-nodes (q-nodes)
    N: array containing neighbors of q-nodes (p-nodes)
    df: array of either p-node out-degrees (q-node in-degrees)
    
    Outputs:
    CB: array containing bipartite clustering coefficients for p-nodes (q-nodes)
    have_neighbors: number of q-nodes (p-nodes) that have neighbors
    '''
    
    # bipartite clustering coefficients     
    CB = [] 
    have_neighbors = 0

    # iterate through all nodes 
    for x in range(0, len(N)): 
        numerator = 0
        denominator = 0
        
        if len(N[x]) != 0:
            have_neighbors += 1
        
        # iterate through neighbors of the node
        for i in N[x]:
            for j in N[x]:
                if i != j:
                    numerator += CN[i - 1][j - 1] - 1
                    denominator += df[i - 1] + df[j - 1] - CN[i - 1][j - 1] - 1   
                    
        if denominator == 0:
            CB.append(0)
        else:
            CB.append(numerator / denominator) 

    return CB, have_neighbors

def remove_status_0(A, n):
    '''
    Takes an adjacency matrix and returns a modified adjacency matrix without rows and columns
    corresponding to status=0 p-nodes.
    
    Input: 
    A: (n+m, n+m) adjacency matrix with first n rows and columns corresponding to p-nodes and 
    last m rows and columns corresponding to q-nodes
    n: number of p-nodes
    
    Output:
    A_new: adjacency matrix without rows and columns corresponding to status=0 p-nodes
    status0: number of status=0 p-nodes removed
    
    '''
    
    delete = []
    A1 = A[:n, n:]
    rows = np.sum(A1, axis=1)
    A2 = A[n:, :n]
    cols = np.sum(A2, axis=0)
    status0 = 0
    
    # identify indices of status=0 p-nodes
    for i in range(n):
        if rows[i] == 0 and cols[i] == 0:
            delete.append(i)
            status0 += 1
    
    # remove rows and columns associated with status=0 p-nodes
    A_new = np.delete(A, delete, 0)
    A_new = np.delete(A_new, delete, 1)
    
    return A_new, status0

def common_neighbors(A, n, m):
    '''
    Takes an adjacency matrix and returns the average number of common neighbors between 
    each pair of p-nodes and each pair of q-nodes, respectively.
    
    Inputs:
    A: (n+m, n+m) adjacency matrix with first n rows/columns representing p-nodes and 
    last m rows/columns representing q-nodes
    n: number of p-nodes
    m: number of q-nodes
    
    Outputs:
    cn_p: average number of common neighbors for each pair of p-nodes
    cn_q: average number of common neighbors for each pair of q-nodes
    '''
    
    # p-nodes
    ATA = np.matmul(A.T, A) 
    iu1 = np.triu_indices(n=n, k=1) # upper triangular section (not including diagonal)
    cn_p = np.mean(ATA[iu1]) 
    
    # q-nodes
    AAT = np.matmul(A, A.T) 
    iu2 = np.triu_indices(n=m, k=1) # upper triangular section (not including diagonal)
    cn_q = np.mean(AAT[iu2]) 
    
    return cn_p, cn_q