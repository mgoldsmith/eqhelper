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
TOP_FREQ 	= 400

RANGE = 10

# freqs = [0, 200, 500, 1000, 4000, 10000, 22000]
# freq_automation = []

numfiles = len(sys.argv) - 1
wavfiles = []
spects = []
automation = []
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

# print len(ducked)
# print len(wavfiles[1][1])

# get the average energy of the given frequency
for i in range(min(len(dominant), len(ducked))):
	total = 0
	for j in range(RANGE):
		total += (min(dominant[i][j], ducked[i][j]) / RANGE)
	automation.append(total)

sample_rate = wavfiles[1][0]

bot = float(BOTTOM_FREQ) / (sample_rate / 2)
top = float(TOP_FREQ) / (sample_rate / 2)

# for i in range(len(wavfiles[1][1]))[::441]:
# 	# print i
# 	if (i + 882) < len(wavfiles[1][1]):
# 		# create a bandstop filter
# 		Wp = [bot, top]  				  # Cutoff frequency 
# 		Ws = [bot + 0.001, top - 0.001]   # Stop frequency 
# 		Rp = 1               			  # passband maximum loss (gpass)
# 		As = automation[i / 441]      # stoppand min attenuation (gstop)

# 		b, a = fd.iirdesign(Wp, Ws, Rp, As, ftype='ellip')

# 		f = lfilter(b, a, wavfiles[1][1][i:i+441])
# 		for sample in f:
# 			filtered.append(sample)


Wp = [bot, top]  				  # Cutoff frequency 
Ws = [bot + 0.001, top - 0.001]   # Stop frequency 
Rp = 1               			  # passband maximum loss (gpass)
As = 10      # stoppand min attenuation (gstop)

b, a = fd.iirdesign(Wp, Ws, Rp, As, ftype='ellip')

filtered = lfilter(b, a, wavfiles[1][1])

# print len(wavfiles[1][1])
# print len(filtered)
# print len(automation)
# print filtered
output =  asarray(filtered, 'int16')

scipy.io.wavfile.write('output.wav', sample_rate, output)
