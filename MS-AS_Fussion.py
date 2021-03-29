# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 10:54:51 2019

@author: vacalder
"""

# PROGRAM TO GENERATE MAINSHOCK - AFTERSHOCK RECORD SEQUENCES
#   Victor A Calderon
#   PhD Student/ Research Assistant
#   NC STATE UNIVERSITY 
#   2019 (c)
import math  as math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import fnmatch
import shutil


# Mainshock and Aftershock Paths

MS_path= r'C:\ConditionDepedentPBEE\GroundmotionSelection\MainShock_Test'
AS_path= r'C:\ConditionDepedentPBEE\GroundmotionSelection\Aftershock_Test'
Seq_path= r'C:\ConditionDepedentPBEE\GroundmotionSelection\Sequences_Test'


# Reading file names

MSListing = os.listdir(MS_path)
ASListing =os.listdir(AS_path)
MainshockFiles = []
AftershockFiles = []


for i in MSListing:
    MainshockFiles.append(i)
    

for j in ASListing:
    AftershockFiles.append(j)


for x in MainshockFiles:
    for y in AftershockFiles:
        

        with open(MS_path+'\\'+x) as GM1:
            head1  = [next(GM1) for x in range(4)]
            Data1 = GM1.read()
            GM1.close
        #print(head)
        
        EQ_DataLine1 = head1[3]
        dt_pos1      = EQ_DataLine1.find("DT=")
        
        # Read from i to i+5 in line 3
        
        dt1  = float(EQ_DataLine1[dt_pos1+5:dt_pos1+11])
        a1   = Data1.split()
        A1   = [float(i) for i in a1]
        NPT1 = len(A1)
        TF1  = dt1*NPT1
        t1   =np.linspace(dt1,TF1,NPT1)
        
        #Reading Aftershock
        
        with open(AS_path+'\\'+y) as GM2:
            head2  = [next(GM2) for x in range(4)]
            Data2 = GM2.read()
            GM2.close
        #print(head)
        
        EQ_DataLine2 = head2[3]
        dt_pos2     = EQ_DataLine2.find("DT=")
        
        # Read from i to i+5 in line 3
        
        dt2 = float(EQ_DataLine2[dt_pos1+5:dt_pos1+10])
        a2  = Data2.split()
        A2   = [float(i) for i in a2]
        
        NPT2   = len(A2)
        NPT2new=NPT2*(dt2/dt1)
        TF2    = dt2*NPT2
        t2     = np.linspace(dt2+TF1,TF2+TF1,NPT2)
        t2_new = np.linspace(dt1+TF1,TF2+TF1,int(NPT2new))
        A2_new = np.interp(t2_new,t2,A2)
        
        
#        plt.plot(t1,A1)
#        plt.plot(t2,A2)
#        plt.plot(t2_new,A2_new)
        
        MS_AS=A1
        MS_AS.extend(A2)
        
        with open(Seq_path+'\\'+x+y+'.g3', 'w') as f:
            for item in MS_AS:
                f.write("%s\n" % item)