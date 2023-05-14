#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pickle
import json
from PIL import Image, ImageOps, ImageTk

class Process:
    def __init__(self):
        self.image_extention = [".jpg", ".JPG", ".png", ".PNG"]
        self.player_extention = [".ply", ".PLY"]
        self.team_extention = [".team", ".TEAM"]

    def file_check(self, filepath):
        extension = os.path.splitext(filepath)[1]
        if extension in self.image_extention:
            return "img"
        elif extension in self.player_extention:
            return "ply"
        elif extension in self.team_extention:
            return "team"
        elif extension == ".json":
            return "json"
        else:
            return False

    def openfile(self, filepath):
        if not os.path.isfile(filepath):
            print("ファイル読み込みエラー")
            return False
        else:
            result = self.file_check(filepath)
            if result == "img":
                data = Image.open(filepath)
            elif result == "ply" or result == "team":
                with open(filepath, "rb") as f:
                    data = pickle.load(f)
            elif result == "json":
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
            return data

    def read_folder(self, folder_path):
        result = os.listdir(folder_path)
        return result

    @classmethod
    def load(cls, file_path):
        if os.path.isfile(file_path):
            with open(file_path, "rb") as f:
                data = pickle.load(f)
            return data

    def save(self, filepath):
        with open(filepath, "wb") as f:
            pickle.dump(self, f)

    def get_imageTk(self, image, resize=None, miror=None):
        if type(image) is str:
            copy_image = self.openfile(image)
        else:
            copy_image = image.copy()
        if resize is not None:
            copy_image.thumbnail(resize, resample=3)
        if miror is not None:
            copy_image = ImageOps.mirror(copy_image)
        return_image = ImageTk.PhotoImage(copy_image)
        return return_image

