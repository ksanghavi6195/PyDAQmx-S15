from __future__ import division
from PyDAQmx import *
import numpy as np
import matplotlib.pyplot as plt


log_rate = 1
seconds = 5
N_samples = log_rate * seconds

num_trials = 2

def generateWave(length):
	# Generate an array to be sent
	return np.random.rand(length)

# TODO waveOut

def signalIn(length):
	# Recieve a signal from MyDAQ
	taskHandleInput = TaskHandle()
	read = int32()
	dataIn = np.zeros((length,), dtype = np.float64)
	DAQmxCreateTask("", byref(taskHandleInput))
	DAQmxCreateAIVoltageChan(taskHandleInput, "Dev1/audioInputLeft", "LVDT", DAQmx_Val_RSE, -2.0, 2.0, DAQmx_Val_Volts, None)
	DAQmxCfgSampClkTiming(taskHandleInput, "", log_rate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps, length)
	DAQmxStartTask(taskHandleInput)
	DAQmxReadAnalogF64(taskHandleInput, length, timeout, DAQmx_Val_GroupByChannel, dataIn, length, byref(read), None)
	return dataIn

def normalize(listIn):
	normalized = listIn / np.max(np.abs(listIn), axis = 0)
	return normalized

def average(numpyList):
	return np.average(numpyList, axis=0)

def plotGraphs(xAxis, yAxis, plotType):
	plt.plot(range(xAxis), yAxis, plotType)
	plt.show()
	
def run():
	waveGen = generateWave(N_samples)
	
	# TODO: Send an array which will be recieved

	# TryExcept here so function does not fail when not connected to DAQ
	try:
		waveRecieved = signalIn(N_samples)
		normalizedWave = normalize(waveRecieved)
	except:
		normalizedWave = normalize(waveGen)
	# initialize a numpy array which will be appended to
	allTrials = normalizedWave
	for remainingTrials in xrange(num_trials - 1):
		try:
			allTrials = np.vstack((allTrials, waveRecieved))
		except:
			allTrials = np.vstack((allTrials, normalizedWave))
	averagedArray = average(allTrials)
	plotGraphs(N_samples, averagedArray, 'bo')

run()