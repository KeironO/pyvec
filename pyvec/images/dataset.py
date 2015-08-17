import os, random, cv2
import numpy as np
from PIL import Image
from keras.utils import np_utils
from collections import Counter


'''
    file name: dataset.py
    author/s: Keiron O'Shea
    description: simple toolkit to load images, with their adjacent labels
    into arrays - suitable for use with keras/theano.
'''

def more_data(directory, image_list, image_height, image_width):
    response = raw_input("Do you want to produce more data? (Y/N): ")
    if response in ('Y', 'y', 'Yes', 'yes'):
        print "Creating new data, this may take awhile depending on the number of images...\n"
        rotation_matrix_1 = cv2.getRotationMatrix2D((image_height/2,image_width/2), 4, 1)
        rotation_matrix_2 = cv2.getRotationMatrix2D((image_height/2,image_width/2), 7, 1)
        rotation_matrix_3 = cv2.getRotationMatrix2D((image_height/2,image_width/2), -7, 1)
        rotation_matrix_4 = cv2.getRotationMatrix2D((image_height/2,image_width/2), -4, 1)
        #I want this to go into memory.
        for images in image_list:
            image = cv2.imread(directory+"/"+images[0]+"/"+images[1])
            rotated_image_1 = cv2.warpAffine(image, rotation_matrix_1, (image_height, image_width))
            rotated_image_2 = cv2.warpAffine(image, rotation_matrix_2, (image_height, image_width))
            rotated_image_3 = cv2.warpAffine(image, rotation_matrix_3, (image_height, image_width))
            rotated_image_4 = cv2.warpAffine(image, rotation_matrix_4, (image_height, image_width))
            cv2.imwrite(directory+"/"+images[0]+"/" + str(images[1]).split('.')[0]+".1.jpg",rotated_image_1)
            cv2.imwrite(directory+"/"+images[0]+"/" + str(images[1]).split('.')[0]+".2.jpg",rotated_image_2)
            cv2.imwrite(directory+"/"+images[0]+"/" + str(images[1]).split('.')[0]+".3.jpg",rotated_image_3)
            cv2.imwrite(directory+"/"+images[0]+"/" + str(images[1]).split('.')[0]+".4.jpg",rotated_image_4)
    else:
        pass


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


'''
load_images()

    Loads the preprocessed images from a folder, and correlates them
    with a correct label for use in keras/theano.

'''
def load_images(directory, image_height, image_width):
    # Retrieves a list of images.
    image_list, class_sizes = get_labels(directory)
    number_files = len(image_list)
    # Creates an array ready for the images to go into vectors.
    train_data = np.empty((number_files, 3, image_height, image_width), dtype="float32")
    # Flattens it.
    train_data.flatten()
    # Creates an array, ready for the labels to go into vectors to correlate with training_data
    train_label = np.empty((number_files,), dtype="uint8")
    for i, image_name in enumerate(image_list):
        # Open the files.
        images = Image.open(directory+"/"+image_name[0]+"/"+image_name[1])
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

'''
splitTrainValidationAndTest()

    Uses the split parameter to split the dataset into two sets.
    One for training (split) and another for validation.

    Standard call from vectorise().

'''

def splitTrainAndValdidation(split, number_images, train_data, label, height, width):
    # Calculating the number of training data.
    number_training_data = number_images * split

    # Calculating the percentage of data used for validation data.
    number_validation_data = number_images * (1.0 - split)

    X_train = train_data[: number_training_data]
    Y_train = label[: number_training_data]

    X_val = train_data[number_training_data ::]
    Y_val = label[number_training_data ::]

    # Setting the shapes for optimised vectorisation.
    X_train = X_train.reshape(X_train.shape[0], 3, height, width)/255
    X_val = X_val.reshape(X_val.shape[0], 3, height, width)/255

    # Setting the datasets to float32. (Single-precision floating-point format) - Suitable for NNs!
    X_train = X_train.astype("float32")
    X_val = X_val.astype("float32")

    # Returning the data (X = data, Y = labels)
    return X_train, Y_train, X_val, Y_val

'''
splitTrainValidationAndTest()

    Uses the split parameter to split the dataset into three sets.
    One for training (split), one for validation (5% of split) and
    another for tesint (5% of split)

    Only used when called with a final boolean value from vectorise()

'''

def splitTrainValidationAndTest(split, number_images, data, label, height, width):
    
    # Calculating the number of training data.
    number_training_data = number_images * split
    
    number_validation_data = number_images * ((1-split)/2)
    number_test_data = number_images * ((1-split)/2)

    print 'total number of images: ',number_images
    #print 'number of data ',data.shape()
    print 'number of training data: ',number_training_data
    print 'number of validation data: ',number_validation_data
    print 'number of testing data: ',number_test_data

    X_train = data[: number_training_data]
    Y_train = label[: number_training_data]

    X_val = data[number_training_data :][0 : number_validation_data]
    Y_val = label[number_training_data :][0 : number_validation_data]

    # Faulty!
    X_test = data[number_training_data::][number_validation_data::]
    Y_test = label[number_training_data::][number_validation_data::]

    # Setting the shapes for optimised vectorisation.
    X_train = X_train.reshape(X_train.shape[0], 3, height, width)/255
    X_val = X_val.reshape(X_val.shape[0], 3, height, width)/255
    X_test = X_test.reshape(X_test.shape[0], 3, height, width)/255

    # Setting the datasets to float32. (Single-precision floating-point format) - Suitable for NNs!
    X_train = X_train.astype("float32")
    X_val = X_val.astype("float32")
    X_test = X_test.astype("float32")

    # Returning the data (X = data, Y = labels)
    return X_train, Y_train, X_val, Y_val, X_test, Y_test


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
        X_train, Y_train, X_val, Y_val = splitTrainAndValdidation(split, number_images, train_data, label, height, width)
        return X_train, Y_train, X_val, Y_val

    # Get train, validation and testing data.
    if with_test == True:
        X_train, Y_train, X_val, Y_val, X_test, Y_test = splitTrainValidationAndTest(split, number_images, train_data, label, height, width)
        return X_train, Y_train, X_val, Y_val, X_test, Y_test




