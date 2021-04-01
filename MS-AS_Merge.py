# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 10:54:51 2019

@author: vacalder
"""

# PROGRAM TO GENERATE MAINSHOCK - AFTERSHOCK RECORD SEQUENCES
#   Victor A Calderon
#   PhD Student/ Research Assistant
#   NC STATE UNIVERSITY 
#   2021 (c)
import math  as math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import fnmatch
import shutil


# Mainshock and Aftershock Paths

MS_path= r'Q:\My Drive\PhD Program\Research\Thesis\Analysis Methods\Groundmotions\Mainshocks'
AS_path= r'Q:\My Drive\PhD Program\Research\Thesis\Analysis Methods\Groundmotions\Aftershocks'
Seq_path= r'Q:\My Drive\PhD Program\Research\Thesis\Analysis Methods\Groundmotions\Sequences'

# Reading file names

MSListing = os.listdir(MS_path)
ASListing =os.listdir(AS_path)
MainshockFiles = []
AftershockFiles = []


for i in MSListing:
    MainshockFiles.append(i)
    

for j in ASListing:
    AftershockFiles.append(j)

# Reading Mainshock - Aftershock database


PeerDB = pd.read_csv('MS-AS_PEER_Website.csv')
# Converting column names to lowercase and spaces changed to lower hyphen _
PeerDB.columns=PeerDB.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

GM_DB = pd.read_csv('MS_AS_DB.csv')

recorded_rsn_ms_as=[]

for i, row in GM_DB.iterrows():
    ms_rsn=row['mainshock_rsn']
    n_as=row['number_of_aftershocks']
    print('For groundmotion with RSN :', ms_rsn)
    filename1=PeerDB[PeerDB.record_sequence_number==int(ms_rsn)]['file_name_horizontal_1']
    filename2=PeerDB[PeerDB.record_sequence_number==int(ms_rsn)]['file_name_horizontal_2']
    string_ending_file1=filename1.to_string().split('\\')[1]
    string_ending_file2=filename2.to_string().split('\\')[1]
    horizontal_file1 = [x for x in MSListing if x.startswith('RSN'+str(int(ms_rsn))) and x.endswith(string_ending_file1)]
    horizontal_file2 = [x for x in MSListing if x.startswith('RSN'+str(int(ms_rsn))) and x.endswith(string_ending_file2)]
    print('file 1 is:', horizontal_file1)
    print('file 2 is:', horizontal_file2)
    
    check1=os.path.exists(r'Q:\My Drive\PhD Program\Research\Thesis\Analysis Methods\Groundmotions\Mainshocks'+'//'+str(horizontal_file1)[2:-2])
    check2=os.path.exists(r'Q:\My Drive\PhD Program\Research\Thesis\Analysis Methods\Groundmotions\Mainshocks'+'//'+str(horizontal_file2)[2:-2])
    if check1==True:
        print('Horizontal file 1 for mainshock exists')
        
    else: 
        print('Horizontal file 1 for mainshock does not exists')
    
    if check2==True:
        print('Horizontal file 2 for mainshock exists')
        
    else: 
        print('Horizontal file 2 for mainshock does not exists')    
        
    
    counter=0
    
    while counter<int(n_as):
    
        as_rsn=row['aftershock_'+str(counter+1)+'_rsn']
        print('Aftershock',str(counter+1),' with RSN :', as_rsn)
        gm='Mainshock '+str(ms_rsn)+' and aftershock'+str(as_rsn)
        recorded_rsn_ms_as.append(gm)
        counter=counter+1
        
        filename1_as=PeerDB[PeerDB.record_sequence_number==int(as_rsn)]['file_name_horizontal_1']
        filename2_as=PeerDB[PeerDB.record_sequence_number==int(as_rsn)]['file_name_horizontal_2']
        string_ending_file1_as=filename1_as.to_string().split('\\')[1]
        string_ending_file2_as=filename2_as.to_string().split('\\')[1]
        horizontal_file1_as = [x for x in ASListing if x.startswith('RSN'+str(int(as_rsn))) and x.endswith(string_ending_file1_as)]
        horizontal_file2_as = [x for x in ASListing if x.startswith('RSN'+str(int(as_rsn))) and x.endswith(string_ending_file2_as)]
        print('file 1 is:', horizontal_file1_as)
        print('file 2 is:', horizontal_file2_as)
        
#        check3=os.path.exists(r'Q:\My Drive\PhD Program\Research\Thesis\Analysis Methods\Groundmotions\Mainshocks'+'//'+str(horizontal_file1_as)[2:-2])
#        check4=os.path.exists(r'Q:\My Drive\PhD Program\Research\Thesis\Analysis Methods\Groundmotions\Mainshocks'+'//'+str(horizontal_file2_as)[2:-2])
#        if check3==True:
#            print('Horizontal file 1 of aftershock exists')
#            
#        else: 
#            print('Horizontal file 1 of aftershock does not exists')
#        
#        if check4==True:
#            print('Horizontal file 2 of aftershock exists')
#            
#        else: 
#            print('Horizontal file 2 of aftershock does not exists')    

#for x in MainshockFiles:
#    for y in AftershockFiles:
#        
#
#        with open(MS_path+'\\'+x) as GM1:
#            head1  = [next(GM1) for x in range(4)]
#            Data1 = GM1.read()
#            GM1.close
#        #print(head)
#        
#        EQ_DataLine1 = head1[3]
#        dt_pos1      = EQ_DataLine1.find("DT=")
#        
#        # Read from i to i+5 in line 3
#        
#        dt1  = float(EQ_DataLine1[dt_pos1+5:dt_pos1+11])
#        a1   = Data1.split()
#        A1   = [float(i) for i in a1]
#        NPT1 = len(A1)
#        TF1  = dt1*NPT1
#        t1   =np.linspace(dt1,TF1,NPT1)
#        
#        #Reading Aftershock
#        
#        with open(AS_path+'\\'+y) as GM2:
#            head2  = [next(GM2) for x in range(4)]
#            Data2 = GM2.read()
#            GM2.close
#        #print(head)
#        
#        EQ_DataLine2 = head2[3]
#        dt_pos2     = EQ_DataLine2.find("DT=")
#        
#        # Read from i to i+5 in line 3
#        
#        dt2 = float(EQ_DataLine2[dt_pos1+5:dt_pos1+10])
#        a2  = Data2.split()
#        A2   = [float(i) for i in a2]
#        
#        NPT2   = len(A2)
#        NPT2new=NPT2*(dt2/dt1)
#        TF2    = dt2*NPT2
#        t2     = np.linspace(dt2+TF1,TF2+TF1,NPT2)
#        t2_new = np.linspace(dt1+TF1,TF2+TF1,int(NPT2new))
#        A2_new = np.interp(t2_new,t2,A2)
#        
#        
##        plt.plot(t1,A1)
##        plt.plot(t2,A2)
##        plt.plot(t2_new,A2_new)
#        
#        MS_AS=A1
#        MS_AS.extend(A2)
#        
#        with open(Seq_path+'\\'+x+y+'.g3', 'w') as f:
#            for item in MS_AS:
#                f.write("%s\n" % item)