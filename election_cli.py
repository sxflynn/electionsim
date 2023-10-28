import time
from election import ElectionSimulator
from election_config import Config, ConfigFile, ElectionResponse, CandidateWin, ElectionSettings

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


def run():
    start_time = time.time()
    config = ConfigFile("config.json")
    election_simulator = ElectionSimulator(config.config_data)
    wins_sorted = election_simulator.run_elections()
    print_winners(config, wins_sorted)
    stop_watch = time.time() - start_time
    print_time(stop_watch)

if __name__ == "__main__":
    run()
