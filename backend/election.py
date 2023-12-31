import random
import json
from typing import List, Tuple
from election_config import ConfigFile


#Utility functions
def sortItems(item_input):
    output_list = sorted(item_input.items(), key=lambda x: (x[1], random.random()), reverse=True) # tie-breaker
    return output_list

def sameList(list1, list2): #returns true if two lists are identical
        return set(list1) == set(list2)

class ElectionSimulator:
    def __init__(self, config: ConfigFile):
        self.config = config
        self.election_returns = {name: 0 for name in self.config.candidates}
        self.election_wins = {name: 0 for name in self.config.candidates}

    def add_wins(self, election_results):
        for i in election_results:
            for key, _ in self.election_wins.items():
                if key == i:
                    self.election_wins[key]+=1

    def run_elections(self) -> List[Tuple[str, int]]:
        """Class method will return a list of tuples like 
        [('Alice', 73), ('Bob', 70), ('Charlie', 35)]
        The string  represents the name of a candidate
        and the integer represents the number of wins that 
        candidate has over numOfSims simulations.

        :return: A list of tuples containing candidate names and win counts.
        :rtype: List[Tuple[str, int]]
        """
        for i in range(self.config.electionSettings.numOfSims):
            election = Election(self.config)
            self.add_wins(election.one_election()) #False means do not run as single election
        wins_sorted = sortItems(self.election_wins)
        return wins_sorted

    def print_time(self, systime):
        hours = int(systime // 3600)
        minutes = int(systime % 3600 // 60)
        seconds = int(systime % 60 // 1)
        milliseconds = int(systime % 1 * 1000)
        formatted_time = f"Running time {hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
        print(formatted_time)

class Election:
    def __init__(self, config: ConfigFile):
        self.config = config
        self.election_returns = {name: 0 for name in self.config.candidates}

    def decide_vote(self, preferences):
        ballot_dict = {name: 0 for name in self.config.candidates}
        rand = random.SystemRandom().uniform(0, 1)  # rand = random.uniform(0, 1)    # rand = random.SystemRandom().uniform(0, 1)
        for _ in range(1): # lower values increase speed and variation
            for candidate, _ in ballot_dict.items():
                if rand < preferences.get(candidate):
                    ballot_dict[candidate] += 1
        return ballot_dict
    
    def vote(self, profile):
        ballot_dict = self.decide_vote(self.config.voterProfiles[profile])
        pref_sorted = sortItems(ballot_dict)
        vote_cast = [k for k, v in pref_sorted if v > 0][:self.config.electionSettings.numOfSims] #bulletvoting now supported
        return vote_cast

    def add_returns(self, ballot):
        for i in ballot:
            self.election_returns[i]+=1

    def people_decide(self, electorate):
        for party, party_proportion in electorate.items():
            num_votes = int(self.config.electionSettings.totalVoters * float(party_proportion))
            for _ in range(num_votes):
                self.add_returns(self.vote(party))

    def one_election(self):    
        self.people_decide(self.config.electorate)
        returns_sorted = dict(sortItems(self.election_returns)[0:self.config.electionSettings.ballotWinners])
        winners = list(returns_sorted.keys())
        return winners