#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 09:56:21 2019

@author: ahir.chatterjee
"""

from bs4 import BeautifulSoup
import requests
import json

#slug = input("Enter slug: ")
headers = {"x-api-key":"0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z"}
leagues = json.loads(requests.get("https://esports-api.lolesports.com/persisted/gw/getLeagues?hl=en-US",headers=headers).text)
slugToId = {}
for tourney in leagues["data"]["leagues"]:
    slugToId[tourney["slug"]] = tourney["id"]
tourniesBySlug = {}
for slug in slugToId:
    tournies = json.loads(requests.get("https://esports-api.lolesports.com/persisted/gw/getTournamentsForLeague?hl=en-US&leagueId=" + slugToId[slug],headers=headers).text)
    tourniesBySlug[slug] = tournies["data"]["leagues"][0]["tournaments"]
uSlug = input("Enter slug: ")
tId = 0
for slug in tourniesBySlug:
    for s in tourniesBySlug[slug]:
        if(s["slug"] == uSlug):
            tId = s["id"]
standings = json.loads(requests.get("https://esports-api.lolesports.com/persisted/gw/getStandings?hl=en-US&tournamentId=" + tId,headers=headers).text)["data"]["standings"][0]["stages"]
regularSeasonGameIds = []
for game in standings[0]["sections"][0]["matches"]:
    regularSeasonGameIds.append(game["id"])
events = json.loads(requests.get("https://esports-api.lolesports.com/persisted/gw/getCompletedEvents?hl=en-US&tournamentId=" + tId,headers=headers).text)
eventDetails = {}
someGame = json.loads(requests.get("https://feed.lolesports.com/livestats/v1/details/102147201375313283").text)
someOtherGame = json.loads(requests.get("https://feed.lolesports.com/livestats/v1/window/102147201375313283").text)
#for gId in regularSeasonGameIds:
#    eventDetail = json.loads(requests.get("https://esports-api.lolesports.com/persisted/gw/getEventDetails?hl=en-US&id=" + gId,headers=headers).text)
#    eventDetails[gId] = eventDetail
#idToCheck = "102147201358732634"
#gameIds = []
#for matchId in eventDetails:
#    for game in eventDetails[matchId]["data"]["event"]["match"]["games"]:
#        gameId = game["id"]
#        gameIds.append(gameId)
#        if(gameId == idToCheck):
#            print("found")