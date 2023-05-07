#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pickle
from PIL import Image, ImageOps
from Process import openfile, returnImageTk, Object_image_create

class Layout:
    def __init__(self):
        self.object_list = []
        self.miror = False

    def set_miror(self):
        self.miror = not self.miror
        self.create_layout_image()

    def set_size(self, size:tuple):
        self.size = size
        self.re_size = size

    def set_position(self, position:tuple):
        self.position = position

    def save(self, filepath):
        self.name = os.path.basename(filepath)
        for obj in self.object_list:
            obj.save_process()
        with open(filepath, "wb") as f:
            pickle.dump(self, f)
        for obj in self.object_list:
            obj.load_process()

    def load(self, filepath):
        if os.path.isfile(filepath):
            with open(filepath, "rb") as f:
                self = pickle.load(f)
        else:
            print("filepath_error")
        for obj in self.object_list:
            obj.load_process()
        return self

    def create_layout_image(self):
        self.image = Image.new("RGBA", size=self.size, color=(0,0,0,0))
        for object in reversed(self.object_list):
            object.miror(self.miror)
            if self.miror:
                size = object.copy.size
                position = (self.size[0] - object.position[0] - size[0],
                            object.position[1])
            else:
                position = object.position
            if object.copy.mode == "RGBA":
                self.image.paste(object.copy, position, mask=object.copy)
            else:
                self.image.paste(object.copy, position)
        self.copy = self.image.copy()
        self.copy.thumbnail(self.re_size)
        self.tk_image = returnImageTk(self.copy)

    def resize(self, size:tuple):
        self.re_size = size
        self.copy = self.image.copy()
        self.copy.thumbnail(size)
        self.tk_image = returnImageTk(self.copy)



class ImageObject:
    def __init__(self, filepath):
        self.name = os.path.basename(filepath)
        self.image = openfile(filepath)
        self.size = self.image.size
        self.copy = self.image.copy()
        self.tk_image = returnImageTk(self.image)

    def resize(self, size:tuple):
        self.size = size
        copy = self.image.copy()
        self.copy = copy.resize(size)
        self.tk_image = returnImageTk(self.copy)

    def set_position(self, position:tuple):
        self.position = position

    def save_process(self):
        del self.tk_image

    def load_process(self):
        self.tk_image = returnImageTk(self.copy)

    def miror(self, miror):
        if miror:
            copy = self.image.copy()
            self.copy = copy.resize(self.size)
            self.copy = ImageOps.mirror(self.copy)
        else:
            copy = self.image.copy()
            self.copy = copy.resize(self.size)
        self.tk_image = returnImageTk(self.copy)


class VariableObject(ImageObject):
    def __init__(self, style:str, square:bool):
        self.name = style
        self.image = Object_image_create(self.name, square)
        self.copy = self.image.copy()
        self.tk_image = returnImageTk(self.image)

    def rename(self, new_name, square:bool):
        self.name = new_name
        self.image = Object_image_create(self.name, square)
        self.tk_image = returnImageTk(self.image)

    def miror(self, miror):
        pass