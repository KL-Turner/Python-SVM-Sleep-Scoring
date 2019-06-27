"""
Written by Christina Echagarruga and Kevin L. Turner

Purpose: apply all the necessary pre-processing steps for the matlab -> python workflow to sleep score
    
Inputs: n matlab files with the extension PythonData.mat, and one file titled animalNotes_baselines.mat with the time indeces
        and filenames for resting baseline calculation and subsequent normalization.

Outputs: two csv files, one with the processed data and one with the normalized data from respective resting baselines.
         one csv file which is essentially the excel version of the animalNotes_baselines structure.
         two subplot pdfs, one for the raw data and one for the normalized data.

Last Revised: April 2nd, 2019
"""

from PreProcData import ConvMAT2CSV
from PreProcData import CalcRestingBaselines
from PreProcData import NormalizeData

# edit data and code directory respectively
rootDir = '/Users/kevinturner/Documents/Jupyter Sleep Scoring/'
codeDir = '/Users/kevinturner/Documents/Core-Analysis/Spyder/'

# convert the matlab file with all the raw data into a csv file. resample it down to 30 hz and apply the necessary filters for the
# respective signals. create a subplot figure showing the raw data.
ConvMAT2CSV(rootDir, codeDir)

# use the start:end time indeces for the baseline files to find the resting baseline for each parameter per day.
uniqueDayArray = CalcRestingBaselines(rootDir, codeDir)

# apply the baseline values for each unique day to each respective signal. create a subplot showing the normalized data.
# save a csv file with the normalized values
NormalizeData(rootDir, codeDir, uniqueDayArray)
