# -*- coding: utf-8 -*-
"""
Created on Sat May 18 16:17:16 2019

@author: Ahir
"""

import requests
import json

api_key = "RGAPI-a21b92ca-d935-48f6-ad4b-8a3dcc828655"
name_to_summ = {     "Ahir":["CrusherCake","Drunk Skeleton"],
                     "Andy":["Lolicept","Yuaru"],
                     "Austin":["GG EVOS NO RE"],
                     "Clayton":["One Epic Potato"],
                     "Dustin":["Poopsers","DustinChang","InMyGunship"],
                     "David":["xRequiem"],
                     "Denis":["Avoxin","4v0x1n"],
                     "Faiz":["Faíz"],
                     "Hwang":["RaÏlgun"],
                     "Isaac":["Pursin"],
                     "James":["lickitloveit","CeIsius"],
                     "Jonathan":["YellowBumbleBee"],
                     "Mason":["mello mental","keep it mello","Melllo"],
                     "Paul":["DDUˉDU DDUˉDU"],
                     "Raymond":["iee jong seok"],
                     "Shubham":["horsecatsmart"],
                     "Ty":["Elementilist","tarzaned5"]
                }
tiers = ["IRON","BRONZE","SILVER","GOLD","PLATINUM","DIAMOND","MASTER","GRANDMASTER","CHALLENGER"]
ranks = ["IV","III","II","I"]

def getScore(rankInfo):
    score = 0
    score += rankInfo["leaguePoints"] + 1000*(tiers.index(rankInfo["tier"])) + 100*(ranks.index(rankInfo["rank"]))
    return score

def rankName(rankInfo):
    tier = rankInfo["tier"][0]
    rank = (str)(4-(int)(ranks.index(rankInfo["rank"])))
    LP = (str)(rankInfo["leaguePoints"]) + " LP"
    if(rankInfo["tier"] == tiers[6] or rankInfo["tier"] == tiers[8]):
        rank = ""
    elif(rankInfo["tier"] == tiers[7]):
        tier = "GM"
        rank = ""
    return (str)(tier + rank + " " + LP)

class Person:
    
    def __init__(self, name, sNames, placed, pos, hPos):
        self.dict = {}
        self.dict["name"] = name        #real name
        self.dict["sNames"] = sNames    #summoner name(s)
        self.dict["placed"] = placed    #boolean (have they placed before or not)
        self.dict["pos"] = pos          #current leaderboard position
        self.dict["hPos"] = hPos        #highest leaderboard position held
    
            
#https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/CrusherCake?api_key=RGAPI-f5ccdc31-e6fd-4063-b4a8-37a73b33b237
leaderboard = []
for name in name_to_summ:
    highAcc = ""
    highRank = ""
    highScore = -1
    for summ in name_to_summ[name]:
        summId = json.loads(requests.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summ + "?api_key=" + api_key).text)["id"]
        rankInfo = json.loads(requests.get("https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/" + summId + "?api_key=" + api_key).text)[0]
        score = getScore(rankInfo)
        if(score > highScore):
            highAcc = summ
            highRank = rankName(rankInfo)
            highScore = score
    for person in leaderboard:
        if(person)
    print(name + ": " + highAcc + ": " + highRank)