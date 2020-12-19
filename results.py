import os
import json

MAX_PAGE=1
PAGE_SIZE=25
FETCH_RESULTS_COMMAND_FORMAT="./getResults.zsh {pageSize} {page}"
FETCH_SCORE_COMMAND_FORMAT="./getScore.zsh {resultId}"
TEMP_OUTPUT_FILE="output.json"
MAP_FILTER = "A Diverse World"
PROJECT_NAME="test"
TEMP_DIR="tmp/"
OUTPUT_DIR="output/"


def isValidResult(result):
    if "id" in result and "payload" in result:
        if "map" in result["payload"]:
            if "name" in result["payload"]["map"] and "gameToken" in result["payload"]["map"]:
                return True
    return False

def isValidScore(score):
    if "props" in score:
        if "pageProps" in score["props"]:
            if "gamePlayedByCurrentUser" in score["props"]["pageProps"]:
                if "rounds" in score["props"]["pageProps"]["gamePlayedByCurrentUser"] and "player" in score["props"]["pageProps"]["gamePlayedByCurrentUser"] and "round" in score["props"]["pageProps"]["gamePlayedByCurrentUser"]:
                    if "guesses" in score["props"]["pageProps"]["gamePlayedByCurrentUser"]["player"]:
                        return True
    return False

def fetchJsonFromCommandOutput(fetchCommand):
    fetchCommandWithOutput = fetchCommand + " > " + TEMP_OUTPUT_FILE
    fetchResponse = os.system(fetchCommandWithOutput)
    outputFileHandle = open(TEMP_OUTPUT_FILE)
    resultData = json.load(outputFileHandle)
    outputFileHandle.close()
    return resultData


def fetchResultIds(pageSize, maxPage):
    resultIds = []
    for page in range(maxPage):
        fetchCommand = FETCH_RESULTS_COMMAND_FORMAT.format(pageSize=pageSize, page=page)
        resultData = fetchJsonFromCommandOutput(fetchCommand)
        for result in resultData:
            if isValidResult(result):
                if result["payload"]["map"]["name"] == MAP_FILTER:
                    resultIds.append(result["payload"]["map"]["gameToken"])
    return resultIds

def fetchScore(resultId):
    fetchCommand = FETCH_SCORE_COMMAND_FORMAT.format(resultId=resultId)
    scoreData = fetchJsonFromCommandOutput(fetchCommand)
    return scoreData

class PlayerRound:
    def __init__(self, lat, lng, scorePercent):
        self.lat = lat
        self.lng = lng
        self.scorePercent = scorePercent
    def printLocation(self):
        return str(self.lat) + "," + str(self.lng)




print("Fetching recent activity...")
resultIds = fetchResultIds(PAGE_SIZE, MAX_PAGE)


    
playerRounds = []

SCORE_PERCENT_THRESHOLD = 100

print("Fetching results from games...")
for resultId in resultIds:
    score = fetchScore(resultId)
    if isValidScore(score):
        numRounds = score["props"]["pageProps"]["gamePlayedByCurrentUser"]["round"]
        rounds = score["props"]["pageProps"]["gamePlayedByCurrentUser"]["rounds"]
        guesses = score["props"]["pageProps"]["gamePlayedByCurrentUser"]["player"]["guesses"]
        for i in range(numRounds):
            round = rounds[i]
            guess = guesses[i]
            scorePercent = guess["roundScoreInPercentage"]
            if scorePercent <= SCORE_PERCENT_THRESHOLD:
                roundLat = round["lat"]
                roundLng = round["lng"]
                playerRound = {"lat": roundLat, "lng": roundLng, "scorePercent": scorePercent}
#                playerRound = PlayerRound(roundLat, roundLng, scorePercent)
                playerRounds.append(playerRound)


# for playerRound in playerRounds:
#     print(playerRound.printLocation())

outputJsonText = "var playerRounds=" + json.dumps(playerRounds, indent=4) + ";"
outputJson = OUTPUT_DIR + "data_" + PROJECT_NAME + ".js"
outputJsonHandle = open(outputJson, mode="w")
outputJsonHandle.write(outputJsonText)
outputJsonHandle.close()




