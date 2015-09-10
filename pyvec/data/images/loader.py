import os, random
import numpy as np
from PIL import Image
from keras.utils import np_utils
from collections import Counter

'''
    file name: loader.py
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
    data = np.empty((number_files, 3, image_height, image_width), dtype="float32")
    data.flatten()
    labels = np.empty((number_files,), dtype="uint8")
    data_name = np.empty((number_files,), dtype=object)
    for i, image_name in enumerate(image_list):
        images = Image.open(directory+"/"+image_name[0]+"/"+image_name[1])
        images = images.resize((image_height, image_width), Image.ANTIALIAS)
        vectored_image = np.asarray(images, dtype="float32")
        data[i,:,:,:] = [vectored_image[:,:,0],vectored_image[:,:,1],vectored_image[:,:,2]]
        labels[i] = image_name[0]
        data_name[i] = image_list[i][1]
    return data, labels, data_name

def split_dataset(split, number_images, data, label, height, width, with_test = False):
    if with_test == True:
        number_training_data = number_images * split
        number_test_and_validation_data = number_images * ((1-split)/2)

        train_data = data[: number_training_data]
        train_data = train_data.reshape(train_data.shape[0], 3, height, width)/255
        train_data = train_data.astype("float32")
        train_label = label[: number_training_data]

        val_data = data[number_training_data :][0 : number_test_and_validation_data]
        val_data = val_data.reshape(val_data.shape[0], 3, height, width)/255
        val_data = val_data.astype("float32")
        val_label = label[number_training_data :][0 : number_test_and_validation_data]

        test_data = data[number_training_data::][number_test_and_validation_data::]
        test_data = test_data.reshape(test_data.shape[0], 3, height, width)/255
        test_data = test_data.astype("float32")
        test_label = label[number_training_data::][number_test_and_validation_data::]

        return train_data, train_label, val_data, val_label, test_data, test_label

    else:
        number_training_data = number_images * split
        number_validation_data = number_images * (1.0 - split)

        train_data = data[: number_training_data]
        train_data = train_data.reshape(train_data.shape[0], 3, height, width)/255
        train_data = train_data.astype("float32")
        train_label = label[: number_training_data]

        val_data = data[number_training_data :][0 : number_validation_data]
        val_data = val_data.reshape(val_data.shape[0], 3, height, width)/255
        val_data = val_data.astype("float32")
        val_label = label[number_training_data :][0 : number_validation_data]

        return train_data, train_label, val_data, val_label

def vectorise(directory, nb_classes, height, width, split, with_test=False): # Get train + val by default.
    data, label, image_names = load_images(directory, height, width)
    number_images = len(label)
    index = [i for i in range(number_images)]
    random.shuffle(index)
    data = data[index]
    label = label[index]
    image_names= image_names[index]


    label = np_utils.to_categorical(label, nb_classes)

    if with_test == False:
        X_train, Y_train, X_val, Y_val = split_dataset(split, number_images, data, label, height, width, False)
        return X_train, Y_train, X_val, Y_val, image_names
    elif with_test == True:
        X_train, Y_train, X_val, Y_val, X_test, Y_test = split_dataset(split, number_images, data, label, height, width, True)
        return X_train, Y_train, X_val, Y_val, X_test, Y_test, image_names


