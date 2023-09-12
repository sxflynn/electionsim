import random
import secrets
import time
start_time = time.time()
print ("Welcome to the November 2021 Upper Arlington School Board Election simulation!")
print ("In Nov 2020, there were 24,622 ballots cast. 61.5% for Biden and 36.7% for Trump, and 1.8% for others. In other races, 49.1% voted for State Senator Kunze(R), and 50.9% voted for Rep. Stivers(R). In previous November elections, 23,309 ballots were cast in 2016, 15,526 in 2017, 21,043 in 2018 and 9,556 in 2019.")
print ("Let's run a simulation of the upcoming school board election.")

demPrefs = {'Liz': .02, 'Lou': .05, 'Nidhi':.98, 'Scott':.40, 'Carol':.70}
indPrefs = {'Liz': .20, 'Lou': .45, 'Nidhi':.35, 'Scott':.70, 'Carol':.45}
gopPrefs = {'Liz': .90, 'Lou': .98, 'Nidhi':.02, 'Scott':.20, 'Carol':.05}

gopVoteShare = .39
indVoteShare = .15
demVoteShare = 1-(indVoteShare+gopVoteShare)
print("The electorate will be composed of " + str(round(float(gopVoteShare*100))) + "% partisan Trump voters, " + str(round(float(indVoteShare*100))) + "% Biden/Stivers voters and " + str(round(float(demVoteShare*100)))+"% partisan Democrats.")


print("A party line Democratic voter's choice probabilities:")
for k, v in demPrefs.items():
    print(k + " " + str(int(v*100))+ "%")

print("A party line Trump voter's choice probabilities:")
for k, v in gopPrefs.items():
    print(k + " " + str(int(v*100))+ "%")

print("A Biden/Stivers voter's choice probabilities:")
for k, v in indPrefs.items():
    print(k + " " + str(int(v*100))+ "%")

# class Voter:
#     def __init__(self, profile):
#         self.profile = profile
#         print("A new " + profile + " voter has been created!")



def vote(profile):
    if profile=='Dem':
        voterPref = demPrefs
    elif profile=='Ind':
        voterPref = indPrefs
    elif profile=='GOP':
        voterPref = gopPrefs
    else:
        print("ERROR!the vote function didn't work!!")
    ballotChoice = {'Liz': 0, 'Lou': 0, 'Nidhi':0, 'Scott':0, 'Carol':0}
    for i in range(5):
        for k, v in ballotChoice.items():
            if random.SystemRandom().uniform(0,1) < voterPref.get(k):
                ballotChoice[k]+=1
                
    prefSorted = sorted(ballotChoice.items(), key=lambda x: x[1], reverse=True)
#     for k, v in prefSorted:
#         print (k + ' is receiving ' + str(v))

    voteCastDict = dict(prefSorted[0:2])
    voteCast = list(voteCastDict.keys())
    return voteCast

# Election return system
electionReturns = {'Liz': 0, 'Lou': 0, 'Nidhi':0, 'Scott':0, 'Carol':0}

def addReturns(ballot):
    for i in ballot:
        for k, v in electionReturns.items():
            if k == i:
                electionReturns[k]+=1
             #    print (electionReturns)

# Do the actual election

def oneElection():
    #totalVoters = random.randint(1300, 1500) # it doesn't need to be the full 19000 to 21000.
    totalVoters = 14500
    gopVoters = random.SystemRandom().uniform(gopVoteShare-.01,gopVoteShare+.01)
    indVoters = random.SystemRandom().uniform(indVoteShare-.02,indVoteShare+.02)
    demVoters = 1 - (gopVoters+indVoters)
    print("Turnout is " + str(totalVoters) + " total voters")
    print(str(int(gopVoters*100)) + "% of voters are party line Trump voters")
    print(str(int(indVoters*100)) + "% of voters are Biden/Stivers voters")
    print(str(int(demVoters*100)) + "% of voters are party line Democratic voters")
    for i in range(int(totalVoters*float(gopVoters))):
        addReturns(vote('GOP'))
        # print (i)
 
    for i in range(int(totalVoters*float(indVoters))):
        addReturns(vote('Ind'))
        # print (i)

    for i in range(int(totalVoters*float(demVoters))):
        addReturns(vote('Dem'))
        # print (i)

    returnsSorted = sorted(electionReturns.items(), key=lambda x: x[1], reverse=True)

    print ("Now let's print the final election returns!")
    for k, v in returnsSorted:
        print (k + ' - ' + str(v))

    returnsDict = dict(returnsSorted[0:2])
    winners = list(returnsDict.keys())
   #  print("The winners are "+ str(winners[0]) + " and " + str(winners[1]))
    return winners

electionWins = {'Liz': 0, 'Lou': 0, 'Nidhi':0, 'Scott':0, 'Carol':0}

def addWins(electionResults):
    for i in electionResults:
        # print (electionResults)
        for k, v in electionWins.items():
            if k == i:
                electionWins[k]+=1

numOfSims = 1
print("Let's simulate " + str(numOfSims) + " elections and calculate each candidate's probability of winning.")

# your code

for i in range(numOfSims):
 #   print (i)
    addWins(oneElection())
    electionReturns = {'Liz': 0, 'Lou': 0, 'Nidhi':0, 'Scott':0, 'Carol':0}


# Finally, let's count up the number of wins.
winsSorted = sorted(electionWins.items(), key=lambda x: x[1], reverse=True)

for k, v in winsSorted:
    print (k + ' - ' + str(v) + " - " + str(round(float(v/numOfSims)*100, 1)) + "% chance of being elected.")
    
e = time.time() - start_time
print("%02d:%02d:%02d" % (e // 3600, (e % 3600 // 60), (e % 60 // 1)))

# aDemocrat = Voter(self,"Dem")
# aDemocrat.vote('Dem')


