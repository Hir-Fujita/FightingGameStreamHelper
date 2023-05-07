#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, filedialog, colorchooser
import os
import pickle

from Process import openfile, returnImageTk
from Player import Player, Team
from Manager import Manager
from Canvas import LayoutItemCreateCanvas, LayoutCanvas
from Object import Layout

class Window:
    def __init__(self):
        self.window = None

    def call(self, manager:Manager, title, width, height):
        self.manager = manager
        self.title = f"{title}_{self.manager.title}"
        self.width = width
        self.height = height

    def create(self):
        if self.window is not None:
            self.window_close()
        self.window = tk.Toplevel()
        self.window.geometry(f"{self.width}x{self.height}")
        self.window.title(f"{self.title}")
        self.window.protocol("WM_DELETE_WINDOW",self.window_close)

    def window_close(self):
        self.window.destroy()
        self.window = None


class PlayerRegisterWindow(Window):
    def __init__(self):
        super().__init__()

    def create(self, manager:Manager, title, width, height):
        super().call(manager, title, width, height)
        super().create()
        self.player = Player()
        game_title = tk.Label(self.window, text=f"GameTitle_{self.manager.title}")
        game_title.pack()
        left_frame = tk.Frame(self.window)
        left_frame.pack(side=tk.LEFT)
        name_label = tk.Label(left_frame, text="プレイヤー名")
        name_label.grid(row=0, column=0, padx=2, pady=2)
        name_box = tk.Entry(left_frame, width=30)
        name_box.grid(row=0, column=1, padx=2, pady=2)
        chara_list = [value for _, value in self.manager.character_dict.items()]
        chara_label = tk.Label(left_frame, text="使用キャラ")
        chara_label.grid(row=1, column=0, padx=2, pady=2)
        chara_box = ttk.Combobox(left_frame, values=chara_list, width=27)
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
        self.face_image = returnImageTk("FightingGameStreamHelper/image/face.png", resize=(250,250))
        face_image_box = tk.Label(right_frame, image=self.face_image)
        face_image_box.grid(row=1, column=0)
        face_button = tk.Button(right_frame, text="画像読み込み",
                                command=lambda:face_image_change(face_image_box))
        face_button.grid(row=2, column=0)

        def face_image_change(widget):
            filename = filedialog.askopenfilename(multiple=False)
            if filename is not None:
                self.player.image = openfile(filename)
                self.face_image = returnImageTk(self.player.image, resize=(250,250))
                widget.config(image=self.face_image)

        def save():
            self.player.name = name_box.get()
            self.player.gametitle = self.manager.title
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
                                                    defaultextension=".ply",
                                                    filetypes=[("player_file", ".ply")],
                                                    initialdir=f"FightingGameStreamHelper/GameTitle/{self.manager.title}/player",
                                                    initialfile=save_filename)
            with open(filename, "wb") as f:
                pickle.dump(self.player, f)

        def load():
            filepath = filedialog.askopenfilename(title="プレイヤーデータ読み込み",
                                                  defaultextension=".ply",
                                                  filetypes=[("player_file", ".ply")],
                                                  initialdir=f"FightingGameStreamHelper/GameTitle/{self.manager.title}/player")
            self.player = openfile(filepath)
            if not self.player:
                self.player = Player()
            else:
                if not self.manager.title == self.player.gametitle:
                    print("ゲームタイトルが不正です")
                else:
                    name_box.delete(0, "end")
                    name_box.insert(0, self.player.name)
                    if self.player.country > 0:
                        country_box.current(self.player.country)
                    twitter_box.delete(0, "end")
                    twitter_box.insert(0, self.player.twitter)
                    affiliation_box.delete(0, "end")
                    affiliation_box.insert(0, self.player.team)
                    memo_box.delete(1.0, "end")
                    memo_box.insert(1.0, self.player.memo)
                    self.face_image = returnImageTk(self.player.image, (250,250))
                    face_image_box.config(image=self.face_image)



class TeamRegisterWindow(Window):
    def __init__(self):
        super().__init__()

    def create(self, manager:Manager, title, width, height):
        super().call(manager, title, width, height)
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
            chara = openfile(f"FightingGameStreamHelper\GameTitle\{self.manager.title}\chara\{player.character}/face.png")
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
            with open(filename, "wb") as f:
                pickle.dump(self.team, f)

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



class RayoutWindow(Window):
    def __init__(self):
        super().__init__()

    def create(self, manager:Manager, title, width, height):
        super().call(manager, title, width, height)
        super().create()
        self.layout_list = []
        self.widget_list = []
        image_frame = tk.Frame(self.window)
        image_frame.pack(side=tk.RIGHT)
        self.canvas = LayoutCanvas(image_frame, 980, 540)
        self.canvas.create_background_image()

        left_frame = tk.LabelFrame(self.window)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH)
        add_frame = tk.LabelFrame(left_frame,
                                  text="オブジェクト追加")
        add_frame.pack()
        layout_list = os.listdir(f"FightingGameStreamHelper/GameTitle/{self.manager.title}/layout")
        layout_add_box = ttk.Combobox(add_frame,
                                      width=40,
                                      values=layout_list)
        layout_add_box.pack()
        layout_add_button = tk.Button(add_frame,
                                      text="   追加   ",
                                      command=lambda:create_layout_image())
        layout_add_button.pack()

        config_frame = tk.LabelFrame(left_frame,
                                     text="オブジェクト設定")
        config_frame.pack()

        layout_create_button = tk.Button(left_frame,
                                         text="新規オブジェクト作成",
                                         command=lambda:self.create_new_layout())
        layout_create_button.pack()

        self.layout_widget_frame = tk.LabelFrame(left_frame,
                                                 text="Setting")
        self.layout_widget_frame.pack()

        def create_layout_image():
            layout = Layout().load(f"FightingGameStreamHelper/GameTitle/{self.manager.title}/layout/{layout_add_box.get()}")
            for item in self.layout_list:
                if item.name == layout.name:
                    layout.name = f"_{layout.name}"
            layout.create_layout_image()
            self.layout_list.append(layout)
            self.canvas.create_layout_object_image(layout)
            layout_setting()

        def set_check(num, set=True):
            self.canvas.canvas.delete(self.layout_list[num].name)
            if set:
                self.layout_list[num].set_miror()
            if self.layout_list[num].miror:
                self.widget_list[num].config(bg="blue")
            else:
                self.widget_list[num].config(bg="SystemButtonFace")
            self.canvas.create_layout_object_image(self.layout_list[num])

        def layout_setting():
            self.layout_widget_frame.destroy()
            self.layout_widget_frame = tk.LabelFrame(left_frame,
                                                 text="Setting")
            self.layout_widget_frame.pack()
            self.widget_list = []
            for num, layout in enumerate(self.layout_list):
                frame = tk.LabelFrame(self.layout_widget_frame,
                                      text=f"{layout.name}")
                frame.pack()
                check_button = tk.Button(frame,
                                         text="miror",
                                         command=lambda num=num:set_check(num))
                self.widget_list.append(check_button)
                set_check(num, False)
                check_button.pack()

    def create_new_layout(self):
        window = CreateNewLayout()
        window.create(self.manager,
                      "新規オブジェクト作成",
                      980 + 300 + 300,
                      540)




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
                                               command=lambda:obj_create(player_image_select_box, "player", True))
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
                                             command=lambda:obj_create(player_text_select_box, "player", False))
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
                                             command=lambda:obj_create(team_image_select_box, "team", True))
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
                                             command=lambda:obj_create(team_text_select_box, "team", False))
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
            name_list = [image.name for image in self.canvas.image_list]
            layer_variable.set(name_list)

        def listbox_select(event):
            num = layer_box.curselection()
            image = self.canvas.image_list[num[0]]
            self.canvas.image_select(image.name)

        def color_select(widget):
            color = colorchooser.askcolor()
            widget.config(background=color[1])

        def name_list_update():
            name_list = [image.name for image in self.canvas.image_list]
            layer_variable.set(name_list)

        def layer_move(sum_number):
            num = layer_box.curselection()[0]
            self.canvas.image_list[num], self.canvas.image_list[num + sum_number] = self.canvas.image_list[num + sum_number], self.canvas.image_list[num]
            name_list_update()
            self.canvas.layer_update()
            layer_box.select_clear(0, tk.END)
            layer_box.select_set(num + sum_number)

        def obj_create(widget, object_title:str, square):
            name_dic = {"プレイヤー名":"name",
                        "使用キャラ":"character",
                        "所属チーム":"team",
                        "twitter":"twitter",
                        "国籍":"country",
                        "備考":"memo",
                        "プレイヤー":"image",
                        "キャラ":"character"}
            name = widget.get()
            if square:
                self.canvas.create_object(f"Image.{object_title}.{name_dic[name]}", square)
            else:
                self.canvas.create_object(f"Text.{object_title}.{name_dic[name]}", square)
            name_list_update()

        def teamname_obj_create():
            self.canvas.create_object("TeamTitle", square=False)
            name_list_update()

        def coutner_obj_create():
            self.canvas.create_object("counter", square=True)
            name_list_update()

        def obj_delete():
            num = layer_box.curselection()
            image = self.canvas.image_list[num[0]]
            self.canvas.image_delete(image)
            name_list_update()