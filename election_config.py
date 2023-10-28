import json
from typing import Dict, List
from pydantic import BaseModel

#Pydantic models
class ElectionSettings(BaseModel):
    numOfSims: int
    totalVoters: int
    ballotWinners: int

class Config(BaseModel):
    candidates: List[str]
    voterProfiles: Dict[str, Dict[str, float]]
    electorate: Dict[str, float]
    electionSettings: ElectionSettings
    message: str

class ConfigFile:
    def __init__(self, config_file=None, json_object=None):
        self.config_data = None
        if config_file:
            self.load_config_from_file(config_file)
        elif json_object:
            self.load_config_from_json(json_object)

    def load_config_from_file(self, config_file):
        try:
            with open(config_file, 'r', encoding="utf-8") as jsonFile:
                json_object = json.load(jsonFile)
                self.config_data = Config(**json_object)  # Using Pydantic model for validation
        except json.JSONDecodeError:
            print("Failed to load config data")
        except FileNotFoundError:
            print("The config.json file does not exist.")
        except IOError:
            print("An IOError occurred while reading the file.")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

    def load_config_from_json(self, json_object):
        try:
            self.config_data = Config(**json_object)  # Using Pydantic model for validation
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")