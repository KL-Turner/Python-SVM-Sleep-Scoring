"""
Written by Christina Echagarruga
Edited by Kevin L. Turner to work with macOS/Unix-based systems

Purpose: Extract data from .mat files and format into DataFrames
    Export as csv file
    
Inputs: PythonData.mat files

Outputs: _out.csv files

Last Revised: March 1st, 2019
"""

#from scipy.io import loadmat
import numpy as np
import pandas as pd
import sys
import os

sys.path.append('/Users/CJ5232/Documents/Python Scripts/sleep/')
from GraphProcData_v3 import GraphProcData_v3

# Creating List of mat files to read 
rootDir = 'G:/T61/Python Data/New Folder/'

list_allfiles = []
for files in os.listdir(rootDir):
    if files.endswith("Normata.csv"):
         list_allfiles.append(files)

frame_rate = 30 #fps
epochs = frame_rate*10 #10seconds
state = []
Ave_Data = pd.DataFrame()
# Creating csv files with relevant information
for jkl in range(len(list_allfiles)):
    file_str = str(rootDir + list_allfiles[jkl]);
    state = []
    print("\n\nPulling data from file number", jkl, "->", file_str[42:])
    data = pd.read_csv(file_str);
    All_ave_Data = pd.DataFrame() ###########
    num_of_epochs = int(len(data)/epochs);
    for iter in range(num_of_epochs):
        starting = epochs*iter
        ending = starting + epochs
        state = GraphProcData_v3(data[starting:ending], file_str[19:34], rootDir,state);
        categories = list(data)
        
        for heading_nums in range(len(categories)-1):
            
            ind_data = data[categories[heading_nums+1]];
            avedata=np.mean(ind_data[starting:ending])
            
            if iter == 0:
                vars()[categories[heading_nums+1]] = []
            vars()[categories[heading_nums+1]].append(avedata);
            
    for heading_nums in range(len(categories)-1): ###########
        All_ave_Data[categories[heading_nums+1]] = vars()[categories[heading_nums+1]] ###########
    All_ave_Data['Manuel_Sleep_Score'] = state ###########
    All_ave_Data.to_csv(rootDir+list_allfiles[jkl][0:12]+'_all_ave_data.csv') ###########
    
    
    for heading_nums in range(len(categories)-1):
        del vars()[categories[heading_nums+1]]
    del state
            
#All_ave_Data = pd.DataFrame()
#        
#for heading_nums in range(len(categories)-1):
#    All_ave_Data[categories[heading_nums+1]] = vars()[categories[heading_nums+1]]
#    
#All_ave_Data['Manuel_Sleep_Score'] = state
#
#All_ave_Data.to_csv(rootDir+'All_ave_data.csv')

    
        
