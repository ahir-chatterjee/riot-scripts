# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 15:07:29 2018

@author: ahirc
"""
import requests
import json
import os

api_key = "?api_key=" + "RGAPI-d9f4ad00-292e-4b46-9f2e-4b80163e60a2"
versionInfo = json.loads(requests.get("https://ddragon.leagueoflegends.com/realms/na.json" + api_key).text)["n"]
itemVersion = versionInfo["item"]
champVersion = versionInfo["champion"]
runeVersion = versionInfo["summoner"]

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

itemInfo = {}
champInfo = {}
runeInfo = {}
loadedInfo = loadFile("items.txt")
if(loadedInfo[0] == itemVersion):
    itemInfo = loadedInfo[1]
    print("items.txt version up to date")
else:
    itemInfo = json.loads(requests.get("http://ddragon.leagueoflegends.com/cdn/" + itemVersion + "/data/en_US/item.json" + api_key).text)
    print("items.txt updated")
loadedInfo = loadFile("champs.txt")
if(loadedInfo[0] == champVersion):
    champInfo = loadedInfo[1]
    print("champs.txt version up to date")
else:
    champInfo = json.loads(requests.get("http://ddragon.leagueoflegends.com/cdn/" + champVersion + "/data/en_US/champion.json" + api_key).text)
    print("champs.txt updated")
loadedInfo = loadFile("runes.txt")
if(loadedInfo[0] == runeVersion):
    runeInfo = loadedInfo[1]
    print("runes.txt version up to date")
else:
    runeInfo = json.loads(requests.get("http://ddragon.leagueoflegends.com/cdn/" + itemVersion + "/data/en_US/runesReforged.json" + api_key).text)
    print("runes.txt updated")

class Item:
    def __init__(self, item, uniqueNum):
        self.name = item["name"]
        self.cost = item["gold"]["base"]
        self.sellCost = item["gold"]["sell"]
        self.builtFrom = []
        if("from" in item.keys()):
            self.builtFrom = item["from"]
        self.buildTo = []
        if("into" in item.keys()):
            self.buildTo = item["into"]
        self.stats = item["stats"]
        self.uniqueNum = uniqueNum
        
class Champ:
    def __init__(self, champ):
        self.name = champ["name"]
        self.mana = True
        if(not(champ["partype"] == "mana")):
            self.mana = False
        self.stats = champ["stats"]
        self.key = champ["key"]
        
class Rune:
    def __init__(self, rune):
        self.rune = rune
        
statDict = {"FlatArmorMod":"armor","FlatCritChanceMod":"crit","FlatHPPoolMod":"hp","FlatMPPoolMod":"mp","FlatMagicDamageMod":"ap",
            "FlatPhysicalDamageMod":"attackdamage","FlatSpellBlockMod":"spellblock","PercentAttackSpeedMod":"attackspeed","PercentLifeStealMod":"lifesteal",
            "PercentMovementSpeedMod":"movespeed"}
        
class Player:
    def __init__(self, items, champ, lvl, runes, other):
        self.items = items
        self.champ = champ
        self.lvl = lvl
        self.runes = runes
        self.other = other
        self.stats = {}
        for stat in champ.stats:
            self.stats[stat] = champ.stats[stat]
        self.stats["ap"] = 0.0
        self.stats["lifesteal"] = 0.0
    def calculateDps(self, target):
        self.updateStats()
        target.updateStats()
    def updateStats(self):
        for stat in self.stats:
            checkString = "perlevel"
            #print(stat[len(stat)-len(checkString):])
            if(stat[len(stat)-len(checkString):] == checkString): #need to check if last 8 characters 
                statToUpdate = stat[:len(stat)-len(checkString)]
                for num in range(2,self.lvl+1):
                    self.stats[statToUpdate] = self.stats[statToUpdate] + (((num*.035)+.65)*(self.stats[stat]))
                    if(statToUpdate == "hp"):
                        print(self.stats[statToUpdate])
        for item in self.items:
            doCode = ""
            
def saveInfo(fileName, data, version):
    wrapperList = []
    with open(fileName,'w') as outfile:
        #for obj in data:
        wrapperList.append(version)
        wrapperList.append(data)
        json.dump(wrapperList,outfile)
        print(fileName + " saved successfully.")
        
#basic
#data
#groups?
#tree?
itemDict = {}
champDict = {}
    
#print(itemInfo["groups"])

for itemNum in itemInfo["data"]:
    item = itemInfo["data"][itemNum]
    if(item["maps"]["11"] == True and item["gold"]["purchasable"]):
        itemDict[item["name"]] = Item(item,itemNum)
    #name
    #description
    #colloq
    #plaintext
    #image
    #gold
    #tags
    #maps
    #stats
    #effect
    #print(itemInfo["data"][key]["name"])
    
for champName in champInfo["data"]:
    champ = champInfo["data"][champName]
    champDict[champ["name"]] = Champ(champ)
    
itemDict.pop("Archangel's Staff (Quick Charge)")
itemDict.pop("Broken Stopwatch")
itemDict.pop("Entropy Field")
itemDict.pop("Flash Zone")
itemDict.pop("Manamune (Quick Charge)")
itemDict.pop("Port Pad")
itemDict.pop("Rod of Ages (Quick Charge)")
itemDict.pop("Shield Totem")
itemDict.pop("Siege Ballista")
itemDict.pop("Siege Refund")
itemDict.pop("Tear of the Goddess (Quick Charge)")
itemDict.pop("Tower: Beam of Ruination")
itemDict.pop("Tower: Storm Bulwark")
itemDict.pop("Vanguard Banner")
#for itemName in itemDict:
#    print(itemName)
#    
#for champName in champDict:
#    print(champName)
 
items = [itemDict.get("Doran's Blade"), itemDict.get("Health Potion")]
oppItems = [itemDict.get("Doran's Blade"), itemDict.get("Health Potion")]
champ = champDict.get("Caitlyn")
oppChamp = champDict.get("Varus")
lvl = 18
oppLvl = 1 
runes = []
oppRunes = []
misc = {}
oppMisc = {}

player = Player(items, champ, lvl, runes, misc)
oppPlayer = Player(oppItems, oppChamp, oppLvl, oppRunes, oppMisc)
player.updateStats()



saveInfo("items.txt",itemInfo,itemVersion)
saveInfo("champs.txt",champInfo,champVersion)
saveInfo("runes.txt",runeInfo,runeVersion)
saveInfo("champId.txt",champDict,champVersion)