'''
This function uses Python to interact with NI myDAQ by using the PyDAQmx library.
A sinusoidal wave is generated using numpy and the DAQ sends this signal via the Audio Output channel. 
Then, the Audio Input channel recieves the signal. This process is repeated for num_trials and the recieved
signals are averaged.
At the moment, a signal is sent, then a signal is recieved, resulting in not-synchronous data collection.
'''

from __future__ import division
from PyDAQmx import *
import numpy as np
import time
import matplotlib.pyplot as plot
numpy.set_printoptions(threshold='inf') #eliminates '...' when printing large numpy array

# Check Measurment and Automation Explorer for device and channel names
devNameIn = 'Dev1'
chanNameIn = 'audioInputLeft'
devNameOut = 'Dev1'
chanNameOut = 'audioOutputLeft'

log_rate = 20000
seconds = 3
N_samples = log_rate * seconds
timeout = 30.0
num_trials = 1

def generateWave(length):
	# Generate a sinusoidal array to be sent
	return np.sin(np.linspace(0, 180, num=length))

def normalize(listIn):
	# Normalize the waveform that is generated
	normalized = listIn / np.max(np.abs(listIn), axis = 0)
	return normalized

def signalOut(dataOut, taskHandleOutput, read):
	# Send signal from myDAQ
	DAQmxWriteAnalogF64(taskHandleOutput, N_samples, True, -1, DAQmx_Val_GroupByChannel, dataOut, byref(read), None)
	DAQmxStopTask(taskHandleOutput)
	
def signalIn(length, taskHandleInput, read):
	# Recieve a signal from myDAQ
	dataIn = np.zeros((length,), dtype = np.float64)
	DAQmxReadAnalogF64(taskHandleInput, length, timeout, DAQmx_Val_GroupByChannel, dataIn, length, byref(read), None)
	DAQmxStopTask(taskHandleInput)
	return dataIn

def average(numpyList):
	# Uses built in numpy operation to average the results from all trials
	return np.average(numpyList, axis=0)

def plotGraphs(N_samples, waveGen, averagedArray, waveRecieved):
	# Plots graphs using matlibplot library
	xAxis = range(N_samples)
	plot.plot(xAxis, waveGen, 'r-', label="Wave Sent")
	plot.plot(xAxis, averagedArray, 'g-', label="Average Wave Recieved")
	plot.legend()
	plot.show()
	
def run():
	# Calls for a wave generation
	waveGen = generateWave(N_samples)
	# Initialize a 2D array which will be populated with data
	signalLength = len(waveGen)
	allTrials = np.zeros(signalLength)

	# Initialize task to handle output signals from myDAQ
	taskHandleOutput = TaskHandle()
	read = int32()
	DAQmxCreateTask("", byref(taskHandleOutput))
	DAQmxCreateAOVoltageChan(taskHandleOutput, "%s/%s" % (devNameOut, chanNameOut), "Output Channel", -2.0, 2.0, DAQmx_Val_Volts, None)
	DAQmxCfgSampClkTiming(taskHandleOutput, "", log_rate, DAQmx_Val_Rising, DAQmx_Val_ContSamps, N_samples)

	# Initalize task to handle input signals from myDAQ
	taskHandleInput = TaskHandle()
	DAQmxCreateTask("", byref(taskHandleInput))
	DAQmxCreateAIVoltageChan(taskHandleInput, "%s/%s" % (devNameIn, chanNameIn), "Input Channel", DAQmx_Val_RSE, -2.0, 2.0, DAQmx_Val_Volts, None)
	DAQmxCfgSampClkTiming(taskHandleInput, "", 2*log_rate, DAQmx_Val_Rising, DAQmx_Val_ContSamps, N_samples)

	# Iterate sending and recieving signals. Keep track of all trials
	for trials in xrange(num_trials):
		# Send signal
		signalOut(waveGen, taskHandleOutput, read)
		# Recieve signal
		waveRecieved = signalIn(N_samples, taskHandleInput, read)
		# Add recieved data to 2D array
		allTrials = np.vstack((allTrials, waveRecieved))
	
	# Remove initial line of zeros and average data
	allTrials = numpy.delete(allTrials, 0, 0)	
	averagedArray = average(allTrials)

	# Write data to a CSV file
	numpy.savetxt('test.csv', np.vstack((allTrials, averagedArray)).transpose() , delimiter=',')

	# Plot data
	plotGraphs(N_samples, waveGen, averagedArray, waveRecieved)

run()
