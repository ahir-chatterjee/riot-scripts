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
    
def scrapeMHData():
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")
    url = input("Enter url: ")
    driver = webdriver.Chrome(executable_path = DRIVER_BIN)
    driver.get(url)
    time.sleep(3)
    
    content = BeautifulSoup(driver.page_source,"html.parser")
    scoreboard = content.find('div',attrs={"class" : "gs-container gs-no-gutter"})
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
    return cStats

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
        
def main():
    cStats = scrapeMHData()
    for champ in cStats:
        champ["player"] = input("Who played " + champ["champion"] + "? ")
    
    print()
    
    for champ in cStats:
        print(champ["champion"] + " played by " + champ["player"])
        
    print()
    saveInfo("output.json",cStats)
    print()
    
    for player in cStats:
        for stat in player:
            print(stat + ": " + player[stat])
        print()
    #writeSheet(champDict)
    
if __name__ == '__main__':
    main()
