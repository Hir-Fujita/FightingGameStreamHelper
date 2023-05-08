#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import tkinter as tk
from Process import openfile, returnImageTk, image_check, Object_image_create
import Object


class Canvas:
    def __init__(self, master, width, height):
        self.canvas = tk.Canvas(master,
                                width=width,
                                height=height,
                                relief="ridge",
                                borderwidth="2")
        self.canvas.bind("<Button-1>", lambda event:self.left_click(event))
        self.canvas.bind("<Button1-Motion>", lambda event:self.mouse_drag(event))
        self.canvas.bind("<ButtonRelease>", lambda event:self.mouse_release())
        self.canvas.pack()
        self.image_list = []

    def overlap_check(self, data):
        if data in self.image_list:
            return True
        else:
            return False

    def tag_get_all(self):
        ids = self.canvas.find_all()
        tags = [self.canvas.gettags(tag) for tag in ids]
        return tags

    def find_bbox(self, name):
        bbox = self.canvas.bbox(name)
        return bbox

    def find_tag(self, event):
        closest_ids = self.canvas.find_closest(event.x, event.y)
        if len(closest_ids) != 0:
            tag = self.canvas.gettags(closest_ids[0])
            return tag

    def rect_delete(self):
        tags = self.tag_get_all()
        for tag in tags:
            if "rect" in tag[0]:
                self.canvas.delete(tag[0])

    def image_select(self, image_name):
        # (x0, y0, x1, y1)
        self.rect_delete()
        self.move_tag_delete()
        color = "red"
        rect_size = 3
        for image in self.image_list:
            if f"{image.name}_{image.number}" == image_name:
                self.tag = (f"{image.name}_{image.number}", "current")
                self.canvas.addtag_withtag("move", image_name)
                bbox = self.find_bbox(f"{image.name}_{image.number}")
                self.canvas.create_rectangle(bbox[0],
                                             bbox[1],
                                             bbox[2],
                                             bbox[3],
                                             width=2,
                                             tag=(f"rect", "move"))
                self.canvas.create_rectangle(bbox[0] -rect_size,
                                             bbox[1] -rect_size,
                                             bbox[0] +rect_size,
                                             bbox[1] +rect_size,
                                             fill=color,
                                             tag=(f"rect_left_top", "move"))
                self.canvas.create_rectangle(bbox[2] -rect_size,
                                             bbox[1] -rect_size,
                                             bbox[2] +rect_size,
                                             bbox[1] +rect_size,
                                             fill=color,
                                             tag=(f"rect_right_top", "move"))
                self.canvas.create_rectangle(bbox[0] -rect_size,
                                             bbox[3] -rect_size,
                                             bbox[0] +rect_size,
                                             bbox[3] +rect_size,
                                             fill=color,
                                             tag=(f"rect_left_bottom", "move"))
                self.canvas.create_rectangle(bbox[2] -rect_size,
                                             bbox[3] -rect_size,
                                             bbox[2] +rect_size,
                                             bbox[3] +rect_size,
                                             fill=color,
                                             tag=(f"rect_right_bottom", "move"))
                x_middle = (bbox[0] + bbox[2]) /2
                y_middle = (bbox[1] + bbox[3]) /2
                self.canvas.create_rectangle(x_middle -rect_size,
                                             bbox[1] -rect_size,
                                             x_middle +rect_size,
                                             bbox[1] +rect_size,
                                             fill=color,
                                             tag=(f"rect_top", "move"))
                self.canvas.create_rectangle(x_middle -rect_size,
                                             bbox[3] -rect_size,
                                             x_middle +rect_size,
                                             bbox[3] +rect_size,
                                             fill=color,
                                             tag=(f"rect_bottom", "move"))
                self.canvas.create_rectangle(bbox[0] -rect_size,
                                             y_middle -rect_size,
                                             bbox[0] +rect_size,
                                             y_middle +rect_size,
                                             fill=color,
                                             tag=(f"rect_left", "move"))
                self.canvas.create_rectangle(bbox[2] -rect_size,
                                             y_middle -rect_size,
                                             bbox[2] +rect_size,
                                             y_middle +rect_size,
                                             fill=color,
                                             tag=(f"rect_right", "move"))

    def tag_check(self, tag):
        RESIZE = ["rect_top", "rect_bottom", "rect_left", "rect_right",
                  "rect_left_top", "rect_right_top", "rect_left_bottom", "rect_right_bottom"]
        for re in RESIZE:
            if re == tag[0]:
                self.resize_direction = tag[0]
                return True
        else:
            return False

    def mouse_drag(self, event):
        if self.resize:
            self.resize_rect(event)
        elif not self.tag_check(self.tag):
            self.canvas.move("move",
                             event.x - self.x,
                             event.y - self.y)
            self.x = event.x
            self.y = event.y

    def resize_rect(self, event):
        self.rect_delete()
        bbox = self.find_bbox(self.tag[0])
        if self.resize_direction == "rect_top":
            self.pos = (bbox[0], event.y, bbox[2], bbox[3])
        if self.resize_direction == "rect_bottom":
            self.pos = (bbox[0], bbox[1], bbox[2], event.y)
        if self.resize_direction == "rect_left":
            self.pos = (event.x, bbox[1], bbox[2], bbox[3])
        if self.resize_direction == "rect_right":
            self.pos = (bbox[0], bbox[1], event.x, bbox[3])
        if self.resize_direction == "rect_left_top":
            self.pos = (event.x, event.y, bbox[2], bbox[3])
        if self.resize_direction == "rect_right_top":
            self.pos = (bbox[0], event.y, event.x, bbox[3])
        if self.resize_direction == "rect_left_bottom":
            self.pos = (event.x, bbox[1], bbox[2], event.y)
        if self.resize_direction == "rect_right_bottom":
            self.pos = (bbox[0], bbox[1], event.x, event.y)
        self.canvas.create_rectangle(self.pos[0],
                                     self.pos[1],
                                     self.pos[2],
                                     self.pos[3],
                                     width=2,
                                     tag="resize_rect")

    def image_resize(self):
        for image in self.image_list:
            if f"{image.name}_{image.number}" == self.tag[0]:
                image.resize((self.pos[2] - self.pos[0],
                              self.pos[3] - self.pos[1]))
                self.canvas.delete(self.tag[0])
                self.canvas.create_image(self.pos[0],
                                         self.pos[1],
                                         anchor="nw",
                                         image=image.tk_image,
                                         tag=f"{image.name}_{image.number}")
                self.rect_delete()
                self.image_select(f"{image.name}_{image.number}")
                break
        self.layer_update()
        self.move_tag_delete()

    def move_tag_delete(self):
        tags = self.tag_get_all()
        for tag in tags:
            if "move" in tag:
                self.canvas.dtag(tag[0], "move")

    def left_click(self, event):
        tag = self.find_tag(event)
        self.resize = False
        print(self.image_list)
        print(f"func_leftClick_{tag}")
        if tag[-1] == "current":
            if "rect" in tag[0]:
                if self.tag_check(tag):
                    self.resize = True
                else:
                    self.rect_delete()
            else:
                self.image_select(tag[0])
                self.tag = tag
                self.x = event.x
                self.y = event.y
        else:
            self.rect_delete()

    def image_delete(self, image):
        self.canvas.delete(f"{image.name}_{image.number}")
        self.image_list.remove(image)
        self.rect_delete()

    def mouse_release(self):
        if self.resize:
            self.image_resize()
            self.resize = False
        self.move_tag_delete()

    def layer_update(self):
        tag_list = self.tag_get_all()
        for image in self.image_list:
            for tag in tag_list:
                if tag[0] == f"{image.name}_{image.number}":
                    self.canvas.lower(tag[0])
                    break

    def save_layout(self, filepath):
        layout = Object.Layout()
        min_x = 980
        max_x = 0
        min_y = 540
        max_y = 0
        for image in self.image_list:
            bbox = self.find_bbox(f"{image.name}_{image.number}")
            if min_x > bbox[0]:
                min_x = bbox[0]
            if min_y > bbox[1]:
                min_y = bbox[1]
            if max_x < bbox[2]:
                max_x = bbox[2]
            if max_y < bbox[3]:
                max_y = bbox[3]
        for image in self.image_list:
            bbox = self.find_bbox(f"{image.name}_{image.number}")
            layout_position = (bbox[0] - min_x, bbox[1] - min_y)
            image.set_position((layout_position[0], layout_position[1]))
            layout.object_list.append(image)
        layout.set_size((max_x - min_x, max_y - min_y))
        layout.set_position((min_x, min_y))
        layout.save(filepath)
        self.create_image_in_layoutObject(layout)


class LayoutCanvas(Canvas):
    def __init__(self, master, width, height):
        super().__init__(master, width, height)

    def create_background_image(self):
        self.main_image = returnImageTk(openfile("FightingGameStreamHelper\image\layout_image.png"))
        self.canvas.create_image(0,
                                 0,
                                 image=self.main_image,
                                 anchor="nw",
                                 tag="system_background")

    def create_layout_object_image(self, layout):
        self.image_list.append(layout)
        self.canvas.create_image(layout.position[0],
                                 layout.position[1],
                                 anchor="nw",
                                 image=self.image_list[-1].tk_image,
                                 tag=f"{layout.name}_{layout.number}")

    def layer_update(self):
        super().layer_update()
        for tag in self.tag_get_all():
            if "system" in tag[0]:
                self.canvas.lower(tag[0])

    def mouse_release(self):
        super().mouse_release()
        for image in self.image_list:
            bbox = self.find_bbox(f"{image.name}_{image.number}")
            image.set_position((bbox[0], bbox[1]))

    def create_image_in_layoutObject(self, layout):
        self.canvas.delete("all")
        self.create_background_image()
        self.image_list = layout.list.copy()
        for obj in reversed(self.image_list):
            self.canvas.create_image(obj.position[0],
                                     obj.position[1],
                                     anchor="nw",
                                     image=obj.tk_image,
                                     tag=f"{obj.name}_{obj.number}")



class LayoutItemCreateCanvas(Canvas):
    def __init__(self, master, width, height, background):
        super().__init__(master, width, height)
        self.canvas.config(bg=background)

    def create_image(self, filepath):
        file = image_check(filepath)
        if file:
            data = Object.ImageObject(filepath)
            while self.overlap_check(data):
                data.rename()
            self.image_list.append(data)
            self.canvas.create_image(100,
                                     100,
                                     anchor="nw",
                                     image=self.image_list[-1].tk_image,
                                     tag=f"{data.name}_{data.number}")
            self.layer_update()

    def create_object(self, square:bool, style:str, sub_style:str):
        data = Object.VariableObject(square, style, sub_style)
        while self.overlap_check(data):
            data.rename()
        self.image_list.append(data)
        self.canvas.create_image(100,
                                 100,
                                 anchor="nw",
                                 image=self.image_list[-1].tk_image,
                                 tag=f"{data.name}_{data.number}")
        self.layer_update()

    def load_layout(self, filepath):
        layout = Object.Layout()
        layout = layout.load(filepath)
        self.create_image_in_layoutObject(layout)

    def create_image_in_layoutObject(self, layout):
        self.canvas.delete("all")
        self.image_list = layout.object_list.copy()
        for object in reversed(layout.object_list):
            self.canvas.create_image(layout.position[0] + object.position[0],
                                     layout.position[1] + object.position[1],
                                     anchor="nw",
                                     image=object.tk_image,
                                     tag=object.name)