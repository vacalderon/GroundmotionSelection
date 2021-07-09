# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 15:43:20 2021

@author: VACALDER
"""

#Program to read mainchocks ant convert them to g3 file
import ReadRecord
import pandas as pd

GM_DB = pd.read_csv(r'C:\ConditionDependentPBEE\GroundmotionSelection\mainshock_file_database.csv')

g3_file_path=r'C:\ConditionDependentPBEE\GroundMotion_Mainshock_Records\g3_files'
# ----------------------------------------------------------------------------
#|                             BATCH RUN
# ----------------------------------------------------------------------------



for GM,row in GM_DB.iterrows():
    i=-1
    GM_fn = row['horizontal_1_filename']
    GM_dt = row['dt_horizontal1']
    GM_npt = row['npt_horizontal1']
    print('GM = ',GM_fn)
    
    infile='C:\ConditionDependentPBEE\GroundMotion_Mainshock_Records'+'\\'+GM_fn
    outfile=r'C:\ConditionDependentPBEE\GroundMotion_Mainshock_Records\g3_files'+"\\"+GM_fn+".g3"
    ReadRecord.ReadRecord(infile,outfile)