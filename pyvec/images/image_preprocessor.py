import os
from PIL import Image
import numpy as np


def crop_images(image):
    return image

def align_to_square(image):
    return image

def preprocess(directory):
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
        image = image.resize((64,64*height/width))
        image = align_to_square(image)
        image.save(save_path +image)