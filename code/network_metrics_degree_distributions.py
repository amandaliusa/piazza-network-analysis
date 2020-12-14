import xlrd 
import matplotlib.pyplot as plt
import matplotlib.colorbar
import matplotlib.colors
import matplotlib.cm
import numpy as np
import pandas as pd
import seaborn as sns
import powerlaw as pl
from scipy.stats import chisquare
from math import factorial
from math import exp
from scipy.stats.distributions import chi2
from mpl_toolkits.axes_grid1 import make_axes_locatable
from plfit import plfit
from collections import Counter
from pq_helper import get_dataframe

'''
Script for analysis of degree distributions within pq network
Author: Amanda Li
'''
    
def chi_squared_test(observed, mu, total):
    expected = []
    sum = 0
    for value in range(len(observed) - 1): 
        expected.append(total * (exp(-mu) * mu**value / factorial(value)))
        sum += total * (exp(-mu) * mu**value / factorial(value))
    expected.append(total - sum)
    (testStatistic, pValue) = chisquare(observed, f_exp=expected, 
                                        ddof=len(observed) - 1)  
    # note: the p-value returned by the chisquare function seems to be 
    # incorrect for the test statistic; I verified the return value of chi2.sf 
    # with both online tables of chi-squared value as well as Mathematica and 
    # MATLAB
    p = chi2.sf(testStatistic, len(observed) - 1)
    return (testStatistic, p)

def color_by_nscore(Outdegree, Indegree, NScore):
    df = pd.DataFrame(dict(Outdegree=Outdegree, Indegree=Indegree, 
                           NScore=NScore))     
    cmap = plt.cm.get_cmap('RdYlBu') 
    
    # Normalize to the range of possible values from NScore
    norm = matplotlib.colors.Normalize(vmin=NScore.min(), vmax=NScore.max())
    
    # create a color dictionary  
    colors = {}
    for cval in NScore:
        colors.update({cval : cmap(norm(cval))})
    
    fig = plt.figure(figsize=(20,5))
    #fig = plt.figure(figsize=(200,5)) # use for zoomed view of outdegree 0
    #fig = plt.figure(figsize=(50,5)) # use for zoomed view of outdegree 1        
    m = sns.swarmplot(Outdegree, Indegree, hue=NScore, palette = colors)
    plt.gca().legend_.remove()
    plt.title('In-Degree vs Out-Degree of P-Nodes') 
    
    divider = make_axes_locatable(plt.gca())
    ax_cb = divider.new_horizontal(size="5%", pad=0.05)
    fig.add_axes(ax_cb)
    clb = matplotlib.colorbar.ColorbarBase(ax_cb, cmap=cmap, norm=norm)
    clb.set_label('N-Score')
    plt.show()     
    
def avg_degree(sheet, total):
    Outdegree = sheet['Out-Degree']
    Indegree = sheet['In-Degree']  
    total_out = 0
    total_in = 0
    counter = 0
    
    for i in range(total):
        if sheet['Status'][i] == 1:
            total_out += Outdegree[i]
            counter += 1
        
    for i in range(total):
        if sheet['Status'][i] == 1:
            total_in += Indegree[i]
            
    # average outdegree of status 1 p-nodes
    avg_out = total_out / counter
    
    # average indegree of status 1 p-nodes
    avg_in = total_in / counter 
    
    return (avg_in, avg_out)
#----------------------------------------------------------------------
if __name__ == '__main__':
    path = 'acm95a100a2018_anonymized_modified.xlsx'
    (p_nodes, q_nodes, links, mod_p_nodes) = get_dataframe(path)
    
    # To get out-degrees: 
    out = links["Start"].value_counts()
    #print(out) # doesn't show all the rows, so use the below instead.
    nodes = links["Start"].value_counts().index
    #for node in nodes:
    #    print(node, out.loc[node])
        
    # list of p-nodes out-degrees (students only)
    p_node_out = [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 17, 18, 20]
        
    # To get in-degrees: 
    ins = links["End"].value_counts()
    #print(ins) # doesn't show all the rows, so use the below instead.
    nodes = links["End"].value_counts().index
    #for node in nodes:
    #    print(node, ins.loc[node]) 
    
    # list of p-nodes in-degrees (students only; note that instructors should 
    # all have in-degrees of zero, since they don't ask questions)
    p_node_in = [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 13, 14, 18, 20]    
    
    # 1. 
    avg_p_in = [] # holds average in-degree of p-nodes with each out-degree 
    avg_n_score = [] # holds average n-score of p-nodes with each out-degree
    for x in p_node_out: 
        total_in = 0
        total_n = 0
        number = 0 
        for i in range(184):
            if mod_p_nodes['Out-Degree'][i] == x:
                total_in += mod_p_nodes['In-Degree'][i]
                number += 1
                total_n += mod_p_nodes['N-Score'][i]
        avg_p_in.append(total_in / number)  
        avg_n_score.append(total_n / number)
        
    #plt.scatter(p_node_out, avg_p_in, c=avg_n_score, cmap='Greens')
    #c = plt.colorbar()
    #c.set_label('Average N-Score')
    #plt.plot(p_node_out, avg_p_in)
    #plt.xlabel('P-Node Out-Degree')
    #plt.ylabel('Average P-Node In-Degree')
    #plt.title('Average In-Degree of P-Nodes for each Out-Degree')
    
    avg_p_out = [] # holds average out-degree of p-nodes with each in-degree 
    avg_n_score2 = [] # holds average n-score of p-nodes with each in-degree
    for x in p_node_in: 
        total_out = 0
        total_n2 = 0
        number2 = 0 
        for i in range(184):
            if mod_p_nodes['In-Degree'][i] == x:
                total_out += mod_p_nodes['Out-Degree'][i]
                number2 += 1
                total_n2 += mod_p_nodes['N-Score'][i]
        avg_p_out.append(total_out / number2)  
        avg_n_score2.append(total_n2 / number2)
        
    #plt.scatter(p_node_in, avg_p_out, c=avg_n_score2, cmap='Greens')
    #c = plt.colorbar()
    #c.set_label('Average N-Score')
    #plt.plot(p_node_in, avg_p_out)
    #plt.xlabel('P-Node In-Degree')
    #plt.ylabel('Average P-Node Out-Degree')
    #plt.title('Average Out-Degree of P-Nodes for each In-Degree')    
    
    # 2.a
    
    # list of in-degrees of status=1 p-nodes (students only) 
    status1_in = []
    for i in range(184):
        if mod_p_nodes['Status'][i] == 1:
            status1_in.append(mod_p_nodes['In-Degree'][i])
    
    #plt.hist(status1_in, bins=20, range=(0, 20))
    #plt.xlabel('P-Node In-Degree')
    #plt.ylabel('Number of Students')
    #plt.title('Histogram of P-Node In-Degrees')
    
    # list of in-degrees of status=1 p-nodes (including TAs and instructor) 
    status1_in_all = []
    for i in range(196):
        if p_nodes['Status'][i] == 1:
            status1_in_all.append(p_nodes['In-Degree'][i])    
    
    #plt.hist(status1_in_all, bins=20, range=(0, 20))
    #plt.xlabel('P-Node In-Degree')
    #plt.ylabel('Number of P-Nodes')
    #plt.title('Histogram of P-Node In-Degrees')   
    
    # list of out-degrees of status=1 p-nodes (students only) 
    status1_out = []
    for i in range(184):
        if mod_p_nodes['Status'][i] == 1:
            status1_out.append(mod_p_nodes['Out-Degree'][i])    
    
    #plt.hist(status1_out, bins=20, range=(0, 20))
    #plt.xlabel('P-Node Out-Degree')
    #plt.ylabel('Number of Students')
    #plt.title('Histogram of P-Node Out-Degrees')  
    
    # list of out-degrees of status=1 p-nodes (including TAs and instructor) 
    status1_out_all = []
    for i in range(196):
        if p_nodes['Status'][i] == 1:
            status1_out_all.append(p_nodes['Out-Degree'][i])      
    
    #plt.hist(status1_out_all, bins=20, range=(0, 125))
    #plt.xlabel('P-Node Out-Degree')
    #plt.ylabel('Number of P-Nodes')
    #plt.title('Histogram of P-Node Out-Degrees')      
    
    #plt.hist(q_nodes['In-Degree'], bins=6, range=(0, 6))
    #plt.xlabel('Q-Node In-Degree')
    #plt.ylabel('Number of Q-Nodes')
    #plt.title('Histogram of Q-Node In-Degrees')    
    
    # 2.c Chi-squared tests
    # I have used the population mean of each dataset as the parameter mu in 
    # the Poisson distribution. The expected frequencies are calculated with 
    # e^(-mu) * mu^k / k!, where k is the bin value.
    
    # average p-node in-degree (all): 2.5
    # use Counter(status1_in_all) to see the number of values in 
    # each bin. The bins are as follows: 0, 1, 2, 3, 4, 5+ (I combined all 
    # values of 5+ to ensure that bin size remained greater than 5). 
    # There are 6 - 1 - 0 = 5 degrees of freedom, since we have 6 bins and no
    # estimated parameters
    (testStatistic1, pValue1) = chi_squared_test([31, 24, 14, 5, 9, 13], 
                                               2.5, 196)
    
    # average p-node out-degree (all): 4.479166666666667    
    # use Counter(status1_out_all) to see the number of values in 
    # each bin. The bins are as follows: 0, 1, 2, 3, 4, 5, 6, 7+       
    (testStatistic2, pValue2) = chi_squared_test([28, 23, 10, 6, 4, 5, 8, 12], 
                                               4.479166666666667 , 196)    
    
    # average p-node in-degree (students): 2.6373626373626373
    # use Counter(status1_in) to see the number of values in 
    # each bin. The bins are as follows: 0, 1, 2, 3, 4, 5+     
    
    (testStatistic3, pValue3) = chi_squared_test([26, 24, 14, 5, 9, 13], 
                                               2.6373626373626373, 184)   
    
    # average p-node out-degree (students): 2.89010989010989
    # use Counter(status1_out) to see the number of values 
    # in each bin. The bins are as follows: 0, 1, 2, 3, 4, 5+     
    
    (testStatistic4, pValue4) = chi_squared_test([28, 20, 10, 6, 4, 5, 8, 10], 
                                               2.89010989010989, 184)       
    
    # average q-node in-degree: 1.780083
    # use q_nodes['In-Degree'].value_counts() to see the number of values 
    # in each bin. The bins are as follows: 0-1, 2, 3, 4, 5+     
    
    observed = [128, 60, 35, 13, 5]
    expected = []
    total = 241
    mu = 1.780083
    sum = 0
    expected.append(total * (exp(-mu) + exp(-mu) * mu))
    sum += total * (exp(-mu) + exp(-mu) * mu)  
    for value in range(2, 5): 
        expected.append(total * (exp(-mu) * mu**value / factorial(value)))
        sum += total * (exp(-mu) * mu**value / factorial(value))
    expected.append(total - sum)
    (testStatistic5, p5) = chisquare(observed, f_exp=expected, ddof=4)    
    pValue5 = chi2.sf(testStatistic5, 4)
    
    # 2c - Status 1 nodes only - average in- and out-degrees 
    # Students only - not including TAs and instructor
    (avg_in, avg_out) = avg_degree(mod_p_nodes, 184)
        
    # including TAs and instructor
    (avg_in2, avg_out2) = avg_degree(p_nodes, 196)    