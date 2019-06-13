# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 15:52:02 2018

@author: ahirc
"""
import requests
import json
import os
import time
from datetime import datetime
import calendar

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

api_key = "?api_key=" + "RGAPI-ba489987-6fdd-4439-8a6d-cb212ee56a29"

versionInfo = json.loads(requests.get("https://ddragon.leagueoflegends.com/realms/na.json" + api_key).text)["n"]
champVersion = versionInfo["champion"]
itemVersion = versionInfo["item"]
ssVersion = versionInfo["summoner"]

champInfo = {}
loadedInfo = loadFile("champs.txt")
if(loadedInfo[0] == champVersion):
    champInfo = loadedInfo[1]
    print("champs.txt version up to date")
else:
    champInfo = json.loads(requests.get("http://ddragon.leagueoflegends.com/cdn/" + champVersion + "/data/en_US/champion.json" + api_key).text)
    saveInfo("champs.txt",champInfo,champVersion)
    print("champs.txt updated")
    
itemInfo = {}
loadedInfo = loadFile("items.txt")
if(loadedInfo[0] == itemVersion):
    itemInfo = loadedInfo[1]
    print("items.txt version up to date")
else:
    itemInfo = json.loads(requests.get("http://ddragon.leagueoflegends.com/cdn/" + itemVersion + "/data/en_US/item.json" + api_key).text)
    print("items.txt updated")
    
ssInfo = {}
loadedInfo = loadFile("summonerSpells.txt")
if(loadedInfo[0] == itemVersion):
    ssInfo = loadedInfo[1]
    print("summonerSpells.txt version up to date")
else:
    ssInfo = json.loads(requests.get("http://ddragon.leagueoflegends.com/cdn/" + itemVersion + "/data/en_US/summoner.json" + api_key).text)
    saveInfo("summonerSpells.txt",ssInfo,ssVersion) 
    print("summonerSpells.txt updated")
    
loadedInfo = loadFile("ssId.txt")
ssDict = {}
if(loadedInfo[0] == champVersion):
    ssDict = loadedInfo[1]
    print("champId.txt version up to date")
else:
    for ss in ssInfo["data"]:
        ssDict[ssInfo["data"][ss]["key"]] = ssInfo["data"][ss]["name"]
    saveInfo("ssId.txt",ssDict,ssVersion)
    print("ssId.txt updated")
    champDict = loadFile("ssId.txt")[1]
    
loadedInfo = loadFile("champId.txt")
champDict = {}
if(loadedInfo[0] == champVersion):
    champDict = loadedInfo[1]
    print("champId.txt version up to date")
else:
    for champ in champInfo["data"]:
        champDict[champInfo["data"][champ]["key"]] = champInfo["data"][champ]["name"]
    saveInfo("champId.txt",champDict,champVersion)
    print("champId.txt updated")
    champDict = loadFile("champId.txt")[1]

loadedInfo = loadFile("SRitems.txt")
itemDict = {}
if(loadedInfo[0] == itemVersion):
    itemDict = loadedInfo[1]
    print("SRitems.txt version up to date")
else:
    for itemNum in itemInfo["data"]:
        item = itemInfo["data"][itemNum]
        if(item["maps"]["11"] == True and item["gold"]["purchasable"]):
            itemDict[item["name"]] = itemNum
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
    tempDict = {}
    for key in itemDict:
        tempDict[itemDict[key]] = key
    itemDict = tempDict
    saveInfo("SRitems.txt",itemDict,itemVersion)
    print("SRitems.txt updated")
    itemDict = loadFile("SRitems.txt")[1]

summonerName = input("Enter summoner name: ")#"raïlgun"## 
accountInfo = json.loads(requests.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summonerName + api_key).text)
accountID = (str)(accountInfo["accountId"])
summonerID = (str)(accountInfo["id"])

def printTeams(matchRequest):
    blue = []
    red = []
    for player in matchRequest["participants"]:
        if player["teamId"] == 100:
            blue.append((champDict[(str)(player["championId"])],player["participantId"]))
        else:
            red.append((champDict[(str)(player["championId"])],player["participantId"]))
    print(blue)
    print(red)
    
def printTimeline(matchRequest, matchTimeline):
    pId = ""
    identities = {}
    for p in matchRequest["participants"]:
        identities[p["participantId"]] = champDict[(str)(p["championId"])]
    for p in matchRequest["participantIdentities"]:
        participantId = p["participantId"]
        if(p["player"]["summonerId"] == summonerID):
            pId = participantId
    for frame in matchTimeline["frames"]:
        for event in frame["events"]:
            printEvent(event, pId, identities)
        #printPFrame(frame["participantFrames"][pId])

def printEvent(event, pId, identities):
    eType = event["type"]
#    if(eType == "ITEM_PURCHASED"):
#        if(event["participantId"] == pId):
#            print("Purchased " + itemDict[(str)(event["itemId"])] + " at " + calcGameTime(event["timestamp"]))
    if(eType == "CHAMPION_KILL"):
        if(event["killerId"] == pId):
            print("Killed " + identities[event["victimId"]] + assistString(event["assistingParticipantIds"],identities) + " at " 
                  + calcGameTime(event["timestamp"]))
        if pId in event["assistingParticipantIds"]:
            assisters = [event["killerId"]]
            for assister in event["assistingParticipantIds"]:
                if(assister != pId):
                    assisters.append(assister)
            print("Assisted killing " + identities[event["victimId"]] + assistString(assisters,identities) + " at " + calcGameTime(event["timestamp"]))
        if event["victimId"] == pId:
            print("Died to " + identities[event["killerId"]] + assistString(event["assistingParticipantIds"],identities) + " at " 
                  + calcGameTime(event["timestamp"]))

def printPFrame(frame):
    print(frame)
    
def calcGameTime(time):
    mins = (str)(round(time/60000))
    secs = (str)(round((time%60000)/1000))
    if(len(secs) == 1):
        secs = "0" + secs
    return (str)((mins + ":" + secs))

def assistString(assistList, identities):
    if(len(assistList) == 0):
        return " solo"
    elif(len(assistList) == 1):
        return " with " + (identities[assistList[0]])
    elif(len(assistList) == 2):
        return " with " + (identities[assistList[0]]) + " and " + (identities[assistList[1]])
    else:
        returnStr = " with " + (identities[assistList[0]])
        for num in range(1,len(assistList)):
            if(num == len(assistList)-1):
                returnStr = returnStr + ", and " + identities[assistList[num]]
            else:
                returnStr = returnStr + ", " + identities[assistList[num]]
        return returnStr
    
def downloadGames():
    limit = 1000000#(int)(input("Enter max number of games to load: "))
    accounts = [summonerName]
    accInput = input("Any other summoners to download? ")
    while(not accInput.upper() == "N"):
        accounts.append((str)(accInput))
        accInput = input("Any other summoner to download? ")
    season = (int)(input("Enter season to track: " )) + 4
    lastTime = time.time()
    for summName in accounts:
        accountId = json.loads(requests.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summName + api_key).text)["accountId"]
        loadedInfo = loadFile(summName + "S" + (str)(season-3) + "games.txt")
        lastGameId = 0
        matchesList = []
        #print(loadedInfo[0], season)
        if((str)(loadedInfo[0]) != (str)(season)):
            print("Games for " + summName + " not previously downloaded for season " + (str)(season-4) + ".")
        else:
            matchesList = loadedInfo[1]
            lastGameId = matchesList[0]["gameId"]
        count = 1
        gamesList = []
        constant = 1
        rateLimit = 120
        shortInterval = 5
        queries = "&queue=420"
        matches = json.loads(requests.get("https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/" + accountId + api_key + queries).text) 
        #print(matches)
        totalGames = matches["totalGames"]
        while(count <= limit and count <= totalGames):
            index = count-constant
            matchID = ""
            matchesList = matches["matches"]
            if(index >= len(matchesList) or count+1 == totalGames):
                if(count+1 == totalGames and not (index >= len(matchesList))):
                    matchID = (str)(matchesList[index]["gameId"])
                constant += len(matchesList)
                index = count-constant
                queries = "&queue=420&beginIndex=" + (str)(count)
                matches = json.loads(requests.get("https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/" + accountId + api_key + queries).text)
                if(matches["totalGames"] > totalGames):
                    totalGames = matches["totalGames"]
            matchID = (str)(matchesList[index]["gameId"])
            if(matchID == (str)(lastGameId)):
                print(matchID)
                break
            matchRequest = json.loads(requests.get("https://na1.api.riotgames.com/lol/match/v4/matches/" + matchID + api_key).text)
            if("status" in matchRequest):
                if(matchRequest["status"]["status_code"] == 404):
                    break
                print("Waiting for API rate limit.")
                time.sleep(rateLimit)
                matchRequest = json.loads(requests.get("https://na1.api.riotgames.com/lol/match/v4/matches/" + matchID + api_key).text)
            while("status" in matchRequest):
                time.sleep(shortInterval)
            if(matchRequest["seasonId"] != season):
                #print(matchRequest)
                break
            #matchTimeline = json.loads(requests.get("https://na1.api.riotgames.com/lol/match/v4/timelines/by-match/" + matchID + api_key).text)
            gamesList.append(matchRequest)
            print(count, end=",")
            count += 1
            
        if(count <= limit):
            print((str)(count) + " games loaded.")
            
        if(not loadedInfo[1] == -1):
            for game in loadedInfo[1]:
                gamesList.append(game)
            
        saveInfo(summName + "S" + (str)(season-3) +"games.txt", gamesList, season)
    return gamesList
    
def findFingerprint(summonerID):
    #loads summoner name games that were already downloaded
    season = 10
    lane = ""#input("Enter lane to check: ").upper()
    smurf = input("Enter smurf to check: ")
    saccountInfo = json.loads(requests.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + smurf + api_key).text)
    ssummonerId = (str)(saccountInfo["id"])
    loadedInfo = loadFile(summonerName + "S" + (str)(season) + "games.txt")
    if(loadedInfo[0] != season+3):
        print("Games for " + summonerName + " not previously downloaded for season " + (str)(season) + ".")
        return
    matchesList = loadedInfo[1]
    loadedInfo = loadFile(smurf + "S" + (str)(season) + "games.txt")
    if(loadedInfo[0] != season+3):
        print("Games for " + smurf + " not previously downloaded for season " + (str)(season) + ".")
        return
    
    uniqueItems = {}
    itemSlots = [[],[],[],[],[],[],[]]
    flashD = 0
    flashF = 0
    matchesChecked = 0
    for match in matchesList:
        matchesChecked += 1
        pID = 0
        #find summoner's participantId in this game
        for p in match["participantIdentities"]:
            if p["player"]["summonerId"] == ssummonerId:
                print("0% chance accounts are related, played in the same game.")
                return
            if p["player"]["summonerId"] == summonerID:
                pID = p["participantId"]
                
        #count flash's on whatever key
        if(match["participants"][pID-1]["spell1Id"] == 4):
            flashD += 1
        elif(match["participants"][pID-1]["spell2Id"] == 4):
            flashF += 1
            
        #gather item data for all the items in the inventory
        for p in match["participants"]:
            if(p["participantId"] == pID):
                for num in range(0,7):
                    itemName = p["stats"]["item"+(str)(num)]
                    uniqueItems[itemName] = 1
                    itemSlots[num].append(itemName)
                    
    #repeat above process for suspected smurf account
    matchesList = loadedInfo[1]
    summonerID = ssummonerId
    suniqueItems = {}
    sitemSlots = [[],[],[],[],[],[],[]]
    sflashD = 0
    sflashF = 0
    smatchesChecked = 0
    
    for match in matchesList:
        smatchesChecked += 1
        pID = 0
        for p in match["participantIdentities"]:
            if p["player"]["summonerId"] == summonerID:
                pID = p["participantId"]
        if(match["participants"][pID-1]["spell1Id"] == 4):
            sflashD += 1
        elif(match["participants"][pID-1]["spell2Id"] == 4):
            sflashF += 1
        for p in match["participants"]:
            if(p["participantId"] == pID):
                for num in range(0,7):
                    suniqueItems[p["stats"]["item"+(str)(num)]] = 1
                    sitemSlots[num].append(p["stats"]["item"+(str)(num)])
                    
    print(flashD,flashF,sflashD,sflashF)
    
    #check flashes
    flashSame = True
    if(not ((flashD > flashF and sflashD > sflashF) or (flashD < flashF and sflashD < sflashF))):
        flashSame = False
        print("Flash different.")
        
    itemsMatrix = {}
    sitemsMatrix = {}
    
    for item in uniqueItems:
        if((str)(item) in itemInfo["data"]):
            #check only active items for keybinding
            if("Active" in itemInfo["data"][(str)(item)]["tags"]):
                #track how often the item goes into a certain inventory slot
                itemName = itemInfo["data"][(str)(item)]["name"]
                itemsMatrix[itemName] = [0,0,0,0,0,0,0,0]
                for num in range(0,7):
                    for oItem in itemSlots[num]:
                        #if we found the item in a slot, increase that slot and the total by one
                        if(item == oItem):
                            itemsMatrix[itemName][num] += 1
                            itemsMatrix[itemName][7] += 1
                for num in range(0,7):
                    #divide by total times item is bought to create percentages
                    itemsMatrix[itemName][num] = itemsMatrix[itemName][num]/itemsMatrix[itemName][7]
                    
    #repeat above process for smurf account
    for item in suniqueItems:
        if((str)(item) in itemInfo["data"]):
            if("Active" in itemInfo["data"][(str)(item)]["tags"]):
                itemName = itemInfo["data"][(str)(item)]["name"]
                sitemsMatrix[itemName] = [0,0,0,0,0,0,0,0]
                for num in range(0,7):
                    for oItem in sitemSlots[num]:
                        if(item == oItem):
                            sitemsMatrix[itemName][num] += 1
                            sitemsMatrix[itemName][7] += 1
                for num in range(0,7):
                    sitemsMatrix[itemName][num] = sitemsMatrix[itemName][num]/sitemsMatrix[itemName][7]
                    
    #check trinkets
    trinkets = ["Oracle Lens","Warding Totem (Trinket)","Farsight Alteration"]
    trinketRanks = {}
    strinketRanks = {}
    for trinket in trinkets:
        trinketRanks[itemsMatrix[trinket][7]] = trinket
        strinketRanks[sitemsMatrix[trinket][7]] = trinket
    trinketsSame = True
    if(not (trinketRanks[max(trinketRanks)] == strinketRanks[max(strinketRanks)] and trinketRanks[min(trinketRanks)] == strinketRanks[min(strinketRanks)])):
        trinketsSame = False
        print("Trinkets are different.")
        
    #variables that need to be tuned
    sampleSizeLimit = 11
    highLimit = .68
    lowLimit = .12
    #variables that need to be tuned
    
    itemsDifferent = []
    itemsBadlyDifferent = []
    matchingItems = []
    itemsToRemove = []
    for item in itemsMatrix:
        if item not in trinkets:
            hasHL = False
            if item in sitemsMatrix:
                if itemsMatrix[item][7] >= sampleSizeLimit and sitemsMatrix[item][7] >= sampleSizeLimit:
                    for num in range(0,7):
                        if((itemsMatrix[item][num] >= highLimit or sitemsMatrix[item][num] >= highLimit) and not hasHL):
                            if(not (sitemsMatrix[item][num] >= highLimit and itemsMatrix[item][num] >= highLimit)):
                                #print(item)
                                #itemsDifferent.append(item)
                                itemsBadlyDifferent.append(item)
                                hasHL = True
                            else:
                                hasHL = True
                                matchingItems.append(item)
                    if(not hasHL):
                        for num in range(0,7):
                            i = itemsMatrix[item][num]
                            si = sitemsMatrix[item][num]
                            if((i < highLimit and i >= lowLimit) or (si < highLimit and si >= lowLimit)):
                                if(not((i < highLimit and i >= lowLimit) and (si < highLimit and si >= lowLimit))):
                                    if(not item in itemsDifferent):
                                        itemsDifferent.append(item)
                                        if(item in matchingItems):
                                            matchingItems.remove(item)
                                elif(not item in matchingItems and (not item in itemsDifferent)):
                                    matchingItems.append(item)
                else:
                    itemsToRemove.append(item)
    for item in itemsToRemove:
        itemsMatrix.pop(item)
        sitemsMatrix.pop(item)
    itemsToRemove = []
    iterateList = []
    diffItemsMatrix = {}
    for item in itemsDifferent:
        iterateList.append(item)
    for item in itemsBadlyDifferent:
        iterateList.append(item)
    print(itemsDifferent, itemsBadlyDifferent)
    for item in iterateList:
        ranks = []
        sranks = []
        for num in range(0,7):
            lowLimit = 0
            maxVal = lowLimit
            maxPos = -1
            smaxVal = lowLimit
            smaxPos = -1
            for num in range(0,7):
                if(maxVal < itemsMatrix[item][num] and not num in ranks):
                    maxVal = itemsMatrix[item][num]
                    maxPos = num
                if(smaxVal < sitemsMatrix[item][num] and not num in sranks):
                    smaxVal = sitemsMatrix[item][num]
                    smaxPos = num
            ranks.append(maxPos)
            sranks.append(smaxPos)
        different = False
        print(item, ranks, sranks)
        for num in range(0,7):
            if(ranks[num] != sranks[num]):
                different = True
        if(not different):
            itemsToRemove.append(item)
        else:
            diffItemsMatrix[item] = [ranks,sranks]
    for item in itemsToRemove:
        if(item in itemsDifferent):
            itemsDifferent.remove(item)
        else:
            itemsBadlyDifferent.remove(item)
    print(itemsDifferent)
    print(itemsBadlyDifferent)
    itemsChecked = min(len(itemsMatrix),len(sitemsMatrix))-3
    print(itemsChecked)
    #print(matchingItems)
    #print(highLimitItems)
    #print(lowLimitItems)
                #if(p["timeline"]["lane"] == lane):
                    #totalGames += 1 
#    print(totalGames)
#    printDict = {}
#    for item in uniqueItems:
#        if((str)(item) in itemInfo["data"]):
#            if("Active" in itemInfo["data"][(str)(item)]["tags"]):
#                print(itemInfo["data"][(str)(item)]["name"] + ": ",end="")
#                totalCount = 0
#                counts = []
#                for num in range(0,7):
#                    count = 0
#                    for oItem in itemSlots[num]:
#                        if(item == oItem):
#                            count += 1
#                    counts.append(count)
#                    totalCount += count
#                    if num == 0:
#                        printDict[itemInfo["data"][(str)(item)]["name"]] = []
#                    printDict[itemInfo["data"][(str)(item)]["name"]].append(count)
#                    print((str)(count) + " ",end="")
#                #for count in counts:
#                #    print((str)(round((count/totalCount)*100,1)) + " ",end="")
#                print()
#    for key in printDict:
#        print(key)
#    for num in range(0,7):
#        print()
#        for key in printDict:
#            print(printDict[key][num])
                
    #print(uniqueItems)
    #print(flashD, flashF)    
    matchNumber = 100
    itemNumber = 6
    relatedChance = 1
    if itemsChecked == 0:
        itemsChecked = 1
    itemRatio = 1/itemsChecked
    if(not flashSame):
        relatedChance = 0.0
    if(len(itemsBadlyDifferent) > 0):
        relatedChance = 0.0
    if(relatedChance > 0):
        if(not trinketsSame):
            relatedChance -= .2
            for item in itemsDifferent:
                relatedChance -= itemRatio*1.5
#            for item in itemsBadlyDifferent:
#                relatedChance -= itemRatio*4
        else:
            for item in itemsDifferent:
                relatedChance -= itemRatio
#            for item in itemsBadlyDifferent:
#                relatedChance -= itemRatio*3.5
    if(relatedChance < 0):
        relatedChance = 0.0
    if(matchesChecked < matchNumber):
        relatedChance /= 2
        print("WARNING: low sample size of matches on " + summonerName + ".")
    if(smatchesChecked < matchNumber):
        relatedChance /= 2
        print("WARNING: low sample size of matches on " + smurf + ".")
    if(not itemsChecked > itemNumber):
        relatedChance /= 2
        print("WARNING: low sample size of items in common.")
    print((str)(round(relatedChance*100,1)) + "% chance that " + summonerName + " and " + smurf + " are the same.")
    return [itemsMatrix, sitemsMatrix]
    
    
def analyzeDownloadedGames():
    d = datetime.utcnow()
    unixtime = calendar.timegm(d.utctimetuple())
    daysConstant = 1000*(60)*(60)*(24) #seconds to minutes, minutes to hours, hours to days
    season = (int)(input("Enter season to track: " ))
    trackChamp = ""#input("Enter champ name: ")
    numDays = (int)(input("Enter number of days to check: "))
    startPatch = 10000#input("Enter startPatch: ")
    endPatch = -1#input("Enter endPatch to track: ")
    lane = input("Enter lane to check: ").upper()
    loadedInfo = loadFile(summonerName + "S" + (str)(season) + "games.txt")    
    if(loadedInfo[0] != season+3):
        print("Games for " + summonerName + " not previously downloaded for season " + (str)(season) + ".")
        return
    matchesList = loadedInfo[1]
    champFreq = {}
    champRoles = {}
    for key in champDict:
        champFreq[champDict[key]] = 0
    count = 0
    for match in matchesList:
        count += 1
        curVersion = (int)(match["gameVersion"].split('.')[1])
        #print((((unixtime*1000)-(int)(match["gameCreation"]))/daysConstant))
        if((((unixtime*1000)-(int)(match["gameCreation"]))/daysConstant) > numDays):
            print((str)(count) + " total games in the past " + (str)(numDays) + " days.")
            break
        if(not(curVersion > (int)(startPatch))):
            if(not(curVersion >= (int)(endPatch))):
                #print(match["gameVersion"].split('.'))
                #print(patch)
                break
            pId = 0
            for p in match["participantIdentities"]:
                if(p["player"]["summonerId"] == summonerID):
                    pId = p["participantId"]
            for p in match["participants"]:
                if(p["participantId"] == pId and champDict[(str)(p["championId"])] == trackChamp):
                    if(p["timeline"]["lane"] not in champRoles):
                        champRoles[p["timeline"]["lane"]] = {p["timeline"]["role"]:1}
                    elif(p["timeline"]["role"] in champRoles[p["timeline"]["lane"]]):
                        champRoles[p["timeline"]["lane"]][p["timeline"]["role"]] += 1
                    else:
                        champRoles[p["timeline"]["lane"]][p["timeline"]["role"]] = 1
                if(p["participantId"] == pId and p["timeline"]["lane"] == lane):
                    champ = champDict[(str)(p["championId"])]
                    champFreq[champ] += 1          
    for champ in sorted(champFreq, key=champFreq.get, reverse=True):
        if(champFreq[champ] > 0):
            print(champ)
    for champ in sorted(champFreq, key=champFreq.get, reverse=True):
        if(champFreq[champ] > 0):
            print(champFreq[champ])
    #print(champRoles)
    return matchesList
        
#gamesList = downloadGames()       
#matchesList = analyzeDownloadedGames()
itemsMatrix = findFingerprint(summonerID)
    
#for match in matches["matches"]:
#    if(count > limit):
#        break
#    matchID = (str)(match["gameId"])
#    matchRequest = json.loads(requests.get("https://na1.api.riotgames.com/lol/match/v4/matches/" + matchID + api_key).text)
#    #matchTimeline = json.loads(requests.get("https://na1.api.riotgames.com/lol/match/v4/timelines/by-match/" + matchID + api_key).text)
#    #printTeams(matchRequest)
#    #printTimeline(matchRequest, matchTimeline)
#    print(count)
#    count += 1

