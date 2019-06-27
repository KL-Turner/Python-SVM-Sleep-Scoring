
"""
Written by Christina Echagarruga
Edited by Kevin L. Turner to work with macOS/Unix-based systems

Purpose: Extract animalNotes from .mat files and format into DataFrame
    Export as csv file
    
Inputs: animalNotes.mat files

Outputs: .csv files

Last Revised: March 6th, 2019
"""
from scipy.io import loadmat
import pandas as pd
import numpy as np
import os

# Load the data into Python 
workingDir = '/Volumes/Blackberry/Jupyter Sleep Scoring'
os.chdir(workingDir)
dst = 'animalNotes_baselines.mat'
data = loadmat(dst)

# Build a list of keys and values for each entry in the structure
vals = data['animalNotes_baselines'][0,0]
keys = data['animalNotes_baselines'][0,0].dtype.descr

# Assemble the keys and values into variables with the same name as that used in MATLAB
for i in range(len(keys)):
    key = keys[i][0]
    val = np.squeeze(vals[key][:][:])  # squeeze is used to covert matlab (1,n) arrays into numpy (1,n) arrays. 
    val_lists = vals[key][:][:]
    exec(key + '=val')

# stupid way of putting fileIDs into a format for DataFrame    
j = str(vals['fileIDs'][:][:])
j = j.replace("[array([",'')    
j = j.replace("], dtype='<U15')]\n",'')
j = j.replace("[",'')    
j = j.replace("], dtype='<U15')]]",'')
j = j.replace("'",'')    
j = j.replace(" ",'')    

fil_list = []
len_fileID = int(len(j)/15)
for x in range(len_fileID):
    beg = (15*x)
    ended = beg+15
    str_fil = j[beg:ended]
    fil_list.append(str_fil)
    fileIDs = pd.DataFrame(fil_list)
    eventTimes = pd.DataFrame(eventTimes)
    durations = pd.DataFrame(durations)

# Merging DataFrames into one DataFrame
animalNotes = pd.DataFrame(index = range(len(fileIDs)))
animalNotes['fileIDs'] = fileIDs
animalNotes['eventTimes'] = eventTimes
animalNotes['durations'] = durations
animalNotes.to_csv('animalNotes_baselines.csv')
