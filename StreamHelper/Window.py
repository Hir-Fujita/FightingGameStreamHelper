#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, filedialog, colorchooser
import os
import pickle

from Manager import Manager
from Object import Player, Team


class Window:
    def __init__(self, title, width, height):
        self.window_title = title
        self.window = None
        self.window_width = width
        self.window_height = height

    def create(self):
        if self.window is not None:
            self.window_close()
        self.window = tk.Toplevel()
        self.window.geometry(f"{self.window_width}x{self.window_height}")
        self.window.title(f"{self.window_title}")
        self.window.protocol("WM_DELETE_WINDOW", self.window_close)

    def window_close(self):
        self.window.destroy()
        self.window = None


class PlayerRegisterWindow(Window):
    def __init__(self, title, width, height, manager:Manager):
        super().__init__(title, width, height)
        self.manager = manager
        self.window_title = f"{self.manager.get_game_title()}_{self.window_title}"

    def create(self):
        super().create()
        self.player = Player()
        game_title = tk.Label(self.window, text=self.window_title)
        game_title.pack()
        left_frame = tk.Frame(self.window)
        left_frame.pack(side=tk.LEFT)
        name_label = tk.Label(left_frame, text="プレイヤー名")
        name_label.grid(row=0, column=0, padx=2, pady=2)
        name_box = tk.Entry(left_frame, width=30)
        name_box.grid(row=0, column=1, padx=2, pady=2)
        chara_label = tk.Label(left_frame, text="使用キャラ")
        chara_label.grid(row=1, column=0, padx=2, pady=2)
        chara_box = ttk.Combobox(left_frame, values=self.manager.character_list, width=27)
        chara_box.grid(row=1, column=1, padx=2, pady=2)
        country_label = tk.Label(left_frame, text="国籍")
        country_label.grid(row=2, column=0, padx=2, pady=2)
        country_box = ttk.Combobox(left_frame, width=27)
        country_box.grid(row=2, column=1, padx=2, pady=2)
        affiliation_label = tk.Label(left_frame, text="所属チーム")
        affiliation_label.grid(row=3, column=0, padx=2, pady=2)
        affiliation_box = tk.Entry(left_frame, width=30)
        affiliation_box.grid(row=3, column=1, padx=2, pady=2)
        twitter_label = tk.Label(left_frame, text="Twitter")
        twitter_label.grid(row=4, column=0, padx=2, pady=2)
        twitter_box = tk.Entry(left_frame, width=30)
        twitter_box.grid(row=4, column=1, padx=2, pady=2)
        memo_label = tk.Label(left_frame, text="備考欄")
        memo_label.grid(row=5, column=0, padx=2, pady=2)
        memo_frame = tk.Frame(left_frame)
        memo_frame.grid(row=5, column=1, padx=2, pady=2)
        memo_box = tk.Text(memo_frame, wrap=tk.NONE, width=23, height=10)
        memo_box.grid(row=0, column=0)
        scroll_y = tk.Scrollbar(memo_frame, orient='vertical', command=memo_box.yview)
        memo_box.config(yscrollcommand=scroll_y.set)
        scroll_y.grid(row=0, column=1, sticky=tk.N + tk.S)
        bottom_frame = tk.Frame(left_frame)
        bottom_frame.grid(row=6, column=0, columnspan=2)
        save_button = tk.Button(bottom_frame, text="save", command=lambda:save())
        save_button.grid(row=6, column=0, padx=20, pady=2)
        load_button = tk.Button(bottom_frame, text="load", command=lambda:load())
        load_button.grid(row=6, column=1, padx=20, pady=2)
        right_frame = tk.Frame(self.window)
        right_frame.pack(side=tk.LEFT)
        face_label = tk.Label(right_frame, text="選手画像")
        face_label.grid(row=0, column=0)
        self.face_image = self.manager.get_imageTk(self.player.image, resize=(250, 250))
        face_image_box = tk.Label(right_frame, image=self.face_image)
        face_image_box.grid(row=1, column=0)
        face_button = tk.Button(right_frame, text="画像読み込み",
                                command=lambda:face_image_change(face_image_box))
        face_button.grid(row=2, column=0)

        def face_image_change(widget):
            filename = filedialog.askopenfilename(multiple=False)
            if filename is not None:
                self.player.image = self.manager.openfile(filename)
                self.face_image = self.manager.get_imageTk(self.player.image, resize=(250,250))
                widget.config(image=self.face_image)

        def save():
            self.player.name = name_box.get()
            self.player.gametitle = self.manager.get_game_title()
            self.player.character = chara_box.current()
            self.player.country = country_box.current()
            self.player.twitter = twitter_box.get()
            self.player.team = affiliation_box.get()
            self.player.memo = memo_box.get("1.0","end")
            if self.player.team == "":
                save_filename = f"{self.player.name}"
            else:
                save_filename = f"{self.player.name}_{self.player.team}"
            filename = filedialog.asksaveasfilename(title="プレイヤーデータ保存",
                                                    parent=self.window,
                                                    defaultextension=".ply",
                                                    filetypes=[("player_file", ".ply")],
                                                    initialdir=f"StreamHelper/GameTitle/{self.manager.get_game_title()}/player",
                                                    initialfile=save_filename)
            self.player.save(filename)

        def load():
            filepath = filedialog.askopenfilename(title="プレイヤーデータ読み込み",
                                                  parent=self.window,
                                                  defaultextension=".ply",
                                                  filetypes=[("player_file", ".ply")],
                                                  initialdir=f"StreamHelper/GameTitle/{self.manager.get_game_title()}/player")
            self.player = Player.load(filepath)
            if not self.manager.get_game_title() == self.player.gametitle:
                print("ゲームタイトルが不正です")
            else:
                name_box.delete(0, "end")
                name_box.insert(0, self.player.name)
                chara_box.delete(0, "end")
                chara_box.current(self.player.character)
                if self.player.country > 0:
                    country_box.current(self.player.country)
                twitter_box.delete(0, "end")
                twitter_box.insert(0, self.player.twitter)
                affiliation_box.delete(0, "end")
                affiliation_box.insert(0, self.player.team)
                memo_box.delete(1.0, "end")
                memo_box.insert(1.0, self.player.memo)
                self.face_image = self.manager.get_imageTk(self.player.image, (250,250))
                face_image_box.config(image=self.face_image)



class TeamRegisterWindow(Window):
    def __init__(self, title, width, height, manager):
        super().__init__(title, width, height)
        self.manager = manager
        self.window_title = f"{self.manager.get_game_title()}_{self.window_title}"

    def create(self, manager:Manager, title, width, height):
        super().create()
        self.team = Team()
        self.team_index = 1
        player_list = os.listdir(f"FightingGameStreamHelper/GameTitle/{self.manager.title}/player")
        self.player_list = [player[:-4] for player in player_list]
        top_frame = tk.Frame(self.window)
        top_frame.pack()
        team_length_label = tk.Label(top_frame, text="チーム人数")
        team_length_label.grid(row=0, column=0)
        team_length_variable = tk.IntVar(value=1)
        team_length_box = tk.Spinbox(top_frame,
                                     textvariable=team_length_variable,
                                     from_=1,
                                     to=9,
                                     command=lambda:[self.team.team_length_change(team_length_variable.get()),
                                                     center_center_frame.config(text=f"player_{self.team_index}/{self.team.team_length}")]
                                     )
        team_length_box.grid(row=0, column=1, padx=5, pady=5)
        team_name_label = tk.Label(top_frame,  text="チーム名")
        team_name_label.grid(row=1, column=0)
        team_name_box = tk.Entry(top_frame, width=30)
        team_name_box.grid(row=1, column=1)
        center_frame = tk.Frame(self.window)
        center_frame.pack()
        left_button = tk.Button(center_frame, text="<<",
                                command=lambda:team_index_change(False))
        left_button.grid(row=0, column=0)
        right_button = tk.Button(center_frame, text=">>",
                                 command=lambda:team_index_change(True))
        right_button.grid(row=0, column=2)

        center_center_frame = tk.LabelFrame(center_frame, text=f"player_{self.team_index}/{self.team.team_length}")
        center_center_frame.grid(row=0, column=1, padx=10, pady=10)
        player_label = tk.Label(center_center_frame, text="プレイヤー名")
        player_label.grid(row=0, column=0)
        player_box = ttk.Combobox(center_center_frame,
                                  values=self.player_list)
        player_box.bind("<<ComboboxSelected>>", lambda e:player_box_selected())
        player_box.grid(row=0, column=1)
        image = openfile("FightingGameStreamHelper/image/face.png")
        image = returnImageTk(image, (100, 100))
        self.label_image = (image, image)
        face_label = tk.Label(center_center_frame, text="プレイヤー画像")
        face_label.grid(row=1, column=0, columnspan=2)
        face_image_label = tk.Label(center_center_frame, image=self.label_image[0])
        face_image_label.grid(row=2, column=0, columnspan=2)
        chara_label = tk.Label(center_center_frame, text="使用キャラクター画像")
        chara_label.grid(row=3, column=0, columnspan=2)
        chara_image_label = tk.Label(center_center_frame, image=self.label_image[1])
        chara_image_label.grid(row=4, column=0, columnspan=2)

        bottom_frame = tk.Frame(self.window)
        bottom_frame.pack()
        save_button = tk.Button(bottom_frame, text="Save",
                                command=lambda:save())
        save_button.grid(row=0, column=0, padx=20)
        load_button = tk.Button(bottom_frame, text="Load",
                                command=lambda:load())
        load_button.grid(row=0, column=1)

        def team_index_change(sign):
            if sign:
                self.team_index = self.team_index +1
                if self.team_index > self.team.team_length:
                    self.team_index = self.team.team_length
            else:
                self.team_index = self.team_index -1
                if self.team_index < 1:
                    self.team_index = 1
            center_center_frame.config(text=f"player_{self.team_index}/{self.team.team_length}")
            widget_update()


        def player_box_selected():
            self.team.player_load(f"FightingGameStreamHelper\GameTitle\{self.manager.title}\player\{player_box.get()}.ply",
                                  self.team_index-1)
            widget_update()

        def widget_update():
            player = self.team.team_list[self.team_index-1]
            if player.name is None:
                player_box.set("")
            else:
                player_box.set(player.name)
            face = returnImageTk(player.image, (100, 100))
            chara = openfile(f"FightingGameStreamHelper\GameTitle\{self.manager.title}\character\{player.character}/face.png")
            if chara:
                chara = returnImageTk(chara, (100, 100))
            else:
                chara = face
            self.label_image = (face, chara)
            face_image_label.config(image=self.label_image[0])
            chara_image_label.config(image=self.label_image[1])

        def save():
            self.team.name = team_name_box.get()
            filename = filedialog.asksaveasfilename(title="チームデータ保存",
                                                    defaultextension=".team",
                                                    filetypes=[("team_file", ".team")],
                                                    initialdir=f"FightingGameStreamHelper/GameTitle/{self.manager.title}/Team",
                                                    initialfile=self.team.name)
            self.team.save(filename)

        def load():
            filepath = filedialog.askopenfilename(title="チームデータ読み込み",
                                                  defaultextension=".team",
                                                  filetypes=[("player_file", ".team")],
                                                  initialdir=f"FightingGameStreamHelper/GameTitle/{self.manager.title}/Team")
            self.team = openfile(filepath)
            if self.team:
                self.team_index = 1
                team_name_box.delete(0, "end")
                team_name_box.insert(0, self.team.name)
                team_length_variable.set(self.team.team_length)
                center_center_frame.config(text=f"player_{self.team_index}/{self.team.team_length}")
                widget_update()



class LayoutWindow(Window):
    def __init__(self):
        super().__init__()

    def create(self, manager:Manager, title, width, height):
        super().call(manager, title, width, height)
        super().create()
        self.widget_list = []
        image_frame = tk.Frame(self.window)
        image_frame.pack(side=tk.RIGHT)
        self.canvas = LayoutCanvas(image_frame, 980, 540)
        self.canvas.create_background_image()

        self.left_frame = tk.LabelFrame(self.window)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH)

        top_frame = tk.Frame(self.left_frame)
        top_frame.pack()
        save_button = tk.Button(top_frame,
                                text="SAVE",
                                command=lambda:self.save())
        save_button.pack(side=tk.LEFT)
        load_button = tk.Button(top_frame,
                                text="LOAD",
                                command=lambda:self.load())
        load_button.pack(side=tk.LEFT, padx=10, pady=5)
        test_button = tk.Button(top_frame,
                                text="test",
                                command=lambda:self.manager.layout.object_check())
        test_button.pack()
        add_frame = tk.LabelFrame(self.left_frame,
                                  text="オブジェクト追加")
        add_frame.pack()
        layout_list = os.listdir(f"FightingGameStreamHelper/GameTitle/{self.manager.title}/layout")
        layout_add_box = ttk.Combobox(add_frame,
                                      width=40,
                                      values=layout_list)
        layout_add_box.pack()
        layout_add_button = tk.Button(add_frame,
                                      text="   追加   ",
                                      command=lambda:self.create_layout_image(layout_add_box))
        layout_add_button.pack()

        config_frame = tk.LabelFrame(self.left_frame,
                                     text="オブジェクト設定")
        config_frame.pack()

        self.layout_widget_frame = tk.LabelFrame(self.left_frame,
                                                 text="Setting")
        self.layout_widget_frame.pack()
        self.layout_setting()
        self.canvas.create_image_in_layoutObject(self.manager.layout)

    def save(self):
        filepath = filedialog.asksaveasfilename(title="LayoutSystemFile保存",
                                                parent=self.window,
                                                defaultextension=".lsf",
                                                filetypes=[("layoutSystemFile", ".lsf")],
                                                initialdir=f"FightingGameStreamHelper/LayoutSystem")
        self.manager.layout.save(filepath)
        self.canvas.create_image_in_layoutObject(self.manager.layout)

    def load(self):
        filepath = filedialog.askopenfilename(title="LayoutSystemFile読み込み",
                                                parent=self.window,
                                                filetypes=[("layoutSystemFile", ".lsf")],
                                                initialdir=f"FightingGameStreamHelper/LayoutSystem")
        self.manager.layout = self.manager.layout.load(filepath)
        self.manager.layout.set_maneger(self.manager)
        self.canvas.create_image_in_layoutObject(self.manager.layout)

    def overlap_check(self, data):
        if data in self.manager.layout.list:
            return True
        else:
            return False

    def create_layout_image(self, box):
        layout = Layout().load(f"FightingGameStreamHelper/GameTitle/{self.manager.title}/layout/{box.get()}")
        while self.overlap_check(layout):
            layout.rename()
        layout.create_layout_image()
        self.manager.layout.list.append(layout)
        self.canvas.create_layout_object_image(layout)
        self.layout_setting()

    def set_check(self, num, set=True):
        self.canvas.image_delete(self.manager.layout.list[num])
        if set:
            self.manager.layout.list[num].set_miror()
        if self.manager.layout.list[num].miror:
            self.widget_list[num].config(bg="blue")
        else:
            self.widget_list[num].config(bg="SystemButtonFace")
        self.canvas.create_layout_object_image(self.manager.layout.list[num])

    def layout_setting(self):
        self.layout_widget_frame.destroy()
        self.layout_widget_frame = tk.LabelFrame(self.left_frame,
                                                text="Setting")
        self.layout_widget_frame.pack()
        self.widget_list = []
        for num, layout in enumerate(self.manager.layout.list):
            frame = tk.LabelFrame(self.layout_widget_frame,
                                    text=f"{layout.name}_{layout.number}")
            frame.pack()
            check_button = tk.Button(frame,
                                        text="miror",
                                        command=lambda num=num:self.set_check(num))
            self.widget_list.append(check_button)
            # set_check(num, False)
            check_button.pack(side=tk.LEFT, padx=5)
            layer_up = tk.Button(frame,
                                    text="▲",
                                    command=lambda num=num:self.layer_move(num, -1))
            layer_up.pack(side=tk.LEFT)
            layer_down = tk.Button(frame,
                                    text="▼",
                                    command=lambda num=num:self.layer_move(num, 1))
            layer_down.pack(side=tk.LEFT)
            delete_button = tk.Button(frame,
                                        text="Delete",
                                        command=lambda num=num:self.layout_delete(num))
            delete_button.pack(side=tk.LEFT, padx=5)

    def layout_delete(self, num):
        self.canvas.image_delete(self.manager.layout.list[num])
        self.canvas.rect_delete()
        del self.manager.layout.list[num]
        del self.widget_list[num]
        self.layout_setting()

    def layer_move(self, num, sum_number):
        self.manager.layout.list[num], self.manager.layout.list[num + sum_number] = self.manager.layout.list[num + sum_number], self.manager.layout.list[num]
        self.layout_setting()
        self.canvas.image_list = self.manager.layout.list.copy()
        self.canvas.layer_update()



class CreateNewLayout(Window):
    def __init__(self):
        super().__init__()

    def create(self, manager:Manager, title, width, height):
        super().call(manager, title, width, height)
        super().create()

        image_frame = tk.Frame(self.window)
        image_frame.pack(side=tk.RIGHT)
        self.canvas = LayoutItemCreateCanvas(image_frame, 980, 540, "green")

        left_frame = tk.LabelFrame(self.window)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH)

        image_create_frame = tk.LabelFrame(left_frame,
                                           text="画像を追加")
        image_create_frame.pack(fill=tk.BOTH)
        # image_create_list_box = ttk.Combobox(image_create_frame,
        #                                      values=["丸を生成",
        #                                              "四角を生成"])
        # image_create_list_box.pack()
        # image_create_list_box.current(0)
        # image_color_frame = tk.Frame(image_create_frame, bg="red")
        # image_color_frame.pack(fill=tk.BOTH)
        # image_color_box = tk.Button(image_color_frame,
        #                             text="色を選択",
        #                             command=lambda:color_select(image_color_frame))
        # image_color_box.pack()
        # image_create_box = tk.Button(image_create_frame,
        #                              text="  生成  ")
        # image_create_box.pack()
        image_load_box = tk.Button(image_create_frame,
                                   text="画像読み込み",
                                   command=lambda:image_create())
        image_load_box.pack(pady=5)

        # text_create_frame = tk.LabelFrame(left_frame,
        #                                   text="文字を追加")
        # text_create_frame.pack()
        # text_entry_box = tk.Entry(text_create_frame,
        #                           width=30)
        # text_entry_box.pack()
        # font_list = os.listdir("FightingGameStreamHelper/font")
        # text_font_box = ttk.Combobox(text_create_frame,
        #                              values=font_list)
        # text_font_box.set("font選択")
        # text_font_box.pack()
        # text_color_frame = tk.Frame(text_create_frame, bg="red")
        # text_color_frame.pack(fill=tk.BOTH)
        # text_color_box = tk.Button(text_color_frame,
        #                             text="色を選択",
        #                             command=lambda:color_select(text_color_frame))
        # text_color_box.pack()
        # text_create_box = tk.Button(text_create_frame,
        #                             text="  生成  ")
        # text_create_box.pack()

        player_obj_create_frame = tk.LabelFrame(left_frame, text="プレイヤー")
        player_obj_create_frame.pack(fill=tk.BOTH)
        player_image_frame = tk.LabelFrame(player_obj_create_frame,
                                           text="画像")
        player_image_frame.pack(fill=tk.BOTH, padx=5, pady=5)
        player_image_select_box = ttk.Combobox(player_image_frame,
                                               values=["プレイヤー",
                                                       "キャラ",
                                                       "国籍",
                                                       "所属チーム"])
        player_image_select_box.current(0)
        player_image_select_box.pack()
        player_image_create_button = tk.Button(player_image_frame,
                                               text="  生成  ",
                                               command=lambda:obj_create(player_image_select_box, True, "player"))
        player_image_create_button.pack(pady=5)
        player_text_frame = tk.LabelFrame(player_obj_create_frame,
                                          text="テキスト")
        player_text_frame.pack(fill=tk.BOTH, padx=5, pady=5)
        player_text_select_box = ttk.Combobox(player_text_frame,
                                             values=["プレイヤー名",
                                                     "使用キャラ",
                                                     "国籍",
                                                     "所属チーム",
                                                     "twitter",
                                                     "備考"])
        player_text_select_box.pack()
        player_text_select_box.current(0)
        player_text_create_button = tk.Button(player_text_frame,
                                             text="  生成  ",
                                             command=lambda:obj_create(player_text_select_box, False, "player"))
        player_text_create_button.pack(pady=5)

        team_create_frame = tk.LabelFrame(left_frame, text="チーム")
        team_create_frame.pack(fill=tk.BOTH)
        team_name_create_button = tk.Button(team_create_frame,
                                            text="チーム名生成",
                                            command=lambda:teamname_obj_create())
        team_name_create_button.pack()
        team_image_create_frame = tk.LabelFrame(team_create_frame, text="画像")
        team_image_create_frame.pack(fill=tk.BOTH, padx=5, pady=5)
        team_image_select_box = ttk.Combobox(team_image_create_frame,
                                             values=["プレイヤー",
                                                     "キャラ",
                                                     "国籍",
                                                     "所属チーム"])
        team_image_select_box.current(0)
        team_image_select_box.pack()
        team_image_create_button = tk.Button(team_image_create_frame,
                                             text="  生成  ",
                                             command=lambda:obj_create(team_image_select_box, True, "team"))
        team_image_create_button.pack(pady=5)
        team_text_create_frame = tk.LabelFrame(team_create_frame, text="テキスト")
        team_text_create_frame.pack(fill=tk.BOTH, padx=5, pady=5)
        team_text_select_box = ttk.Combobox(team_text_create_frame,
                                             values=["プレイヤー名",
                                                     "使用キャラ",
                                                     "国籍",
                                                     "所属チーム",
                                                     "twitter",
                                                     "備考"])
        team_text_select_box.pack()
        team_text_select_box.current(0)
        team_text_create_button = tk.Button(team_text_create_frame,
                                             text="  生成  ",
                                             command=lambda:obj_create(team_text_select_box, False, "team"))
        team_text_create_button.pack(pady=5)

        counter_create_frame = tk.LabelFrame(left_frame,
                                             text="カウンター")
        counter_create_frame.pack(fill=tk.BOTH)
        counter_create_button = tk.Button(counter_create_frame,
                                          text="  生成  ",
                                          command=lambda:coutner_obj_create())
        counter_create_button.pack(padx=5, pady=5)


        layer_frame = tk.Frame(self.window)
        layer_frame.pack(side=tk.LEFT)
        layer_variable = tk.StringVar(value="")
        layer_box  = tk.Listbox(layer_frame,
                                listvariable=layer_variable,
                                height=30,
                                width=40)
        layer_box.bind('<<ListboxSelect>>', lambda event:listbox_select(event))
        layer_box.pack(side=tk.LEFT)
        delete_button = tk.Button(layer_frame,
                                  text="Delete",
                                  command=lambda:obj_delete())
        delete_button.pack()
        save_button = tk.Button(layer_frame,
                                text="Save",
                                command=lambda:save())
        save_button.pack(pady=5)
        load_button = tk.Button(layer_frame,
                                text="Load",
                                command=lambda:load())
        load_button.pack(pady=5)
        layer_button_frame = tk.Frame(layer_frame)
        layer_button_frame.pack(side=tk.LEFT)
        layer_up_button = tk.Button(layer_button_frame, text="↑",
                                    command=lambda:layer_move(-1))
        layer_up_button.pack()
        layer_down_button = tk.Button(layer_button_frame, text="↓",
                                      command=lambda:layer_move(1))
        layer_down_button.pack()

        def save():
            filepath = filedialog.asksaveasfilename(title="LayoutObject保存",
                                                    parent=self.window,
                                                    defaultextension=".layout",
                                                    filetypes=[("layout_file", ".layout")],
                                                    initialdir=f"FightingGameStreamHelper/GameTitle/{self.manager.title}/layout")
            self.canvas.save_layout(filepath)

        def load():
            filepath = filedialog.askopenfilename(title="LayoutObject読み込み",
                                                  parent=self.window,
                                                  filetypes=[("layout_file", ".layout")],
                                                  initialdir=f"FightingGameStreamHelper/GameTitle/{self.manager.title}/layout")
            self.canvas.load_layout(filepath)
            name_list_update()

        def image_create():
            filepath = filedialog.askopenfilename(title="画像読み込み",
                                                  parent=self.window,
                                                  initialdir=f"FightingGameStreamHelper/image")
            self.canvas.create_image(filepath)
            name_list = [f"{image.name}_{image.number}" for image in self.canvas.image_list]
            layer_variable.set(name_list)

        def listbox_select(event):
            num = layer_box.curselection()
            image = self.canvas.image_list[num[0]]
            self.canvas.image_select(image.name)

        def color_select(widget):
            color = colorchooser.askcolor()
            widget.config(background=color[1])

        def name_list_update():
            name_list = [f"{image.name}_{image.number}" for image in self.canvas.image_list]
            layer_variable.set(name_list)

        def layer_move(sum_number):
            num = layer_box.curselection()[0]
            self.canvas.image_list[num], self.canvas.image_list[num + sum_number] = self.canvas.image_list[num + sum_number], self.canvas.image_list[num]
            name_list_update()
            self.canvas.layer_update()
            layer_box.select_clear(0, tk.END)
            layer_box.select_set(num + sum_number)

        def obj_create(widget, square:bool, style:str):
            name_dic = {"プレイヤー名":"name",
                        "使用キャラ":"character",
                        "所属チーム":"team",
                        "twitter":"twitter",
                        "国籍":"country",
                        "備考":"memo",
                        "プレイヤー":"image",
                        "キャラ":"character"}
            name = widget.get()
            self.canvas.create_object(square, style, name_dic[name])
            name_list_update()

        def teamname_obj_create():
            self.canvas.create_object(False, "team", "title")
            name_list_update()

        def coutner_obj_create():
            self.canvas.create_object(True, "counter", "counter")
            name_list_update()

        def obj_delete():
            num = layer_box.curselection()
            image = self.canvas.image_list[num[0]]
            self.canvas.image_delete(image)
            name_list_update()