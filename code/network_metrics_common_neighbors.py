import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chisquare
from scipy.stats import poisson

'''
Script for analysis of common neighbors
Author: Siqiao Mu
'''

xl = pd.ExcelFile("acm95a100a2018_anonymized_modified.xlsx")
df = xl.parse("Links")
df = df.apply(pd.to_numeric, errors='ignore')
df['End is Q or P'] = [item[0] for item in df['End']]

N = 196

#Analysis of common neighbors of p-nodes
Q_df = df.loc[df['End is Q or P'] == 'Q'] #contains only people answering particular questions

p_node_list = []
for i in range(1, N + 1):
    p_node_list.append('P' + str(i))

CN_matrix = np.zeros((N, N))

Q_list = ['Q' + str(i) for i in range(1, 241 + 1)] #list of questions

for Q0 in Q_list: #iterating through questions
    new_df = Q_df.loc[Q_df['End'] == Q0] #selecting the set of people answering a particular question
    plst = np.array(new_df['Start']) #list of people answering that question
    if len(plst) > 1:#ignoring cases where only one person answered a question
        for i in range(len(plst)): 
            for j in range(i + 1, len(plst)): 
                P1 = plst[i]
                P2 = plst[j]
                m = p_node_list.index(P1)
                n = p_node_list.index(P2)
                CN_matrix[m, n] += 1
                CN_matrix[n, m] += 1
                
iu1 = np.triu_indices(n = N, m = N, k = 1)#upper triangular section (not including diagonal)

average_cn = np.mean(CN_matrix[iu1])

f_obs = np.bincount(CN_matrix[iu1].astype(int))

def poisson_expected_frequency(N, a, b): #N is number of observations, a is range of values tested) 
    f = []
    for i in range(a, b):
        n = int(poisson.pmf(i, average_cn) * N)
        f.append(n)
    nfinal = int((1 - poisson.cdf(b, average_cn)) * N)
    f.append(nfinal)
    return np.array(f)

f_exp = poisson_expected_frequency(len(CN_matrix[iu1]), 0, 7)
            
#chisquare(f_obs, f_exp + 1) 

plt.hist(CN_matrix[iu1], range=(0, 8))
plt.title('Distribution of Common Neighbors for p-nodes')
plt.xlabel('Common Neighbors')
plt.show()

plt.hist(CN_matrix[iu1], range=(1, 8))
plt.title('Distribution of Common Neighbors for p-nodes (excluding 0)')
plt.xlabel('Common Neighbors')
plt.show()


