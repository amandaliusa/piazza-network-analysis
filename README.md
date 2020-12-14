# PQ Learning Collaboration Networks

## Dataset 

The dataset used in this project is a learning collaboration network of students at Caltech who took ACM 95a/100a taught by Kostia Zuev during Winter 2018. The data was obtained from the course page on Piazza, an online collaboration forum for students and instructors. The full network is directed and bipartite with two types of nodes: p-nodes representing people (students, TAs, instructor) and q-nodes representing questions asked by students. A link from node `q_k` to node `p_j` represents a question `q_k` asked by student `p_j`. A link from node `p_i` to node `q_k` represents an answer by person `p_i` to question `q_k`. A dyadic link `p_i` &rarr; `q_k` &rarr; `p_j` thus represents a flow of knowledge from person `p_i` to person `p_j` through question `q_k`. The network data is stored in `data/acm95a100a2018_anonymized.xlsx` with three tabs:

### P-nodes
	
Each p-node has the following attributes:
	
ID - node ID.

Role - one of four possible values: Student, TA, Head TA, Instructor.

Class - one of U2 (Sophomore), U3 (Junior), U4 (Senior), G1, etc (graduate students).

Option - the option of the corresponding student.

Section - one of 10 sections the student/TA was assigned to.

DaysOnline - a statistic collected by Piazza.

Views - a statistic collected by Piazza.

Contributions, Questions,	Notes, Answers - statistics collected by Piazza

N-Score - final score of students, normalized via a linear transformation so that the min score is 0 and the max score is 1. 

Grade - final grade (based on the final score): A+, A, A-, etc.

Status - the status of participation of the node in the network: 1 -- yes, 0 -- no. 
	
### Q-nodes
	
The only attribute of q-nodes is their ID.

### Links

Links have three attributes:

ID - link ID.

Start - node ID where the directed link starts.

End - node ID where the directed link ends.

## Goals

The main goal of this project is to extract signals from this dataset; that is, to form plausible hypotheses about collaboration between students in particular and people in general. The evidence for these hypotheses provided by the considered dataset should be statistically significant. This will motivate testing the existence of derived signals in other collaboration networks (Piazza, other online forums, StackExchange, company email correspondence, etc). 

## Acknowledgments 

This repository was authored by [Amanda Li](https://github.com/amandaliusa), with contributions from Siqiao Mu and project mentorship and conception by [Professor Konstantin Zuev](https://github.com/Kostia-Zuev) (Caltech). 
