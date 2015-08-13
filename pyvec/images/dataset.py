import os, csv
import numpy as np
from PIL import Image

'''
    file name: dataset.py
    author/s: Keiron O'Shea
    description: simple toolkit to load images, with their adjacent labels
    into arrays - suitable for use with keras/theano.
'''

'''
get_labels()

    Allows the correlation of labels to its image for pre-labelling purposes.

'''

def get_labels(directory):
	imglist = []
	for dirname,dirnames,filenames in os.walk(directory):
		for filename in filenames:
			label = os.path.basename(os.path.normpath(dirname))
			imglist.append([label, filename])
	return imglist

'''
load_images()

    Loads the preprocessed images from a folder, and correlates them
    with a correct label for use in keras/theano.

'''
def load_images(directory, image_height, image_width):
    image_list = get_labels(directory)
    number_files = len(image_list)
    train_data = np.empty((number_files, 3, image_height, image_width), dtype="float32")
    train_data.flatten()
    train_label = np.empty((number_files,), dtype="uint8")
    for i, image_name in enumerate(image_list):
        images = Image.open(directory+"/"+image_name[0]+"/"+image_name[1])
        vectored_image = np.asarray(images, dtype="float32")
        train_data[i,:,:,:] = [vectored_image[:,:,0],vectored_image[:,:,1],vectored_image[:,:,2]]
        train_label[i] = image_name[0]
    return train_data, train_label