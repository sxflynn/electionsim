import pytest
import time
import sys
import random
from election import ElectionSimulator, Election
from election_config import ConfigFile


@pytest.fixture
def election_simulator():
    config = ConfigFile("config.json")
    simulator = ElectionSimulator(config.config_data)
    simulator.config.electionSettings.numOfSims = 10
    simulator.config.electionSettings.totalVoters = 100
    return simulator

def test_add_wins(election_simulator):
    election_results = ['Jenny McKenna', 'Liz Stump', 'Sumia Mohamed']
    election_simulator.add_wins(election_results)
    assert election_simulator.election_wins['Jenny McKenna'] == 1
    assert election_simulator.election_wins['Liz Stump'] == 1
    assert election_simulator.election_wins['Sumia Mohamed'] == 1
    assert election_simulator.election_wins['Ruth Edmonds'] == 0
    