import random
import time
from jsonReader import *

start_time = time.time()

electionWins = {}
electionReturns = {}
ballotChoice = {}

def vote(profile):
    voterPref = voterProfiles[profile]

    for element, index in enumerate(candidate_names): # initialize the ballotChoice dictionary
        ballotChoice[index] = 0
    
    for i in range(len(ballotChoice)):
        for k, v in ballotChoice.items():
            if random.SystemRandom().uniform(0,1) < voterPref.get(k):
                ballotChoice[k]+=1
                
    prefSorted = sorted(ballotChoice.items(), key=lambda x: x[1], reverse=True)

    voteCastDict = dict(prefSorted[0:numOfBallotWinners])
    voteCast = list(voteCastDict.keys())
    return voteCast

for element, index in enumerate(candidate_names): #initialize the electionReturns dictionary
    electionReturns[index] = 0

def addReturns(ballot):
    for i in ballot:
        for k, v in electionReturns.items():
            if k == i:
                electionReturns[k]+=1
             #    print (electionReturns)

def oneElection():    
    # gopVoters = gopVoteShare
    # indVoters = indVoteShare
    # demVoters = 1 - (gopVoters+indVoters)
    # print("Turnout is " + str(totalVoters) + " total voters")
    # print(str(int(gopVoters*100)) + "% of voters are party line Trump voters")
    # print(str(int(indVoters*100)) + "% of voters are Biden/Stivers voters")
    # print(str(int(demVoters*100)) + "% of voters are party line Democratic voters")
    
    for party in electorateData:
        for w in range(int(totalVoters*float(electorateData[party]))):
            addReturns(vote(party))

    returnsSorted = sorted(electionReturns.items(), key=lambda x: x[1], reverse=True)

    #print ("Now let's print the final election returns!")
    # for k, v in returnsSorted:
    #     print (k + ' - ' + str(v))

    returnsDict = dict(returnsSorted[0:numOfBallotWinners])
    winners = list(returnsDict.keys())
    return winners


for element, index in enumerate(candidate_names): #initialize the electionWins dictionary
    electionWins[index] = 0

def addWins(electionResults):
    for i in electionResults:
        for k, v in electionWins.items():
            if k == i:
                electionWins[k]+=1

# print("Let's simulate " + str(numOfSims) + " elections and calculate each candidate's probability of winning.")

for i in range(numOfSims):
    addWins(oneElection())
    for element, index in enumerate(candidate_names): # reinitialize the electionReturns dict back to zeros for the next election
        electionReturns[index] = 0


# Finally, let's count up the number of wins.
winsSorted = sorted(electionWins.items(), key=lambda x: x[1], reverse=True)

for k, v in winsSorted:
    print (k + ' - ' + str(v) + " - " + str(round(float(v/numOfSims)*100, 1)) + "% chance of being elected.")
    
e = time.time() - start_time
print("Running time %02d:%02d:%02d" % (e // 3600, (e % 3600 // 60), (e % 60 // 1)))