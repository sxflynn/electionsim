import random
import time
from datetime import datetime
import json


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
                self.initDictionary(self.electionReturns, self.candidateNames)
                self.initDictionary(self.electionWins, self.candidateNames)

        except json.JSONDecodeError:
            print("Failed to load election data")
        except FileNotFoundError:
            print("The config.json file does not exist.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        finally:
            jsonFile.close()


    def initDictionary(self, inputDict, names): #initialize dictionary
        for element, index in enumerate(names): 
            inputDict[index] = 0

    def sortItems(self, itemInput):
        outputList = sorted(itemInput.items(), key=lambda x: (x[1], random.random()), reverse=True) # tie-breaker
        return outputList

    def decideVote(self, ballotDict,preferences):
        self.initDictionary(ballotDict,self.candidateNames)
        for _ in range(2): # lower values increase speed and variation
            rand = random.SystemRandom().uniform(0,1)
            for k, _ in ballotDict.items():
                if rand < preferences.get(k):
                    ballotDict[k]+=1

    def vote(self, profile):
        voterPref = self.voterProfiles[profile]
        self.decideVote(self.ballotChoice,voterPref)
        prefSorted = self.sortItems(self.ballotChoice)
        voteCastDict = dict(prefSorted[0:self.numOfBallotWinners])
        voteCast = list(voteCastDict.keys())
        return voteCast

    def addReturns(self, ballot):
        for i in ballot:
            for key, _ in self.electionReturns.items():
                if key == i:
                    self.electionReturns[key]+=1

    def peopleDecide(self, electorateData):
        for party in electorateData:
                for _ in range(int(self.totalVoters*float(electorateData[party]))):
                    self.addReturns(self.vote(party))
        #print("electionReturns are " + str(electionReturns))


    def oneElection(self):    
        self.peopleDecide(self.electorateData)
        returnsSorted = dict(self.sortItems(self.electionReturns)[0:self.numOfBallotWinners])
        winners = list(returnsSorted.keys())
        return winners
        
    def addWins(self, electionResults):
        for i in electionResults:
            for key, _ in self.electionWins.items():
                if key == i:
                    self.electionWins[key]+=1
        self.initDictionary(self.electionReturns,self.candidateNames) # reinitialize the electionReturns dict back to zeros for the next election


    def runElections(self, howMany):
        for i in range(howMany):
            self.addWins(self.oneElection())

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
        
    def checkElectionJson(self, jsonData):    

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

def sameList(list1, list2): #returns true if two lists are identical
        set1 = set(list1)
        set2 = set(list2)
        return set1 == set2


if __name__ == "__main__":
    
    startTime = time.time()
    
    election_simulator = ElectionSimulator("config.json")
    election_simulator.initDictionary(election_simulator.electionReturns,election_simulator.candidateNames) #initialize the electionReturns dictionary
    election_simulator.initDictionary(election_simulator.electionWins,election_simulator.candidateNames) #initialize the electionReturns dictionary
    
    
    election_simulator.runElections(election_simulator.numOfSims)
    
    
    winsSorted = election_simulator.sortItems(election_simulator.electionWins) # Count the number of wins.

    election_simulator.outputAsJson(winsSorted)
    stopWatch = time.time() - startTime
    election_simulator.printTime(stopWatch)


