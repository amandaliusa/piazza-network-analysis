import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pq_helper import get_dataframe

'''
Script for analysis of one-mode projections
Author: Amanda Li
'''

#----------------------------------------------------------------------
if __name__ == "__main__":
    
    path = 'acm95a100a2018_anonymized_modified.xlsx'
    (p_nodes, q_nodes, links, mod_p_nodes) = get_dataframe(path)    
    
    # get status=1 p-nodes only
    status1 = [] # include TAs and instructor
    status1_students = [] # exclude TAs and instructor
    for item in links['Start']:
        if (item[0] == 'P'):
            if (int(item[1:]) not in status1):
                status1.append(int(item[1:]))
            if (int(item[1:]) < 185) and (int(item[1:]) not in status1_students):
                status1_students.append(int(item[1:]))        
    for item in links['End']:
        if (item[0] == 'P'):
            if (int(item[1:]) not in status1):
                status1.append(int(item[1:]))
            if (int(item[1:]) < 185) and (int(item[1:]) not in status1_students):
                status1_students.append(int(item[1:]))    
    status1.sort()
    status1_students.sort()
    s = np.array(status1)
    ss = np.array(status1_students)
    
    # initialize empty adjacency matrices
    A = np.zeros((len(status1), len(status1))) 
    A_students = np.zeros((len(status1_students), len(status1_students)))
    l = 0 # count number of links in real network
    
    for i in range(len(links)):
        if links['Start'][i][0] == 'P':
            answerer = links['Start'][i]
            question = links['End'][i]
            c = np.where(links['Start'] == question)
            
            asker = links['End'][c[0][0]]
            ask_idx = np.where(s == int(asker[1:]))
            ans_idx = np.where(s == int(answerer[1:]))  
            
            # update adjacency matrix with students only
            if (int(asker[1:]) < 185) and (int(answerer[1:]) < 185):  
                l += 1
                ask_idx_s = np.where(ss == int(asker[1:]))
                ans_idx_s = np.where(ss == int(answerer[1:]))                
                A_students[int(ans_idx_s[0])][int(ask_idx_s[0])] = 1

            # update adjacency matrix with all p-nodes
            ask_idx = np.where(s == int(asker[1:]))
            ans_idx = np.where(s == int(answerer[1:]))
            A[int(ans_idx[0])][int(ask_idx[0])] = 1
    
    # create directed graphs from adjacency matrices
    G = nx.from_numpy_matrix(A, create_using=nx.DiGraph())
    G2 = nx.from_numpy_matrix(A_students, create_using=nx.DiGraph()) 
    
    # relabel nodes 
    new_labels = {}
    for i in range(len(status1)):
        p = 'P' + str(status1[i])
        new_labels[i] = p   
    nx.relabel_nodes(G, new_labels, copy=False)  
    
    new_labels_s = {}
    for i in range(len(status1_students)):
        p = 'P' + str(status1_students[i])
        new_labels_s[i] = p   
    nx.relabel_nodes(G2, new_labels_s, copy=False)    
    
    # adjust k to change how closely nodes are distributed in image: larger k = nodes 
    # more concentrated at outside of graph
    nodePos = nx.layout.spring_layout(G, k=0.6, iterations=20)    
    
    # color nodes in G by TA/instructor vs students
    node_color = {}
    for node in G.nodes():
        if int(node[1:]) > 184:
            node_color[node] = 'blue'
        else:
            node_color[node] = 'red'
    
    nx.set_node_attributes(G, node_color, 'color')   
    node_colors = ['blue', 'red']
    
    # plot graph with all p-nodes
    for color in node_colors:
        if color == 'blue':
            node_label = 'TA/instructor'
        else:
            node_label = 'student'
        nx.draw_networkx_nodes(G, nodePos, 
                               nodelist=[sNode[0] for sNode in filter(lambda x: x[1]['color']==color, G.nodes(data = True))],
                               node_size=25, node_color=color, label=node_label) 
        
    nx.draw_networkx_edges(G, nodePos)   
    plt.legend()
    plt.figure()
    # Use the following line to visualize the network with labeled p-nodes
    nx.draw_networkx(G, nodePos, node_size=25, font_size=10)  
    plt.title('One-Mode Projection of P-nodes (Including TAs/Instructor)')
    
    # plot graph with students only
    plt.figure()
    nx.draw_networkx(G2, nodePos, node_size=25, font_size=10, with_labels=False)  
    plt.title('One-Mode Projection of P-nodes (Excluding TAs/Instructor)')    
    
    # find cycles 
    cycles = list(nx.simple_cycles(G2))
    cycle_lengths = {}
    
    for cycle in cycles:
        if len(cycle) not in cycle_lengths:
            cycle_lengths[len(cycle)] = 1
        else:
            cycle_lengths[len(cycle)] += 1

    # find percentage of each cycle that is UG/Grad
    ugrad = []
    total = 0
    for cycle in cycles: 
        u = 0
        for node in cycle:
            idx = int(node[1:]) - 1
            if p_nodes.loc[idx]['Class'][0] == 'U':
                u += 1
        p = u / len(cycle) * 100
        ugrad.append(p)
        total += p
    avg = total / len(cycles)
      
    # find percentage of UG out of total students 
    ug = 0
    for idx in range(184):
        if p_nodes.loc[idx]['Class'][0] == 'U':
            ug += 1
    ug /= 1.84
    
    # find percentage of UG in status=1 students
    ug_1 = 0
    for i in status1_students:
        if p_nodes.loc[i-1]['Class'][0] == 'U':
            ug_1 += 1
    ug_1 /= len(status1_students)      
        
    plt.figure()
    plt.hist(ugrad, label='% UG in a cycle')
    plt.title('Percentage of Undergraduates in Each Cycle')
    plt.xlabel('Percentage of Undergraduates')
    plt.ylabel('Number of Cycles')
    plt.axvline(x=ug, label='% UG out of all students')
    #plt.axvline(x=ug_1*100 , label='% UG out of status=1 students')
    plt.legend()
            
    # look at standard deviation of N-scores within each cycle
    sds = []
    lengths = []
    for cycle in cycles: 
        n_scores = []
        lengths.append(len(cycle))
        for node in cycle:
            idx = int(node[1:]) - 1
            n_scores.append(p_nodes.loc[idx]['N-Score'])
        sd = np.std(n_scores)
        sds.append(sd)
        
    plt.figure()
    plt.hist(sds)
    plt.title('Standard Deviation of N-Scores in Each Cycle')
    plt.xlabel('SD of N-Score')
    plt.ylabel('Number of Cycles')
        
    plt.figure()
    plt.scatter(lengths, sds)
    plt.title('Standard Deviation of N-Score vs Cycle Length')
    plt.xlabel('Cycle Length')
    plt.ylabel('SD of N-Score')    
    
    # look at majors within cycles 
    eas = ['ACM', 'CS', 'ME', 'MS', 'AsPh', 'SE', 'EE', 'Eng', 'Ae', 'APh', 'MedE', 'Eng (CNS)', 'AM']
    non_eas = ['Ph', 'ChE (BM)', 'BE', 'ChE (MS)', 'ChE (PS)', 'PlSc', 'Ch', 'Bi', 'ChE (Env)', 'BMB', 'Ge', 'ChE']
    
    eas_majors = []
    total = 0
    for cycle in cycles: 
        u = 0
        for node in cycle:
            idx = int(node[1:]) - 1
            if p_nodes.loc[idx]['Option'] in eas:
                u += 1
        p = u / len(cycle) * 100
        eas_majors.append(p)
        total += p
    avg_eas = total / len(cycles)    
    
    # find percentage of EAS majors out of total students 
    num_eas = 0
    for idx in range(184):
        if p_nodes.loc[idx]['Option'] in eas:
            num_eas += 1
    num_eas /= 1.84
    
    # find percentage of EAS majors in status=1 students
    num_eas_1 = 0
    for i in status1_students:
        if p_nodes.loc[i-1]['Option'] in eas:
            num_eas_1 += 1
    num_eas_1 /= len(status1_students)    
    
    plt.figure()
    plt.hist(eas_majors, label='% EAS majors in a cycle')
    plt.axvline(x=num_eas, label='% EAS majors out of all students')
    #plt.axvline(x=num_eas_1*100 , label='% EAS majors out of status=1 students')    
    plt.title('Percentage of EAS Majors in Each Cycle')
    plt.xlabel('Percentage of EAS Majors')
    plt.ylabel('Number of Cycles')
    plt.legend()    
    
    