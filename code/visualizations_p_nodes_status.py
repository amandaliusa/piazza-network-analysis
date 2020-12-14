import xlrd 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

'''
Script for visualizing pq network based on p-node status
Author: Amanda Li
'''

def get_dataframe(path):
    book = pd.ExcelFile(path)
    p_nodes = book.parse('P-Nodes')
    q_nodes = book.parse('Q-Nodes')
    links = book.parse('Links')
    mod_p_nodes = book.parse('P-Nodes-Modified')
    return (p_nodes, q_nodes, links, mod_p_nodes)     

def annotated_bar_chart(x_axis, y_axis, labels, shift, x_label, y_label, title):
    index = np.arange(len(x_axis))
    plt.figure()
    y = pd.Series.from_array(y_axis)
    ax = y.plot(kind='bar')
    plt.xlabel('%s' % x_label, fontsize=10)
    plt.ylabel('%s' % y_label, fontsize=10)
    plt.xticks(index, x_axis, fontsize=10, rotation=0)
    plt.yticks(fontsize=10)
    plt.title('%s' % title)
    counter = 0
    for i in ax.patches:
        ax.text(i.get_x() + i.get_width() * shift, i.get_height(), 
                labels[counter])
        counter += 1
    plt.show() 

#----------------------------------------------------------------------
if __name__ == "__main__":
    path = "acm95a100a2018_anonymized_modified.xlsx"
    (p_nodes, q_nodes, links, mod_p_nodes) = get_dataframe(path)
    
    options = ['ACM', 'AM', 'APh', 'Ae', 'AsPh', 'BE', 'BMB', 'Bi', 'CS', 'Ch', 
               'ChE', 'ChE (BM)', 'ChE (Env)', 'ChE (MS)', 'ChE (PS)', 'EE', 
               'Eng', 'Eng (CNS)', 'Ge', 'ME', 'MS', 'MedE', 'Ph', 'PlSc', 'SE']
    combined_options = ['ACM', 'AM', 'APh', 'Ae', 'AsPh', 'BE', 'BMB', 'Bi', 
                        'CS', 'Ch', 'ChE', 'EE', 'Eng', 'Ge', 'ME', 'MS', 
                        'MedE', 'Ph', 'PlSc', 'SE']    
    classes = ['U2', 'U3', 'U4', 'G1', 'G2', 'G5']   
    grades = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+']  
    combined_grades = ['A', 'B', 'C', 'D']
    levels = ['Undergraduate', 'Graduate']

    # B.2 
    # Use the following two lines to see the number of students from each class 
    # with Status=1: 
    #df = pd.crosstab(p_nodes['Class'], p_nodes['Status'])
    #print(df)
    
    #class_statuses = [44, 16, 4, 25, 1, 1]     
    # Note: percentages refer to percentage of students within a class that 
    # have status 1, not percentage of total students with status 1 that fall
    # within a class.
    #percentages = ['52.4%', '41.0%', '100%', '46.3%', ' 50%', '100%']
    
    # The same plot, combining Undergrads and Grads:
    #annotated_bar_chart(classes, class_statuses, percentages, 0, 'Classes', 
    #          'Number of students', 
    #          'Distribution of Students with Status=1') 
    
    #level_statuses = [64, 27] 
    #percentages = ['50.4%', '47.4%']
    
    #annotated_bar_chart(levels, level_statuses, percentages, 1/3, '', 
    #          'Number of students', 
    #          'Distribution of Students with Status=1')     
    
    # B.3 
    # Use the following two lines to see the number of students from each option 
    # (combined) with Status=1: 
    #df = pd.crosstab(mod_p_nodes['Option'], mod_p_nodes['Status'])
    #print(df)           
    #option_statuses = [7, 0, 2, 5, 3, 4, 1, 1, 2, 0, 9, 14, 3, 1, 11, 1, 3,
    #                   16, 0, 8] 
    #percentages = ['100%', '', '50%', '83.3%', '42.9%', '57.1%', '100%', '100%',
    #               '66.7%', '', '69.2%', '40%', '75%', '100%', '40.7%', '10%',
    #               '50%', '44.4%', '', '72.7%']
   
    #annotated_bar_chart(combined_options, option_statuses, percentages, 0, 
    #                    'Option', 'Number of students', 
    #                    'Distribution of Students with Status=1') 
    
    # Use the following two lines to see the number of students from each option 
    # with Status=1:     
    #df = pd.crosstab(p_nodes['Option'], mod_p_nodes['Status'])
    #print(df)           
    #option_statuses = [7, 0, 2, 5, 3, 4, 1, 1, 2, 0, 2, 2, 2, 1, 2, 14, 1, 2, 1, 
    #                   11, 1, 3, 16, 0, 8] 
    #percentages = ['100%', '', '50%', '83.3%', '42.9%', '57.1%', '100%', '100%',
    #               '66.7%', '', '100%', '50%', '100%', '50%', '66.7%', '40%', 
    #               '100%', '66.7%', '100%', '40.7%', '10%', '50%', '44.4%', '', 
    #               '72.7%']
    
    #annotated_bar_chart(options, option_statuses, percentages, 0, 
    #                    'Option', 'Number of students', 
    #                    'Distribution of Students with Status=1')      
    
    # B.5
    # Use the following two lines to see the number of students with each 
    # grade (A-D) with Status=1: 
    #df = pd.crosstab(mod_p_nodes['Grade'], mod_p_nodes['Status'])
    #print(df)    
    #grade_statuses = [83, 5, 2, 1] 
    #percentages = ['56.5%', '17.3%', '28.6%', '100%']
    
    #annotated_bar_chart(combined_grades, grade_statuses, percentages, 1/5, 
    #                    'Grade', 'Number of students', 
    #                    'Distribution of Students with Status=1')  
    
    # Use the following two lines to see the number of students with each 
    # grade (A+-D+) with Status=1: 
    #df = pd.crosstab(p_nodes['Grade'], mod_p_nodes['Status'])
    #print(df)      
    #grade_statuses = [37, 33, 13, 2, 1, 2, 1, 1, 0, 1] 
    #percentages = ['69.8%', '51.6%', '43.3%', '13.3%', '14.3%', '28.6%', '50%', 
    #               '33.3%', '', '100%']
    
    #annotated_bar_chart(grades, grade_statuses, percentages, -0.1, 
    #                    'Grade', 'Number of students', 
    #                    'Distribution of Students with Status=1')     
    