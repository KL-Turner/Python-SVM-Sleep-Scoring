"""
Written by Christina Echagarruga

Purpose: Extract data from .mat files and format into DataFrames
    Export as csv file
    
Inputs: PythonData.mat files

Outputs: _out.csv files

Last Revised: February 26, 2019
"""

from scipy.io import loadmat
from scipy import signal
import numpy as np
import pandas as pd
import os

# Creating List of mat files to read 
rootdir=r'D:'

list_allfiles=[]
for files in os.listdir(rootdir):
    if files.endswith("PythonData.mat"):
        list_allfiles.append(files)
#print(list_allfiles)
     
# Creating csv files with relevant information
for jkl in range(len(list_allfiles)):
    file_str=str('D:'+list_allfiles[jkl])
    data=loadmat(file_str)

    # Build list of keys and values for each entry in the structure
    vals = data['PythonData'][0,0]
    keys = data['PythonData'][0,0].dtype.descr
    All_Data = pd.DataFrame()

    # Assemble the keys and values into variables 
    # Same name as that used in MATLAB
    for i in range(len(keys)):
        key = keys[i][0]
        val = np.squeeze(vals[key][0][:])  # squeeze is used to covert matlat (1,n) arrays into numpy (1,) arrays. 
        val_lists=list(signal.resample(val,45000))
        All_Data=All_Data.assign(**{key:val_lists})
        #exec(key + '=val')

        # Save as .csv 
        All_Data.to_csv(file_str[2:17]+'_out.csv')