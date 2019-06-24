# -*- coding: utf-8 -*-
"""
Created on Sat May 18 16:17:16 2019

@author: Ahir
"""

import requests
import json

api_key = "RGAPI-2513966d-feeb-400f-a112-8e839d224c62"
name_to_summ = {     "Ahir":["CrusherCake","Drunk Skeleton"],
                     "Andy":["Lolicept","Yuaru"],
                     "Austin":["GG EVOS NO RE"],
                     "Ben":["Monsterblah"],
                     "Booker":["Brimst"],
                     "Clayton":["One Epic Potato"],
                     "Dustin":["Poopsers","DustinChang","InMyGunship"],
                     "David":["xRequiem"],
                     "Denis":["Avoxin","4v0x1n"],
                     "Faiz":["Faíz"],
                     "Gavin":["GHamski"],
                     "Hwang":["RaÏlgun"],
                     "Isaac":["Pursin"],
                     "James":["lickitloveit","CeIsius"],
                     "Jonathan":["YellowBumbleBee"],
                     "Khayame":["Is That Hymn"],
                     "Louis":["FobAsian"],
                     "Mason":["mello mental","keep it mello","Melllo"],
                     "Nabil":["Nabuilt"],
                     "Paul":["DDUˉDU DDUˉDU"],
                     "Raymond":["iee jong seok"],
                     "Shubham":["horsecatsmart"],
                     "Spencer":["recneps"],
                     "Tailer":["kraymos"],
                     "Ty":["Elementilist"],
                     "Vincent":["BobChuckyJoe"]
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
        rankInfo = json.loads(requests.get("https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/" + summId + "?api_key=" + api_key).text)
        for queue in rankInfo:
            if(queue["queueType"] == "RANKED_SOLO_5x5"):
                rankInfo = queue
        score = getScore(rankInfo)
        if(score > highScore):
            highAcc = summ
            highRank = rankName(rankInfo)
            highScore = score
    if(len(leaderboard) == 0):
        leaderboard.append([name,highRank,highAcc,highScore])
    else:
        index = 0
        done = False
        for person in leaderboard:
            if(highScore > person[3] and not done):
                leaderboard.insert(index,[name,highRank,highAcc,highScore])
                done = True
            index += 1
        if(not done):
            leaderboard.append([name,highRank,highAcc,highScore])
    print(name + " " + highRank + " " + highAcc)
    
rank = 1
for person in leaderboard:
    output = ""
    output += (str)(rank) + ")"
    while(len(output)<5):
        output += " "
    output += person[0]
    while(len(output)<14):
        output += " "
    output += "- "
    ladder = person[1].split(" ")
    output += ladder[0] + " "
    if(ladder[0] == "M" or ladder[0] == "C"):
        output += " "
    spaces = 3-len(ladder[1])
    while(spaces>0):
        output += " "
        spaces -= 1
    output += ladder[1]
    output += " LP - "
    spaces = 16-len(person[2])
    output += person[2]
    while(spaces>0):
        output += " "
        spaces -= 1
    output += "- "
    print(output)
    rank += 1
    
