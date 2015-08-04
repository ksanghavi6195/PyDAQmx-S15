'''
This function uses Python to only send an input signal. syncTestOut.py will send a signal.
Syncing the two functions, one to send a signal and one to listen for a signal, is an issue
'''

from PyDAQmx import *
import numpy as np
import matplotlib.pyplot as plot

taskHandleIn = TaskHandle()

log_rate = 20000
seconds = 3
N_samples = log_rate * seconds
timeout = 30.0
num_trials = 1

dataIn = np.zeros((2*log_rate+N_samples,), dtype=np.float64)
read1 = int32()

DAQmxCreateTask("", byref(taskHandleIn))
DAQmxCreateAIVoltageChan(taskHandleIn, "Dev4/audioInputLeft", "Read1", DAQmx_Val_RSE, -2.0, 2.0, DAQmx_Val_Volts, None)
DAQmxCfgSampClkTiming(taskHandleIn, "", 2*log_rate, DAQmx_Val_Rising, DAQmx_Val_ContSamps, len(dataIn))
DAQmxReadAnalogF64(taskHandleIn, len(dataIn), timeout, DAQmx_Val_GroupByChannel, dataIn, len(dataIn), byref(read1), None)
