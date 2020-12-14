import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''
This file is identical to adjacency_matrix.py written by Siqiao Mu, except it includes
all p-nodes, not just status=1 p-nodes. 

Modified by: Amanda Li
'''

xl = pd.ExcelFile("acm95a100a2018_anonymized_modified.xlsx")
df = xl.parse("Links")
df = df.apply(pd.to_numeric, errors='ignore')

Np = 196
Nq = 241
p_node_list = ['P' + str(i) for i in range(1, Np + 1)] #list of questions
p_node_list = np.asarray(p_node_list)
q_node_list = ['Q' + str(i) for i in range(1, Nq + 1)] #list of questions
q_node_list = np.asarray(q_node_list)

adjacency_matrix = np.zeros((Np + Nq, Np + Nq)) #constructing adjacency matrix for directed graph, where arrows point from answerer to question and question to asker (column to row)
for index, row in df.iterrows():
    if row['Start'][0] == 'Q': #this kind of row is question asked by person
        i = np.where(p_node_list == row['End'])[0]
        alpha = np.where(q_node_list == row['Start'])[0] + Np
        adjacency_matrix[i, alpha] = 1 #this matrix is asymmetric because it is a directed graph
    if row['Start'][0] == 'P': #this kind of row is person answering question
        i = np.where(p_node_list == row['Start'])[0]
        alpha = np.where(q_node_list == row['End'])[0] + Np       
        adjacency_matrix[alpha, i] = 1

np.savetxt("adjacency_matrix_all.csv", adjacency_matrix, delimiter=",")