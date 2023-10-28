import random
from datetime import datetime
import json


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
                    self.candidate_names = json_object["candidates"]
                    self.num_of_ballot_winners = json_object["electionSettings"]["ballotWinners"]
                    self.num_of_sims = json_object["electionSettings"]["numOfSims"]
                    self.total_voters = json_object["electionSettings"]["totalVoters"]
                    self.voter_profiles = json_object["voterProfiles"]
                    self.message = json_object["message"]
                    self.electorate_data = json_object["electorate"]
                    self.settings_data = json_object["electionSettings"]
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
        self.candidate_names = config.candidate_names
        self.num_of_ballot_winners = config.settings_data["ballotWinners"]
        self.num_of_sims = config.settings_data["numOfSims"]
        self.total_voters = config.settings_data["totalVoters"]
        self.voter_profiles = config.voter_profiles
        self.electorate_data = config.electorate_data
        self.settings_data = config.settings_data
        #self.message = config.message  #unimplemented
        self.election_returns = {}
        self.election_wins = {}
        self.ballotChoice = {}
        self.election_returns = {name: 0 for name in self.candidate_names}
        self.election_wins = {name: 0 for name in self.candidate_names}
        
    def add_wins(self, election_results):
        for i in election_results:
            for key, _ in self.election_wins.items():
                if key == i:
                    self.election_wins[key]+=1
        # self.election_returns = {name: 0 for name in self.candidate_names} # reinitialize the election_returns dict back to zeros for the next election

    def runElections(self):
        for i in range(self.num_of_sims):
            election = Election(
            self.candidate_names, 
            self.total_voters, 
            self.num_of_ballot_winners, 
            self.voter_profiles, 
            self.electorate_data
        )
            self.add_wins(election.one_election())
        wins_sorted = sortItems(self.election_wins)
        return wins_sorted

    def percent_display(self, num):
        percent_string = str(round(float(num/self.num_of_sims)*100, 1)) + "%"
        return percent_string

    def print_winners(self, input_list):
        for k, v in input_list:
            print(f"{k:<15} - {v:>3} - {self.percent_display(v):>8} chance of being elected.")

    def outputAsJson(self, winner_list):
        candidates = {}
        for name, num_of_wins in winner_list:
            candidates[name] = {
                "numberOfWins": num_of_wins,
                "probabilityToWin": self.percent_display(num_of_wins)
        }
        now = datetime.now()
        string_date = now.strftime("%d/%m/%Y %H:%M:%S")
        combined_json = {
            "timestamp": string_date,
            "electionSettings": self.settings_data,
            "candidates": candidates,
            "voter_profiles": self.voter_profiles,
            "electorate": self.electorate_data
        }
        print(json.dumps(combined_json, indent = 3))
    
    def print_time(self, systime):
        print(f"Running time {int(systime // 3600):02d}:{int(systime % 3600 // 60):02d}:{int(systime % 60 // 1):02d}.{int(systime % 1 * 1000):03d}")

    def check_election_json(self, json_data):    # Pydantic will make most of this unnecesary
        candidates = json_data.get("candidates", [])  # Extract candidates, voter profiles, and electorate data
        voter_profiles = json_data.get("voter_profiles", {})
        electorate = json_data.get("electorate", {})
        for _, profiles in voter_profiles.items(): # Check if candidates match the voter profiles
            if not sameList(candidates, profiles.keys()):
                print("The candidates list does not match the candidates in the voter profiles.")
                return False
        if not sameList(list(electorate.keys()), list(voter_profiles.keys())): # Check if parties in electorate match the voter profiles
            print("The parties listed in the electorate key do not match the parties in the voter profiles.")
            return False
        return True


class Election:
    def __init__(self, candidate_names, total_voters, num_of_ballot_winners, voter_profiles, electorate_data):
        self.candidate_names = candidate_names
        self.total_voters = total_voters
        self.num_of_ballot_winners = num_of_ballot_winners
        self.voter_profiles = voter_profiles
        self.electorate_data = electorate_data
        self.election_returns = {name: 0 for name in self.candidate_names}
        self.election_wins = {name: 0 for name in self.candidate_names}
        
    def decide_vote(self, preferences):
        ballot_dict = {name: 0 for name in self.candidate_names}
        rand = random.SystemRandom().uniform(0, 1)  # rand = random.uniform(0, 1)    # rand = random.SystemRandom().uniform(0, 1)
        for _ in range(1): # lower values increase speed and variation
            for candidate, _ in ballot_dict.items():
                if rand < preferences.get(candidate):
                    ballot_dict[candidate] += 1
        return ballot_dict
    
    def vote(self, profile):
        ballot_dict = self.decide_vote(self.voter_profiles[profile])
        pref_sorted = sortItems(ballot_dict)
        vote_cast = [k for k, v in pref_sorted if v > 0][:self.num_of_ballot_winners] #bulletvoting now supported
        return vote_cast

    def add_returns(self, ballot):
        for i in ballot:
            self.election_returns[i]+=1

    def people_decide(self, electorate_data):
        for party, party_proportion in electorate_data.items():
            num_votes = int(self.total_voters * float(party_proportion))
            for _ in range(num_votes):
                self.add_returns(self.vote(party))

    def one_election(self):    
        self.people_decide(self.electorate_data)
        returns_sorted = dict(sortItems(self.election_returns)[0:self.num_of_ballot_winners])
        winners = list(returns_sorted.keys())
        return winners