"""
Compute and display a spectrogram.
Give WAV file as input
"""
from matplotlib import *
import scipy.io.wavfile
from scipy import *
from pylab import *
import numpy as np
import sys

STEP_SIZE   = 0.01
WINDOW_SIZE = 0.02

numfiles = len(sys.argv) - 1
wavfiles = []
spects = []

for i in range(numfiles):
	wavfiles[i] = sys.argv[i + 1]

	sr,x = scipy.io.wavfile.read(wavfile)

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
	spects[i] = np.zeros( (len(nn), nwin/2) )

	for j,n in enumerate(nn):
	    xseg = x[n-nwin:n]                  # nwin-sized segment
	    z = np.fft.fft(window * xseg)       # create fft of the hamming window
	    z = np.abs(z)
	    spects[i][j,:] = np.log(z[:nwin/2])         # use the log of it

# plt.imshow(spects[i].T, origin='lower', aspect='auto')

# plt.show()
