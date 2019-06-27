def GraphProcData_v3(allData, fileStr, rootDir,state):
    """
    Written by Kevin L. Turner 
    
    Purpose: create a plot of the filtered and resampled data
        
    Inputs: dataTypes and data arrays
    
    Outputs: saves figure to rootDir
    
    Last Revised: March 6th, 2019
    """
    import tkinter as tk
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    import numpy as np 
    
    def Wake_ret():
        state.append("W")
        master.destroy()
        return state
    def REM_ret():
        state.append("S")
        master.destroy()
        return state
    def NREM_ret():
        state.append("S")
        master.destroy()
        return state
    def Transition_ret():
        state.append("T")
        master.destroy()
        return state
    
    
    master = tk.Tk()
    
    master.title("Manual Sleep Scoring")
    l = tk.Label(master,text="Choose state")
    
    b1 = tk.Button(master, text="Wake",command=Wake_ret)
    b2 = tk.Button(master, text="REM",command=REM_ret)
    b3 = tk.Button(master, text="NREM",command=NREM_ret)
    b4 = tk.Button(master, text="Transition",command=Transition_ret)
    
    l.pack()
    b1.pack()
    b2.pack()
    b3.pack()
    b4.pack()
    

    figure = Figure(figsize=(10,8), dpi=100)
    
    chart_type = FigureCanvasTkAgg(figure, master)
    chart_type.get_tk_widget().pack()

    
    
    # time vector that is 300 seconds long (5 min) with 30 Hz divisions
    t = np.arange(0, 300, 1);

    ax1 = figure.add_subplot(3,2,1);
    ax1.plot(t, allData.iloc[:,9]);
    ax1.xaxis.set_tick_params(size = 6);
    ax1.set_title('Whisker angle');
    ax1.set_ylabel('Degrees \n(protraction)');
    ax1.set_ylim([-30, 30]);
    #ax1.subplots_adjust(hspace = 1, wspace = 0.5);
    
    ax2 = figure.add_subplot(3,2,2, sharex = ax1);
    #plt.setp(ax1.get_xticklabels(), fontsize = 6);
    ax2.plot(t, allData.iloc[:,1], color = 'k');
    ax2.plot(t, allData.iloc[:,4], color = 'tab:orange');
    ax2.set_title('Delta band power');
    ax2.set_ylabel(r'$Power (V^2$)');
    ax2.set_ylim([-5, 20]);
    #plt.legend((allData.iloc[:,0], allData.iloc[:,3]), ('LH', 'RH'));
    #plt.subplots_adjust(hspace = 1, wspace = 0.5);
    
    ax3 = figure.add_subplot(3,2,3, sharex = ax1);
    ax3.plot(t, allData.iloc[:,7]);
    #plt.setp(ax1.get_xticklabels(), fontsize = 6);
    ax3.set_title('Force Sensor');
    ax3.set_ylabel('Volts (V))');
    ax3.set_ylim([-0.7, 0.7])
    #plt.subplots_adjust(hspace = 1, wspace = 0.5);
    
    ax4 = figure.add_subplot(3,2,4, sharex = ax1);
    #plt.setp(ax1.get_xticklabels(), fontsize = 6);
    ax4.plot(t, allData.iloc[:,2], color = 'k');
    ax4.plot(t, allData.iloc[:,5], color = 'tab:orange');
    ax4.set_title('Theta band power');
    ax4.set_ylabel(r'$Power (V^2$)');
    ax4.set_ylim([-5, 20]);
    #plt.legend((allData.iloc[:,1], allData.iloc[:,4]), ('LH', 'RH'));
    #plt.subplots_adjust(hspace = 1, wspace = 0.5);
    
    ax5 = figure.add_subplot(3,2,5, sharex = ax1);
    ax5.plot(t, allData.iloc[:,8]);
    #plt.setp(ax1.get_xticklabels(), fontsize = 6);
    ax5.set_title('EMG');
    ax5.set_xlabel('Frames');
    ax5.set_ylabel('Volts (V))');
    ax5.set_ylim([-5, 4000]);
    #plt.subplots_adjust(hspace = 1, wspace = 0.5);
    
    ax6 = figure.add_subplot(3,2,6, sharex = ax1);
    #plt.setp(ax1.get_xticklabels(), fontsize = 6);
    ax6.plot(t, allData.iloc[:,3], color = 'k');
    ax6.plot(t, allData.iloc[:,6], color = 'tab:orange');
    ax6.set_title('Gamma band power');
    ax6.set_xlabel('Frames');
    ax6.set_ylabel(r'$Power (V^2$)');
    ax6.set_ylim([-5, 30]);
    #plt.legend((allData.iloc[:,2], allData.iloc[:,6]), ('LH', 'RH'));
    #plt.subplots_adjust(hspace = 1, wspace = 0.5);
    
    #plt.savefig(rootDir+fileStr+'_ResampFiltData.pdf');
    #plt.show();
    
    master.mainloop()
    
    return state;
