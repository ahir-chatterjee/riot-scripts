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

def scrapeChampData():
    region = input("Enter region to scrape (i.e. LCS, LEC, LCK, LPL): ")
    validWeeks = input("Enter valid weeks (i.e 1, 2, 3): ").split(", ")
    url = 'https://lol.gamepedia.com/' + region + '/2019_Season/Summer_Season/Champion_Statistics'
    response = requests.get(url)
    content = BeautifulSoup(response.content,"html.parser")
    
    table = content.find('table', attrs={"class": "wikitable"})
    print(table)

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
    champDict = scrapePBData()
    writeSheet(champDict)
    
if __name__ == '__main__':
    main()
