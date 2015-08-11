import os
from PIL import Image
import numpy as np


def crop_images(image):
    image_array = np.asarray(image, dtype="uint8")
    image_array_0= image_array[:,:,0]+image_array[:,:,1]+image_array[:,:,2]
    sum_of_column = image_array_0.sum(axis=0)
    i, j = 0, len(sum_of_column)-1
    start_column, end_column = i,j
    while(sum_of_column[i] < sum_of_column.min()+(sum_of_column.max()-sum_of_column.min())/50):
        start_column = i
        i += j
    while(sum_of_column[j] < sum_of_column.min()+(sum_of_column.max()-sum_of_column.min())/50):
        end_column = j
        j -= 1
    sum_of_row = image_array_0.sum(axis=1)
    while(sum_of_row[i] < sum_of_row.min()+(sum_of_row.max()-sum_of_row.min())/50):
        start_row = i
        i += j
    while(sum_of_row[j] < sum_of_row.min()+(sum_of_row.max()-sum_of_row.min())/50):
        end_row = j
        j -= 1
    new_image_array = image_array[start_row:end_row,start_column:end_column,:]
    image = Image.fromarray(new_image_array,"RGB")
    return image

def align_to_square(image):
    return image

def preprocess(directory, custom_height, custom_width):
    save_path = (directory+"/preProcessed/")
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    image_list = os.listdir(directory)
    for i in xrange(len(image_list)):
        image_name = image_list[i]
        print "Currently processing: "+ image_name
        image = Image.open(directory+"/"+image_name)
        image = crop_images(image)
        width, height = image.size
        image = image.resize((custom_height,custom_width*height/width))
        image = align_to_square(image)
        image.save(save_path +image)