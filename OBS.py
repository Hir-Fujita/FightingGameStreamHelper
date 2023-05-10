#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from obswebsocket import obsws, requests as rq
import json
from pprint import pprint

HOST = "192.168.1.11"
PORT = "4444"
PASS = "T3MlHQt7WEOcEzUL"

class OBS:
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password
        self.obs = obsws(self.host, self.port, self.password)

    def obsTextChange(self, scene_name: str, source_name: str, filename):
        self.obs.connect()
        source = self.obs.call(rq.GetSceneItemList(sceneName=scene_name)).datain["sceneItems"]
        for s in source:
            if s["sourceName"] == source_name:
                break
        print(s)
        # a = self.obs.call(rq.GetSceneItemId(sourceName=source_name, sceneName=scene_name))
        # id = a.datain["sceneItemId"]
        # a = self.obs.call(rq.GetSceneItemTransform(sceneName=scene_name, sceneItemId=id))
        # print(a)
        # a = self.obs.call(rq.SetSceneItemTransform(sceneName=scene_name, sceneItemId=id, sceneItemTransform={"scale.x": 2, "scale.y": 2}))
        a = self.obs.call(rq.SetCurrentProgramScene(sceneName=scene_name))
        # print(a)

        scene_list = self.obs.call(rq.GetSceneList())
        if scene_list.status:
            sources = scene_list.getSources()
            print(sources)
        else:
            print("Failed to get sources list")
        for scene in scene_list.getScenes():
            sources = scene.getSources()
            for source in sources:
                print(source.getName())
        self.obs.disconnect()




a = OBS(HOST, PORT, PASS)
a.obsTextChange("scene1", "画像", "FightingGameStreamHelper/image/あいざっく.jpg")


