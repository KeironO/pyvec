import scipy.io.wavfile as wavfile
import numpy, os.walk

def get_labels(directory):
    audlist = []
    for dir_name, dir_names, file_name in os.walk(directory):
        for file in file_name:
            label = os.path.basename(os.path.normpath(dir_name))
            audlist.append([label, file])
    return audlist


def get_max_length(directory):
    return 0
    # ToDo

def vectorise_audio(directory, length):
    audlist = get_labels(directory)
    read_file = wavfile.read(file)
    sound_vector = numpy.array(read_file[1], dtype="float32")
    return sound_vector
