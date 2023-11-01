import NumberInput from './NumberInput';
function ElectionSettingsInput({ data, updateNestedObject, maxBallotWinners }) {
    return (
      <div>
        <h2>Election Settings</h2>
        <div>
        <NumberInput 
          label="Number of Simulations"
          value={data.electionSettings.numOfSims}
          min = {1}
          max = {1000}
          onChange={(e) => updateNestedObject(['electionSettings', 'numOfSims'], parseInt(e.target.value, 10))}
        />
        </div>
        <>
        <NumberInput 
          label="Total Voters"
          value={data.electionSettings.totalVoters}
          min = {100}
          max = {1000}
          onChange={(e) => updateNestedObject(['electionSettings', 'totalVoters'], parseInt(e.target.value, 10))}
        />
        </>
        <div>
        <NumberInput 
          label="Ballot Winners"
          value={data.electionSettings.ballotWinners}
          min = {1}
          max = {maxBallotWinners}
          onChange={(e) => updateNestedObject(['electionSettings', 'ballotWinners'], parseInt(e.target.value, 10))}
        />
        </div>
      </div>
    );
  }
  

export default ElectionSettingsInput;
