import json

# Open the JSON file for reading
with open('config.json', 'r') as electionFile:
    # Parse JSON data
    jsonObject = json.load(electionFile)

candidate_names = jsonObject['candidates']

numOfBallotWinners = jsonObject["electionSettings"]["ballotWinners"]
numOfSims = jsonObject["electionSettings"]["numOfSims"]
totalVoters = jsonObject["electionSettings"]["totalVoters"]

numOfVoterProfiles = len(jsonObject['voterProfiles'])

electorateData = jsonObject['electorate']


# electorateData = {"gopVoteShare": 0.4, "indVoteShare": 0.15, "demVoteShare": 0.46}

def getElectorate(electorateObj):
    ##checking that it adds up to 1.0
    totalOne = 0
    for k in electorateObj.values():
        totalOne += k
    print (totalOne)
    
    if (totalOne == 1.0):
        print ("It adds to 1!")
        return electorateObj
    
    # TODO : Write simple algo for when totalOne != 1
    abbsDiff = round((abs(totalOne - 1)),2)
    electorateSorted = sorted(electorateObj.items(), key=lambda x: x[1], reverse=True)
    # print (electorateSorted)
    electDict = dict(electorateSorted)
    # print (electDict)
    if (totalOne > 1):
        return
    #else: ## forcing a 1.0 sum by subtracting sum of smallest values from largest value
        
# getElectorate(electorateData)