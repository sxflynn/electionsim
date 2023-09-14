import random
import time
from jsonReader import *

start_time = time.time()

electionWins = {}
electionReturns = {}
ballotChoice = {}

# OPENING MESSAGE
# print ("Welcome to the November 2021 Upper Arlington School Board Election simulation!")
# print ("In Nov 2020, there were 24,622 ballots cast. 61.5% for Biden and 36.7% for Trump, and 1.8% for others. In other races, 49.1% voted for State Senator Kunze(R), and 50.9% voted for Rep. Stivers(R). In previous November elections, 23,309 ballots were cast in 2016, 15,526 in 2017, 21,043 in 2018 and 9,556 in 2019.")
# print ("Let's run a simulation of the upcoming school board election.")
# print("The electorate will be composed of " + str(round(float(gopVoteShare*100))) + "% partisan Trump voters, " + str(round(float(indVoteShare*100))) + "% Biden/Stivers voters and " + str(round(float(demVoteShare*100)))+"% partisan Democrats.")


# print("A party line Democratic voter's choice probabilities:")
# for k, v in demPrefs.items():
#     print(k + " " + str(int(v*100))+ "%")

# print("A party line Trump voter's choice probabilities:")
# for k, v in gopPrefs.items():
#     print(k + " " + str(int(v*100))+ "%")

# print("A Biden/Stivers voter's choice probabilities:")
# for k, v in indPrefs.items():
#     print(k + " " + str(int(v*100))+ "%")

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