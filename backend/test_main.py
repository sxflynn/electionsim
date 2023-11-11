from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

request_data = {
    "candidates":[
        "Jenny McKenna",
        "Lori Trent",
        "Glen Dugger",
        "Ruth Edmonds",
        "Sumia Mohamed",
        "Liz Stump"
    ],
    "voterProfiles":{
        "Democrats":{"Jenny McKenna": 0.60, "Lori Trent": 0.40, "Glen Dugger":0.05, "Ruth Edmonds":0.05, "Sumia Mohamed":0.85, "Liz Stump":0.85},
        "Independents":{"Jenny McKenna": 0.90, "Lori Trent": 0.75, "Glen Dugger":0.30, "Ruth Edmonds":0.10, "Sumia Mohamed":0.45, "Liz Stump":0.45},
        "Republicans":{"Jenny McKenna": 0.25, "Lori Trent": 0.45, "Glen Dugger":0.95, "Ruth Edmonds":0.90, "Sumia Mohamed":0.05, "Liz Stump":0.05}
    },
    "electorate":{
        "Democrats":{"size":0.46,"percentStrictPreference":0.20},
        "Independents":{"size":0.15,"percentStrictPreference":0.40},
        "Republicans":{"size":0.39,"percentStrictPreference":0.90}
    },
    "electionSettings":{
        "numOfSims": 100,
        "totalVoters":100,
        "ballotWinners":3,
        "SystemRandom":False,
        "StrictPreferenceVoting":False
    },
    "message":"This feature is unused."
}


def test_multielection():

    # Sending a POST request to the /election endpoint
    response = client.post("/election", json=request_data)

    # Asserting the response status code
    assert response.status_code == 200, "Response status code should be 200"

    # Parsing response data
    response_data = response.json()
    assert "datetime" in response_data, "Response should have a 'datetime' field"
    assert "candidates" in response_data, "Response should have a 'candidates' field"
    assert isinstance(response_data["candidates"], dict), "'candidates' should be a dictionary"

    # More detailed checks can be added here, for example:
    # Asserting the structure and type of each key in the response
    assert "voterProfiles" in response_data, "Response should contain 'voterProfiles'"
    assert "electorate" in response_data, "Response should contain 'electorate'"
    assert "electionSettings" in response_data, "Response should contain 'electionSettings'"
    
    # Asserting the structure of nested data
    assert isinstance(response_data["electionSettings"], dict), "'electionSettings' should be a dictionary"

def test_response_status_code():
    response = client.post("/election", json=request_data)
    assert response.status_code == 200, "Response status code should be 200"

def test_response_contains_datetime():
    response = client.post("/election", json=request_data)
    assert "datetime" in response.json(), "Response should have a 'datetime' field"

def test_response_contains_candidates():
    response = client.post("/election", json=request_data)
    assert "candidates" in response.json(), "Response should have a 'candidates' field"

def test_candidates_type():
    response = client.post("/election", json=request_data)
    assert isinstance(response.json()["candidates"], dict), "'candidates' should be a dictionary"

def test_election_response_structure():
    response = client.post("/election", json=request_data)
    assert response.status_code == 200

    data = response.json()
    assert "datetime" in data
    assert isinstance(data["datetime"], str)
    assert "candidates" in data
    assert isinstance(data["candidates"], dict)

    # Checking structure of 'candidates'
    for name, details in data["candidates"].items():
        assert "numberOfWins" in details
        assert isinstance(details["numberOfWins"], int)
        assert "probabilityToWin" in details
        assert isinstance(details["probabilityToWin"], str)

def test_one_election_response_structure():
    response = client.post("/one_election", json=request_data)
    assert response.status_code == 200

    data = response.json()
    assert "datetime" in data and isinstance(data["datetime"], str)
    assert "results" in data and isinstance(data["results"], dict)

    # Check structure of 'results'
    for candidate, votes in data["results"].items():
        assert isinstance(votes, int)