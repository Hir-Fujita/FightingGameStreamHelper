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

def generate_image(text:str, fontname:str, fill="white", width=5, stroke_fill="black"):
    size, font = textsize(text, fontname)
    image = Image.new("RGBA", size=size, color=(0,0,0,0))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0),
              text,
              font=font,
              fill=fill,
              stroke_width=width,
              stroke_fill=stroke_fill)
    return image

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

class Variable:
    def __init__(self):
        self.team_length = tk.IntVar(value=1)

