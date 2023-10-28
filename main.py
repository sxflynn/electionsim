from typing import Union
import time
from fastapi import FastAPI
from election_config import Config, ConfigFile, ElectionResponse, CandidateWin, ElectionSettings
from election import Election, ElectionSimulator

app = FastAPI()


@app.post("/election", response_model=ElectionResponse)
def main(config: Config):
    election_simulator = ElectionSimulator(config)
    wins_sorted = election_simulator.run_elections()
    candidates_dict = {}    
    for candidate, wins in wins_sorted:
        probability_to_win = (wins / config.electionSettings.numOfSims) * 100
        candidates_dict[candidate] = {
            "numberOfWins": wins,
            "probabilityToWin": f"{probability_to_win:.1f}%"
        }
    datetime_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    election_settings = ElectionSettings(
        numOfSims=config.electionSettings.numOfSims,
        totalVoters=config.electionSettings.totalVoters,
        ballotWinners=config.electionSettings.ballotWinners
    )
    response_data = {
        "datetime": datetime_str,
        "candidates": candidates_dict,
        "voterProfiles": config.voterProfiles,
        "electorate": config.electorate,
        "electionSettings": election_settings
    }
    election_response = ElectionResponse(**response_data)
    return election_response