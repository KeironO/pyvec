import scipy.io.wavfile
import numpy as np


'''
    Very much a WIP.
'''

def load_audio(data):
    # rate = int, data = numpy array.
    rate, data = scipy.io.wavfile(data)
    data = data.astype("float32")
    return rate, data