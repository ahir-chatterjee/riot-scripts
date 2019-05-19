import requests
import json
import time

api_key = "?api_key=" + "RGAPI-9a24747a-4d4c-44de-91b7-d3da7b2ec728"

# Make a get request to get the latest position of the international space station from the opennotify api.
summonerName = "Tamjung"
howManyMatches = 25
role = "TOP"
summonerID = (str)(json.loads(requests.get("https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/" + summonerName + api_key).text)["accountId"])
#print(summonerID)
matchList = json.loads(requests.get("https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/" + summonerID + api_key).text)

champDict = {
        "1": "Annie",
        "2": "Olaf",
        "3": "Galio",
        "4": "TwistedFate",
        "5": "XinZhao",
        "6": "Urgot",
        "7": "Leblanc",
        "8": "Vladimir",
        "9": "Fiddlesticks",
        "10": "Kayle",
        "11": "MasterYi",
        "12": "Alistar",
        "13": "Ryze",
        "14": "Sion",
        "15": "Sivir",
        "16": "Soraka",
        "17": "Teemo",
        "18": "Tristana",
        "19": "Warwick",
        "20": "Nunu",
        "21": "MissFortune",
        "22": "Ashe",
        "23": "Tryndamere",
        "24": "Jax",
        "25": "Morgana",
        "26": "Zilean",
        "27": "Singed",
        "28": "Evelynn",
        "29": "Twitch",
        "30": "Karthus",
        "31": "Chogath",
        "32": "Amumu",
        "33": "Rammus",
        "34": "Anivia",
        "35": "Shaco",
        "36": "DrMundo",
        "37": "Sona",
        "38": "Kassadin",
        "39": "Irelia",
        "40": "Janna",
        "41": "Gangplank",
        "42": "Corki",
        "43": "Karma",
        "44": "Taric",
        "45": "Veigar",
        "48": "Trundle",
        "50": "Swain",
        "51": "Caitlyn",
        "53": "Blitzcrank",
        "54": "Malphite",
        "55": "Katarina",
        "56": "Nocturne",
        "57": "Maokai",
        "58": "Renekton",
        "59": "JarvanIV",
        "60": "Elise",
        "61": "Orianna",
        "62": "MonkeyKing",
        "63": "Brand",
        "64": "LeeSin",
        "67": "Vayne",
        "68": "Rumble",
        "69": "Cassiopeia",
        "72": "Skarner",
        "74": "Heimerdinger",
        "75": "Nasus",
        "76": "Nidalee",
        "77": "Udyr",
        "78": "Poppy",
        "79": "Gragas",
        "80": "Pantheon",
        "81": "Ezreal",
        "82": "Mordekaiser",
        "83": "Yorick",
        "84": "Akali",
        "85": "Kennen",
        "86": "Garen",
        "89": "Leona",
        "90": "Malzahar",
        "91": "Talon",
        "92": "Riven",
        "96": "KogMaw",
        "98": "Shen",
        "99": "Lux",
        "101": "Xerath",
        "102": "Shyvana",
        "103": "Ahri",
        "104": "Graves",
        "105": "Fizz",
        "106": "Volibear",
        "107": "Rengar",
        "110": "Varus",
        "111": "Nautilus",
        "112": "Viktor",
        "113": "Sejuani",
        "114": "Fiora",
        "115": "Ziggs",
        "117": "Lulu",
        "119": "Draven",
        "120": "Hecarim",
        "121": "Khazix",
        "122": "Darius",
        "126": "Jayce",
        "127": "Lissandra",
        "131": "Diana",
        "133": "Quinn",
        "134": "Syndra",
        "136": "AurelionSol",
        "141": "Kayn",
        "142": "Zoe",
        "143": "Zyra",
        "145": "Kaisa",
        "150": "Gnar",
        "154": "Zac",
        "157": "Yasuo",
        "161": "Velkoz",
        "163": "Taliyah",
        "164": "Camille",
        "201": "Braum",
        "202": "Jhin",
        "203": "Kindred",
        "222": "Jinx",
        "223": "TahmKench",
        "236": "Lucian",
        "238": "Zed",
        "240": "Kled",
        "245": "Ekko",
        "254": "Vi",
        "266": "Aatrox",
        "267": "Nami",
        "268": "Azir",
        "412": "Thresh",
        "420": "Illaoi",
        "421": "RekSai",
        "427": "Ivern",
        "429": "Kalista",
        "432": "Bard",
        "497": "Rakan",
        "498": "Xayah",
        "516": "Ornn"}

averageWPM = 0
averageCSPM = 0
averageDamagePerGold = 0
num = 0
matchesToCheck = howManyMatches
t = time
champsPlayed = []
while(num < matchesToCheck):
    match = matchList["matches"][num]
    #print(match)
    if(match["queue"] <= 450):
        if(match["lane"] == role):
            num = num+1
            matchID = (str)(match["gameId"])
            #print(matchID)
            matchRequest = json.loads(requests.get("https://na1.api.riotgames.com/lol/match/v3/matches/" + matchID + api_key).text)
            #t.sleep(.5)
            if(matchRequest["mapId"] == 11):
                tempChamp = (str)(match["champion"])
                for key in champDict:
                    if(tempChamp == key):
                        alreadyPlayed = False
                        for champ in champsPlayed:
                            if(champ == champDict[key]):
                                alreadyPlayed = True
                        if(not alreadyPlayed):
                            champsPlayed.append(champDict[key])
                        #print(champDict[key])
                        #print(key)
                participantId = ""
                for player in matchRequest["participantIdentities"]:
                    #print(player["player"]["summonerName"])
                    if (player["player"]["summonerName"] == summonerName):
                        participantId = player["participantId"]
                teamColor = 0
                for player in matchRequest["participants"]:
                    if(player["participantId"] == participantId):
                        teamColor = player["teamId"]
                totalDamage = 0
                totalGold = 0
                for player in matchRequest["participants"]:
                    if (player["teamId"] == teamColor):
                        totalGold = totalGold + player["stats"]["goldEarned"]
                        totalDamage = totalDamage + player["stats"]["totalDamageDealtToChampions"]

                #print(participantId)        
                for player in matchRequest["participants"]:
                    if(player["participantId"] == participantId):
                        wards = player["stats"]["wardsPlaced"]
                        time = (float)(matchRequest["gameDuration"])/60
                        gold = (float)(player["stats"]["goldEarned"])
                        damage = (float)(player["stats"]["totalDamageDealtToChampions"])
                        WPM = round(wards/time,2)
                        CSPM = round((player["stats"]["totalMinionsKilled"]/((float)(matchRequest["gameDuration"])/60)),2)
                        goldShare = round(gold/totalGold*100,1)
                        damageShare = round(damage/totalDamage*100,1)
                        damagePerGold = round((damage/totalDamage)/(gold/totalGold),2)
                        averageWPM = averageWPM + WPM
                        averageCSPM = averageCSPM + CSPM
                        averageDamagePerGold = averageDamagePerGold + damagePerGold
                        
                        #print("WPM = " + (str)(WPM))
                        #print("CSPM = " + (str)(CSPM))
                        #print("Gold Share = " + (str)(goldShare) + "%")
                        #print("Damage Share = " + (str)(damageShare) + "%")
                        #print("Damage/Gold = " + (str)(damagePerGold))
                        #print("")
        else:
            matchesToCheck = matchesToCheck + 1
            num = num+1
    else:
        matchesToCheck = matchesToCheck + 1
        num = num+1
        

averageWPM = round(averageWPM/howManyMatches,2)
averageCSPM = round(averageCSPM/howManyMatches,2)
averageDamagePerGold = round(averageDamagePerGold/howManyMatches,2)
print(summonerName + " " + role)
print("Average WPM = " + (str)(averageWPM))
print("Average CSPM = " + (str)(averageCSPM))
print("Average Damage/Gold = " + (str)(averageDamagePerGold))
print(champsPlayed)
