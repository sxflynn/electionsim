import json

def sameList(list1, list2): #returns true if two lists are identical
    set1 = set(list1)
    set2 = set(list2)
    return set1 == set2

def checkElectionJson(jsonData):    

    candidates = jsonData.get("candidates", [])  # Extract candidates, voter profiles, and electorate data
    voterProfiles = jsonData.get("voterProfiles", {})
    electorate = jsonData.get("electorate", {})
    
    for party, profiles in voterProfiles.items(): # Check if candidates match the voter profiles
        if not sameList(candidates, profiles.keys()):
            print("The candidates list does not match the candidates in the voter profiles.")
            return False
    
    if not sameList(list(electorate.keys()), list(voterProfiles.keys())): # Check if parties in electorate match the voter profiles
        print("The parties listed in the electorate key do not match the parties in the voter profiles.")
        return False
    
    return True

try:
    with open("config.json", 'r') as jsonFile:
        jsonObject = json.load(jsonFile)
        ## Initializing JSON data to variables
        if not checkElectionJson(jsonObject):
            print("JSON data integrity check failed. Exiting.")
        
        candidate_names = jsonObject["candidates"]
        numOfBallotWinners = jsonObject["electionSettings"]["ballotWinners"]
        numOfSims = jsonObject["electionSettings"]["numOfSims"]
        multiP = jsonObject["electionSettings"]["multiprocessing"]
        totalVoters = jsonObject["electionSettings"]["totalVoters"]
        voterProfiles = jsonObject["voterProfiles"]
        message = jsonObject["message"]
        electorateData = jsonObject["electorate"]
        settingsData = jsonObject["electionSettings"]

except json.JSONDecodeError:
    print("Failed to load election data")
except FileNotFoundError:
    print("The config.json file does not exist.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    jsonFile.close()