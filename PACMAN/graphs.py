# import numpy as np
# import matplotlib.pyplot as plt
from learningAgents import *

def graph_builder(Avg_10,Avg_all):
    fp=open('Avg_10.txt', 'w')
    s=""
    for i in Avg_10:
        s+=str(i)+','
    fp.write(s)
    fp.close()
    fp_1=open('Avg_all.txt', 'w')
    s_1=""
    for i in Avg_all:
        s_1+=str(i)+','
    fp_1.write(s_1)
    fp_1.close()
