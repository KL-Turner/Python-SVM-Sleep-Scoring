def ConvMAT2CSV(rootDir, codeDir):
    """
    Written by Christina Echagarruga and Kevin L. Turner to work with macOS/Unix-based systems
    
    Purpose: Extract data from .mat files and format into DataFrames
        Export as csv file
        
    Inputs: PythonData.mat files, animalNotes_baselines.mat file
    
    Outputs: .csv files
    
    Last Revised: April 2nd, 2019
    """
    
    from scipy.io import loadmat
    import numpy as np
    import pandas as pd
    import sys
    import os
    
    sys.path.append(codeDir)
    from PreProcData import ResampFiltData
    from GraphData import GraphData
    
    # Load the baseline file         
    baseFileStr = ("baselineInfo.mat")
    baseData = loadmat(rootDir + baseFileStr)
    
    # Build list of keys and values for the baseline data
    baseVals = baseData['animalNotes_baselines'][0,0]
    baseKeys = baseData['animalNotes_baselines'][0,0].dtype.descr
    baseResultsArray = pd.DataFrame()
    
    # Assemble the baseline file keys and values into variables 
    for a in range(len(baseKeys)):
        baseKey = baseKeys[a][0]
        baseVal = baseVals[baseKey][:]
        df = pd.DataFrame(baseVal)
        baseResultsArray = pd.concat([baseResultsArray, df], axis = 1, ignore_index = True)

    for b in range(len(baseKeys)):
        baseResultsArray = baseResultsArray.rename({b: baseKeys[b][0]}, axis = 'columns')
    
    baseResultsArray.to_csv(rootDir + "baselineInfo.csv", encoding = 'utf-8', index = False)
    
    # Creating List of mat files to read 
    allMatFiles = []
    for files in os.listdir(rootDir):
        if files.endswith("PythonData.mat"):
             allMatFiles.append(files)
             
    # Create the matlab data csv file with the relevant information
    for c in range(len(allMatFiles)):
        fileStr = str(rootDir + allMatFiles[c])
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
        GraphData(allData, fileStr[51:66], rootDir, 'Proc')
        allData.to_csv(rootDir + fileStr[51:66] + '_ProcData.csv')
    
    return
    
def ResampFiltData(dataType, data):
    """
    Written by Kevin L. Turner 
    
    Purpose: filter and resample date based on dataType
        
    Inputs: raw data array
    
    Outputs: processed data array
    
    Last Revised: April 2nd, 2019
    """
    from scipy import signal
    
    # compare the input string to determine which filtering and resampling conditions to use.
    if str(dataType) == 'deltaBandPower_LH' or str(dataType) == 'deltaBandPower_RH':
                    fs = 20000
                    fpass = [1, 4]   # delta band 1-4 Hz
                    smooth = 1
                    nyq = 0.5*fs
                    low = fpass[0]/nyq
                    high = fpass[1]/nyq
                    b1, a1 = signal.butter(2, [low, high], 'bandpass', analog = False)
                    fData = signal.filtfilt(b1, a1, data)
                    b2, a2 = signal.butter(4, (smooth/nyq), 'low', analog = False)
                    ffData = signal.filtfilt(b1, a1, fData)
                    ffrData = signal.resample((ffData**2), 9000)
    elif str(dataType) == 'thetaBandPower_LH' or str(dataType) == 'thetaBandPower_RH':
                    fs = 20000
                    fpass = [4, 8]   # theta band 4-8 Hz
                    smooth = 1
                    nyq = 0.5*fs
                    low = fpass[0]/nyq
                    high = fpass[1]/nyq
                    b1, a1 = signal.butter(2, [low, high], 'bandpass', analog = False)
                    fData = signal.filtfilt(b1, a1, data)
                    b2, a2 = signal.butter(4, (smooth/nyq), 'low', analog = False)
                    ffData = signal.filtfilt(b1, a1, fData)
                    ffrData = signal.resample((ffData**2), 9000)
    elif str(dataType) == 'gammaBandPower_LH' or str(dataType) == 'gammaBandPower_RH':
                    fs = 20000
                    fpass = [40, 100]   # gamma band 40-100 Hz
                    smooth = 1
                    nyq = 0.5*fs
                    low = fpass[0]/nyq
                    high = fpass[1]/nyq
                    b1, a1 = signal.butter(2, [low, high], 'bandpass', analog = False)
                    fData = signal.filtfilt(b1, a1, data)
                    b2, a2 = signal.butter(4, (smooth/nyq), 'low', analog = False)
                    ffData = signal.filtfilt(b1, a1, fData)
                    ffrData = signal.resample((ffData**2), 9000)
    elif str(dataType) == 'EMG':
                    fs = 20000
                    fpass = [30, 300]   # electromyography filtered to 30-300, also may try 1000-3000 for multi-unit 
                    nyq = 0.5*fs
                    low = fpass[0]/nyq
                    high = fpass[1]/nyq
                    b1, a1 = signal.butter(2, [low, high], 'bandpass', analog = False)
                    fData = signal.filtfilt(b1, a1, data)
                    ffrData = signal.resample((fData**2), 9000)
    elif str(dataType) == 'forceSensor':
                    fs = 20000
                    fpass = 20   # smooth high-freq noise
                    nyq = 0.5*fs
                    b1, a1 = signal.butter(2, (fpass/nyq), 'low', analog = False)
                    fData = signal.filtfilt(b1, a1, data)
                    ffrData = signal.resample(fData, 9000)
    elif str(dataType) == 'whiskerAngle':
                    fs = 150
                    fpass = 20   # smooth high-freq noise
                    nyq = 0.5*fs
                    b1, a1 = signal.butter(2, (fpass/nyq), 'low', analog = False)
                    fData = signal.filtfilt(b1, a1, data)
                    ffrData = signal.resample(fData, 9000)
    else:
                    print('Invalid string name entered')
                    return
                
    return ffrData

def CalcRestingBaselines(rootDir, codeDir):
    """
    Written by Kevin L. Turner

    Purpose: 
        
    Inputs: 
    
    Outputs: 
    
    Last Revised: April 2nd, 2019
    """
    
    import numpy as np
    import pandas as pd
    import sys
    import os
    
    sys.path.append(codeDir)
    
    # Load the baseline csv file    
    baseFileStr = ("baselineInfo.csv")
    
    # Determine the number of file IDs used in baseline calculations
    allBaseFiles = pd.read_csv(rootDir + baseFileStr)
    allBaseFiles['fileIDs'] = allBaseFiles['fileIDs'].str[2:17]
    
    uniqueBaseFiles = list(set(allBaseFiles.iloc[:,0]))
    uniqueBaseFiles = np.sort(uniqueBaseFiles)   # sort to ascending order
    
    allEventBaseFiles = list(allBaseFiles.iloc[:,0])
    allEventBaseFiles = np.sort(allEventBaseFiles)   # sort to ascending order
    
    # Determine the number of unique file dates used in baseline calculations
    allDays = pd.read_csv(rootDir + baseFileStr)
    allDays['fileIDs'] = allDays['fileIDs'].str[2:8]
    
    uniqueDays = list(set(allDays.iloc[:,0]))
    uniqueDays = np.sort(uniqueDays)   # sort to ascending order
    
    # Create the list of all processed csv data files
    allProcDataFiles = []
    for files in os.listdir(rootDir):
        if files.endswith('ProcData.csv'):
             allProcDataFiles.append(files)
             
    allProcDataFiles = [snip[0:15] for snip in allProcDataFiles]
    allProcDataFiles = np.sort(allProcDataFiles)   # sort to ascending order
    
    fs = 30;
    uniqueDayArray = pd.DataFrame()
    for a in range(len(uniqueDays)):
        day = uniqueDays[a]
        uniqueDayData = pd.DataFrame()
        for b in range(len(uniqueBaseFiles)):
            uniqueBaseFile = uniqueBaseFiles[b]
            if day == uniqueBaseFile[0:6]:
                baseFileEventArray = pd.DataFrame()
                for c in range(len(allEventBaseFiles)):
                    eventBaseFile = allEventBaseFiles[c]
                    if uniqueBaseFile == eventBaseFile:
                        for d in range(len(allProcDataFiles)):
                            procDataFile = allProcDataFiles[d]
                            if eventBaseFile == procDataFile:
                                baseData = pd.read_csv(rootDir + procDataFile + '_ProcData.csv')
                                baseData = baseData.drop(columns = 'Unnamed: 0')
                                startTime = int((allBaseFiles.loc[c,'eventTimes'])*fs)
                                endTime = int(startTime + (allBaseFiles.loc[c, 'durations'])*fs)
                                eventMeanArray = pd.DataFrame()
                                for e in range(np.shape(baseData)[1]):
                                    eventMean = pd.DataFrame.mean(baseData.iloc[startTime:endTime, e])
                                    eventMean = pd.DataFrame([eventMean])
                                    eventMeanArray = pd.concat([eventMeanArray, eventMean], axis = 1, ignore_index = True)
                                baseFileEventArray = pd.concat([baseFileEventArray, eventMeanArray], axis = 0, ignore_index = True)   
                baseFileEventArrayMean = pd.DataFrame.mean(baseFileEventArray, axis = 0)
                baseFileEventArrayMean = pd.Series.to_frame(baseFileEventArrayMean)
                baseFileEventArrayMean = baseFileEventArrayMean.T
                uniqueDayData = pd.concat([uniqueDayData, baseFileEventArrayMean], axis = 0, ignore_index = True)
        uniqueDayDataMean = pd.DataFrame.mean(uniqueDayData, axis = 0)               
        uniqueDayDataMean = pd.Series.to_frame(uniqueDayDataMean)
        uniqueDayDataMean = uniqueDayDataMean.T
        uniqueDayArray = pd.concat([uniqueDayArray, uniqueDayDataMean], axis = 0, ignore_index = True)
        
    for f in range(len(uniqueDayArray)):
        uniqueDayArray = uniqueDayArray.rename({f: uniqueDays[f]}, axis = 'index')
        
    variableNames = list(baseData.columns.values)    
    for g in range(len(variableNames)):
        uniqueDayArray = uniqueDayArray.rename({g: variableNames[g]}, axis = 'columns')
    
    return uniqueDayArray

def NormalizeData(rootDir, codeDir, uniqueDayArray):
    """
    Written by Kevin L. Turner 
    
    Purpose: filter and resample date based on dataType
        
    Inputs: raw data array
    
    Outputs: processed data array
    
    Last Revised: April 2nd, 2019
    """
    
    import numpy as np
    import pandas as pd
    import sys
    import os
    
    sys.path.append(codeDir)
    from GraphData import GraphData
        
    # Load the baseline csv file    
    baseFileStr = ("baselineInfo.csv")
        
    # Determine the number of unique file dates used in baseline calculations
    allDays = pd.read_csv(rootDir + baseFileStr)
    allDays['fileIDs'] = allDays['fileIDs'].str[2:8]
    uniqueDays = list(set(allDays.iloc[:,0]))
    uniqueDays = np.sort(uniqueDays)   # sort to ascending order
    
    # Create the list of all processed csv data files
    allProcDataFiles = []
    for files in os.listdir(rootDir):
        if files.endswith('ProcData.csv'):
             allProcDataFiles.append(files)
             
    allProcDataFiles = [snip[0:15] for snip in allProcDataFiles]
    allProcDataFiles = np.sort(allProcDataFiles)   # sort to ascending order
    
    for a in range(len(allProcDataFiles)):
        procDataFile = allProcDataFiles[a]
        print("\n\nNormalizing data from file number", a, "->", procDataFile)
        procData = pd.read_csv(rootDir + procDataFile + '_ProcData.csv')
        procData = procData.drop(columns = 'Unnamed: 0')
        day = procDataFile[0:6]
        baseData = uniqueDayArray.loc[[day]]
        dataTypes = list(baseData.columns.values)  
        normData = pd.DataFrame()
        for b in range(len(dataTypes)):
            dataType = dataTypes[b]
            if dataType == 'forceSensor' or dataType == 'whiskerAngle':
                normArray = procData.loc[:, dataType]
                normArray = pd.Series.to_frame(normArray)
            else:
                baseVal = baseData.loc[:, dataType]
                dataArray = procData.loc[:, dataType]
                normArray = (dataArray - float(baseVal)) / float(baseVal)
                normArray = pd.Series.to_frame(normArray)
            normData = pd.concat([normData, normArray], axis = 1)
        GraphData(normData, procDataFile, rootDir, 'Norm')
        normData.to_csv(rootDir + procDataFile + '_Normata.csv')
                    
    return