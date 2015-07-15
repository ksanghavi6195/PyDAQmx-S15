from __future__ import division
from PyDAQmx import *
import numpy as np
import matplotlib.pyplot as plot


log_rate = 20
seconds = 2
N_samples = log_rate * seconds
timeout = 30.0

num_trials = 3

def generateWave(length):
	# Generate an array to be sent
	return normalize(np.random.rand(length))

def signalOut(dataOut, taskHandleOutput, read):
	DAQmxWriteAnalogF64(taskHandleOutput, N_samples, True, -1, DAQmx_Val_GroupByChannel, dataOut, byref(read), None)
	# DAQmxWaitUntilTaskDone(taskHandleOutput, -1)
	DAQmxStopTask(taskHandleOutput)
	
def signalIn(length, taskHandleInput, read):
	# Recieve a signal from MyDAQ
	dataIn = np.zeros((length,), dtype = np.float64)
	# DAQmxStartTask(taskHandleInput)
	DAQmxReadAnalogF64(taskHandleInput, length, timeout, DAQmx_Val_GroupByChannel, dataIn, length, byref(read), None)
	DAQmxStopTask(taskHandleInput)
	return dataIn

def normalize(listIn):
	normalized = listIn / np.max(np.abs(listIn), axis = 0)
	return normalized

def average(numpyList):
	return np.average(numpyList, axis=0)

def plotGraphs(N_samples, waveGen, averagedArray):
	xAxis = range(N_samples)

	plot.plot(xAxis, waveGen, 'ro', xAxis, averagedArray, 'bo')
	plot.show()
	
def run():
	waveGen = generateWave(N_samples)
	allTrials = np.zeros(N_samples)
	print "waveGen", waveGen

	taskHandleOutput = TaskHandle()
	read = int32()
	DAQmxCreateTask("", byref(taskHandleOutput))
	DAQmxCreateAOVoltageChan(taskHandleOutput, "Dev1/audioOutputLeft", "LVDTO", -2.0, 2.0, DAQmx_Val_Volts, None)
	DAQmxCfgSampClkTiming(taskHandleOutput, "", log_rate, DAQmx_Val_Rising, DAQmx_Val_ContSamps, N_samples)

	taskHandleInput = TaskHandle()
	DAQmxCreateTask("", byref(taskHandleInput))
	DAQmxCreateAIVoltageChan(taskHandleInput, "Dev1/audioInputLeft", "LVDT", DAQmx_Val_RSE, -2.0, 2.0, DAQmx_Val_Volts, None)
	DAQmxCfgSampClkTiming(taskHandleInput, "", log_rate, DAQmx_Val_Rising, DAQmx_Val_ContSamps, N_samples)

	for trials in xrange(num_trials):
		print trials, 'start'
		signalOut(waveGen, taskHandleOutput, read)
		waveRecieved = normalize(signalIn(N_samples, taskHandleInput, read))
		print 'waveRecieved', waveRecieved
		allTrials = np.vstack((allTrials, waveRecieved))
		print trials, 'done'
	
	allTrials = numpy.delete(allTrials, 0, 0)
	print "allTrials"
	print allTrials	
	
	averagedArray = average(allTrials)
	print 'averagedArray', averagedArray

	numpy.savetxt('test.csv', np.vstack((allTrials, averagedArray)).transpose() , delimiter=',')

	plotGraphs(N_samples, waveGen, averagedArray)


run()