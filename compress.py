# compress.py

"""
Compute and display a spectrogram.
Give WAV file as input
"""
from matplotlib import *
import scipy.io.wavfile
from scipy.signal import filter_design as fd
from  scipy.signal import lfilter
from scipy import *
from pylab import *
import numpy as np
import sys

STEP_SIZE   = 0.01
WINDOW_SIZE = 0.02

DECAY = 10000.0
ATTACK = 1000.0
RATIO = 0.1
THRESH = 3
MAKEUP = 1.3

numfiles = len(sys.argv) - 1
wavfiles = []
spects = []
output = []
filtered = []

for i in range(numfiles):

	sr,x = scipy.io.wavfile.read(sys.argv[i + 1])

	wavfiles.append((sr, x))

	# Parameters: 10ms step, 20ms window
	nstep = int(sr * STEP_SIZE)
	nwin  = int(sr * WINDOW_SIZE)

	# creates hamming ratios for the window size
	window = np.hamming(nwin)

	# will take windows x[n1:n2].  generate
	# and loop over n2 such that all frames
	# fit within the waveform
	nn = range(nwin, len(x), nstep)

	# create two-dimensional array to store spectrogram info
	spects.append(np.zeros( (len(nn), nwin/2) ))

	for j,n in enumerate(nn):
	    xseg = x[n-nwin:n]                  # nwin-sized segment
	    z = np.fft.fft(window * xseg)       # create fft of the hamming window
	    z = np.abs(z)
	    spects[i][j,:] = np.log(z[:nwin/2])         # use the log of it

dominant = spects[0]
weak = spects[1]
ducked = np.array(weak)

automation = np.zeros(len(wavfiles[1][1]))
sample_rate = wavfiles[1][0]

def myFunc(x, y):
	return min(x, y)

minlength = min(len(dominant), len(ducked))
minlengthvert = min(len(dominant[0]), len(ducked[0]))

added = STEP_SIZE * sample_rate

# plot the second highest in each frequency
for i in range(minlength):
	for j in range(minlengthvert):
		ducked[i][j] = myFunc(dominant[i][j], ducked[i][j])

	total = 0
	for j in range(minlengthvert):
		total += ducked[i][j] / float(minlengthvert)
	if i * added < len(automation) and total > THRESH:
		automation[i * added] = total * RATIO

# forward sweep through automation
for i in range(len(automation)):
	if i != 0 and (automation[i] < automation[i - 1] - (1 / DECAY)):
		automation[i] = automation[i - 1] - (1 / DECAY)

# backward sweep through automation
for i in reversed(range(len(automation))):
	if (i != len(automation) - 1) and (automation[i] < automation[i + 1] - (1 / ATTACK)):
		automation[i] = automation[i + 1] - (1 / ATTACK)

plt.plot(automation)
plt.show()



# print filtered
output =  asarray(wavfiles[1][1] * (1 - automation) * MAKEUP + wavfiles[0][1], 'int16')

scipy.io.wavfile.write('output.wav', sample_rate, output)
