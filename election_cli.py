import time
from election import ElectionSimulator
from election_config import ConfigFile

def run():
    start_time = time.time()
    config = ConfigFile("config.json")
    election_simulator = ElectionSimulator(config)
    wins_sorted = election_simulator.runElections()
    election_simulator.print_winners(wins_sorted)
    stop_watch = time.time() - start_time
    election_simulator.print_time(stop_watch)

if __name__ == "__main__":
    run()
