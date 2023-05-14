#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from Process import Process

class Manager(Process):
    def __init__(self, frame):
        super().__init__()
        self.frame = frame

        self.game_title_variable = tk.IntVar()
        self.game_title_list = self.read_folder("StreamHelper/GameTitle")

    def set_character_dict(self):
        title = self.get_game_title()
        self.character_dict = self.openfile(f"StreamHelper/GameTitle/{title}/game.json")["JPN"]
        self.character_list = [item for item in self.character_dict.values()]

    def get_game_title(self):
        result = self.game_title_list[self.game_title_variable.get()]
        return result


