'''
This function uses Python to only send an output signal. syncTestIn.py will recieve a signal.
Syncing the two functions, one to send a signal and one to listen for a signal, is an issue
'''

from PyDAQmx import *
import numpy as np
import matplotlib.pyplot as plot

log_rate = 20000
seconds = 3
N_samples = log_rate * seconds
timeout = 30.0
num_trials = 1

taskHandle1 = TaskHandle()
write = int32()

def normalize(listIn):
	# Normalize the waveform that is generated
	normalized = listIn / np.max(np.abs(listIn), axis = 0)
	return normalized

# Generate wave with buffer 0s before and after the desired signal
waveGen = normalize(np.sin(np.linspace(0, 180, num=N_samples)))
waveGen = np.append(np.zeros(log_rate), waveGen)
waveGen = np.append(waveGen, np.zeros(log_rate))
signalLength = len(waveGen)

DAQmxCreateTask("", byref(taskHandle1))
DAQmxCreateAOVoltageChan(taskHandle1, "Dev4/audioOutputLeft", "Generator", -2.0, 2.0, DAQmx_Val_Volts, None)
DAQmxCfgSampClkTiming(taskHandle1, "", log_rate, DAQmx_Val_Rising, DAQmx_Val_ContSamps, signalLength)

DAQmxWriteAnalogF64(taskHandle1, 3*signalLength, True, -1, DAQmx_Val_GroupByChannel, np.tile(waveGen,3), byref(write), None)
