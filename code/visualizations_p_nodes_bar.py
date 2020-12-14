import xlrd 
import matplotlib.pyplot as plt
import numpy as np
import scipy.sparse as sps
from scipy.sparse import csr_matrix 
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

'''
Script for visualizing pq network via bar charts
Author: Amanda Li
'''

def get_dataframe(path):
    book = pd.ExcelFile(path)
    p_nodes = book.parse('P-Nodes')
    q_nodes = book.parse('Q-Nodes')
    links = book.parse('Links')
    mod_p_nodes = book.parse('P-Nodes-Modified')
    return (p_nodes, q_nodes, links, mod_p_nodes)     

def bar_chart(x_axis, y_axis, x_label, y_label, title):
    index = np.arange(len(x_axis))
    plt.bar(index, y_axis)
    plt.xlabel('%s' % x_label, fontsize=10)
    plt.ylabel('%s' % y_label, fontsize=10)
    plt.xticks(index, x_axis, fontsize=10, rotation=0)    
    plt.title('%s' % title)
    plt.show() 
    
def stacked_bar_chart(sheet, x_label, y_label, title, normal):
    df = pd.crosstab(sheet[x_label], sheet[y_label], normalize=normal)
    df.plot(kind='bar', stacked=True, fontsize=20)
    plt.title('%s' % title, fontsize=25)   
    plt.xticks(rotation=0, fontsize=20)        
    if normal == False: 
        plt.ylabel('Number of Students', fontsize=20)
    else:
        plt.ylabel('Fraction of Students', fontsize=20)
    plt.legend( loc = 'upper right', fancybox=True, framealpha=0.5)
    plt.show()  

def matrix(row_label, col_label, data_label, row_list, col_list, title, r, c):
    x = p_nodes.groupby([row_label, col_label]).mean()   
    row = []
    for j in range(len(c)):
        row.append(row_list.index(r[j]))
    row = np.array(row)
    col = []
    for i in range(len(c)):
        col.append(col_list.index(c[i]))
    col = np.array(col)
    data = [] 
    for i in range(len(c)):
        data.append(x[data_label][i])
    data = np.array(data)
    
    avg_views = csr_matrix((data, (row, col)), 
                           shape=(len(row_list), len(col_list))).toarray()
    plt.imshow(avg_views, cmap='Blues')
    plt.title(title)
    plt.xticks(np.arange(len(col_list)), col_list, rotation=90)    
    plt.yticks(np.arange(len(row_list)), row_list)
    clb = plt.colorbar(cmap=plt.cm.get_cmap('Blues'))
    plt.xlabel(col_label)
    plt.ylabel(row_label)
    clb.set_label('Average %s' % data_label)    
    
def scatter3D(x_list, y_list, z_list, colors, labels):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')    
    
    for i in range(len(x_list)): # only look at students, not TAs/instructor
        ax.scatter(x_list[i], y_list[i], z_list[i], c=colors[i], 
                   label=labels[i]) 
        
    ax.set_xlabel('N-Score')
    ax.set_ylabel('Days Online')
    ax.set_zlabel('Views')
    plt.legend(loc=2)
    
    plt.show()
#----------------------------------------------------------------------
if __name__ == "__main__":
    path = "acm95a100a2018_anonymized_modified.xlsx"
    (p_nodes, q_nodes, links, mod_p_nodes) = get_dataframe(path)
    
    option_dict = {'ACM': 'CMS', 'AM': 'MCE', 'APh': 'APMS', 'Ae':'EAS', 
                   'Aph':'APMS', 'BE':'BBE', 'BMB':'CCE', 'Bi':'BBE', 
                   'CS':'CMS', 'Ch':'CCE', 'ChE': 'CCE', 'ChE (BM)':'CCE', 
                   'ChE (Env)':'CCE', 'ChE (MS)':'CCE', 'ChE (PS)': 'CCE', 
                   'EE':'EE', 'Eng': 'Hum', 'Eng (CNS)': 'Hum', 'Ge': 'GPS', 
                   'ME':'MCE', 'MS':'APMS', 'MedE': 'MedE', 'Ph': 'PMA', 
                   'PlSc':'Hum', 'SE':'EAS', 'AsPh':'PMA'}
    options = ['ACM', 'AM', 'APh', 'Ae', 'AsPh', 'BE', 'BMB', 'Bi', 'CS', 'Ch', 
               'ChE', 'ChE (BM)', 'ChE (Env)', 'ChE (MS)', 'ChE (PS)', 'EE', 
               'Eng', 'Eng (CNS)', 'Ge', 'ME', 'MS', 'MedE', 'Ph', 'PlSc', 'SE']
    classes = ['G1', 'G2', 'G5', 'U2', 'U3', 'U4']
    undergrad = ['U2', 'U3', 'U4']      
    grade_dict = {'A+': 'A', 'A': 'A', 'A-': 'A', 'B+': 'B', 'B': 'B', 
                    'B-': 'B', 'C+': 'C', 'C': 'C', 'C-': 'C', 'D+': 'D'}
    grades = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+']    
    
    # Separate by UG vs G (N means neither (Instructor and TAs))
    mod_p_nodes['Seniority'] = [item[0] for item in mod_p_nodes['Class'][0:184]] + ['N'] * 12    
    p_nodes['Seniority'] = [item[0] for item in p_nodes['Class'][0:184]] + ['N'] * 12         
    
    # A.1
    #plt.figure(1) 
    #p_nodes['Class'].value_counts().plot(kind='bar', 
    #                        title='Distribution of Students among Classes')
    #plt.xlabel('Classes')
    #plt.ylabel('Number of Students')
    #plt.xticks(rotation=0)
    
    #classes = ['U2', 'U3', 'U4', 'G1', 'G2', 'G5']
    #class_numbers = [84, 39, 4, 54, 2, 1]  
    #bar_chart(classes, class_numbers, 'Classes', 'Number of students', 
    #          'Distribution of Students among Classes') 
    
    # undergrad vs grad
    #bar_chart(['UG', 'G'], [127, 57], 'Seniority', 'Number of students', 
    #          'Distribution of Students among Undergrad vs Grad')     
    
    # A.2
    #stacked_bar_chart(p_nodes, 'Class', 'Option', 
    #                 'Distribution of Options within Classes', False) 
    #stacked_bar_chart(p_nodes, 'Class', 'Option', 
    #                 'Distribution of Options within Classes', 'index')      
    #stacked_bar_chart(mod_p_nodes, 'Class', 'Option', 
    #                 'Distribution of Options within Classes', False)
    #stacked_bar_chart(mod_p_nodes, 'Class', 'Option', 
    #                'Distribution of Options within Classes', 'index') 
    # Taking the top 6 options only and putting the rest as 'Other':
    #stacked_bar_chart(mod_p_nodes, 'Class', 'Option2', 
    #                'Distribution of Options within Classes', False)  
    #stacked_bar_chart(mod_p_nodes, 'Class', 'Option2', 
    #                'Distribution of Options within Classes', 'index') 
    #stacked_bar_chart(mod_p_nodes, 'Seniority', 'Option2', 
    #                'Distribution of Options within Undergrads and Grads', False)    
    
    
    # A.3
    #stacked_bar_chart(p_nodes, 'Class', 'Grade', 
    #                 'Distribution of Grades within Classes', False)
    #stacked_bar_chart(p_nodes, 'Class', 'Grade', 
    #                 'Distribution of Grades within Classes', 'index')    
    #stacked_bar_chart(mod_p_nodes, 'Class', 'Grade', 
    #                 'Distribution of Grades within Classes', False) 
    #stacked_bar_chart(mod_p_nodes, 'Class', 'Grade', 
    #                 'Distribution of Grades within Classes', 'index') 
    #stacked_bar_chart(mod_p_nodes, 'Seniority', 'Grade', 
    #                 'Distribution of Grades within Undergrads vs Grads', False)     
    
    # A.4
    #plt.figure(4) 
    #p_nodes['Option'].value_counts().plot(kind='bar', fontsize=15)
    #plt.title('Distribution of Students among Options', fontsize=25)
    #plt.xlabel('Options', fontsize=10)
    #plt.ylabel('Number of Students', fontsize=15) 
    #plt.xticks(rotation=60, fontsize=10)
        
    # combined all ChE options together, and combined Eng(CNS) with Eng    
    #plt.figure(5) 
    #mod_p_nodes['Option'].value_counts().plot(kind='bar', fontsize=20)
    #plt.title('Distribution of Students among Options', fontsize=25)
    #plt.xlabel('Options', fontsize=20)
    #plt.ylabel('Number of Students', fontsize=20)  
    #plt.xticks(rotation=30)    
    
    # A.5
    #stacked_bar_chart(p_nodes, 'Option', 'Class', 
    #                 'Distribution of Classes within Options', False) 
    #stacked_bar_chart(p_nodes, 'Option', 'Class', 
    #                 'Distribution of Classes within Options', 'index')     
    #stacked_bar_chart(mod_p_nodes, 'Option', 'Class', 
    #                 'Distribution of Classes within Options', False) 
    #stacked_bar_chart(mod_p_nodes, 'Option', 'Class', 
    #                 'Distribution of Classes within Options', 'index') 
    
    # reorder the bars so that they go from option with most to least people
    #df = pd.crosstab(mod_p_nodes['Option'], mod_p_nodes['Seniority'])
    #df2 = df.loc[['Ph', 'EE', 'ME', 'ChE', 'SE', 'MS', 'BE', 'AsPh', 'ACM', 
    #              'MedE', 'Ae', 'Eng', 'APh', 'PlSc', 'CS', 'Ge', 'BMB', 'Ch', 
    #              'Bi', 'AM']]
    #df2.plot(kind='bar', stacked=True, fontsize=20)   
    #plt.title('Distribution of Undergrad vs Grad within Options', fontsize=25)
    #plt.xlabel('Options', fontsize=20)
    #plt.ylabel('Number of Students', fontsize=20)  
    #plt.xticks(rotation=30)     
    
    # A.6
    #stacked_bar_chart(p_nodes, 'Option', 'Grade', 
    #                 'Distribution of Grades within Options', False)  
    #stacked_bar_chart(p_nodes, 'Option', 'Grade', 
    #                 'Distribution of Grades within Options', 'index')      
    #stacked_bar_chart(mod_p_nodes, 'Option', 'Grade', 
    #                 'Distribution of Grades within Options', False)
    #stacked_bar_chart(mod_p_nodes, 'Option', 'Grade', 
    #                 'Distribution of Grades within Options', 'index')   
    
    # reorder the bars so that they go from option with most to least people
    #df = pd.crosstab(mod_p_nodes['Option'], mod_p_nodes['Grade'])
    #df2 = df.loc[['Ph', 'EE', 'ME', 'ChE', 'SE', 'MS', 'BE', 'AsPh', 'ACM', 
    #              'MedE', 'Ae', 'Eng', 'APh', 'PlSc', 'CS', 'Ge', 'BMB', 'Ch', 
    #              'Bi', 'AM']]
    #df2.plot(kind='bar', stacked=True, fontsize=20)   
    #plt.title('Distribution of Classes within Options', fontsize=25)
    #plt.xlabel('Options', fontsize=20)
    #plt.ylabel('Number of Students', fontsize=20)  
    #plt.xticks(rotation=30)     
    
    # A.7
    #plt.figure(7) 
    #p_nodes['Grade'].value_counts().plot(kind='bar', 
    #                        title='Distribution of Final Grades')  
    #plt.xlabel('Grades')
    #plt.ylabel('Number of Students') 
    #plt.xticks(rotation=0)        
        
    #grades_numbers = [53, 64, 30, 15, 7, 7, 2, 3, 2, 1]  
    #bar_chart(grades, grades_numbers, 'Grades', 'Number of students', 
    #          'Distribution of Final Grades')  
    #plt.xticks(rotation=0)            
    
    #plt.figure(7) 
    #mod_p_nodes['Grade'].value_counts().plot(kind='bar', 
    #                        title='Distribution of Final Grades')  
    #plt.xlabel('Grades')
    #plt.ylabel('Number of Students') 
    #plt.xticks(rotation=0)            
    
    # A.8
    #stacked_bar_chart(p_nodes, 'Grade', 'Class', 
    #                 'Distribution of Classes within Grades', False)
    #stacked_bar_chart(p_nodes, 'Grade', 'Class', 
    #                 'Distribution of Classes within Grades', 'index')    
    #stacked_bar_chart(mod_p_nodes, 'Grade', 'Class', 
    #                 'Distribution of Classes within Grades', False) 
    #stacked_bar_chart(mod_p_nodes, 'Grade', 'Class', 
    #                 'Distribution of Classes within Grades', 'index') 
    #stacked_bar_chart(mod_p_nodes, 'Grade', 'Seniority', 
    #                 'Distribution of Undergrad vs Grad within Grades', False)     
    
    # A.9
    #stacked_bar_chart(p_nodes, 'Grade', 'Option', 
    #                 'Distribution of Options within Grades', False) 
    #stacked_bar_chart(p_nodes, 'Grade', 'Option', 
    #                 'Distribution of Options within Grades', 'index')     
    #stacked_bar_chart(mod_p_nodes, 'Grade', 'Option', 
    #                 'Distribution of Options within Grades', False) 
    #stacked_bar_chart(mod_p_nodes, 'Grade', 'Option', 
    #                 'Distribution of Options within Grades', 'index')
    #stacked_bar_chart(mod_p_nodes, 'Grade', 'Option2', 
    #                 'Distribution of Options within Grades', False) 
    #stacked_bar_chart(mod_p_nodes, 'Grade', 'Option2', 
    #                 'Distribution of Options within Grades', 'index')     
    
    
    # note: useful function in excel 
    # AVERAGEIFS( average_range, criteria1_range, criteria1, [criteria2_range, 
    # criteria2, criteria3_range, criteria3, ...] )    
    
    # A.17
    r = ['G1'] * 10 + ['G2'] + ['G5'] + ['U2'] * 16 + ['U3'] * 8 + ['U4'] * 3
    c = ['AM', 'Ae', 'BE', 'Bi', 'ChE', 'EE', 'ME', 'MS', 'MedE', 
                    'SE', 'EE', 'BMB', 'ACM', 'APh', 'AsPh', 'BE', 'Ch', 
                    'ChE (BM)', 'ChE (Env)', 'ChE (MS)', 'ChE (PS)', 'EE', 
                    'Eng (CNS)', 'Ge', 'ME', 'MS', 'Ph', 'PlSc', 'AsPh', 'BE', 
                    'CS', 'EE', 'Eng (CNS)', 'ME', 'Ph', 'PlSc', 'CS', 'EE', 
                    'Eng'] # total 39    
    #matrix('Class', 'Option', 'DaysOnline', classes, options,
    #       'Average Days Online', r, c)    
    
    # based on seniority instead of class
    r1 = ['G'] * 11 + ['UG'] * 18
    c1 = ['AM', 'Ae', 'BE', 'BMB', 'Bi', 'ChE', 'EE', 'ME', 'MS', 'MedE', 
                    'SE', 'ACM', 'APh', 'AsPh', 'BE', 'CS', 'Ch', 'ChE (BM)', 
                    'ChE (Env)', 'ChE (MS)', 'ChE (PS)', 'EE', 'Eng', 
                    'Eng (CNS)', 'Ge', 'ME', 'MS', 'Ph', 'PlSc'] # total 29    
    #matrix('Seniority', 'Option', 'DaysOnline', ['G', 'UG'], options,
    #       'Average Days Online', r1, c1)     
    
    # A.22
    #matrix('Class', 'Option', 'Views', classes, options,
    #       'Average Views', r, c)
    #matrix('Seniority', 'Option', 'Views', ['G', 'UG'], options,
    #      'Average Views', r1, c1)     
    
    # A.29   
    #matrix('Class', 'Option', 'N-Score', classes, options,
    #       'Average N-Score', r, c)  
    #matrix('Seniority', 'Option', 'N-Score', ['G', 'UG'], options,
    #       'Average N-Scores', r1, c1)    
    
    # A.30
    # first plot undergrads vs grads 
    #x_u = [] 
    #y_u = []
    #z_u = []
    #x_g = []
    #y_g = []
    #z_g = [] 
    
    #for i in range(184): # only look at students, not TAs/instructor
    #    if mod_p_nodes['Class'][i] in undergrad:
    #        x_u.append(mod_p_nodes['N-Score'][i])
    #        y_u.append(mod_p_nodes['DaysOnline'][i])
    #        z_u.append(mod_p_nodes['Views'][i])
    #    else: # grad students
    #        x_g.append(mod_p_nodes['N-Score'][i])
    #        y_g.append(mod_p_nodes['DaysOnline'][i])
    #        z_g.append(mod_p_nodes['Views'][i])  
    
    #scatter3D([x_u, x_g], [y_u, y_g], [z_u, z_g], ['r', 'b'], 
    #          ['Undergraduate', 'Graduate'])
    
    # now plot by grades
    #x_a = [] 
    #y_a = []
    #z_a = []
    #x_b = []
    #y_b = []
    #z_b = [] 
    #x_c = [] 
    #y_c = []
    #z_c = []
    #x_d = []
    #y_d = []
    #z_d = [] 
    
    #for i in range(184): # only look at students, not TAs/instructor
    #    if mod_p_nodes['Grade'][i] == 'A':
    #        x_a.append(mod_p_nodes['N-Score'][i])
    #        y_a.append(mod_p_nodes['DaysOnline'][i])
    #        z_a.append(mod_p_nodes['Views'][i])
    #    elif mod_p_nodes['Grade'][i] == 'B':
    #        x_b.append(mod_p_nodes['N-Score'][i])
    #        y_b.append(mod_p_nodes['DaysOnline'][i])
    #        z_b.append(mod_p_nodes['Views'][i])  
    #    elif mod_p_nodes['Grade'][i] == 'C':
    #        x_c.append(mod_p_nodes['N-Score'][i])
    #        y_c.append(mod_p_nodes['DaysOnline'][i])
    #        z_c.append(mod_p_nodes['Views'][i]) 
    #    else: # grade = D
    #        x_d.append(mod_p_nodes['N-Score'][i])
    #        y_d.append(mod_p_nodes['DaysOnline'][i])
    #        z_d.append(mod_p_nodes['Views'][i])             
    
    #scatter3D([x_a, x_b, x_c, x_d], [y_a, y_b, y_c, y_d], [z_a, z_b, z_c, z_d], 
    #          ['r', 'b', 'g', 'c'], ['A', 'B', 'C', 'D'])    
    
    # now plot by (top 6) options 
    #x_ph = [] 
    #y_ph = []
    #z_ph = []
    #x_ee = []
    #y_ee = []
    #z_ee = [] 
    #x_me = [] 
    #y_me = []
    #z_me = []
    #x_che = []
    #y_che = []
    #z_che = [] 
    #x_se = [] 
    #y_se = []
    #z_se = []
    #x_ms = []
    #y_ms = []
    #z_ms = []     
    #x_other = []
    #y_other = []
    #z_other = []     
    
    #for i in range(184): # only look at students, not TAs/instructor
    #    if mod_p_nodes['Option2'][i] == 'Ph':
    #        x_ph.append(mod_p_nodes['N-Score'][i])
    #        y_ph.append(mod_p_nodes['DaysOnline'][i])
    #        z_ph.append(mod_p_nodes['Views'][i])
    #    elif mod_p_nodes['Option2'][i] == 'EE':
    #        x_ee.append(mod_p_nodes['N-Score'][i])
    #        y_ee.append(mod_p_nodes['DaysOnline'][i])
    #        z_ee.append(mod_p_nodes['Views'][i])  
    #    elif mod_p_nodes['Option2'][i] == 'ME':
    #        x_me.append(mod_p_nodes['N-Score'][i])
    #        y_me.append(mod_p_nodes['DaysOnline'][i])
    #        z_me.append(mod_p_nodes['Views'][i]) 
    #    elif mod_p_nodes['Option2'][i] == 'ChE':
    #        x_che.append(mod_p_nodes['N-Score'][i])
    #        y_che.append(mod_p_nodes['DaysOnline'][i])
    #        z_che.append(mod_p_nodes['Views'][i]) 
    #    elif mod_p_nodes['Option2'][i] == 'SE':
    #        x_se.append(mod_p_nodes['N-Score'][i])
    #        y_se.append(mod_p_nodes['DaysOnline'][i])
    #        z_se.append(mod_p_nodes['Views'][i]) 
    #    elif mod_p_nodes['Option2'][i] == 'MS':
    #        x_ms.append(mod_p_nodes['N-Score'][i])
    #        y_ms.append(mod_p_nodes['DaysOnline'][i])
    #        z_ms.append(mod_p_nodes['Views'][i])             
    #    else: # option = other
    #        x_other.append(mod_p_nodes['N-Score'][i])
    #        y_other.append(mod_p_nodes['DaysOnline'][i])
    #        z_other.append(mod_p_nodes['Views'][i])             
    
    #scatter3D([x_ph, x_ee, x_me, x_che, x_se, x_ms, x_other], 
    #          [y_ph, y_ee, y_me, y_che, y_se, y_ms, y_other], 
    #          [z_ph, z_ee, z_me, z_che, z_se, z_ms, z_other], 
    #          ['r', 'b', 'g', 'c', 'm', 'y', 'k'], 
    #          ['Ph', 'EE', 'ME', 'ChE', 'SE', 'MS', 'Other'])        
    

