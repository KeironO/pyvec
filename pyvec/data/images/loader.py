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

def get_class_size(image_list):
    list_of_classes = Counter(labels[0] for labels in image_list).iteritems()
    return list_of_classes

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
    class_sizes = get_class_size(imglist)
    return imglist, class_sizes


def check_class_stabilitiy(image_list):
    origlist = []
    labels = []
    list_of_classes = get_class_size(image_list)
    for list1 in list_of_classes:
        origlist.append(list1[1])
        labels.append(list1[0])
    for i in range(len(origlist)):
        list2 = origlist[:]
        labels2 = labels[:]
        list2.pop(i)
        labels2.pop(i)
    for j in range(len(list2)):
        perIncrease = float((origlist[i]-list2[j]))/float(origlist[i])
        print "percentage increase ",perIncrease
        if ( perIncrease  > 0.3):
            print "add more data of class ",labels2[j]


'''
load_images()

    Loads the preprocessed images from a folder, and correlates them
    with a correct label for use in keras/theano.

'''


def load_images(directory, image_height, image_width):
    # Retrieves a list of images.
    image_list, class_sizes = get_labels(directory)
    number_files = len(image_list)
    # check_class_stabilitiy(image_list)
    # Creates an array ready for the images to go into vectors.
    train_data = np.empty((number_files, 3, image_height, image_width), dtype="float32")
    # Flattens it.
    train_data.flatten()
    # Creates an array, ready for the labels to go into vectors to correlate with training_data
    train_label = np.empty((number_files,), dtype="uint8")
    for i, image_name in enumerate(image_list):
    #for i, image_name in image_list.items(): 
        # Open the files.
        images = Image.open(directory+"/"+image_name[0]+"/"+image_name[1])
	dird = directory+"/"+image_name[0]+"/"+image_name[1]
	#print dird  
        images = images.resize((image_height, image_width))
        # Converts the images into float32 representation
        vectored_image = np.asarray(images, dtype="float32")
        # 3 shape vector..
        train_data[i,:,:,:] = [vectored_image[:,:,0],vectored_image[:,:,1],vectored_image[:,:,2]]
        string = image_name[0]
        #Assigns label to the image.
        train_label[i] = int(string)
    get_class_size(image_list)
    return train_data, train_label

def load_images_unlabel(directory, image_height, image_width):
     image_list,labels = get_lables(directory)
     number_files = len(image_list)
     
     train_data = np.empty((number_files, 3, imag_height, image_width), dtype="float32")
     train_data.flatten()
  
     # no need for labels 
     for i, image_name in enumerate(image_list):
	#no labels
	images = Image.open(directory+"/"+image_name[0]+"/"+image_name[1])
	dird = directory+"/"+image_name[0]+"/"+image_name[1]
	print dird	 
	images = images.resize((image_height, image_width))
	vectored_image = np.asarray(images, dtype = "float32")
	train_data[i,:,:,:] = [vectored_image[:,:,0],vectored_image[:,:,1],vectored_image[:,:,2]]
     
     return train_data
	
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
    # Nasty-ass unoptimised image vectors with labels.
    train_data, train_label= load_images(directory, height, width)
    number_images = len(train_label)
    index = [i for i in range(number_images)]
    # Shuffling the dataset
    random.shuffle(index)
    train_data = train_data[index]
    train_label = train_label[index]
    # Convert class vector to binary class matrices for categorial_crossentropy.
    label = np_utils.to_categorical(train_label, nb_classes)
    # Just get train + validation
    if with_test == False:
        X_train, Y_train, X_val, Y_val = split_dataset(split, number_images, train_data, label, height, width, False)
        return X_train, Y_train, X_val, Y_val
    # Get train, validation and testing data.
    if with_test == True:
        X_train, Y_train, X_val, Y_val, X_test, Y_test = split_dataset(split, number_images, train_data, label, height, width, True)
        return X_train, Y_train, X_val, Y_val, X_test, Y_test
