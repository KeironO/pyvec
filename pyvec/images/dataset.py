import os, csv, random
import numpy as np
from PIL import Image
from keras.utils import np_utils, generic_utils
import os.path as path


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
        string = image_name[0]
        train_label[i] = int(string)
    return train_data, train_label

def vectorise(directory, nb_classes, height, width, split):
    train_data, train_label= load_images(directory, height, width)
    number_images = len(train_label)
    index = [i for i in range(number_images)]
    random.shuffle(index)
    train_data = train_data[index]
    train_label = train_label[index]

    label = np_utils.to_categorical(train_label, nb_classes)

    number_training_data = number_images * split
    number_validation_data = number_images * (1.0 - split)

    X_train = train_data[0 : number_training_data]
    Y_train = label[0 : number_training_data]

    X_val = train_data[0 : number_validation_data]
    Y_val = label[0 : number_validation_data]

    X_train = X_train.reshape(X_train.shape[0], 3, height, width)/255
    X_val = X_val.reshape(X_val.shape[0], 3, height, width)/255

    X_train = X_train.astype("float32")
    X_val = X_val.astype("float32")


    return X_train, Y_train, X_val, Y_val

