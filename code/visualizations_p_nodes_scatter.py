import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''
Script for visualizing pq network via scatter plots
Author: Siqiao Mu
'''

df = pd.read_excel("acm95a100a2018_anonymized.xlsx")
df = df.apply(pd.to_numeric, errors='ignore')

Grade = df['Grade']
Class = df['Class']
Option = df['Option']
Nstudent = 184

Grade_values = [u'A+', u'A', u'A-', u'B+', u'B', u'B-', u'C+', u'C', u'C-', u'D+']
option_dict = {'ACM': 'CMS', 'AM': 'MCE', 'APh': 'APMS', 'Ae':'EAS', 'Aph':'APMS', 'BE':'BBE', 'BMB':'CCE', 'Bi':'BBE', 'CS':'CMS', 'Ch':'CCE', 'ChE': 'CCE', 'ChE (BM)':'CCE', 'ChE (Env)':'CCE', 'ChE (MS)':'CCE', 'ChE (PS)': 'CCE', 'EE':'EE', 'Eng': 'Hum', 'Eng (CNS)': 'Hum', 'Ge': 'GPS', 'ME':'MCE', 'MS':'APMS', 'MedE': 'MedE', 'Ph': 'PMA', 'PlSc':'Hum', 'SE':'EAS', 'AsPh':'PMA'}

top_options_list = ['PMA', 'EE', 'MCE', 'EAS', 'CCE', 'APMS']

new_option_dict = dict()
for k in option_dict:
    if option_dict[k] in top_options_list:
        new_option_dict[k] = option_dict[k]
    else:
        new_option_dict[k] = 'Other'

sorted_options = np.array([option_dict[i] for i in Option[0:Nstudent]]) #Options sorted into broader categories
new_sorted_options = np.array([new_option_dict[i] for i in Option[0:Nstudent]])
sorted_grades = [grade[0] for grade in Grade[0:Nstudent]] #grades with 
sorted_grade_values = sorted(set(sorted_grades))

sorted_u_g = [clas[0] for clas in Class[0:Nstudent]]

df_student = df.iloc[0:Nstudent] #construction a dataframe that omits TAs and and includes columns for "SortedOption" which sorts indiidual's options into departments and grades into grades without +/-
df_student['SortedOption'] = pd.Series(sorted_options)
df_student['NewSortedOption'] = pd.Series(new_sorted_options)
df_student['SortedGrade'] = pd.Series(sorted_grades)
df_student['UndergradorGrad'] = pd.Series(sorted_u_g)

clas = df['Class']
clas_values = sorted(set(clas[0:Nstudent]))
Nscore = df['N-Score']



############################
plt.hist(df_student['Views'], bins=10)
plt.title('Views Distribution')
plt.xlabel('Views')
plt.show()

plt.hist(df_student['DaysOnline'], bins=10)
plt.title('DaysOnline Distribution')
plt.xlabel('DaysOnline')
plt.show()


######################
#Scatter Plots
#by year
plt.title('Views vs. DaysOnline: Year')
plt.xlabel('Views')
plt.ylabel('DaysOnline')
for i in range(len(clas_values)):
    plt.scatter(df_student.loc[df_student['Class']==clas_values[i]]['Views'], df_student.loc[df_student['Class']==clas_values[i]]['DaysOnline'], label= clas_values[i])
plt.legend()
plt.show()

plt.title('Views vs. DaysOnline: Undergrad vs. Grad')
plt.xlabel('Views')
plt.ylabel('DaysOnline')
plt.scatter(df_student.loc[df_student['UndergradorGrad'] =='U']['Views'], df_student.loc[df_student['UndergradorGrad'] == 'U']['DaysOnline'], label= 'Undergrad')
plt.scatter(df_student.loc[df_student['UndergradorGrad'] =='G']['Views'], df_student.loc[df_student['UndergradorGrad'] == 'G']['DaysOnline'], label= 'Grad')
plt.legend()
plt.show()

#by nscore
plt.scatter(df_student['Views'], df_student['DaysOnline'], c =Nscore[0:Nstudent]) 
plt.title('Views vs. DaysOnline: Nscore')
plt.colorbar()
plt.xlabel('Views')
plt.ylabel('DaysOnline')
plt.show()

#by grade
plt.title('Views vs. DaysOnline: Grades')
plt.xlabel('Views')
plt.ylabel('DaysOnline')
for i in range(len(Grade_values)):
    plt.scatter(df_student.loc[df_student['Grade']==Grade_values[i]]['Views'], df_student.loc[df_student['Grade']==Grade_values[i]]['DaysOnline'], label=Grade_values[i])
plt.legend()
plt.show()

#by sorted grade
plt.title('Views vs. DaysOnline: Grades (Without +/-)')
plt.xlabel('Views')
plt.ylabel('DaysOnline')
for i in range(len(sorted_grade_values)):
    plt.scatter(df_student.loc[df_student['SortedGrade']==sorted_grade_values[i]]['Views'], df_student.loc[df_student['SortedGrade']==sorted_grade_values[i]]['DaysOnline'], label=sorted_grade_values[i])
plt.legend()
plt.show()


#by Option
plt.title('Views vs. DaysOnline: Option')
plt.xlabel('Views')
plt.ylabel('DaysOnline')
opt_values = list(set(option_dict.values()))
for i in range(len(opt_values)):
    plt.scatter(df_student.loc[df_student['SortedOption']==opt_values[i]]['Views'], df_student.loc[df_student['SortedOption']==opt_values[i]]['DaysOnline'], label=opt_values[i])
    plt.legend()
plt.show()

#by Option (list truncated)
plt.title('Views vs. DaysOnline: Option')
plt.xlabel('Views')
plt.ylabel('DaysOnline')
new_opt_values = list(set(new_option_dict.values()))
for i in range(len(new_opt_values)):
    plt.scatter(df_student.loc[df_student['NewSortedOption']==new_opt_values[i]]['Views'], df_student.loc[df_student['NewSortedOption']==new_opt_values[i]]['DaysOnline'], label=new_opt_values[i])
    plt.legend()
plt.show()