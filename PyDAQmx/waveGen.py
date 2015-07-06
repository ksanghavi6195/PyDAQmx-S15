# Random Wave Generator
log_rate = 44
seconds = 5
N_samples = log_rate * seconds

import numpy
import random

numpy.set_printoptions(threshold='inf')
# removes "..." from print statement

def waveGen(length):
	return numpy.random.rand(length)

print waveGen(N_samples)