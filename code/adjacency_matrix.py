import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''
Script for constructing adjacency matrix for the pq network
Author: Siqiao Mu
'''

xl = pd.ExcelFile("acm95a100a2018_anonymized.xlsx")
df = xl.parse("Links")
df = df.apply(pd.to_numeric, errors='ignore')

p_node_list = [] #list of status=1 p-nodes
for item in df['Start']:
    if (item[0] == 'P') and (item not in p_node_list):
        p_node_list.append(item)
for item in df['End']:
    if (item[0] == 'P') and (item not in p_node_list):
        p_node_list.append(item)

p_node_list = np.asarray(p_node_list)
     
Np = len(p_node_list)
Nq = 241

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

np.savetxt("adjacency_matrix.csv", adjacency_matrix, delimiter=",")