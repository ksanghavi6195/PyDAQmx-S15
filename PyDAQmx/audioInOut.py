'''
This function uses Python to interact with NI myDAQ using the library PyDAQmx. 
The DAQ device will use its audio Input and Output terminals to listen for signals and regenerate them, respectively.
Data is plotted to show the signals recieved in the right and left audio channels.
'''

import numpy as np
from PyDAQmx import *
import matplotlib.pyplot as plt
import time
numpy.set_printoptions(threshold='inf') #eliminates '...' when printing large numpy array

log_rate = 400
seconds = 3
N_samples = log_rate * seconds
timeout = 30.0
read = int32()

# Create one task handle to acquire data and one to write data
taskHandleInput = TaskHandle()
taskHandleOutput = TaskHandle()

# initialize the variable which will be written to
data = np.zeros((2*N_samples,), dtype=np.float64)

DAQmxCreateTask("", byref(taskHandleInput))
DAQmxCreateTask("", byref(taskHandleOutput))

DAQmxCreateAIVoltageChan(taskHandleInput, "Dev4/audioInputLeft", "LVDT", DAQmx_Val_RSE, -2.0, 2.0, DAQmx_Val_Volts, None)
DAQmxCreateAIVoltageChan(taskHandleInput, "Dev4/audioInputRight", "RVDT", DAQmx_Val_RSE, -2.0, 2.0, DAQmx_Val_Volts, None)
DAQmxCfgSampClkTiming(taskHandleInput, "", log_rate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps, N_samples)

# Start the task of acquiring data
DAQmxStartTask(taskHandleInput)
DAQmxReadAnalogF64(taskHandleInput, N_samples, timeout, DAQmx_Val_GroupByChannel, data, 2*N_samples, byref(read), None)

# Create output channels for writing data
DAQmxCreateAOVoltageChan(taskHandleOutput, "Dev4/audioOutputLeft", "LVDTO", -2.0, 2.0, DAQmx_Val_Volts, None)
DAQmxCreateAOVoltageChan(taskHandleOutput, "Dev4/audioOutputRight", "LVDTO2", -2.0, 2.0, DAQmx_Val_Volts, None)

# Create required timer
DAQmxCfgSampClkTiming(taskHandleOutput, "",  log_rate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps, N_samples)
DAQmxWriteAnalogF64(taskHandleOutput, N_samples, True, timeout, DAQmx_Val_GroupByChannel, data, byref(read), None)

plt.plot(range(N_samples), data[0:N_samples], 'b-', range(N_samples), data[N_samples:2*N_samples], 'r-')

plt.show()
