import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''
Script for analysis of common neighbors
Author: Siqiao Mu
'''

xl = pd.ExcelFile("acm95a100a2018_anonymized.xlsx")
df = xl.parse("Links")
df = df.apply(pd.to_numeric, errors='ignore')

p_node_list = [] #list of status=1 p-nodes!!!
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

adjacency_matrix = np.loadtxt(open("adjacency_matrix.csv", "rb"), delimiter=",")

AtA = np.dot(np.transpose(adjacency_matrix), adjacency_matrix) #common neighbors matrix for p-nodes
iu1 = np.triu_indices(n = Np, m = Np, k = 1)#upper triangular section (not including diagonal)
p_data = AtA[iu1] # all pairings
#0.06535087719298245

#fig = plt.figure()
#plt.hist(p_data, range=(0, 8))
#plt.title('Distribution of Common Neighbors for p-nodes')
#plt.xlabel('Common Neighbors')
##plt.show()
#fig.savefig('2. Histogram of common neighbors for p-nodes.png')

AAt = np.dot(adjacency_matrix, np.transpose(adjacency_matrix)) #common neighbors matrix for q-nodes
CN_q_matrix = AAt[Np:, Np:,]
iu1 = np.triu_indices(n = Nq, m = Nq, k = 1)#upper triangular section (not including diagonal)
q_data = CN_q_matrix[iu1] #all pairings
#mean 0.3261410788381743

#fig = plt.figure()
#plt.hist(q_data, range=(0, 5))
#plt.title('Distribution of Common Neighbors for q-nodes')
#plt.xlabel('Common Neighbors')
#plt.show()
#fig.savefig('5. Histogram of common neighbors for q-nodes.png')

#looking at whether having the same option means having different amounts of common neighbors
new_df = xl.parse("P-Nodes")
new_df = new_df.apply(pd.to_numeric, errors='ignore')

new_df = new_df[new_df['Role'] == 'Student'][['ID', 'Option']]

option_matrix = np.zeros((Np, Np))

status_1_students = [i in new_df['ID'] for i in p_node_list]

for i in range(Np):
    for j in range(Np):
        if p_node_list[i] in status_1_students and p_node_list[j] in status_1_students:
            if new_df[new_df['ID'] == p_node_list[i]]['Option'].iloc[0] == new_df[new_df['ID'] == p_node_list[j]]['Option'].iloc[0]:
                option_matrix[i, j] = 1
                option_matrix[j, i] = 1