import scipy.io.wavfile as wavfile
import numpy, os.walk

def get_labels(directory):
    audlist = []
    for dir_name, dir_names, file_name in os.walk(directory):
        for file in file_name:
            label = os.path.basename(os.path.normpath(dir_name))
            audlist.append([label, file])
    return audlist

def music_to_vector(file_name):
    data = wav.read(file_name)
    vector = data[1].astype("float32") / 32767.0
    return vector, data[0] 

def get_sample_blocks(song_array, block_size):
    blocks = []
    total_number_samples = song_array.shape[0]
    number_of_samples = 0
    while(number_of_samples < total_number_samples):
        song_block = song_array[number_of_samples:number_of_samples + block_size]
        if (block.shape[0] < block_size):
            padding = np.zeros((block_size - block.shape[0],))
            block = np.concatenate((block, padding))
        blocks.append(block)
        number_of_samples += block_size
    return blocks



