%________________________________________________________________________________________________________________________
% Written by Kevin L. Turner
% The Pennsylvania State University, Dept. of Biomedical Engineering
% https://github.com/KL-Turner
%________________________________________________________________________________________________________________________
%
%   Purpose: Organize the data into simplified strucutres only containing the parameters of interest.
%________________________________________________________________________________________________________________________
%
%   Inputs: RestingBaselines.mat file containing indeces and filesnames of the resting periods in the first 30 min.
%           List of all RawData.mat files in the current directory.
%
%   Outputs: animalNotes.mat file with relevant imaging information.
%            PythonData.mat file(s) corresponding to each 5 minute session's unique file ID.
%
%   Last Revised: February 25th, 2019    
%________________________________________________________________________________________________________________________

%% BLOCK PURPOSE: [0] Load the script's necessary variables and data structures.
% Clear the workspace variables and command window.
clc;
clear;

RestingBaselinesFile = dir('*_RestingBaselines.mat');   % Load the RestingBaselines struct.
if ~isempty(RestingBaselinesFile)
    load(RestingBaselinesFile.name);
else
    RestingBaselines = [];
end

rawDirectory = dir('*_RawData.mat');   % Pull a list of all RawData.mat files in this folder.
rawDataFiles = {rawDirectory.name}';
rawDataFiles = char(rawDataFiles);

%% BLOCK PURPOSE: [1] Create a notes file with all relevent info needed for this project.
disp('Creating an animalNotes file containing relevant experiment information.'); disp(' ');
animalNotes.baselines.fileIDs = RestingBaselines.baselineFileInfo.fileIDs;         % List of files with valid rest times
animalNotes.baselines.eventTimes = RestingBaselines.baselineFileInfo.eventTimes;   % Times rest periods start
animalNotes.baselines.durations = RestingBaselines.baselineFileInfo.durations;     % Duration of resting period
animalNotes.baselines.targetMinutes = RestingBaselines.targetMinutes;   % Only files considered are first 30 minutes of each day
animalNotes.baselines.restMinimum_sec = 10;      % All rest periods are >= 10 sec
animalNotes.animalID = 'T61';                    % Animal's name tag
animalNotes.samplingRates.forceSensor = 20000;   % All 'animalNotes.samplingRates are 'Fs' in Hz
animalNotes.samplingRates.neural = 20000;        
animalNotes.samplingRates.EMG = 20000;
animalNotes.samplingRates.whiskerCam = 150;
animalNotes.trialDuration_sec = 300;             % 5 minute (300 seconds) per file.
animalNotes.amplifierGain.neural = 10000;        % amp gains
animalNotes.amplifierGain.EMG = 10000;
animalNotes.amplifierGain.forceSensor = 50;
animalNotes.amplifierGain.whiskerCam = NaN;

[pathstr, ~, ~] = fileparts(cd);       % Create.Save to Python Data folder
dirpath = [pathstr '/Python Data/']; 

if ~exist(dirpath, 'dir')
    mkdir(dirpath);
end

save([dirpath 'animalNotes'], 'animalNotes')

%% BLOCK PURPOSE: [2] Extract important raw data from each file, trim excess or pad missing frames with zeros.
disp('Converting RawData files to PythonData files.'); disp(' ');
expectedWhiskLength = animalNotes.trialDuration_sec*animalNotes.samplingRates.whiskerCam;   % 150 Hz * 300 seconds
expectedAnalogLength = animalNotes.trialDuration_sec*animalNotes.samplingRates.neural;   % 20000 Hz * 300 seconds, same for all analog signals

for f = 1:length(rawDataFiles)   % Loop through the list of all RawData.mat files
    rawDataFile = rawDataFiles(f, :);   % designate file in row and load into workspace
    load(rawDataFile)
    [~, ~, ~, fileID] = GetFileInfo(rawDataFile);
    disp(['Creating PythonData file ' num2str(f) ' of ' num2str(size(rawDataFiles, 1)) '...']); disp(' ');
    
    % Find the difference between the expected length of the analog signal and trim any excess data
    % Rarely, the last packet gets dropped and a very small (< 100) of the last 20,000 samples doesn't get saved
    % In this instance, duplicate the last value of the signal for the remaining few samples to meet the end length
    % as it was the last packet that was lost and there's no way to accurately extrapolate the data.
    if length(RawData.Data.EMG) < expectedAnalogLength
        endPad_rawNeural_LH = (ones(1, (expectedAnalogLength - length(RawData.Data.Neural_LH))))*RawData.Data.Neural_LH(end);
        endPad_rawNeural_RH = (ones(1, (expectedAnalogLength - length(RawData.Data.Neural_RH))))*RawData.Data.Neural_RH(end);
        endPad_forceSensor = (ones(1, (expectedAnalogLength - length(RawData.Data.Force_Sensor))))*RawData.Data.Force_Sensor(end);
        endPad_EMG = (ones(1, (expectedAnalogLength - length(RawData.Data.EMG))))*RawData.Data.EMG(end);
        PythonData.rawNeural_LH = horzcat(RawData.Data.Neural_LH, endPad_rawNeural_LH);
        PythonData.rawNeural_RH = horzcat(RawData.Data.Neural_RH, endPad_rawNeural_RH);
        PythonData.forceSensor = horzcat(RawData.Data.Force_Sensor, endPad_forceSensor);
        PythonData.EMG = horzcat(RawData.Data.EMG, endPad_EMG);
    else
        PythonData.rawNeural_LH = RawData.Data.Neural_LH(1:expectedAnalogLength);
        PythonData.rawNeural_RH = RawData.Data.Neural_RH(1:expectedAnalogLength);
        PythonData.forceSensor = RawData.Data.Force_Sensor(1:expectedAnalogLength);
        PythonData.EMG = RawData.Data.EMG(1:expectedAnalogLength);
    end
    
    % Occassionally a few frames get dropped throughout the trial - pad the end with zeros to account for any
    % missing frames. The ideal solution here is to interpolate inbetween the indeces surrounding each missed frame(s),
    % Nonetheless, the amount of dropped frames is typically very low (< 10 for the entire 300 seconds)
    % and at a sampling rate of 150 Hz this is almost certainly not significant.
    if length(RawData.Data.WhiskerAngle) < expectedWhiskLength
        zeroPad = zeros(1, (expectedWhiskLength - length(RawData.Data.WhiskerAngle)));
        PythonData.whiskerAngle = horzcat(RawData.Data.WhiskerAngle, zeroPad);
    else
        PythonData.whiskerAngle = RawData.Data.WhiskerAngle(1:expectedWhiskLength);
    end
    
    % Save to Python Data folder
    save([dirpath fileID '_PythonData'], 'PythonData')
end
