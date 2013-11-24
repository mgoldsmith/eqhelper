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

BOTTOM_FREQ = 30
TOP_FREQ 	= 1000

freqs = [0, 200, 500, 1000, 4000, 10000, 22000]
freq_automation = []

numfiles = len(sys.argv) - 1
wavfiles = []
spects = []


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

# simple subtraction of sound
# for i in range(min(len(dominant), len(ducked))):
# 	for j in range(min(len(dominant[i]), len(ducked[i]))):
# 		ducked[i][j] = abs(ducked[i][j] - (dominant[i][j] / 2))

def myFunc(x, y):
	second = min(x, y)
	thresh = 9.0
	if (second > thresh):
		return 1
	else:
		return 0

# plot the second highest in each frequency
for i in range(min(len(dominant), len(ducked))):
	for j in range(min(len(dominant[i]), len(ducked[i]))):
		ducked[i][j] = myFunc(dominant[i][j], ducked[i][j])

plt.imshow(dominant.T, origin='lower', aspect='auto')
plt.figure()
plt.imshow(weak.T, origin='lower', aspect='auto')
plt.figure()
plt.imshow(ducked.T, origin='lower', aspect='auto')
plt.show()

# sample_rate = wavfiles[1][0]

# bot = float(BOTTOM_FREQ) / (sample_rate / 2)
# top = float(TOP_FREQ) / (sample_rate / 2)

# print bot

# # create a bandstop filter
# Wp = [0.001, 0.01]   # Cutoff frequency 
# Ws = [0.002, 0.009]   # Stop frequency 
# Rp = 1                # passband maximum loss (gpass)
# As = 10              # stoppand min attenuation (gstop)

# b, a = fd.iirdesign(Wp, Ws, Rp, As, ftype='ellip')

# filtered = lfilter(b, a, wavfiles[1][1])

# integerised_filtered =  asarray(filtered, 'int16')

# scipy.io.wavfile.write('output.wav', sample_rate, integerised_filtered)
