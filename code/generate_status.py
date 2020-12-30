import xlrd 
import pandas as pd

from pq_helper import get_dataframe

'''
Script for assigning participation status to each p-node
Author: Amanda Li
'''  

#----------------------------------------------------------------------
if __name__ == "__main__":
    path = "acm95a100a2018_anonymized_modified.xlsx"
    (p_nodes, q_nodes, links, mod_p_nodes) = get_dataframe(path)

    # new column in dataframe for holding status 
    mod_p_nodes['S'] = [0] * 196

    for item in links['Start']:
        if item[0] == 'P': # p-nodes only
            mod_p_nodes['S'][int(item[1:]) - 1] = 1
        
    for item in links['End']:
        if item[0] == 'P': # p-nodes only
            mod_p_nodes['S'][int(item[1:]) - 1] = 1  