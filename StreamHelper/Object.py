#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pickle
import os
from PIL import Image

from Process import Process

class Player(Process):
    def __init__(self):
        super().__init__()
        self.name = None
        self.gametitle = None
        self.character = None
        self.country = None
        self.twitter = None
        self.team = None
        self.memo = None
        self.image = self.openfile("FightingGameStreamHelper/image/face.png")

    def __repr__(self):
        return repr((f"name:{self.name}",
                     f"gametitle:{self.gametitle}",
                     f"character:{self.character}",
                     f"country:{self.country}",
                     f"twitter:{self.twitter}",
                     f"team:{self.team}",
                     f"memo:{self.memo}"))


class Team(Process):
    def __init__(self):
        super().__init__()
        self.check_flag = False

    def __repr__(self):
        pass