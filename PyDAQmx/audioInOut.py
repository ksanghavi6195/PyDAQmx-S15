import numpy as np
from PyDAQmx import *
import matplotlib.pyplot as plt
import time
numpy.set_printoptions(threshold='inf')

# Run time at 44000 Hz is exceptionally long. 22000 is better, but for quick simulations 100 Hz works
N_samples = 5*1
log_rate = 5.0
timeout = 30.0

time0 = time.time()
time0_1 = time.time() - time0
print 'start', time0_1

# Create one task handle to acquire data
taskHandleInput = TaskHandle()
# Create another task handle to write data
taskHandleOutput = TaskHandle()

time1 = time.time() - time0 - time0_1
print 'handles created', time1
read = int32()

# initialize the variable which will be written to
data = np.zeros((2*N_samples,), dtype=np.float64)
## CHANGE FROM 2 to 1


# Create one task to acquire, one to write data
DAQmxCreateTask("", byref(taskHandleInput))
DAQmxCreateTask("", byref(taskHandleOutput))

time2 = time.time() - time1 - time0
print 'tasks created', time2

# Create two input channels for the acquisition task - 
# PARAMS: (physicalChannel, nameToAssignToChnnel, terminalConfig, minVal, maxVal, units, customScaleName)
DAQmxCreateAIVoltageChan(taskHandleInput, "Dev1/audioInputLeft", "LVDT", DAQmx_Val_RSE, -2.0, 2.0, DAQmx_Val_Volts, None)
DAQmxCreateAIVoltageChan(taskHandleInput, "Dev1/audioInputRight", "RVDT", DAQmx_Val_RSE, -2.0, 2.0, DAQmx_Val_Volts, None)

time3 = time.time() - time2 - time0
print 'input channels created', time3

# Note: Device Name is unique for each piece of DAQ hardware. Find the name and replace it with "Dev1/..." 

# Create a required timer
# PARAMS: (taskHandle, source, rate, activeEdge, sampleMode, sampsPerChan)
DAQmxCfgSampClkTiming(taskHandleInput, "", log_rate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps, N_samples)

# Start the task of acquiring data
DAQmxStartTask(taskHandleInput)

time4 = time.time() - time3 - time0
print 'task started', time4
# PARAMS: (taskHandle, numSampsPerChan, timeout, fillMode, readArray, arraySizeInSamps, sampsPerChanRead, reserved)
DAQmxReadAnalogF64(taskHandleInput, N_samples, timeout, DAQmx_Val_GroupByChannel, data, 2*N_samples, byref(read), None)
	# GroupByScanNumber (interleaved) - first sample, left then right
	# GroupByChannelNumber - all left, then all right

time5 = time.time() - time4 - time0
print 'data written', time4

# Create output channels for writing data
# PARAMS: (taskHandleOutput, N_samples, 10.0, DAQmx_Val_GroupByChannel, data2, N_samples, byref(read), None)
DAQmxCreateAOVoltageChan(taskHandleOutput, "Dev1/audioOutputLeft", "LVDTO", -2.0, 2.0, DAQmx_Val_Volts, None)
DAQmxCreateAOVoltageChan(taskHandleOutput, "Dev1/audioOutputRight", "LVDTO2", -2.0, 2.0, DAQmx_Val_Volts, None)

time6 = time.time() - time5 - time0
print 'out channels created', time6

# Create required timer
DAQmxCfgSampClkTiming(taskHandleOutput, "",  log_rate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps, N_samples)

# Write output data
DAQmxWriteAnalogF64(taskHandleOutput, N_samples, True, timeout, DAQmx_Val_GroupByChannel, data, byref(read), None)
	# Set to write ByChannel so that audio is heard the way it should be

time7 = time.time() - time6 - time0
print 'out data written/plot start', time7 

print data
print 'left', data[0:N_samples]
print 'right', data[N_samples:2*N_samples]

# outLeft = []
# outRight = []
# for i in xrange(len(data)):
# 	outLeft = outLeft + [data[i][0]]
# 	outRight = outRight + [data[i][1]]

time8_1 = time.time() - time7 - time0
print 'outLeft/Right created', time8_1

if len(data) % 2 == 0:
	plt.plot(range(N_samples), data[0:N_samples], 'bo', range(N_samples), data[N_samples:2*N_samples], 'ro')


time8_2 = time.time() - time8_1 - time0
print 'plotted', time8_2

plt.show()
print 'plot was open for %fs' % (time.time() - time8_2 - time0)