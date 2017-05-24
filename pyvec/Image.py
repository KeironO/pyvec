'''
    pyvec/Image.py
    
    pyvec Image Class
    
    Author: Keiron O'Shea <keo7@aber.ac.uk>
    Author: Mona Alshahrani <mona.alshahrani@kaust.edu.sa>
    Author: Nicholas Dimonaco <nid16@aber.ac.uk>
    
    This file implements an Image object.

'''

import os, numpy as np, PIL.Image, matplotlib.pyplot as plt

class Image(object):
    def __init__(self, file_path, colour="RGB"):
        self.file_path = file_path
        self.name = os.path.basename(file_path).split(".")[0]
        self.colour = colour
        self.details = self.__get_details()
        self.image_data = self.__load_image(colour)

    def __load_image(self, colour):
        if colour == "BW":
            return PIL.Image.open(self.file_path).convert("1")
        elif colour == "G":
            return PIL.Image.open(self.file_path).convert("LA")
        return PIL.Image.open(self.file_path)

    def to_numpy(self):
        return np.array(self.image_data)

    def view(self):
        plt.imshow(self.image_data)
        plt.title(self.name)
        plt.show()

    def resize(self, height, width):
        self.image_data.thumbnail([height, width], PIL.Image.ANTIALIAS)

    def __get_details(self):
        return {
            "name" : self.name,
            "file_path" : self.file_path,
            "colour" : self.colour,
        }