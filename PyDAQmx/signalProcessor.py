from __future__ import division
from PyDAQmx import *
import numpy as np
import matplotlib.pyplot as plt


log_rate = 1
seconds = 5
N_samples = log_rate * seconds

num_trials = 2

def waveGen(length):
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
	waveGen0 = waveGen(N_samples)
	# TODO: Send array
	# waveRecieved = signalIn(N_samples)
	normalizedWave = normalize(waveGen0)
	allTrials = normalizedWave
	for remainingTrials in xrange(num_trials - 1):
		waveGenN = waveGen(N_samples)
		# TODO: Send array
		# waveRecieved = signalIn(N_samples)
		normalizedWave = normalize(waveGenN)
		allTrials = np.vstack((allTrials, normalizedWave))
	averagedArray = average(allTrials)
	plotGraphs(N_samples, averagedArray, 'bo')

run()