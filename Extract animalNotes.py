
"""
Written by Christina Echagarruga

Purpose: Extract animalNotes from .mat files and format into DataFrame
    Export as csv file
    
Inputs: animalNotes.mat files

Outputs: .csv files

Last Revised: February 28th, 2019
"""
from scipy.io import loadmat
import pandas as pd
import numpy as np


# Load the data into Python 
dst=r'D:animalNotes_baselines.mat'
data=loadmat(dst)

# Build a list of keys and values for each entry in the structure
vals = data['animalNotes_baselines'][0,0]
keys = data['animalNotes_baselines'][0,0].dtype.descr

# Assemble the keys and values into variables with the same name as that used in MATLAB
for i in range(len(keys)):
    key = keys[i][0]
    val = np.squeeze(vals[key][:][:])  # squeeze is used to covert matlat (1,n) arrays into numpy (1,) arrays. 
    val_lists=vals[key][:][:]
    exec(key + '=val')

# stupid way of putting fileIDs into a format for DataFrame    
j=str(vals['fileIDs'][:][:])
j=j.replace("[array([",'')    
j=j.replace("], dtype='<U15')]\n",'')
j=j.replace("[",'')    
j=j.replace("], dtype='<U15')]]",'')
j=j.replace("'",'')    
j=j.replace(" ",'')    

fil_list = []
len_fileID=int(len(j)/15)
for x in range(len_fileID):
    str_fil=x
    beg=(15*x)
    ended=beg+15
    str_fil = j[beg:ended]
    fil_list.append(str_fil)
fileIDs=pd.DataFrame(fil_list)
eventTimes_pd=pd.DataFrame(eventTimes)
durations_pd=pd.DataFrame(durations)

# Merging DataFrames into one DataFrame
animalNotes=pd.DataFrame(index=range(len(j)))
animalNotes['fileIDs']=fileIDs
animalNotes['eventTimes']=eventTimes_pd
animalNotes['durations']=durations_pd
animalNotes.to_csv('animalNotes_baselines.csv')
