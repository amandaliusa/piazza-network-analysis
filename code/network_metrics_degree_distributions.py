import xlrd 
import matplotlib.pyplot as plt
import matplotlib.colorbar
import matplotlib.colors
import matplotlib.cm
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import chisquare
from math import factorial
from math import exp
from scipy.stats.distributions import chi2
from mpl_toolkits.axes_grid1 import make_axes_locatable
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

#----------------------------------------------------------------------
if __name__ == '__main__':
    path = 'acm95a100a2018_anonymized_modified.xlsx'
    (p_nodes, q_nodes, links, mod_p_nodes) = get_dataframe(path)
        
    # list of p-nodes out-degrees (students only)
    p_node_out = np.sort(mod_p_nodes['Out-Degree'].value_counts().index)
    
    # list of p-nodes in-degrees (students only; note that instructors should 
    # all have in-degrees of zero, since they don't ask questions)
    p_node_in = np.sort(mod_p_nodes['In-Degree'].value_counts().index)   
    
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
    status1_in = mod_p_nodes[:184].loc[mod_p_nodes[:184]['Status'] == 1]['In-Degree']
    
    #plt.hist(status1_in, bins=20, range=(0, 20))
    #plt.xlabel('P-Node In-Degree')
    #plt.ylabel('Number of Students')
    #plt.title('Histogram of P-Node In-Degrees')
    
    # list of in-degrees of status=1 p-nodes (including TAs and instructor) 
    status1_in_all = p_nodes.loc[p_nodes['Status'] == 1]['In-Degree']    
    
    #plt.hist(status1_in_all, bins=20, range=(0, 20))
    #plt.xlabel('P-Node In-Degree')
    #plt.ylabel('Number of P-Nodes')
    #plt.title('Histogram of P-Node In-Degrees')   
    
    # list of out-degrees of status=1 p-nodes (students only) 
    status1_out = mod_p_nodes[:184].loc[mod_p_nodes[:184]['Status'] == 1]['Out-Degree']  
    
    #plt.hist(status1_out, bins=20, range=(0, 20))
    #plt.xlabel('P-Node Out-Degree')
    #plt.ylabel('Number of Students')
    #plt.title('Histogram of P-Node Out-Degrees')  
    
    # list of out-degrees of status=1 p-nodes (including TAs and instructor) 
    status1_out_all = p_nodes.loc[p_nodes['Status'] == 1]['Out-Degree']    
    
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
