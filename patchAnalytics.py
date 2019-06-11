#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 11:07:27 2019

@author: ahir.chatterjee
"""

import os
import json
import requests

class Champ:
    
    def __init__(self, name, regions, picks, bans, presence):
        self.name = name
        self.regions = regions

def loadFile(fileName):
    tempStr = ""
    tempList = [-1,-1]
    if(os.path.exists(fileName)):
        openFile = open(fileName,'r')
        for line in openFile:
            tempStr += line
        if(len(tempStr) > 0):
            tempList = json.loads(tempStr)
    return tempList

def saveInfo(fileName, data, version):
    wrapperList = []
    with open(fileName,'w') as outfile:
        #for obj in data:
        wrapperList.append(version)
        wrapperList.append(data)
        json.dump(wrapperList,outfile)
        print(fileName + " saved successfully.")
        
def createChampList():    
    api_key = "?api_key=" + "RGAPI-ea84a7a7-23e9-4d37-8a86-9a94bae78a88"
    
    versionInfo = json.loads(requests.get("https://ddragon.leagueoflegends.com/realms/na.json" + api_key).text)["n"]
    champVersion = versionInfo["champion"]    
    
    champInfo = {}
    loadedInfo = loadFile("champs.txt")
    if(loadedInfo[0] == champVersion):
        champInfo = loadedInfo[1]
        print("champs.txt version up to date")
    else:
        champInfo = json.loads(requests.get("http://ddragon.leagueoflegends.com/cdn/" + champVersion + "/data/en_US/champion.json" + api_key).text)
        saveInfo("champs.txt",champInfo,champVersion)
        print("champs.txt updated")
    
    champList = []
    for champ in champInfo["data"]:
        champList.append(champInfo["data"][champ]["name"])
    
    return champList
        
champList = createChampList()
