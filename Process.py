#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pickle
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageOps, ImageFont

IMAGE_EXTENSION = ["jpg", "JPG", "png", "PNG"]

def image_check(filepath):
    if filepath[-3:] in IMAGE_EXTENSION:
        return True
    else:
        return False

def Object_check(filepath):
    if filepath[-3:] == "ply" or filepath[-4:] == "team":
        return True
    else:
        return False

def textsize(text, font="meiryo.ttc"):
    image = Image.new("RGBA", size=(100,100), color=(0,0,0,0))
    font = ImageFont.truetype(f"FightingGameStreamHelper/font/{font}", 40)
    draw = ImageDraw.Draw(image)
    size = draw.textsize(text, font)
    return size, font

def Object_image_create(style:str, square=False):
    size, font = textsize(style)
    if square:
        out_size = (300, 300)
        rect_color = "blue"
        style = style.replace(".", "\n")
    else:
        out_size = (int(size[0]*1.2), int(size[1]*1.2))
        rect_color = "red"
    image = Image.new("RGBA", size=out_size, color=(0,0,0,0))
    draw = ImageDraw.Draw(image)
    draw.rectangle([(0,0),(out_size[0]-1, out_size[1]-1)],
                   width=5,
                   outline=rect_color)
    draw.text((int(out_size[0]/2),(int(out_size[1]/2))),
              style,
              font=font,
              fill="white",
              stroke_width=5,
              stroke_fill="black",
              anchor="mm")
    return image

# def generate_image(text:str, fontname:str, fill="white", width=5, stroke_fill="black"):
#     size, font = textsize(text, fontname)
#     image = Image.new("RGBA", size=size, color=(0,0,0,0))
#     draw = ImageDraw.Draw(image)
#     draw.text((0, 0),
#               text,
#               font=font,
#               fill=fill,
#               stroke_width=width,
#               stroke_fill=stroke_fill)
#     return image

def openfile(filepath):
    if not os.path.isfile(filepath):
        print("ファイル読み込みエラー")
        return False
    else:
        if image_check(filepath):
            data = Image.open(filepath)
        if Object_check(filepath):
            with open(filepath, "rb") as f:
                data = pickle.load(f)
        return data

def returnImageTk(image, resize=None, miror=None):
    if type(image) is str:
        copy_image = Image.open(image)
    else:
        copy_image = image.copy()
    if resize is not None:
        copy_image.thumbnail(resize, resample=3)
    if miror is not None:
        copy_image = ImageOps.mirror(copy_image)
    return_image = ImageTk.PhotoImage(copy_image)
    return return_image

def name_paste(image, name):
    draw = ImageDraw.Draw(image)
    _, font = textsize(name)
    draw.text((0, 0),
              name,
              font=font,
              fill="yellow",
              stroke_width=5,
              stroke_fill="black")
    return image

def text_image_create(text, size):
    t_size, font = textsize(text)
    image = Image.new("RGBA", size=(t_size[0]+10, t_size[1]+10), color=(0,0,0,0))
    draw = ImageDraw.Draw(image)
    draw.text((5, 5),
              text,
              font=font,
              fill="yellow",
              stroke_width=5,
              stroke_fill="black")
    image = image.resize(size)
    return image

class GenerateImage:
    def __init__(self, maneger):
        self.maneger = maneger
        self.image = Image.new("RGBA", size=(1920, 1080), color=(0,0,0,0))

    def debug_show(self):
        self.image.show("title")

    def image_object_create(self, object, layout):
        size = (object.size[0]*2,
                object.size[1]*2)
        if layout.miror:
            position = (layout.position[0]*2 + (layout.size[0]*2 - object.position[0]*2- size[0]),
                        layout.position[1]*2 + object.position[1]*2)
        else:
            position = (layout.position[0]*2 + object.position[0]*2,
                        layout.position[1]*2 + object.position[1]*2)
        image = object.resize(size, return_flag=True)
        if layout.miror:
            image = ImageOps.mirror(image)
        if image.mode == "RGBA":
            self.image.paste(image, position, mask=image)
        else:
            self.image.paste(image, position)

    def player_object_create(self, object, player, layout):
        image = None
        size = (object.size[0]*2,
                object.size[1]*2)
        if layout.miror:
            position = (layout.position[0]*2 + (layout.re_size[0]*2 - object.position[0]*2- size[0]),
                        layout.position[1]*2 + object.position[1]*2)
        else:
            position = (layout.position[0]*2 + object.position[0]*2,
                        layout.position[1]*2 + object.position[1]*2)

        if object.category == "image":
            if object.sub_style == "character":
                image = Image.open(f"FightingGameStreamHelper\GameTitle\{player.gametitle}\character\{player.character}/face.png")
                image = image.resize(size)
            if object.sub_style == "image":
                image = player.image.resize(size)
            if layout.miror:
                image = ImageOps.mirror(image)
        if object.category == "text":
            if object.sub_style == "name":
                text = player.name
            elif object.sub_style == "character":
                text = self.maneger.character_dict[str(player.character)]
            elif object.sub_style == "team":
                text = player.team
            elif object.sub_style == "twitter":
                text = player.twitter
            elif object.sub_style == "country":
                text = player.country
            elif object.sub_style == "memo":
                text = player.memo
            if text != "":
                image = text_image_create(text, size)
        if image is not None:
            if image.mode == "RGBA":
                self.image.paste(image, position, mask=image)
            else:
                self.image.paste(image, position)

    def save(self, filename):
        if filename != "":
            self.image.save(f"FightingGameStreamHelper/{filename}.png")
        else:
            print("filename_error")





class Variable:
    def __init__(self):
        self.team_length = tk.IntVar(value=1)

