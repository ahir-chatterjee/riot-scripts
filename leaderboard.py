# -*- coding: utf-8 -*-
"""
Created on Sat May 18 16:17:16 2019

@author: Ahir
"""

import requests
import json

api_key = "RGAPI-ef329658-83e8-4054-9ee6-f1b5548cda18"
name_to_summ = {     "Ahir":["CrusherCake","Drunk Skeleton"],
                     "Andy":["Lolicept","Yuaru"],
                     #"Austin":["GG EVOS NO RE"],
                     "Ben":["Monsterblah"],
                     "Booker":["Brimst"],
                     "Caleb":["naas"],
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
                     "Raymond":["iee jong seok","mental is strong"],
                     "Shubham":["horsecatsmart","alvayj"],
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
def runLeaderboard():
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
        
    cur = open("currentLeaderboard.txt","w")
    prev = open("prevLeaderboard.txt","r")
    prevDict = {}
    numDict = {"1":"one",
               "2":"two",
               "3":"three",
               "4":"four",
               "5":"five",
               "6":"six",
               "7":"seven",
               "8":"eight",
               "9":"nine",
               "10":"ten",
               "10+":"over ten"
               }
    for line in prev:
        fields = line.split("-")
        iden = fields[0].split(")")
        iden[1] = iden[1].strip()
        prevDict[iden[1]] = (int)(iden[0])
        #print(iden)
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
        change = prevDict[person[0]] - rank
        move = "up"
        if(change < 0):
            move = "down"
            change = change*-1
        if(change > 10):
            output += move + " by " + numDict["10+"]
        if(change > 0):
            output += move + " by " + numDict[(str)(change)]
        print(output)
        cur.write(output + "\n")
        rank += 1
        
    cur.close()
    prev.close()    

def main():
    runLeaderboard()
    
if __name__ == '__main__':
    main()