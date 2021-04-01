# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 14:52:27 2019

@author: VACALDER
"""

# PROGRAM TO FILTER GROUNDMOTIONS 
# Victor A Calderon
# PhD Student / Research Assistant
# NC STATE UNIVERSITY 
# 2019 (c)

# The program has the capability to filter data according to different parameters
# depending on the different properties listed in the PEER NGA West 2 DB
# the program then can either download the files from PEER Website or from
# Kowalsky Group Folder, the program will be further developed to download only
# the files that are not downloaded since PEER website has a limit of 
# 200 downloads every 2 weeks and 400 downloads per month, if the required downloads
# are larger than this limit it is sugested to download a maximum of 200
# this script is specifically designed to download sequences of Mainshocks and
# Aftershocks.


import math  as math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.axes as ax
import pandas as pd
#from selenium import webdriver
#from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import os
import fnmatch
import shutil


# EARTHQUAKE SELECTION PROGRAM
# Data base is taken fron NGA West 2 database from  PEER

PeerDB = pd.read_csv('MS-AS_PEER_Website.csv')
# Converting column names to lowercase and spaces changed to lower hyphen _
PeerDB.columns=PeerDB.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

# Data is filtered according to the following criteria:
# * Moment Magnitude M=>5
# * PGA>0.04
# * PGV>1 cm/s
# * Vs30>100m/s & Vs30<1000m/s
# * Lowest ussable frequency is less than 1Hz
# * Rrup<60km

magnitude_filter=(PeerDB.earthquake_magnitude>=5)
pga_filter=(PeerDB.pga_g>=0.04)
pgv_filter=(PeerDB.pgv_cm_sec>=1)
vs30_filter=(PeerDB.vs30_m_s_selectedforanalysis.between(100,1000))
freq_filter=(PeerDB.lowestusablefreq_h1_hz<=1)
rrup_filter=(PeerDB.joyner_booredist_km <= 60)
counts = PeerDB['station_name'].value_counts()
repeat=(PeerDB['station_name'].isin(counts.index[counts > 1]))
all_filters=magnitude_filter & pga_filter & pgv_filter & vs30_filter & freq_filter & rrup_filter & repeat


Peer_Filtered=PeerDB[all_filters]

# Plotting Data Points

Peer_Filtered.plot.scatter(x='joyner_booredist_km',y='earthquake_magnitude',s=20,c='earthquake_magnitude',colormap='viridis')
plt.title('Main Shock and Aftershock Selection',fontsize=32)
plt.xlabel('Rrup (km)',fontsize=24)
plt.ylabel('Magnitude (Mw)',fontsize=24)
plt.tick_params(direction='out',axis='both',labelsize=20)
plt.show

# Selecting Mainshocks and generate string to download RSN

dwnstr=''

for x in range(0,2):
    print('the valu of x is ',x)
    Main_Shocks=Peer_Filtered[Peer_Filtered['earthquake_name'].str.contains('0'+str(x))]

for i, row in Main_Shocks.iterrows():
    dwnstr=','+str(row['record_sequence_number'])+dwnstr
    
MSstr=dwnstr[1:]
Number_of_Mainshocks=MSstr.count(',')+1

#Saving Mainshock Database
#Main_Shocks.to_excel(r'C:\ConditionDepedentPBEE\GroundmotionSelection\Mainshock_DB.xlsx')

MSdownloadfilter=pd.isna(Main_Shocks.downloaded)
MS_2download=Main_Shocks[MSdownloadfilter]

MSdwnstr=''

for i, row in MS_2download.iterrows():
    MSdwnstr=','+str(row['record_sequence_number'])+MSdwnstr


Main_Shocks.plot.scatter(x='joyner_booredist_km',y='earthquake_magnitude',s=20,c='earthquake_magnitude',colormap='viridis')
plt.title('Main Shock Selection',fontsize=32)
plt.xlabel('Rrup (km)',fontsize=24)
plt.ylabel('Magnitude (Mw)',fontsize=24)
plt.tick_params(direction='out',axis='both',labelsize=20)
plt.show

# Copying already Downloaded files in Kowalsky Group Folder:

#source = r"Q:\My Drive\NGA Ground Motion Downloads\01_AccelerationFiles"
#destination = r"C:\ConditionDepedentPBEE\GroundmotionSelection\Mainshocks"
#
#for i, row in Main_Shocks.iterrows():
#    if row['downloaded']=="Yes":
#        for filename in os.listdir(r'Q:\My Drive\NGA Ground Motion Downloads\01_AccelerationFiles'):
#            if fnmatch.fnmatch(filename, 'RSN'+str(row['record_sequence_number'])+'*.AT2'):
#                print(filename)
#                filesrc=source+"\\"+filename
#                filedtn=destination+"\\"+filename
#                shutil.copyfile(filesrc,filedtn) 
#    else:
#        print('notdownloaded yet')


# Accesing  PEER Website

#browser = webdriver.Chrome() 
#url="https://ngawest2.berkeley.edu/users/sign_in?unauthenticated=true"    
#browser.get(url)
#browser.find_element_by_id("user_email").send_keys('vacalder@ncsu.edu')
#browser.find_element_by_id("user_password").send_keys("ViCk2016")
#browser.find_element_by_id("user_submit").click()
#url2="https://ngawest2.berkeley.edu/"
#browser.get(url2)
#browser.find_element_by_xpath('//*[@id="content"]/table[1]/tbody/tr[1]/td[2]/a').click()
#browser.find_element_by_xpath('//*[@id="buttons"]/button').click()
#WebDriverWait(browser, 10) # seconds
#url4="https://ngawest2.berkeley.edu/spectras/223218/searches/new"
#browser.get(url4)
#browser.find_element_by_xpath('//*[@id="search_search_nga_number"]').send_keys(MSstr)
#browser.find_element_by_xpath('//*[@id="new_search"]/div[2]/fieldset/button').click()
#browser.find_element_by_xpath('//*[@id="middle_submit"]/fieldset[3]/button[2]').click()
#browser.find_element_by_id('show-alert').click()
#alert = browser.switch_to.alert
#alert.accept()
#alert.accept()
    
# Selecting Aftershocks and generate String to download RSN

    
for y in range (2,3):
    print('the valu of y is ',y)
    Aftershocks=Peer_Filtered[Peer_Filtered['earthquake_name'].str.contains('0'+str(y))]
    
    
for y in range (3,8):
    print('the valu of y is ',y)
    df=Peer_Filtered[Peer_Filtered['earthquake_name'].str.contains('0'+str(y))]
    Aftershocks=Aftershocks.append(df)

for i, row in Aftershocks.iterrows():
    dwnstr2=','+str(row['record_sequence_number'])+dwnstr

ASstr=dwnstr2[1:]

Number_of_Aftershocks=ASstr.count(',')+1

#Saving Mainshock Database
#Aftershocks.to_excel(r'C:\ConditionDepedentPBEE\GroundmotionSelection\Aftershock_DB.xlsx')

ASdownloadfilter=pd.isna(Aftershocks.downloaded)
AS_2download=Aftershocks[ASdownloadfilter]

ASdwnstr=''

for i, row in AS_2download.iterrows():
    ASdwnstr=','+str(row['record_sequence_number'])+ASdwnstr

for j, row in Main_Shocks.iterrows():
   msi=row['station_name']
   print(row['record_sequence_number'])
   str_as_df=Aftershocks[(Aftershocks.station_name==msi)]['record_sequence_number']
   z=str_as_df.to_numpy()
   

# Copying already Downloaded files in Kowalsky Group Folder:
#
#source = r"Q:\My Drive\NGA Ground Motion Downloads\01_AccelerationFiles"
#destination = r"C:\ConditionDepedentPBEE\GroundmotionSelection\Aftershocks"
#
#for i, row in Aftershocks.iterrows():
#    if row['downloaded']=="Yes":
#        for filename in os.listdir(r'Q:\My Drive\NGA Ground Motion Downloads\01_AccelerationFiles'):
#            if fnmatch.fnmatch(filename, 'RSN'+str(row['record_sequence_number'])+'*.AT2'):
#                print(filename)
#                filesrc=source+"\\"+filename
#                filedtn=destination+"\\"+filename
#                shutil.copyfile(filesrc,filedtn) 
#    else:
#        print('notdownloaded yet')


#browser = webdriver.Chrome() 
#url="https://ngawest2.berkeley.edu/users/sign_in?unauthenticated=true"    
#browser.get(url)
#browser.find_element_by_id("user_email").send_keys('vacalder@ncsu.edu')
#browser.find_element_by_id("user_password").send_keys("ViCk2016")
#browser.find_element_by_id("user_submit").click()
#url2="https://ngawest2.berkeley.edu/"
#browser.get(url2)
#browser.find_element_by_xpath('//*[@id="content"]/table[1]/tbody/tr[1]/td[2]/a').click()
#browser.find_element_by_xpath('//*[@id="buttons"]/button').click()
#WebDriverWait(browser, 10) # seconds
#url4="https://ngawest2.berkeley.edu/spectras/223218/searches/new"
#browser.get(url4)
#browser.find_element_by_xpath('//*[@id="search_search_nga_number"]').send_keys(ASstr)
#WebDriverWait(browser, 300) # seconds
#browser.find_element_by_xpath('//*[@id="new_search"]/div[2]/fieldset/button').click()
#WebDriverWait(browser, 300) # seconds
#browser.find_element_by_xpath('//*[@id="middle_submit"]/fieldset[3]/button[2]').click()
#browser.find_element_by_id('show-alert').click()
#alert = browser.switch_to.alert
#alert.accept()
#alert.accept()