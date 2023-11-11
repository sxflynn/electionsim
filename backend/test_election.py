import pytest
import time
import sys
import random
from unittest.mock import patch
from election import ElectionSimulator, Election
from election_config import ConfigFile


@pytest.fixture
def simulator():
    config = ConfigFile("config.json")
    simulator = ElectionSimulator(config.config_data)
    simulator.config.electionSettings.numOfSims = 10
    simulator.config.electionSettings.totalVoters = 100
    return simulator

def test_add_wins(simulator):
    election_results = ['Jenny McKenna', 'Liz Stump', 'Sumia Mohamed']
    simulator.add_wins(election_results)
    assert simulator.election_wins['Jenny McKenna'] == 1
    assert simulator.election_wins['Liz Stump'] == 1
    assert simulator.election_wins['Sumia Mohamed'] == 1
    assert simulator.election_wins['Ruth Edmonds'] == 0
    assert simulator.election_wins['Lori Trent'] == 0
    assert simulator.election_wins['Glen Dugger'] == 0
    
def test_run_elections(simulator):
    result = simulator.run_elections()
    assert isinstance(result,list)
    assert all(isinstance(item, tuple) for item in result)
    result_candidates = [candidate for candidate, _ in result]
    for candidate in simulator.config.candidates:
        assert candidate in result_candidates

@pytest.fixture
def one_election():
    config = ConfigFile("config.json")
    election = Election(config.config_data)
    election.config.electionSettings.totalVoters = 100
    return election

def test_election_start(one_election):
    assert one_election

def test_decide_vote(one_election):
    preferences = {'Jenny McKenna': 0.6, 'Lori Trent': 0.4, 'Glen Dugger': 0.05, 'Ruth Edmonds': 0.05, 'Sumia Mohamed': 0.99, 'Liz Stump': 0.99}
    ballot_dict = one_election.decide_vote(preferences)
    assert any(vote_count > 0 for vote_count in ballot_dict.values()), "At least one candidate should have more than 0 votes"
    
def test_vote_democrats_no_strict_returns_full_ballot(one_election):
    profile = 'Democrats'
    one_election.config.electionSettings.StrictPreferenceVoting = False
    with patch('random.uniform', return_value=0.5): #force random to be 0.5
        vote_cast = one_election.vote(profile)
        assert len(vote_cast) == one_election.config.electionSettings.ballotWinners
    
def test_vote_democrats_strict_returns_smaller_ballot(one_election):
    one_election.config.voterProfiles['Democrats'] = {'Jenny McKenna': 0.01, 'Lori Trent': 0.01, 'Glen Dugger': 0.01, 'Ruth Edmonds': 0.01, 'Sumia Mohamed': 0.99, 'Liz Stump': 0.99}
    num_of_winners = one_election.config.electionSettings.ballotWinners
    profile = 'Democrats'
    one_election.config.electionSettings.StrictPreferenceVoting = True
    one_election.config.electorate['Democrats']['percentStrictPreference'] = 0.99
    with patch('random.uniform', return_value=0.5): #force random to be 0.5
        vote_cast = one_election.vote(profile)
        assert len(vote_cast) < num_of_winners
    
def test_vote_democrats_strict_empty_ballot_returns_full_ballot(one_election):
    one_election.config.voterProfiles['Democrats'] = {'Jenny McKenna': 0.01, 'Lori Trent': 0.01, 'Glen Dugger': 0.01, 'Ruth Edmonds': 0.01, 'Sumia Mohamed': 0.01, 'Liz Stump': 0.01}
    num_of_winners = one_election.config.electionSettings.ballotWinners
    profile = 'Democrats'
    one_election.config.electionSettings.StrictPreferenceVoting = True
    one_election.config.electorate['Democrats']['percentStrictPreference'] = 0.99
    with patch('random.uniform', return_value=0.5): #force random to be 0.5
        vote_cast = one_election.vote(profile)
        assert len(vote_cast) == num_of_winners
    

def test_add_returns(one_election):
    ballot = ['Jenny McKenna', 'Liz Stump', 'Lori Trent']
    returns = {'Jenny McKenna': 1, 'Lori Trent': 1, 'Glen Dugger': 0, 'Ruth Edmonds': 0, 'Sumia Mohamed': 0, 'Liz Stump': 1}
    one_election.add_returns(ballot)
    assert one_election.election_returns == returns
    
def test_people_decide(one_election):
    electorate = one_election.config.electorate
    one_election.people_decide(electorate)
    total_votes = sum(one_election.election_returns.values())
    # assert total_votes == one_election.config.electionSettings.totalVoters
    