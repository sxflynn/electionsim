import json

# Open the JSON file for reading
with open('config.json', 'r') as electionFile:
    # Parse JSON data
    jsonObject = json.load(electionFile)

candidates = jsonObject['candidates']

numOfBallotWinners = jsonObject['ballotWinners']

numOfVoterProfiles = len(jsonObject['voterProfiles'])

for numOfVoterProfiles
