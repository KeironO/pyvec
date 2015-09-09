import scipy.io.wavfile as wavfile
import numpy


def vectorise_audio(file):
    read_file = wavfile.read(file)
    sound_vector = numpy.array(read_file[1], dtype="float32")
    return sound_vector
