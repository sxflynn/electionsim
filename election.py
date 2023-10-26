import random
import time
from datetime import datetime
import json


#Utility functions
def sortItems(itemInput):
    outputList = sorted(itemInput.items(), key=lambda x: (x[1], random.random()), reverse=True) # tie-breaker
    return outputList

def sameList(list1, list2): #returns true if two lists are identical
        return set(list1) == set(list2)

class ElectionSimulator:

    def __init__(self, config_file):
        self.config_file = config_file
        self.loadConfig()

    def loadConfig(self):
        try:
            with open(self.config_file, 'r') as jsonFile:
                jsonObject = json.load(jsonFile)
                self.candidateNames = jsonObject["candidates"]
                self.numOfBallotWinners = jsonObject["electionSettings"]["ballotWinners"]
                self.numOfSims = jsonObject["electionSettings"]["numOfSims"]
                self.totalVoters = jsonObject["electionSettings"]["totalVoters"]
                self.voterProfiles = jsonObject["voterProfiles"]
                self.message = jsonObject["message"]
                self.electorateData = jsonObject["electorate"]
                self.settingsData = jsonObject["electionSettings"]
                self.electionReturns = {}
                self.electionWins = {}
                self.ballotChoice = {}
                self.electionReturns = {name: 0 for name in self.candidateNames}
                self.electionWins = {name: 0 for name in self.candidateNames}

        except json.JSONDecodeError:
            print("Failed to load election data")
        except FileNotFoundError:
            print("The config.json file does not exist.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        
    def addWins(self, electionResults):
        for i in electionResults:
            for key, _ in self.electionWins.items():
                if key == i:
                    self.electionWins[key]+=1
        self.electionReturns = {name: 0 for name in self.candidateNames} # reinitialize the electionReturns dict back to zeros for the next election

    def runElections(self):
        for i in range(self.numOfSims):
            election = Election(
            self.candidateNames, 
            self.totalVoters, 
            self.numOfBallotWinners, 
            self.voterProfiles, 
            self.electorateData
        )
            self.addWins(election.oneElection())
        winsSorted = sortItems(self.electionWins)
        return winsSorted

    def percentDisplay(self, num):
        percentString = str(round(float(num/self.numOfSims)*100, 1)) + "%"
        return percentString

    # def printWinnters(inputList):
    #     for k, v in inputList:
    #         print (k + ' - ' + str(v) + " - " + percentDisplay(v) + " chance of being elected.")

    def outputAsJson(self, winnerList):
        candidates = {}
        for name, numOfWins in winnerList:
            candidates[name] = {
                "numberOfWins": numOfWins,
                "probabilityToWin": self.percentDisplay(numOfWins)
        }
        now = datetime.now()
        stringDate = now.strftime("%d/%m/%Y %H:%M:%S")
        combinedJson = {
            "timestamp": stringDate,
            "electionSettings": self.settingsData,
            "candidates": candidates,
            "voterProfiles": self.voterProfiles,
            "electorate": self.electorateData
        }
        print(json.dumps(combinedJson, indent = 3))

    def printTime(self, time):
        print("Running time %02d:%02d:%02d.%03d" % (time // 3600, (time % 3600 // 60), (time % 60 // 1), (time % 1 * 1000)))
        
    def checkElectionJson(self, jsonData):    # Pydantic will make most of this unnecesary
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


class Election:
    def __init__(self, candidateNames, totalVoters, numOfBallotWinners, voterProfiles, electorateData):
        self.candidateNames = candidateNames
        self.totalVoters = totalVoters
        self.numOfBallotWinners = numOfBallotWinners
        self.voterProfiles = voterProfiles
        self.electorateData = electorateData
        self.electionReturns = {name: 0 for name in self.candidateNames}
        self.electionWins = {name: 0 for name in self.candidateNames}
        
    def decideVote(self, preferences):
        ballot_dict = {name: 0 for name in self.candidateNames}
        rand = random.SystemRandom().uniform(0, 1)  # rand = random.uniform(0, 1)    # rand = random.SystemRandom().uniform(0, 1)
        for _ in range(1): # lower values increase speed and variation
            for candidate, _ in ballot_dict.items():
                if rand < preferences.get(candidate):
                    ballot_dict[candidate] += 1
        return ballot_dict
    
    def vote(self, profile):
        ballot_dict = self.decideVote(self.voterProfiles[profile])
        pref_sorted = sortItems(ballot_dict)
        vote_cast = [k for k, v in pref_sorted if v > 0][:self.numOfBallotWinners] #bulletvoting now supported
        return vote_cast

    def addReturns(self, ballot):
        for i in ballot:
            self.electionReturns[i]+=1

    def peopleDecide(self, electorateData):
        for party, party_proportion in electorateData.items():
            num_votes = int(self.totalVoters * float(party_proportion))
            for _ in range(num_votes):
                self.addReturns(self.vote(party))
        #print("electionReturns are " + str(electionReturns))

    def oneElection(self):    
        self.peopleDecide(self.electorateData)
        returnsSorted = dict(sortItems(self.electionReturns)[0:self.numOfBallotWinners])
        winners = list(returnsSorted.keys())
        return winners