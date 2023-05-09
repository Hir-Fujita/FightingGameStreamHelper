#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import pickle
import tkinter as tk
from tkinter import ttk
import Process
from Player import Player, Team

class Manager:
    def __init__(self, language, frame):
        self.layout = LayoutData(self)
        self.main_frame = frame
        self.player_list = []
        self.team_list = []
        self.counter_list = []

        self.gametitle_variable = tk.IntVar()
        self.gametitle_list = os.listdir("FightingGameStreamHelper/GameTitle")
        self.language_variable = tk.IntVar()
        self.language_list = language
        self.gametitle_select()
        self.variable = Process.Variable()
        self.layout_image = Process.openfile("FightingGameStreamHelper/image/layout_image.png")
        self.frame = tk.Frame(self.main_frame)
        self.frame.pack()

    def gametitle_select(self):
        self.title = self.gametitle_list[self.gametitle_variable.get()]
        with open(f"FightingGameStreamHelper/Gametitle/{self.title}/game.json", "r", encoding="utf-8") as f:
            json_data = json.load(f)
        self.character_dict = json_data[self.language_list[self.language_variable.get()]]

    def create_frame(self):
        self.player_list = []
        self.team_list = []
        self.coutner_list = []
        children = self.frame.winfo_children()
        for child in children:
            child.destroy()
        self.counter_frame = tk.Frame(self.frame)
        self.counter_frame.pack()
        self.player_frame = tk.Frame(self.frame)
        self.player_frame.pack()
        self.team_frame = tk.Frame(self.frame)
        self.team_frame.pack()
        create_frame = tk.LabelFrame(self.frame,
                                     text="ファイル名")
        create_frame.pack(side=tk.BOTTOM)
        name_entry = tk.Entry(create_frame)
        name_entry.pack(padx=5, pady=5)
        create_button = tk.Button(create_frame,
                                  text="生成")
        create_button.pack(padx=5, pady=5)

    def create_widget(self, widget, layout):
        if widget == "player":
            player_list = os.listdir(f"FightingGameStreamHelper/Gametitle/{self.title}/player")
            player_frame = tk.LabelFrame(self.player_frame,
                                         text=f"{layout.name}_{layout.number}")
            player_frame.pack(side=tk.LEFT)
            player_box = ttk.Combobox(player_frame,
                                      values=player_list)
            player_box.pack(padx=5, pady=5)
            self.player_list.append(Player())

        elif widget == "team":
            team_list = os.listdir(f"FightingGameStreamHelper/Gametitle/{self.title}/team")
            team_frame = tk.LabelFrame(self.team_frame,
                                       text=f"{layout.name}_{layout.number}")
            team_frame.pack(side=tk.LEFT)
            team_box = ttk.Combobox(team_frame,
                                    values=team_list)
            team_box.pack(padx=5, pady=5)
            self.team_list.append(Team())

        elif widget == "counter":
            counter_list = []
            for i in range(10):
                counter_list.append(i)
            counter_frame = tk.LabelFrame(self.counter_frame,
                                          text=f"{layout.name}_{layout.number}")
            counter_frame.pack(side=tk.LEFT)
            counter_box = ttk.Combobox(counter_frame,
                                       values=counter_list)
            counter_box.pack(padx=5, pady=5)
            self.counter_list.append("")

    def create_team_widget(self, count):
        frame_list = self.team_frame.winfo_children()
        if len(frame_list) == 0:
            pass
        else:
            for i in range(count):
                labelframe = tk.LabelFrame(frame_list[-1],
                                            text=f"Player.{i+1}")
                labelframe.pack()
                box = ttk.Combobox(labelframe)
                box.pack(padx=5, pady=5)




class LayoutData:
    def __init__(self, maneger:Manager):
        self.maneger = maneger
        self.list = []

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
        self.maneger.create_frame()
        if self.list == []:
            print("None")
        else:
            print(self.list)
            for layout in self.list:
                count = 0
                c = layout.count()
                if len(c) > 0:
                    if c[0][1] > count:
                        count = c[0][1]
                    if "player" in c[0][0]:
                        self.maneger.create_widget("player", layout)
                    if "team" in c[0][0]:
                        self.maneger.create_widget("team", layout)
                        self.maneger.create_team_widget(count)
                    if "counter" in c[0][0]:
                        self.maneger.create_widget("counter", layout)






