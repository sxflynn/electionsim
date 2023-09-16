import random
import time
import multiprocessing
from jsonReader import *
from datetime import datetime



electionWins = {}
electionReturns = {}
ballotChoice = {}

def initDictionary(inputDict, names): #initialize dictionary
    for element, index in enumerate(names): 
        inputDict[index] = 0

def sortItems(itemInput):
    outputList = sorted(itemInput.items(), key=lambda x: x[1], reverse=True)
    return outputList

def decideVote(ballotDict,preferences):
    initDictionary(ballotDict,candidate_names)
    for i in range(len(ballotDict)):
            for k, v in ballotDict.items():
                if random.SystemRandom().uniform(0,1) < preferences.get(k):
                    ballotDict[k]+=1

def vote(profile):
    voterPref = voterProfiles[profile]
    decideVote(ballotChoice,voterPref)
    prefSorted = sortItems(ballotChoice)
    voteCastDict = dict(prefSorted[0:numOfBallotWinners])
    voteCast = list(voteCastDict.keys())
    return voteCast

def addReturns(ballot):
    for i in ballot:
        for key, val in electionReturns.items():
            if key == i:
                electionReturns[key]+=1

def oneElection():    
    for party in electorateData:
        for w in range(int(totalVoters*float(electorateData[party]))):
            addReturns(vote(party))
    returnsSorted = sortItems(electionReturns)
    returnsDict = dict(returnsSorted[0:numOfBallotWinners])
    winners = list(returnsDict.keys())
    return winners

def addWins(electionResults):
    for i in electionResults:
        for key, val in electionWins.items():
            if key == i:
                electionWins[key]+=1

def percentDisplay(num):
    percentString = str(round(float(num/numOfSims)*100, 1)) + "%"
    return percentString

def printWinnters(inputList):
    for k, v in inputList:
        print (k + ' - ' + str(v) + " - " + percentDisplay(v) + " chance of being elected.")

initDictionary(electionReturns,candidate_names) #initialize the electionReturns dictionary
initDictionary(electionWins,candidate_names) #initialize the electionReturns dictionary

startTime = time.time()

for i in range(numOfSims):
    addWins(oneElection())
    initDictionary(electionReturns,candidate_names) # reinitialize the electionReturns dict back to zeros for the next election

winsSorted = sortItems(electionWins) # Count the number of wins.

def outputAsJson(winnerList):
    candidates = {}
    for name, numOfWins in winnerList:
        candidates[name] = {
            "numberOfWins": numOfWins,
            "probabilityToWin": percentDisplay(numOfWins)
    }
    now = datetime.now()
    stringDate = now.strftime("%d/%m/%Y %H:%M:%S")  

    combinedJson = {
        "timestamp": stringDate,
        "electionSettings": settingsData,
        "candidates": candidates,
        "voterProfiles": voterProfiles,
        "electorate": electorateData
    }
    print(json.dumps(combinedJson, indent = 3))

outputAsJson(winsSorted)

e = time.time() - startTime
print("Running time %02d:%02d:%02d.%03d" % (e // 3600, (e % 3600 // 60), (e % 60 // 1), (e % 1 * 1000)))
