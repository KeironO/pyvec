import os, random, csv
import numpy as np
from PIL import Image
from keras.utils import np_utils

np.set_printoptions(threshold='nan')

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
    size = image_height, image_width
    for i, image_name in enumerate(image_list):
        images = Image.open(directory+"/"+image_name[0]+"/"+image_name[1]).convert("RGB")
        images = images.resize(size, Image.ANTIALIAS)
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


def load_labels_and_file_name(tsv_file):
    with open(tsv_file, "rb") as tsv:
        reader = csv.reader(tsv, delimiter="\t", lineterminator="\n")
        tsv_list = list(reader)
        return tsv_list

def load_images_using_tsv(directory, tsv_file, height, width):
    labels_file_name = load_labels_and_file_name(tsv_file)
    number_of_images = len(labels_file_name)
    data = np.empty((number_of_images, 3, height, width), dtype="float32")
    data.flatten()
    labels = np.empty((number_of_images, ), dtype=np.dtype("a16"))
    for i, details in enumerate(labels_file_name):
        vectored_image = vectorise_image(directory, details[1], height, width)
        data[i,:,:,:] = [vectored_image[:,:,0],vectored_image[:,:,1],vectored_image[:,:,2]]
        data /= 255
        labels[i] = details[0]
    return data, labels

def vectorise_image(directory, file_name, height, width):
    loaded_image = Image.open(directory+"/"+file_name)
    loaded_image = loaded_image.resize((height, width), Image.ANTIALIAS)
    vectored_image = np.asarray(loaded_image, dtype="float32")
    return vectored_image

def split_test_and_train(data, labels, split):
    number_of_images = len(data)

    number_of_training_images = number_of_images * split
    number_of_testing_images = number_of_images * (1.0 - split)

    train_data = data[:number_of_training_images]
    train_data = train_data.reshape(train_data.shape[0], 3, data.shape[2], data.shape[3])
    train_labels = labels[:number_of_training_images]

    test_data = data[number_of_training_images:][0:number_of_testing_images]
    test_data = test_data.reshape(test_data.shape[0], 3,  data.shape[2], data.shape[3])

    test_labels = labels[number_of_training_images:][0:number_of_testing_images]

    return (train_data, train_labels),(test_data, test_labels)

