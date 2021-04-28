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
import RecordMerge
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
outputfilename1_col=[]
filename1_col=[]
outputfilename2_col=[]
filename2_col=[]
dt1ms_col=[]
dt1as_col=[]
dt1seq_col=[]
dt2ms_col=[]
dt2as_col=[]
dt2seq_col=[]
npt1ms_col=[]
npt2ms_col=[]
npt1as_col=[]
npt2as_col=[]
npt1seq_col=[]
npt2seq_col=[]
rsn_ms1=[]
rsn_as1=[]
rsn_ms2=[]
rsn_as2=[]

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
        
        mainshockfile1=MS_path+'\\'+str(horizontal_file1)[2:-2]
        aftershockfile1=AS_path+'\\'+str(horizontal_file1_as)[2:-2]
        outputfile1=Seq_path+'\\'+str(ms_rsn)+'_'+str(as_rsn)+'_'+'01.g3'
        file1=str(ms_rsn)+'_'+str(as_rsn)+'_'+'01.g3'
        mainshockfile2=MS_path+'\\'+str(horizontal_file2)[2:-2]
        aftershockfile2=AS_path+'\\'+str(horizontal_file2_as)[2:-2]
        outputfile2=Seq_path+'\\'+str(ms_rsn)+'_'+str(as_rsn)+'_'+'02.g3'
        file2 = str(ms_rsn) + '_' + str(as_rsn) + '_' + '02.g3'


        merger1=RecordMerge.RecordMerge(mainshockfile1, aftershockfile1, outputfile1)
        dt_ms1=merger1[0]
        npt_ms1=merger1[1]
        dt_as1=merger1[2]
        npt_as1=merger1[3]
        dt_seq1=merger1[4]
        npt_seq1=merger1[5]
        npt_4s1=merger1[6]
        outputfilename1_col.append(outputfile1)
        filename1_col.append(file1)
        dt1ms_col.append(dt_ms1)
        npt1ms_col.append(npt_ms1)
        dt1as_col.append(dt_as1)
        npt1as_col.append(npt_as1)
        dt1seq_col.append(dt_seq1)
        npt1seq_col.append(npt_seq1)
        rsn_ms1.append(ms_rsn)
        rsn_as1.append(as_rsn)
        
        
        merger2=RecordMerge.RecordMerge(mainshockfile2, aftershockfile2, outputfile2)
        dt_ms2=merger2[0]
        npt_ms2=merger2[1]
        dt_as2=merger2[2]
        npt_as2=merger2[3]
        dt_seq2=merger2[4]
        npt_seq2=merger2[5]
        npt_4s2=merger2[6]
        outputfilename2_col.append(outputfile2)
        filename2_col.append(file2)
        dt2ms_col.append(dt_ms2)
        npt2ms_col.append(npt_ms2)
        dt2as_col.append(dt_as2)
        npt2as_col.append(npt_as2)
        dt2seq_col.append(dt_seq2)
        npt2seq_col.append(npt_seq2)
        rsn_ms2.append(ms_rsn)
        rsn_as2.append(as_rsn)
        
dataDict={'mainshock_aferchock_horizontal1':outputfilename1_col,
          'horizontal_1_filename':filename1_col,
          'dt_sequence_horizontal1':dt1seq_col,
          'npt_sequence_horizontal1':npt1seq_col,
          'dt_mainshock_horizontal1':dt1ms_col,
          'npt_mainshock_horizontal1':npt1ms_col,
          'dt_aftershock_horizontal1':dt1as_col,
          'npt_aftershock_horizontal1':npt1as_col,
          'rsn_mainshock_horizontal1':rsn_ms1,
          'rsn_aftershock_horizontal1':rsn_as1,
          'mainshock_aferchock_horizontal2':outputfilename2_col,
          'horizontal_2_filename':filename2_col,
          'dt_sequence_horizontal2':dt2seq_col,
          'npt_sequence_horizontal2':npt2seq_col,
          'dt_mainshock_horizontal2':dt2ms_col,
          'npt_mainshock_horizontal2':npt2ms_col,
          'dt_aftershock_horizontal2':dt2as_col,
          'npt_aftershock_horizontal2':npt2as_col,
          'rsn_mainshock_horizontal2':rsn_ms2,
          'rsn_aftershock_horizontal2':rsn_as2,}
DataFrame_Out=pd.DataFrame(dataDict)
DataFrame_Out.to_csv('mainshock_aftershock_file_database.csv')
        
