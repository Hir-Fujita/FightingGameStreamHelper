#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image
from Process import openfile

class Player:
    def __init__(self):
        self.name = None
        self.gametitle = None
        self.character = None
        self.country = None
        self.twitter = None
        self.team = None
        self.memo = None
        self.image = openfile("FightingGameStreamHelper/image/face.png")

    def __repr__(self):
        return repr((f"name:{self.name}",
                     f"gametitle:{self.gametitle}",
                     f"character:{self.character}",
                     f"country:{self.country}",
                     f"twitter:{self.twitter}",
                     f"team:{self.team}",
                     f"memo:{self.memo}"))


class Team:
    def __init__(self):
        self.name = None
        self.team_list = []
        self.team_length = 0
        self.team_length_change(1)

    def team_length_change(self, length=int):
        if self.team_length < length:
            for i in range(length - self.team_length):
                player = Player()
                self.team_list.append(player)
        else:
            for i in range(self.team_length - length):
                self.team_list.remove(self.team_list[-1])
        self.team_length = length

    def player_load(self, filepath, index=int):
        player = openfile(filepath)
        if player:
            self.team_list[index] = player

