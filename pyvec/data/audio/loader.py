import scipy.io.wavfile as wavfile
import numpy, os.walk

normalize = 32767

def get_labels(directory):
    audlist = []
    for dir_name, dir_names, file_name in os.walk(directory):
        for file in file_name:
            label = os.path.basename(os.path.normpath(dir_name))
            audlist.append([label, file])
    return audlist

def music_to_vector(file_name):
    data = wavfile.read(file_name)
    vector = data[1].astype("float32") / normalize
    return vector, data[0] 


def time_to_fft(time):
    fft = []
    for block in time:
        fft_block = numpy.fft.fft(block)
        new = numpy.concatenate(numpy.real((fft_block), numpy.imag(fft_block)))
        fft.append(new)
    return fft

def get_sample_blocks(song_array, block_size):
    blocks = []
    total_number_samples = song_array.shape[0]
    number_of_samples = 0
    while(number_of_samples < total_number_samples):
        song_block = song_array[number_of_samples:number_of_samples + block_size]
        if (song_block.shape[0] < block_size):
            padding = numpy.zeros((block_size - song_block.shape[0],))
            song_block = numpy.concatenate((song_block, padding))
        blocks.append(song_block)
        number_of_samples += block_size
    return blocks

