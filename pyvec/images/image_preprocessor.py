import os
from PIL import Image
import numpy as np
import os.path as path

'''
    file name: image_preprocessor.py
    author/s: Keiron O'Shea
    description: preproccesses the images for standard height and width
'''

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
    i, j = 0,len(sum_of_row)-1
    start_row, end_row = i,j
    while(sum_of_row[i] < sum_of_row.min()+(sum_of_row.max()-sum_of_row.min())/50):
        start_row = i
        i += 1
    while(sum_of_row[j] < sum_of_row.min()+(sum_of_row.max()-sum_of_row.min())/50):
        end_row = j
        j -= 1
    new_image_array = image_array[start_row:end_row,start_column:end_column,:]
    image = Image.fromarray(new_image_array,"RGB")
    return image

def align_to_square(image, custom_height, custom_width):
    width,height = image.size
    if height < width:
        filler = (width - height)/2
        image_array = np.asarray(image)
        new_image_array = np.zeros((custom_height, custom_width, 3), dtype="uint8")
        new_image_array[filler:filler+height,:,:]=image_array[:,:,:]
        image = Image.fromarray(new_image_array, "RGB")
    if height > width:
        length = height - width
        image_array = np.asarray(image)
        image = Image.fromarray(image_array[0:height-length,:,:],"RGB")
    return image

def load_directories(directory):
	image_list = []
	for dir_name,dir_names,file_names in os.walk(directory):
		for file in file_names:
			label = os.path.basename(os.path.normpath(dir_name))
			image_list.append([label, file])
	return image_list

def preprocess(directory, custom_directory, custom_height, custom_width):
    save_path = path.abspath(path.join(directory, "../", custom_directory))
    print save_path
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    image_list = load_directories(directory)
    for image_name in image_list:
        image = Image.open(directory+"/"+image_name[0]+"/"+image_name[1])
        image = crop_images(image)
        width, height = image.size
        image = image.resize((custom_height, custom_width*height/width))
        image = align_to_square(image, custom_height, custom_width)
        if not os.path.exists(save_path + "/" + image_name[0]):
            os.makedirs(save_path + "/" + image_name[0])
        image.save(save_path+"/"+image_name[0]+"/"+image_name[1])