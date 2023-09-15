import random
import time
from jsonReader import *

start_time = time.time()

electionWins = {}
electionReturns = {}
ballotChoice = {}

def initDictionary(inputDict, names): #initialize dictionary
    for element, index in enumerate(names): 
        inputDict[index] = 0

def sortItems(itemInput):
    outputList = sorted(itemInput.items(), key=lambda x: x[1], reverse=True)
    return outputList

def vote(profile):
    voterPref = voterProfiles[profile]

    initDictionary(ballotChoice,candidate_names)
    
    for i in range(len(ballotChoice)):
        for k, v in ballotChoice.items():
            if random.SystemRandom().uniform(0,1) < voterPref.get(k):
                ballotChoice[k]+=1
                
    prefSorted = sortItems(ballotChoice)

    voteCastDict = dict(prefSorted[0:numOfBallotWinners])
    voteCast = list(voteCastDict.keys())
    return voteCast

def addReturns(ballot):
    for i in ballot:
        for k, v in electionReturns.items():
            if k == i:
                electionReturns[k]+=1
             #    print (electionReturns)

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
        for k, v in electionWins.items():
            if k == i:
                electionWins[k]+=1

def printWinnters(inputList):
    for k, v in inputList:
        print (k + ' - ' + str(v) + " - " + str(round(float(v/numOfSims)*100, 1)) + "% chance of being elected.")                


initDictionary(electionReturns,candidate_names) #initialize the electionReturns dictionary
initDictionary(electionWins,candidate_names) #initialize the electionReturns dictionary

for i in range(numOfSims):
    addWins(oneElection())
    initDictionary(electionReturns,candidate_names) # reinitialize the electionReturns dict back to zeros for the next election

winsSorted = sortItems(electionWins) # Count the number of wins.

printWinnters(winsSorted)
    
e = time.time() - start_time
print("Running time %02d:%02d:%02d" % (e // 3600, (e % 3600 // 60), (e % 60 // 1)))