"""
Written by Christina Echagarruga
and Kevin L. Turner to work with macOS/Unix-based systems

Purpose: Extract data from .mat files and format into DataFrames
    Export as csv file
    
Inputs: PythonData.mat files, animalNotes_baselines.mat file

Outputs: .csv files

Last Revised: March 25th, 2019
"""

from scipy.io import loadmat
import numpy as np
import pandas as pd
import sys
import os

sys.path.append('/Users/kevinturner/Documents/Core-Analysis/Spyder/')
from ResampFiltData import ResampFiltData
from GraphProcData import GraphProcData
rootDir = '/Users/kevinturner/Documents/Jupyter Sleep Scoring/'

# Load the baseline file         
baseFileStr = ("animalNotes_baselines.mat")
baseData = loadmat(rootDir + baseFileStr)

# Build list of keys and values for the baseline data
baseVals = baseData['animalNotes_baselines'][0,0]
baseKeys = baseData['animalNotes_baselines'][0,0].dtype.descr
baseResultsArray = pd.DataFrame()
baseFileIDs = []

# Assemble the baseline file keys and values into variables 
for a in range(len(baseKeys)):
    baseKey = baseKeys[a][0]
    # squeeze is used to covert matlab (1,n) arrays into numpy (1,n) arrays.
    baseVal = np.squeeze(baseVals[baseKey][:])
    vars()[baseKey] = baseVal
    
temp = []
for b in range(len(baseFileIDs)):
    temp.append(str(baseFileIDs[b]))
    
# Create the matlab baselines csv file with the relevant information
baseResultsArray['fileIDs']= baseFileIDs
baseResultsArray[baseKeys[1][0]] = vars()[baseKeys[1][0]]
baseResultsArray[baseKeys[2][0]] = vars()[baseKeys[2][0]]
baseResultsArray.to_csv(rootDir + baseFileStr + ".csv", encoding = 'utf-8', index = False)

# Creating List of mat files to read 
allMatFiles = []
for files in os.listdir(rootDir):
    if files.endswith("PythonData.mat"):
         allMatFiles.append(files)
         
# Create the matlab data csv file with the relevant information
for c in range(len(allMatFiles)):
    fileStr = str(rootDir + allMatFiles[a])
    print("\n\nPulling data from file number", c, "->", fileStr[51:])
    matData = loadmat(fileStr)
    
    # Build list of keys and values for each entry in the structure
    matVals = matData['PythonData'][0,0]
    matKeys = matData['PythonData'][0,0].dtype.descr

    resultsArray = np.empty((0, 9000))
    dataTypeArray = [];
    # Assemble the keys and values into variables 
    for d in range(len(matKeys)):
        matKey = matKeys[d][0]
        matVal = np.squeeze(matVals[matKey][0][:])  # squeeze is used to covert matlab (1,n) arrays into numpy (1,n) arrays.
        if matKey == 'rawNeural_LH':
            dataTypes = ['deltaBandPower_LH', 'thetaBandPower_LH', 'gammaBandPower_LH']
            for dT in range(len(dataTypes)):
                dataType = dataTypes[dT]
                result = list(ResampFiltData(dataType, matVal))
                resultsArray = np.append(resultsArray, [result], axis = 0)
                dataTypeArray.append(dataType)

        elif matKey == 'rawNeural_RH':
            dataTypes = ['deltaBandPower_RH', 'thetaBandPower_RH', 'gammaBandPower_RH']
            for dT in range(len(dataTypes)):
                dataType = dataTypes[dT]
                result = list(ResampFiltData(dataType, matVal))
                resultsArray = np.append(resultsArray, [result], axis = 0)
                dataTypeArray.append(dataType)

        elif matKey == 'EMG':
            dataType = 'EMG'
            result = list(ResampFiltData(dataType, matVal))
            resultsArray = np.append(resultsArray, [result], axis = 0)
            dataTypeArray.append(dataType)

        elif matKey == 'forceSensor':
            dataType = 'forceSensor'
            result = list(ResampFiltData(dataType, matVal))
            resultsArray = np.append(resultsArray, [result], axis = 0)
            dataTypeArray.append(dataType)

        elif matKey == 'whiskerAngle':
            dataType = 'whiskerAngle'
            result = list(ResampFiltData(dataType, matVal))
            resultsArray = np.append(resultsArray, [result], axis = 0)
            dataTypeArray.append(dataType)

    resultsArray = [*zip(*resultsArray)]
    allData = pd.DataFrame.from_records(resultsArray, columns = dataTypeArray)
    GraphProcData(allData, fileStr[51:66], rootDir)
    allData.to_csv(rootDir + fileStr[51:66] + '.csv')
    