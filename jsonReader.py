import json

def sameList(list1, list2): #returns true if two lists are identical
    set1 = set(list1)
    set2 = set(list2)
    return set1 == set2

def checkElectionJson(jsonData):    
    # Extract candidates, voter profiles, and electorate data
    candidates = jsonData.get("candidates", [])
    voterProfiles = jsonData.get("voterProfiles", {})
    electorate = jsonData.get("electorate", {})
    
    # Check if candidates match the voter profiles
    for party, profiles in voterProfiles.items():
        if not sameList(candidates, profiles.keys()):
            return False
    
    # Check if parties in electorate match the voter profiles
    if not sameList(list(electorate.keys()), list(voterProfiles.keys())):
        return False
    
    return True


# def getElectorate(electorateObj):
#     ##checking that it adds up to 1.0
#     totalOne = 0
#     for k in electorateObj.values():
#         totalOne += k
#     print (totalOne)
    
#     if (totalOne == 1.0):
#         print ("It adds to 1!")
#         return electorateObj
    
#     # # TODO : Write simple algo for when totalOne != 1
#     # abbsDiff = round((abs(totalOne - 1)),2)
#     # electorateSorted = sorted(electorateObj.items(), key=lambda x: x[1], reverse=True)
#     # # print (electorateSorted)
#     # electDict = dict(electorateSorted)
#     # # print (electDict)
#     # if (totalOne > 1):
#     #     return
#     # #else: ## forcing a 1.0 sum by subtracting sum of smallest values from largest value
        


# Open the JSON file for reading
try:
    with open('config.json', 'r') as electionFile:
        jsonObject = json.load(electionFile)
        ## Initializing JSON data to variables
        
        print ("checkElection is " + str(checkElectionJson(jsonObject)))
        
        candidate_names = jsonObject['candidates']

        numOfBallotWinners = jsonObject["electionSettings"]["ballotWinners"]

        numOfSims = jsonObject["electionSettings"]["numOfSims"]

        totalVoters = jsonObject["electionSettings"]["totalVoters"]

        voterProfiles = jsonObject["voterProfiles"]


        message = jsonObject["message"]

        numOfVoterProfiles = len(jsonObject['voterProfiles'])

        electorateData = jsonObject['electorate']


except json.JSONDecodeError:
    print("Failed to load election data")



