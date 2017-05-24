'''

    pyvec/Video.py
    
    pyvec Video Class
    
    Author: Keiron O'Shea <keo7@aber.ac.uk>
    
    This file implements an Video object.

'''

import os

class Video(object):
    def __init__(self, file_path, colour="RGB", fps="auto"):
        self.file_path = file_path
        self.name = os.path.basename(file_path).split(".")[0]
        self.colour = colour
        self.fps = fps
        self.details = self.__get_details()

    def __load_video(self):
        pass

    def __get_details(self):
        return {}