import time
import sys
import random
from election import ElectionSimulator, Election
from election_config import ConfigFile

#CLI utility functions
def percent_display(config, num):
    percent_string = str(round(float(num/config.config_data.electionSettings.numOfSims)*100, 1)) + "%"
    return percent_string

def print_winners(config, input_list):
    for k, v in input_list:
        print(f"{k:<15} - {v:>3} - {percent_display(config, v):>8} chance of being elected.")

def print_time(systime):
    hours = int(systime // 3600)
    minutes = int(systime % 3600 // 60)
    seconds = int(systime % 60 // 1)
    milliseconds = int(systime % 1 * 1000)
    formatted_time = f"Running time {hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
    print(formatted_time)

#single election run method
def run_one():
    start_time = time.time()
    config = ConfigFile("config.json")
    config.config_data.electionSettings.totalVoters = random.randint(9000, 12000) #override totalVoters for single election
    election = Election(config.config_data)
    election.one_election()
    results = election.election_returns
    print("strict_voters_by_party" + str(election.strict_voters_by_party))
    
    print("total_voters_by_party" + str(election.total_voters_by_party))
    print("total_candidates_voted_by_party" + str(election.total_candidates_voted_by_party))
    print("strict_voters_by_party" + str(election.strict_voters_by_party))
    print("percent_strict_voters_by_party" + str(election.percent_strict_voters_by_party))
    print("avg_candidates_per_ballot_by_party" + str(election.avg_candidates_per_ballot_by_party))
    
    
    print(str(results))
    stop_watch = time.time() - start_time
    print_time(stop_watch)

#election simulation run method
def run_multiple():
    start_time = time.time()
    config = ConfigFile("config.json")
    election_simulator = ElectionSimulator(config.config_data)
    wins_sorted = election_simulator.run_elections()
    print_winners(config, wins_sorted)
    stop_watch = time.time() - start_time
    print_time(stop_watch)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("Single argument provided. One election.")
        run_one()
    else:
        run_multiple()
