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

    labels_file must be in the following format:
        image name\tlabel
        example\t0
        example2\t1
'''
def get_labels(labels_file):
    table={}
    with open(labels_file, "rb") as labels_reader:
        labels_reader = csv.reader(labels_file, delimiter="\t", lineterminator="\n")
        labels_reader.next() #Skip the heading line
        for labels in labels_reader:
            table[labels[0]] = int(labels[1])
        return table

'''
load_images()

    Loads the preprocessed images from a folder, and correlates them
    with a correct label for use in keras/theano.

'''
def load_images(directory, image_height, image_width):
    images = os.listdir(directory)
    number_images = len(images)
    table = get_labels()
    train_data = np.empty((number_images,3,image_height,image_width),dtype="float32")
    train_data.flatten()
    train_label = np.empty((number_images,),dtype="uint8")
    for i in range(number_images):
        image_name = images[i]
        images = Image.open(directory+image_name)
        vectored_image = np.asarray(images, dtype="float32")
        train_data[i,:,:,:] = [vectored_image[:,:,0],vectored_image[:,:,1],vectored_image[:,:,2]]
        train_label[i] = table[image_name.split('.')[0]]
    return train_data, train_label