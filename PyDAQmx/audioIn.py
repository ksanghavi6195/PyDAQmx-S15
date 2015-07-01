from PyDAQmx import *
import numpy

analog_input = Task()
read = int32()
data = numpy.zeros((10,), dtype=numpy.float64)

# DAQmx Configure Code
analog_input.CreateAIVoltageChan("Dev1/audioInputLeft","inputLeft",DAQmx_Val_Cfg_Default,-2.0,2.0,DAQmx_Val_Volts,None)
# analog_input.CreateAIVoltageChan("Dev1/audioInputRight","inputRight",DAQmx_Val_Cfg_Default,-2.0,2.0,DAQmx_Val_Volts,None)
analog_input.CfgSampClkTiming("",10000.0,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,10)

# DAQmx Start Code
analog_input.StartTask()

# DAQmx Read Code
analog_input.ReadAnalogF64(10,10.0,DAQmx_Val_GroupByChannel,data,10,byref(read),None)

print "Acquired %d points"%read.value
print data