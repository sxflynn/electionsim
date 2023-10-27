from election import ElectionSimulator
from election import Config
import time

def run():
    startTime = time.time()
    config = Config("config.json")
    election_simulator = ElectionSimulator(config)
    winsSorted = election_simulator.runElections()
    election_simulator.printWinnters(winsSorted)
    stopWatch = time.time() - startTime
    election_simulator.printTime(stopWatch)

if __name__ == "__main__":
    run()
