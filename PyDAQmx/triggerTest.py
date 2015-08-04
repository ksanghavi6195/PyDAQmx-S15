from PyDAQmx import *
import numpy as np

log_rate = 2000
seconds = 2
N_samples = log_rate * seconds
timeout = 30.0
num_trials = 1

genData = np.sin(np.linspace(0, 180, num=N_samples) * np.pi / 180)
dataWrite = np.zeros(N_samples)

read = int32()

taskHandleInput = TaskHandle()
DAQmxCreateTask("", byref(taskHandleInput))
DAQmxCreateAIVoltageChan(taskHandleInput, "Dev4/audioInputLeft", "LVDT", DAQmx_Val_RSE, -2.0, 2.0, DAQmx_Val_Volts, None)
DAQmxCfgSampClkTiming(taskHandleInput, "", 2*log_rate, DAQmx_Val_Rising, DAQmx_Val_ContSamps, N_samples)

taskHandleOutput = TaskHandle()
DAQmxCreateTask("", byref(taskHandleOutput))
DAQmxCreateAOVoltageChan(taskHandleOutput, "Dev4/audioOutputLeft", "LVDTO", -2.0, 2.0, DAQmx_Val_Volts, None)
DAQmxCfgSampClkTiming(taskHandleOutput, "", log_rate, DAQmx_Val_Rising, DAQmx_Val_ContSamps, N_samples)

# DAQmxCfgAnlgWindowStartTrig(taskHandleInput, "Dev4/audioOutputLeft", DAQmx_Val_EnteringWin, 0.95, 0.85)

DAQmxWriteAnalogF64(taskHandleOutput, N_samples, True, -1, DAQmx_Val_GroupByChannel, genData, byref(read), None)
DAQmxReadAnalogF64(taskHandleInput, N_samples, timeout, DAQmx_Val_GroupByChannel, dataWrite, N_samples, byref(read), None)



