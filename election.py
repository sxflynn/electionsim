import random
import json
from typing import Dict, List
from pydantic import BaseModel

#Pydantic models
class ElectionSettings(BaseModel):
    numOfSims: int
    totalVoters: int
    ballotWinners: int

class Config(BaseModel):
    candidates: List[str]
    voterProfiles: Dict[str, Dict[str, float]]
    electorate: Dict[str, float]
    electionSettings: ElectionSettings
    message: str

#Utility functions
def sortItems(item_input):
    output_list = sorted(item_input.items(), key=lambda x: (x[1], random.random()), reverse=True) # tie-breaker
    return output_list

def sameList(list1, list2): #returns true if two lists are identical
        return set(list1) == set(list2)

class ConfigFile:
    def __init__(self,config_file):
        self.config_file = config_file
        self.load_config()

    def load_config(self):
        try:
            with open(self.config_file, 'r', encoding="utf-8") as jsonFile:
                json_object = json.load(jsonFile)
                config_data = Config(**json_object) # call Pydantic model
                self.candidates = config_data.candidates
                self.num_of_ballot_winners = config_data.electionSettings.ballotWinners
                self.num_of_sims = config_data.electionSettings.numOfSims
                self.total_voters = config_data.electionSettings.totalVoters
                self.voter_profiles = config_data.voterProfiles
                self.message = config_data.message
                self.electorate_data = config_data.electorate
                self.settings_data = config_data.electionSettings
        except json.JSONDecodeError:
            print("Failed to load config data")
        except FileNotFoundError:
            print("The config.json file does not exist.")
        except IOError:
            print("An IOError occurred while reading the file.")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

class ElectionSimulator:

    def __init__(self, config: ConfigFile):
        self.config = config
        self.election_returns = {name: 0 for name in self.config.candidates}
        self.election_wins = {name: 0 for name in config.candidates}

    def add_wins(self, election_results):
        for i in election_results:
            for key, _ in self.election_wins.items():
                if key == i:
                    self.election_wins[key]+=1

    def runElections(self):
        for i in range(self.config.num_of_sims):
            election = Election(self.config)
            self.add_wins(election.one_election())
        wins_sorted = sortItems(self.election_wins)
        return wins_sorted

    def percent_display(self, num):
        percent_string = str(round(float(num/self.config.num_of_sims)*100, 1)) + "%"
        return percent_string

    def print_winners(self, input_list):
        for k, v in input_list:
            print(f"{k:<15} - {v:>3} - {self.percent_display(v):>8} chance of being elected.")

    def print_time(self, systime):
        print(f"Running time {int(systime // 3600):02d}:{int(systime % 3600 // 60):02d}:{int(systime % 60 // 1):02d}.{int(systime % 1 * 1000):03d}")

class Election:
    def __init__(self, config: ConfigFile):
        self.config = config
        self.election_returns = {name: 0 for name in config.candidates}
        self.election_wins = {name: 0 for name in config.candidates}

    def decide_vote(self, preferences):
        ballot_dict = {name: 0 for name in self.config.candidates}
        rand = random.SystemRandom().uniform(0, 1)  # rand = random.uniform(0, 1)    # rand = random.SystemRandom().uniform(0, 1)
        for _ in range(1): # lower values increase speed and variation
            for candidate, _ in ballot_dict.items():
                if rand < preferences.get(candidate):
                    ballot_dict[candidate] += 1
        return ballot_dict
    
    def vote(self, profile):
        ballot_dict = self.decide_vote(self.config.voter_profiles[profile])
        pref_sorted = sortItems(ballot_dict)
        vote_cast = [k for k, v in pref_sorted if v > 0][:self.config.num_of_ballot_winners] #bulletvoting now supported
        return vote_cast

    def add_returns(self, ballot):
        for i in ballot:
            self.election_returns[i]+=1

    def people_decide(self, electorate_data):
        for party, party_proportion in electorate_data.items():
            num_votes = int(self.config.total_voters * float(party_proportion))
            for _ in range(num_votes):
                self.add_returns(self.vote(party))

    def one_election(self):    
        self.people_decide(self.config.electorate_data)
        returns_sorted = dict(sortItems(self.election_returns)[0:self.config.num_of_ballot_winners])
        winners = list(returns_sorted.keys())
        return winners