import numpy as np
from PyDAQmx import *
import matplotlib.pyplot as plt
numpy.set_printoptions(threshold='inf')

N_samples = 20*5
log_rate = 20.0 #Hz
# length = 3 #seconds
# N_samples = length * log_rate
timeout = 30
read = int32()
# Initialize data array to be written to
data = np.zeros((N_samples,2), dtype=np.float64)
data2 = np.zeros((N_samples,1), dtype=np.uint8)

#Start Input task
taskHandleAnIn = TaskHandle()
DAQmxCreateTask("", byref(taskHandleAnIn))
DAQmxCreateAIVoltageChan(taskHandleAnIn, "Dev1/audioInputLeft", "LVDT", DAQmx_Val_RSE, -2.0, 2.0, DAQmx_Val_Volts, None)
DAQmxCreateAIVoltageChan(taskHandleAnIn, "Dev1/audioInputRight", "RVDT", DAQmx_Val_RSE, -2.0, 2.0, DAQmx_Val_Volts, None)
# DAQmxCfgSampClkTiming(taskHandleAnIn, "", log_rate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps, N_samples)
# DAQmxStartTask(taskHandleAnIn)
# DAQmxReadAnalogF64(taskHandleAnIn, N_samples, timeout, DAQmx_Val_GroupByScanNumber, data, 2*N_samples, byref(read), None)

# print type(data2), type(data2[0]), type(data)

LP_c_long = POINTER(c_long)
a = LP_c_long()
print a, type(a)

taskHandleDigIn = TaskHandle()
DAQmxCreateTask("", byref(taskHandleDigIn))
DAQmxCreateDIChan(taskHandleDigIn, "Dev1/port0/line1", "DigIn", DAQmx_Val_ChanPerLine)
DAQmxReadDigitalLines(taskHandleDigIn, N_samples, timeout, DAQmx_Val_GroupByScanNumber, data2, N_samples, byref(read), a, None)

print data2