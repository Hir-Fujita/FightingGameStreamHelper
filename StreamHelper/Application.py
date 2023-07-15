#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk

import Manager
import Window

NAME = "FightingGameStreamHelper"
VERSION = "Test"


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        master.geometry("600x300")
        master.title(f"{NAME}_{VERSION}.ver")
        self.frame = tk.Frame(master)
        self.frame.pack()
        self.manager = Manager.Manager(self.frame)

        self.player_register_window = Window.PlayerRegisterWindow("プレイヤー登録", 600, 400, self.manager)
        self.team_register_window = Window.TeamRegisterWindow("チーム登録", 600, 400, self.manager)
        # self.layout_window = Window.LayoutWindow("レイアウト設定", 980 + 300, 540, self.manager)
        # self.object_create_window = Window.CreateNewLayout("オブジェクト作成", 980 + 300 + 300, 540, self.manager)
        self.create_menu(master)
        self.manager.set_character_dict()

    def create_menu(self, master):
        self.menu_widget = tk.Menu(master)
        master.config(menu=self.menu_widget)
        # ゲーム選択
        menu_gametitle = tk.Menu(self.menu_widget, tearoff=0)

        for num, title in enumerate(self.manager.game_title_list):
            menu_gametitle.add_radiobutton(label=title,
                                           variable=self.manager.game_title_variable,
                                           value=num,
                                           command=self.manager.set_character_dict)
        self.menu_widget.add_cascade(label=f"ゲームタイトル選択",
                                     menu=menu_gametitle)
        # プレイヤー登録
        self.menu_widget.add_command(label=f"プレイヤー登録",
                                     command=lambda:self.player_register())
        # チーム登録
        self.menu_widget.add_command(label=f"チーム登録",
                                     command=lambda:self.team_register())
        # レイアウト設定
        self.menu_widget.add_command(label=f"レイアウト設定",
                                     command=lambda:self.layout_register())
        # レイアウトオブジェクト作成
        self.menu_widget.add_command(label="オブジェクト作成",
                                     command=lambda:self.layout_object_create())

    def player_register(self):
        if self.player_register_window.window is None:
            self.player_register_window.create()
        else:
            self.player_register_window.window_close()
            self.player_register_window.create()

    def team_register(self):
        if self.team_register_window.window is None:
            self.team_register_window.create()
        else:
            self.team_register_window.window_close()
            self.team_register_window.create()

    def layout_register(self):
        if self.layout_window.window is None:
            self.layout_window.create()
        else:
            self.layout_window.window_close()
            self.layout_window.create()

    def layout_object_create(self):
        if self.object_create_window.window is None:
            self.object_create_window.create()
        else:
            self.object_create_window.window_close()
            self.object_create_window.create()


def main():
	win = tk.Tk()
	app = Application(master = win)
	app.mainloop()

if __name__ == "__main__":
    main()
