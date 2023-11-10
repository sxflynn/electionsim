#debugging start
import uvicorn
#debugging end
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from election_config import Config, ElectionResponse, ElectionSettings, SingleElectionResponse
from election import ElectionSimulator, Election
import random




app = FastAPI()


# CORS middleware settings
origins = [
    "http://localhost:5173",  # Local development
    "http://127.0.0.1:5173",  # Alternative local development
    "https://staging.ballotbear.app",  # Staging domain
    "https://vercel.app",  # Vercel staging
    "https://ballotbear.app",  # Production domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/election", response_model=ElectionResponse)
def multielection(config: Config):
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
        ballotWinners=config.electionSettings.ballotWinners,
        SystemRandom=config.electionSettings.SystemRandom,
        StrictPreferenceVoting=config.electionSettings.StrictPreferenceVoting
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


@app.post("/one_election", response_model=SingleElectionResponse)
def singleelection(config: Config):
    config.electionSettings.totalVoters = random.randint(9000, 12000)
    election = Election(config)
    election.one_election()
    results = election.election_returns
    sorted_results = {k: v for k, v in sorted(results.items(), key=lambda item: item[1], reverse=True)}
    datetime_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    election_settings = ElectionSettings(
        numOfSims=config.electionSettings.numOfSims,
        totalVoters=config.electionSettings.totalVoters,
        ballotWinners=config.electionSettings.ballotWinners,
        SystemRandom=config.electionSettings.SystemRandom,
        StrictPreferenceVoting=config.electionSettings.StrictPreferenceVoting
    )
    response_data = {
        "datetime": datetime_str,
        "results": sorted_results,
        "voterProfiles": config.voterProfiles,
        "electorate": config.electorate,
        "electionSettings": election_settings
    }
    single_election_response = SingleElectionResponse(**response_data)
    return single_election_response

#debugging
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)