import time
from election import ElectionSimulator
from election_config import ConfigFile, ElectionResponse, CandidateWin, ElectionSettings

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
    election_simulator = ElectionSimulator(config)
    wins_sorted = election_simulator.run_elections()
    
    candidates_dict = {}    
    for candidate, wins in wins_sorted:
        probability_to_win = (wins / config.config_data.electionSettings.numOfSims) * 100
        candidates_dict[candidate] = {
            "numberOfWins": wins,
            "probabilityToWin": f"{probability_to_win:.1f}%"
        }

    datetime_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    election_settings = ElectionSettings(
        numOfSims=config.config_data.electionSettings.numOfSims,
        totalVoters=config.config_data.electionSettings.totalVoters,
        ballotWinners=config.config_data.electionSettings.ballotWinners
    )
    response_data = {
        "datetime": datetime_str,
        "candidates": candidates_dict,
        "voterProfiles": config.config_data.voterProfiles,
        "electorate": config.config_data.electorate,
        "electionSettings": election_settings
    }
    election_response = ElectionResponse(**response_data)

    response_json_str = election_response.model_dump_json()
    
    print_winners(config, wins_sorted)
    #print(response_json_str)
    
    stop_watch = time.time() - start_time
    print_time(stop_watch)

if __name__ == "__main__":
    run()
