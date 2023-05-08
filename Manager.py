#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import pickle
import tkinter as tk
import Process
from Object import ImageObject, VariableObject

class Manager:
    def __init__(self, language):
        self.layout = LayoutData()
        self.gametitle_variable = tk.IntVar()
        self.gametitle_list = os.listdir("FightingGameStreamHelper/GameTitle")
        self.language_variable = tk.IntVar()
        self.language_list = language
        self.gametitle_select()
        self.variable = Process.Variable()
        self.layout_image = Process.openfile("FightingGameStreamHelper/image/layout_image.png")

    def gametitle_select(self):
        self.title = self.gametitle_list[self.gametitle_variable.get()]
        with open(f"FightingGameStreamHelper/Gametitle/{self.title}/game.json", "r", encoding="utf-8") as f:
            json_data = json.load(f)
        self.character_dict = json_data[self.language_list[self.language_variable.get()]]



class LayoutData:
    def __init__(self):
        self.list = []
        self.flag_player = False
        self.flag_count = False
        self.team_count = 0

    def save(self, filepath):
        self.name = os.path.basename(filepath)
        for layout in self.list:
            layout.save_process()
        with open(filepath, "wb") as f:
            pickle.dump(self, f)
        for layout in self.list:
            layout.load_process()

    def load(self, filepath):
        if os.path.isfile(filepath):
            with open(filepath, "rb") as f:
                self = pickle.load(f)
        else:
            print("filepath_error")
        for layout in self.list:
            layout.load_process()
        return self

    def object_check(self):
        if self.list == []:
            print("None")
        else:
            for layout in self.list:
                test = []
                for obj in layout.object_list:
                    if type(obj) == ImageObject:
                        pass
                    if type(obj) == VariableObject:
                        test.append(f"{obj.category}_{obj.style}_{obj.sub_style}")
                        print(obj.number)
                import collections
                c = collections.Counter(test)
                print(test)
                print(c)


