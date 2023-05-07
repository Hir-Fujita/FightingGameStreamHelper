#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import json
import os
import tkinter as tk
from tkinter import ttk

import Manager
import Window

NAME = "FightingGameStreamHelper"
VERSION = "Test"
LANGUAGE_LIST = ["JPN","ENG"]

"""

"""

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        master.geometry("400x200")
        master.title(f"{NAME}_{VERSION}.ver")
        self.manager = Manager.Manager(LANGUAGE_LIST)

        with open("FightingGameStreamHelper/language.json", "r", encoding="utf-8") as f:
            label_data = json.load(f)
            language = LANGUAGE_LIST[self.manager.language_variable.get()]
            self.label_data = [label_data[label][language] for label in label_data]

        self.create_menu(master)
        self.create_main_widget(master)
        self.player_register_window = Window.PlayerRegisterWindow()
        self.team_register_window = Window.TeamRegisterWindow()
        self.rayout_window = Window.RayoutWindow()

    def create_menu(self, master):
        self.menu_widget = tk.Menu(master)
        master.config(menu=self.menu_widget)
        # ゲーム選択
        menu_gametitle = tk.Menu(self.menu_widget, tearoff=0)
        for num, title in enumerate(self.manager.gametitle_list):
            menu_gametitle.add_radiobutton(label=title,
                                           variable=self.manager.gametitle_variable,
                                           value=num,
                                           command=self.manager.gametitle_select)
        self.menu_widget.add_cascade(label=f"{self.label_data[0]}",
                                     menu=menu_gametitle)
        # プレイヤー登録
        self.menu_widget.add_command(label=f"{self.label_data[1]}",
                                     command=lambda:self.player_register(self.label_data[1]))
        # チーム登録
        self.menu_widget.add_command(label=f"{self.label_data[2]}",
                                     command=lambda:self.team_register(self.label_data[2]))
        # レイアウト設定
        self.menu_widget.add_command(label=f"{self.label_data[3]}",
                                     command=lambda:self.layout_register("レイアウト設定"))
        # 言語設定
        menu_language = tk.Menu(self.menu_widget, tearoff=0)
        self.language_variable = tk.IntVar()
        for num, lang in enumerate(LANGUAGE_LIST):
            menu_language.add_radiobutton(label=lang,
                                          variable=self.manager.language_variable,
                                          value=num)
        self.menu_widget.add_cascade(label=f"{self.label_data[4]}",
                                     menu=menu_language)

    def player_register(self, title):
        if self.player_register_window.window is None:
            self.player_register_window.create(self.manager, title, 600, 400)
        else:
            self.player_register_window.window_close()
            self.player_register_window.create(self.manager, title, 600, 400)

    def team_register(self, title):
        if self.team_register_window.window is None:
            self.team_register_window.create(self.manager, title, 600, 400)
        else:
            self.team_register_window.window_close()
            self.team_register_window.create(self.manager, title, 600, 400)

    def layout_register(self, title):
        if self.rayout_window.window is None:
            self.rayout_window.create(self.manager, title, 980 + 300, 540)
        else:
            self.rayout_window.window_close()
            self.rayout_window.create(self.manager, title, 980 + 300, 540)

    def create_main_widget(self, master):
        pass

def main():
	win = tk.Tk()
	app = Application(master = win)
	app.mainloop()

if __name__ == "__main__":
    main()
