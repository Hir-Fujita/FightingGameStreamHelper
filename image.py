#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup
import io
from PIL import Image
from pprint import pprint


url = requests.get("https://www.guiltygear.com/ggst/jp/character/")
soup = BeautifulSoup(url.text,"html.parser")

face_start = '<img alt="" src='
face_end = '/><i class='


face_list = re.findall(r'<a href="(.*)">', str(soup))
new_list = [url.replace("'","") for url in face_list if "https://www.guiltygear.com/ggst/jp/character/" in url]
new_list = new_list[1:-1]

# for num, face in enumerate(face_list):
#     image = Image.open(io.BytesIO(requests.get(face).content))
#     image.save(f"FightingGameStreamHelper/image/{num}.png", quality=95)





for url in new_list:
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    image_url = re.findall(r' srcset="(.*)"/><img alt="" src=', str(soup))
    # image_url = re.findall(r'srcset="https://www.guiltygear.com/(.*).png', str(image_url))
    print(image_url)
