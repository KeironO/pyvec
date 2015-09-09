import scipy.io.wavfile as wavfile
import numpy


def vectorise_audio(file):
    sound_vector = numpy.array(file[1], dtype="float32")
    return sound_vector
