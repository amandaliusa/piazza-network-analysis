import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''
Script for visualizing pq network via boxplots
Author: Siqiao Mu
'''

df = pd.read_excel("acm95a100a2018_anonymized.xlsx")
df = df.apply(pd.to_numeric, errors='ignore')

#
Grade = df['Grade']
Option = df['Option']
Nstudent = 184

Grade_values = [u'A+', u'A', u'A-', u'B+', u'B', u'B-', u'C+', u'C', u'C-', u'D+']
option_dict = {'ACM': 'CMS', 'AM': 'MCE', 'APh': 'APMS', 'Ae':'EAS', 'Aph':'APMS', 'BE':'BBE', 'BMB':'CCE', 'Bi':'BBE', 'CS':'CMS', 'Ch':'CCE', 'ChE': 'CCE', 'ChE (BM)':'CCE', 'ChE (Env)':'CCE', 'ChE (MS)':'CCE', 'ChE (PS)': 'CCE', 'EE':'EE', 'Eng': 'Hum', 'Eng (CNS)': 'Hum', 'Ge': 'GPS', 'ME':'MCE', 'MS':'APMS', 'MedE': 'MedE', 'Ph': 'PMA', 'PlSc':'Hum', 'SE':'EAS', 'AsPh':'PMA'}

sorted_options = np.array([option_dict[i] for i in Option[0:Nstudent]]) #Options sorted into broader categories
sorted_grades = [grade[0] for grade in Grade[0:Nstudent]] #grades with 
sorted_grade_values = sorted(set(sorted_grades))

df_student = df.iloc[0:Nstudent] #construction a dataframe that omits TAs and and includes columns for "SortedOption" which sorts indiidual's options into departments and grades into grades without +/-
df_student['SortedOption'] = pd.Series(sorted_options)
df_student['SortedGrade'] = pd.Series(sorted_grades)


clas = df['Class']
clas_values = sorted(set(clas[0:Nstudent]))
Nscore = df['N-Score']
#


##################
#Boxplots of DaysOnline

#Undergrad vs. Grad
Undergrad = ['U2', 'U3', 'U4']
Undergrad_df = df.loc[df['Class'].isin(Undergrad)]

Grad = ['G1', 'G2', 'G5']
Grad_df = df.loc[df['Class'].isin(Grad)]

fig, axs = plt.subplots(1, 2)

axs[0].boxplot(Undergrad_df['DaysOnline'])
axs[0].set_title('Undergrad DaysOnline')
bottom, top = axs[0].get_ylim()

axs[1].boxplot(np.array(Grad_df['DaysOnline']))
axs[1].set_title('Grad DaysOnline')
axs[1].set_ylim(bottom, top)

plt.show()

#Class

fig, axs = plt.subplots(1, 3)

axs[0].boxplot(df.loc[df['Class']=='U2']['DaysOnline'])
axs[0].set_title('U2 DaysOnline')
bottom, top = axs[0].get_ylim()

axs[1].boxplot(np.array(df.loc[df['Class']=='U3']['DaysOnline']))
axs[1].set_title('U3 DaysOnline')
axs[1].set_ylim(bottom, top)

axs[2].boxplot(np.array(df.loc[df['Class']=='G1']['DaysOnline']))
axs[2].set_title('G1 DaysOnline')
axs[2].set_ylim(bottom, top)

plt.show()

#Options
fig, axs = plt.subplots(2, 5)
set1 = ['MedE', 'EE', 'BBE', 'CCE', 'MCE'] #Excluding GPS as there was only 1 person 
set2 = ['Hum', 'MCE', 'APMS', 'PMA', 'CMS']

for i in range(len(set1)):
    axs[0, i].boxplot(np.array(df_student.loc[df_student['SortedOption'] == set1[i]]['DaysOnline']))
    axs[0, i].set_title(set1[i] + ' DaysOnline')
    axs[0, i].set_ylim(0, 275)

for j in range(len(set2)):
    axs[1, j].boxplot(np.array(df_student.loc[df_student['SortedOption'] == set2[j]]['DaysOnline']))
    axs[1, j].set_title(set2[j] + ' DaysOnline')
    axs[1, j].set_ylim(0, 275)
    
plt.show()

#Grades
set3 = ['A', 'B', 'C'] #only one person with a D, so we omit them

fig, axs = plt.subplots(1, 3)
for k in range(len(set3)):
    axs[k].boxplot(np.array(df_student.loc[df_student['Grade']==set3[k]]['DaysOnline']))
    axs[k].set_title(set3[k] + ' DaysOnline')    
    axs[k].set_ylim(0, 210)
plt.show()

#####################################
#Boxplots of Views

#Undergrad vs. Grad
fig, axs = plt.subplots(1, 2)

axs[0].boxplot(Undergrad_df['Views'])
axs[0].set_title('Undergrad Views')
axs[0].set_ylim(0, 250)

axs[1].boxplot(np.array(Grad_df['Views']))
axs[1].set_title('Grad Views')
axs[1].set_ylim(0, 250)

plt.show()

#Class

fig, axs = plt.subplots(1, 3)

axs[0].boxplot(df.loc[df['Class']=='U2']['Views'])
axs[0].set_title('U2 Views')
axs[0].set_ylim(0, 225)

axs[1].boxplot(np.array(df.loc[df['Class']=='U3']['Views']))
axs[1].set_title('U3 Views')
axs[1].set_ylim(0, 225)

axs[2].boxplot(np.array(df.loc[df['Class']=='G1']['Views']))
axs[2].set_title('G1 Views')
axs[2].set_ylim(0, 225)

plt.show()

#Options
fig, axs = plt.subplots(2, 5)
set1 = ['MedE', 'EE', 'BBE', 'CCE', 'MCE'] #Excluding GPS as there was only 1 person 
set2 = ['Hum', 'MCE', 'APMS', 'PMA', 'CMS']

for i in range(len(set1)):
    axs[0, i].boxplot(np.array(df_student.loc[df_student['SortedOption'] == set1[i]]['Views']))
    axs[0, i].set_title(set1[i] + ' Views')
    axs[0, i].set_ylim(0, 225)

for j in range(len(set2)):
    axs[1, j].boxplot(np.array(df_student.loc[df_student['SortedOption'] == set2[j]]['Views']))
    axs[1, j].set_title(set2[j] + ' Views')
    axs[1, j].set_ylim(0, 225)

plt.show()

#Grades
set3 = ['A', 'B', 'C'] #only one person with a D, so we omit them

fig, axs = plt.subplots(1, 3)
for k in range(len(set3)):
    axs[k].boxplot(np.array(df_student.loc[df_student['Grade']==set3[k]]['Views']))
    axs[k].set_title(set3[k] + ' Views')    
    axs[k].set_ylim(0, 225)
    
plt.show()


###############################
#Boxplots of N-Scores

#Undergrad vs. Grad
Undergrad = ['U2', 'U3', 'U4']
Undergrad_df = df.loc[df['Class'].isin(Undergrad)]

Grad = ['G1', 'G2', 'G5']
Grad_df = df.loc[df['Class'].isin(Grad)]

fig, axs = plt.subplots(1, 2)

axs[0].boxplot(Undergrad_df['N-Score'])
axs[0].set_title('Undergrad N-Score')
axs[0].set_ylim(0, 1)

axs[1].boxplot(np.array(Grad_df['N-Score']))
axs[1].set_title('Grad N-Score')
axs[1].set_ylim(0, 1)

plt.show()

#Class

fig, axs = plt.subplots(1, 3)

axs[0].boxplot(df.loc[df['Class']=='U2']['N-Score'])
axs[0].set_title('U2 N-Score')
axs[0].set_ylim(0, 1)

axs[1].boxplot(np.array(df.loc[df['Class']=='U3']['N-Score']))
axs[1].set_title('U3 N-Score')
axs[1].set_ylim(0, 1)

axs[2].boxplot(np.array(df.loc[df['Class']=='G1']['N-Score']))
axs[2].set_title('G1 N-Score')
axs[2].set_ylim(0, 1)

plt.show()

#Options
fig, axs = plt.subplots(2, 5)
set1 = ['MedE', 'EE', 'BBE', 'CCE', 'MCE'] #Excluding GPS as there was only 1 person 
set2 = ['Hum', 'MCE', 'APMS', 'PMA', 'CMS']

for i in range(len(set1)):
    axs[0, i].boxplot(np.array(df_student.loc[df_student['SortedOption'] == set1[i]]['N-Score']))
    axs[0, i].set_title(set1[i] + ' N-Score')
    axs[0, i].set_ylim(0, 1)

for j in range(len(set2)):
    axs[1, j].boxplot(np.array(df_student.loc[df_student['SortedOption'] == set2[j]]['N-Score']))
    axs[1, j].set_title(set2[j] + ' N-Score')
    axs[1, j].set_ylim(0, 1)

plt.show()


#matrix
def OptionYearMatrix(par): #sorted options
    C = list(set(df_student['Class']))
    O = list(set(df_student['SortedOption']))
    mat = np.zeros((len(C), len(O)))
    x = df
    for i in range(len(C)):
        for j in range(len(O)):
            newdf = df_student.loc[(df_student['Class'] == C[i]) & (df_student['SortedOption'] == O[j])]
            if len(newdf[par]) == 0:
                mat[i, j] = 0
            else:
                mat[i, j] = sum(newdf[par])/len(newdf[par])
    return mat

OptionYearMatrix('DaysOnline')