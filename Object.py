#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import collections
import pickle
from PIL import Image, ImageOps
from Process import openfile, returnImageTk, Object_image_create, generate_image, name_paste

class Layout:
    def __init__(self):
        self.object_list = []
        self.miror = False
        self.number = 0

    def __eq__(self, other):
        if not isinstance(other, Layout):
            return NotImplemented
        return self.name == other.name and self.number == other.number

    def count(self):
        counter = []
        for obj in self.object_list:
            if type(obj) == VariableObject:
                counter.append(obj.count())
        c = collections.Counter(counter)
        c = c.most_common()
        return c

    def rename(self):
        self.number += 1

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

    def save_process(self):
        del self.tk_image
        for obj in self.object_list:
            obj.save_process()

    def load(self, filepath):
        if os.path.isfile(filepath):
            with open(filepath, "rb") as f:
                self = pickle.load(f)
        else:
            print("filepath_error")
        for obj in self.object_list:
            obj.load_process()
        return self

    def load_process(self):
        self.create_layout_image()
        for obj in self.object_list:
            obj.load_process()

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
        self.image = name_paste(self.image, f"{self.name}_{self.number}")
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
        self.number = 0
        self.image = openfile(filepath)
        self.size = self.image.size
        self.copy = self.image.copy()
        self.tk_image = returnImageTk(self.image)

    def __eq__(self, other):
        if not isinstance(other, ImageObject):
            return NotImplemented
        return self.name == other.name and self.number == other.number

    def rename(self):
        self.number += 1

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

    def count(self):
        pass


class VariableObject(ImageObject):
    def __init__(self, square:bool, style:str, sub_style:str):
        if square:
            self.category = "image"
        else:
            self.category = "text"
        self.square = square
        self.style = style
        self.sub_style = sub_style
        self.name = f"{self.category}.{self.style}.{self.sub_style}"
        self.number = 0
        self.image = Object_image_create(f"{self.name}_{self.number}", self.square)
        self.copy = self.image.copy()
        self.tk_image = returnImageTk(self.image)

    def rename(self):
        super().rename()
        self.image = Object_image_create(f"{self.name}_{self.number}", self.square)
        self.tk_image = returnImageTk(self.image)

    def miror(self, miror):
        pass

    def count(self):
        return f"{self.style}_{self.sub_style}"

    def generate(self, variable):
        if os.path.isfile(variable):
            self.image = openfile(variable)
        else:
            self.image = generate_image(variable)
        self.image.thumbnail(self.size)
