#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 08:40:09 2019

@author: ahir.chatterjee
"""

from bs4 import BeautifulSoup
import requests
import json
import os
import xlwt
from selenium import webdriver
import time

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

def saveInfo(fileName, data):
    wrapperList = []
    with open(fileName,'w') as outfile:
        #for obj in data:
        wrapperList.append(data)
        json.dump(wrapperList,outfile)
        print(fileName + " saved successfully.")

def createChampDict():    
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
    
    champDict = {}
    for champ in champInfo["data"]:
        champDict[(champInfo["data"][champ]["name"])] = {"picks":0,"bans":0}
        
    return champDict

def scrapePBData():
    region = input("Enter region to scrape (i.e. LCS, LEC, LCK, LPL): ")
    validWeeks = input("Enter valid weeks (i.e 1, 2, 3): ").split(", ")
    url = 'https://lol.gamepedia.com/Special:RunQuery/PickBanHistory?PBH%5Bpage%5D=' + region + '%202019%20Summer&PBH%5Btextonly%5D=Yes&pfRunQueryFormName=PickBanHistory'
    response = requests.get(url)
    content = BeautifulSoup(response.content,"html.parser")
    
    table = content.find('table', attrs={"class": "wikitable"})
    rows = table.findAll('tr')
    validRows = []
    for row in rows:
        data = row.findAll('td')
        if(len(data) > 0):
            for week in validWeeks:
                if(data[0].text == "Week " + (str)(week)):
                    validRows.append(row)
            
    champDict = createChampDict()
    count = 0
    for row in validRows:
        for data in row.findAll('td', attrs={"class": "pbh-cell"}):
            ban = False
            place = count%17
            if(place == 0):
                print()
            if(place < 6 or (place > 9 and place < 14)):
                ban = True
                print("Banned", end=" ")
            else:
                print("Picked", end=" ")
            champs = data.text.split(", ")
            for champ in champs:
                if(not champ == "None"):
                    if(champ == "sejunai"):
                        champ = "Sejuani"
                    print(champ, end=" ")
                    if(ban):
                        champDict[champ]["bans"] += 1
                    else:
                        champDict[champ]["picks"] += 1
            print()
            count += 1
    print((str)(len(validRows)) + " games")
    return champDict

def createCStats(players):
    cStats = []
    for player in players:
        name = player.find('div',attrs={"class" : "champion-nameplate-name"}).text
        name = name[1:len(name)-1]
        cStats.append({"champion":name})
    return cStats

def scrapeChampData():
    region = input("Enter region to scrape (i.e. LCS, LEC, LCK, LPL): ")
    validWeeks = input("Enter valid weeks (i.e 1, 2, 3): ").split(", ")
    url = 'https://lol.gamepedia.com/' + region + '/2019_Season/Summer_Season/Champion_Statistics'
    response = requests.get(url)
    content = BeautifulSoup(response.content,"html.parser")
    
    table = content.find('table', attrs={"class": "wikitable"})
    print(table)
    
def scrapeMHData(MHurl):
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")
    url = MHurl
    driver = webdriver.Chrome(executable_path = DRIVER_BIN)
    driver.get(url)
    time.sleep(3)
    
    content = BeautifulSoup(driver.page_source,"html.parser")
    general = {}
    count = 0
    divs = content.find('div',attrs={"class" : "default-2-3"}).findAll('div')
    for div in divs:
        if(count == len(divs)-2):
            general["time"] = div.text
        elif(count == len(divs)-1):
            general["date"] = div.text
        count += 1
    scoreboard = content.find('div',attrs={"class" : "gs-container gs-no-gutter"})
    general["result"] = scoreboard.find('div',attrs={"class" : "game-conclusion"}).text.strip()
    stats = content.find('table',attrs={"class" : "table table-bordered"})
    players = scoreboard.findAll('li')
    
    cStats = createCStats(players)
    
#    headerRow = stats.find('tr',attrs={"class" : "grid-header-row"})
#    data = headerRow.findAll('td')
#    for d in data:
#        #print(d)
#        div = d.find('div')
#        div = div.find('div')
#        if(div is not None):
#            div = div.find('div')
#            print(div["data-rg-id"])
    
    rows = stats.findAll('tr')
    for row in rows:
        if(row.has_attr("class") and not row["class"][0] == "view" and not row["class"][0] == "grid-header-row"):
            data = row.findAll('td')
            i = 0
            statName = ""
            for d in data:
                #if(d.has_attr("class") and d["class"][0] == "grid-label"):
                    #print()
                #print(d.text)
                if(statName == ""):
                    statName = d.text
                else:
                    cStats[i][statName] = d.text
                    i += 1
    
    driver.close()
    return {"cStats":cStats, "general":general}

def writeSheet(champDict):
    wb = xlwt.Workbook()
    ws = wb.add_sheet("t")
    row = 0
    for champ in champDict:
        ws.write(row,0,champ)
        ws.write(row,1,champDict[champ]["bans"])
        ws.write(row,2,champDict[champ]["picks"])
        row += 1
    wb.save("Stats.xls")
    

def writeInhouseSheet(url,num):
    MHData = scrapeMHData(url)
    general = MHData["general"]
    cStats = MHData["cStats"]
    for champ in cStats:
        champ["player"] = input("Who played " + champ["champion"] + "? ")
    
    print()
    general["kills1"] = 0
    general["kills2"] = 0
    general["gold1"] = 0
    general["gold2"] = 0
    general["dmg1"] = 0
    general["dmg2"] = 0
    count = 0
    for champ in cStats:
        kda = champ["KDA"].split("/")
        champ["CS"] = (float)(champ["Minions Killed"])
        if(not champ["Neutral Minions Killed"] == "-"):
            champ["CS"] += (float)(champ["Neutral Minions Killed"])
        champ["kills"] = (float)(kda[0])
        champ["deaths"] = (float)(kda[1])
        champ["assists"] = (float)(kda[2])
        champ["Gold Earned"] = (float)(champ["Gold Earned"].split("k")[0])*1000
        champ["Total Damage to Champions"] = (float)(champ["Total Damage to Champions"].split("k")[0])*1000
        champ["Wards Placed"] = (float)(champ["Wards Placed"])
        if(champ["Control Wards Purchased"] == '-'):
            champ["Control Wards Purchased"] = 0
        else:
            champ["Control Wards Purchased"] = (float)(champ["Control Wards Purchased"])
        if(champ["Wards Destroyed"] == '-'):
            champ["Wards Destroyed"] = 0
        else:
            champ["Wards Destroyed"] = (float)(champ["Wards Destroyed"])
        champ["Wards Destroyed"] = float(champ["Wards Destroyed"])
        if(champ["deaths"] == 0):
            champ["KDA"] = champ["kills"] + champ["assists"]
        else:
            champ["KDA"] = ((champ["kills"] + champ["assists"])/champ["deaths"])
        if(count < 5):
            general["kills1"] += champ["kills"]
            general["gold1"] += champ["Gold Earned"]
            general["dmg1"] += champ["Total Damage to Champions"]
        else:
            general["kills2"] += champ["kills"]
            general["gold2"] += champ["Gold Earned"]
            general["dmg2"] += champ["Total Damage to Champions"]
        count += 1
        
        
    roles = ["Top","Jungle","Mid","Bot","Support"]
    wb = xlwt.Workbook()
    count = 0
    for champ in cStats:
        ws = wb.add_sheet(champ["player"])
        ws.write(0,0,general["date"])
        gameTime = (float)(general["time"].split(":")[0])+ ((float)(general["time"].split(":")[1]))/60
        ws.write(0,2,gameTime)
        ws.write(0,5,champ["champion"])
        ws.write(0,7,champ["kills"])
        ws.write(0,8,champ["deaths"])
        ws.write(0,9,champ["assists"])
        ws.write(0,13,champ["KDA"])
        ws.write(0,19,champ["CS"])
        ws.write(0,21,champ["CS"]/gameTime)
        ws.write(0,23,champ["Gold Earned"])
        ws.write(0,27,champ["Gold Earned"]/gameTime)
        ws.write(0,29,champ["Total Damage to Champions"])
        ws.write(0,33,champ["Total Damage to Champions"]/gameTime)
        ws.write(0,35,champ["Wards Placed"])
        ws.write(0,37,champ["Control Wards Purchased"])
        ws.write(0,39,champ["Wards Destroyed"])
        ws.write(0,41,(float)(champ["Wards Placed"])/gameTime)
        ws.write(0,43,(champ["Total Damage to Champions"]/champ["Gold Earned"]))
        if(count < 5):
            oppChamp = cStats[count+5]
            if(general["result"] == "VICTORY"):
                ws.write(0,1,"W")
            else:
                ws.write(0,1,"L")
            ws.write(0,3,general["kills1"])
            ws.write(0,4,general["kills2"])
            ws.write(0,6,oppChamp["champion"])
            ws.write(0,10,champ["kills"]-oppChamp["kills"])
            ws.write(0,11,champ["deaths"]-oppChamp["deaths"])
            ws.write(0,12,champ["assists"]-oppChamp["assists"])
            ws.write(0,14,champ["KDA"]-oppChamp["KDA"])
            ws.write(0,15,(champ["kills"]+champ["assists"])/general["kills1"])
            ws.write(0,16,((champ["kills"]+champ["assists"])/general["kills1"])-((oppChamp["kills"]+oppChamp["assists"])/general["kills2"]))
            ws.write(0,17,(champ["deaths"]/general["kills2"]))
            ws.write(0,18,(champ["deaths"]/general["kills2"])-(champ["deaths"]/general["kills1"]))
            ws.write(0,20,champ["CS"]-oppChamp["CS"])
            ws.write(0,22,(champ["CS"]/gameTime)-(oppChamp["CS"]/gameTime))
            ws.write(0,24,champ["Gold Earned"]-oppChamp["Gold Earned"])
            ws.write(0,25,champ["Gold Earned"]/general["gold1"])
            ws.write(0,26,(champ["Gold Earned"]/general["gold1"])-(oppChamp["Gold Earned"]/general["gold2"]))
            ws.write(0,28,(champ["Gold Earned"]/gameTime)-(oppChamp["Gold Earned"]/gameTime))
            ws.write(0,30,champ["Total Damage to Champions"]-oppChamp["Total Damage to Champions"])
            ws.write(0,31,(champ["Total Damage to Champions"]/general["dmg1"]))
            ws.write(0,32,(champ["Total Damage to Champions"]/general["dmg1"])-(oppChamp["Total Damage to Champions"]/general["dmg2"]))
            ws.write(0,34,(champ["Total Damage to Champions"]/gameTime)-(oppChamp["Total Damage to Champions"]/gameTime))
            ws.write(0,36,champ["Wards Placed"]-oppChamp["Wards Placed"])
            ws.write(0,38,champ["Control Wards Purchased"]-oppChamp["Control Wards Purchased"])
            ws.write(0,40,champ["Wards Destroyed"]-oppChamp["Wards Destroyed"])
            ws.write(0,42,((float)(champ["Wards Placed"])/gameTime)-((float)(oppChamp["Wards Placed"])/gameTime))
            ws.write(0,44,(champ["Total Damage to Champions"]/champ["Gold Earned"])-(oppChamp["Total Damage to Champions"]/oppChamp["Gold Earned"]))
            ws.write(0,45,(champ["Total Damage to Champions"]/(champ["Gold Earned"]/general["gold1"])))
            ws.write(0,46,(champ["Total Damage to Champions"]/(champ["Gold Earned"]/general["gold1"]))-(oppChamp["Total Damage to Champions"]/(oppChamp["Gold Earned"]/general["gold2"])))
            ws.write(0,47,((champ["Total Damage to Champions"]/general["dmg1"])/(champ["Gold Earned"]/general["gold1"])))  
            ws.write(0,48,((champ["Total Damage to Champions"]/general["dmg1"])/(champ["Gold Earned"]/general["gold1"]))-((oppChamp["Total Damage to Champions"]/general["dmg2"])/(oppChamp["Gold Earned"]/general["gold2"])))
        else:
            oppChamp = cStats[count-5]
            if(general["result"] == "DEFEAT"):
                ws.write(0,1,"W")
            else:
                ws.write(0,1,"L")
            ws.write(0,3,general["kills2"])
            ws.write(0,4,general["kills1"])
            ws.write(0,6,oppChamp["champion"])
            ws.write(0,10,champ["kills"]-oppChamp["kills"])
            ws.write(0,11,champ["deaths"]-oppChamp["deaths"])
            ws.write(0,12,champ["assists"]-oppChamp["assists"])
            ws.write(0,14,champ["KDA"]-oppChamp["KDA"])
            ws.write(0,15,(champ["kills"]+champ["assists"])/general["kills2"])
            ws.write(0,16,((champ["kills"]+champ["assists"])/general["kills2"])-((oppChamp["kills"]+oppChamp["assists"])/general["kills1"]))
            ws.write(0,17,(champ["deaths"]/general["kills1"]))
            ws.write(0,18,(champ["deaths"]/general["kills1"])-(champ["deaths"]/general["kills2"]))
            ws.write(0,20,champ["CS"]-oppChamp["CS"])
            ws.write(0,22,(champ["CS"]/gameTime)-(oppChamp["CS"]/gameTime))
            ws.write(0,24,champ["Gold Earned"]-oppChamp["Gold Earned"])
            ws.write(0,25,champ["Gold Earned"]/general["gold2"])
            ws.write(0,26,(champ["Gold Earned"]/general["gold2"])-(oppChamp["Gold Earned"]/general["gold1"]))
            ws.write(0,28,(champ["Gold Earned"]/gameTime)-(oppChamp["Gold Earned"]/gameTime))
            ws.write(0,30,champ["Total Damage to Champions"]-oppChamp["Total Damage to Champions"])
            ws.write(0,31,(champ["Total Damage to Champions"]/general["dmg2"]))
            ws.write(0,32,(champ["Total Damage to Champions"]/general["dmg2"])-(oppChamp["Total Damage to Champions"]/general["dmg1"]))
            ws.write(0,34,(champ["Total Damage to Champions"]/gameTime)-(oppChamp["Total Damage to Champions"]/gameTime))
            ws.write(0,36,champ["Wards Placed"]-oppChamp["Wards Placed"])
            ws.write(0,38,champ["Control Wards Purchased"]-oppChamp["Control Wards Purchased"])
            ws.write(0,40,champ["Wards Destroyed"]-oppChamp["Wards Destroyed"])
            ws.write(0,42,((float)(champ["Wards Placed"])/gameTime)-((float)(oppChamp["Wards Placed"])/gameTime)) 
            ws.write(0,44,(champ["Total Damage to Champions"]/champ["Gold Earned"])-(oppChamp["Total Damage to Champions"]/oppChamp["Gold Earned"]))   
            ws.write(0,45,(champ["Total Damage to Champions"]/(champ["Gold Earned"]/general["gold2"])))
            ws.write(0,46,(champ["Total Damage to Champions"]/(champ["Gold Earned"]/general["gold2"]))-(oppChamp["Total Damage to Champions"]/(oppChamp["Gold Earned"]/general["gold1"])))
            ws.write(0,47,((champ["Total Damage to Champions"]/general["dmg2"])/(champ["Gold Earned"]/general["gold2"])))  
            ws.write(0,48,((champ["Total Damage to Champions"]/general["dmg2"])/(champ["Gold Earned"]/general["gold2"]))-((oppChamp["Total Damage to Champions"]/general["dmg1"])/(oppChamp["Gold Earned"]/general["gold1"])))    
        count += 1
    wb.save("inhouse" + (str)(num) + ".xls")
        
def main():
    urls = ["https://matchhistory.na.leagueoflegends.com/en/#match-details/NA1/3069625106/42251275?tab=overview",
            "https://matchhistory.na.leagueoflegends.com/en/#match-details/NA1/3069714444/217845797?tab=overview",
            "https://matchhistory.na.leagueoflegends.com/en/#match-details/NA1/3069671355/42251275?tab=overview",
            "https://matchhistory.na.leagueoflegends.com/en/#match-details/NA1/3069671091/42251275?tab=overview",
            "https://matchhistory.na.leagueoflegends.com/en/#match-details/NA1/3069670658/42251275?tab=overview",
            "https://matchhistory.na.leagueoflegends.com/en/#match-details/NA1/3068006918/42251275?tab=overview",
            "https://matchhistory.na.leagueoflegends.com/en/#match-details/NA1/3068006634/42251275?tab=overview",
            "https://matchhistory.na.leagueoflegends.com/en/#match-details/NA1/3068006400/42251275?tab=overview",
            "https://matchhistory.na.leagueoflegends.com/en/#match-details/NA1/3066130444/42251275?tab=overview",
            "https://matchhistory.na.leagueoflegends.com/en/#match-details/NA1/3066060160/42251275?tab=overview",
            "https://matchhistory.na.leagueoflegends.com/en/#match-details/NA1/3064875714/42251275?tab=overview",
            "https://matchhistory.na.leagueoflegends.com/en/#match-details/NA1/3064875278/42251275?tab=overview",
            "https://matchhistory.na.leagueoflegends.com/en/#match-details/NA1/3064874630/42251275?tab=overview",
            "https://matchhistory.na.leagueoflegends.com/en/#match-details/NA1/3063640452/42251275?tab=overview",
            "https://matchhistory.na.leagueoflegends.com/en/#match-details/NA1/3063640252/42251275?tab=overview",
            "https://matchhistory.na.leagueoflegends.com/en/#match-details/NA1/3061707387/42251275?tab=overview",
            "https://matchhistory.na.leagueoflegends.com/en/#match-details/NA1/3061707090/42251275?tab=overview"
            ]
    count = 0
    for url in urls:
        writeInhouseSheet(url,count)
        count += 1
#    champDict = scrapePBData()
#    writeSheet(champDict)
    
if __name__ == '__main__':
    main()