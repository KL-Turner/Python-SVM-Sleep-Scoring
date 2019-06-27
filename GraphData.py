def GraphData(allData, fileStr, rootDir, gType):
    """
    Written by Kevin L. Turner 
    
    Purpose: create a plot of the filtered and resampled data
        
    Inputs: dataTypes and data arrays
    
    Outputs: saves figure to rootDir
    
    Last Revised: March 25th, 2019
    """
    import matplotlib.pyplot as plt
    import numpy as np 
    
    # time vector that is 300 seconds long (5 min) with 30 Hz divisions
    t = np.arange(0, 300, 1/30)    
    
    ax1 = plt.subplot(3,2,1)
    plt.plot(t, allData.iloc[:,8], color = 'k')
    plt.setp(ax1.get_xticklabels(), fontsize = 5)
    plt.title('Whisker angle', fontsize = 10)
    plt.ylabel('Degrees \n(protraction)')
    plt.subplots_adjust(hspace = 1, wspace = 0.5)
    
    plt.subplot(3,2,2, sharex = ax1)
    plt.setp(ax1.get_xticklabels(), fontsize = 5)
    plt.plot(t, allData.iloc[:,0], color = 'k', label = 'LH')
    plt.plot(t, allData.iloc[:,3], color = 'tab:orange', label = 'RH')
    plt.title('Delta power', fontsize = 10)
    plt.ylabel(r'$Power (V^2$)')
    plt.legend(fontsize = 5, loc = 'upper right')
    plt.subplots_adjust(hspace = 1, wspace = 0.5)
    
    plt.subplot(3,2,3, sharex = ax1)
    plt.plot(t, allData.iloc[:,6], color = 'k')
    plt.setp(ax1.get_xticklabels(), fontsize = 5)
    plt.title('Force Sensor', fontsize = 10)
    plt.ylabel('Volts (V))')
    plt.subplots_adjust(hspace = 1, wspace = 0.5)
    
    plt.subplot(3,2,4, sharex = ax1)
    plt.setp(ax1.get_xticklabels(), fontsize = 5)
    plt.plot(t, allData.iloc[:,1], color = 'k', label = 'LH')
    plt.plot(t, allData.iloc[:,4], color = 'tab:orange', label = 'RH')
    plt.title('Theta power', fontsize =10)
    plt.ylabel(r'$Power (V^2$)')
    plt.legend(fontsize = 5, loc = 'upper right')
    plt.subplots_adjust(hspace = 1, wspace = 0.5)
    
    plt.subplot(3,2,5, sharex = ax1)
    plt.plot(t, allData.iloc[:,7], color = 'k')
    plt.setp(ax1.get_xticklabels(), fontsize = 5)
    plt.title('EMG', fontsize = 10)
    plt.xlabel('Time (sec)')
    plt.ylabel('Volts (V))')
    plt.subplots_adjust(hspace = 1, wspace = 0.5)
    
    plt.subplot(3,2,6, sharex = ax1)
    plt.setp(ax1.get_xticklabels(), fontsize = 5)
    plt.plot(t, allData.iloc[:,2], color = 'k', label = 'LH')
    plt.plot(t, allData.iloc[:,5], color = 'tab:orange', label = 'RH')
    plt.title('Gamma power', fontsize = 10)
    plt.xlabel('Time (sec)')
    plt.ylabel(r'$Power (V^2$)')
    plt.legend(fontsize = 5, loc = 'upper right')
    plt.subplots_adjust(hspace = 1, wspace = 0.5)
    
    plt.savefig(rootDir+fileStr+'_' + gType + 'Data.pdf')
    plt.show()
    
    return