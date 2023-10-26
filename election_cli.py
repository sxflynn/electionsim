from election import ElectionSimulator
import time

def run():
    startTime = time.time()
    election_simulator = ElectionSimulator("config.json")
    winsSorted = election_simulator.runElections()
    election_simulator.printWinnters(winsSorted)
    stopWatch = time.time() - startTime
    election_simulator.printTime(stopWatch)

if __name__ == "__main__":
    run()
