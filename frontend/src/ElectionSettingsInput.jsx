import NumberInput from './NumberInput';

function ElectionSettingsInput({ data, updateNestedObject, maxBallotWinners }) {
    return (
      <div>
        <h2>Election Settings</h2>
        <table>
            <tbody>
                <tr><td>Number of Simulations</td><td>
                    <NumberInput 
                        value={data.electionSettings.numOfSims}
                        min={1}
                        max={1000}
                        onChange={(e) => updateNestedObject(['electionSettings', 'numOfSims'], parseInt(e.target.value, 10))}
                    />
                </td></tr>
                <tr><td>Number of voters</td><td>
                    <NumberInput 
                        value={data.electionSettings.totalVoters}
                        min={100}
                        max={1000}
                        onChange={(e) => updateNestedObject(['electionSettings', 'totalVoters'], parseInt(e.target.value, 10))}
                    />
                </td></tr>
                <tr><td>Number of winners</td><td>
                    <NumberInput 
                        value={data.electionSettings.ballotWinners}
                        min={1}
                        max={maxBallotWinners}
                        onChange={(e) => updateNestedObject(['electionSettings', 'ballotWinners'], parseInt(e.target.value, 10))}
                    />
                </td></tr>
            </tbody>
        </table>
      </div>
    );
}

export default ElectionSettingsInput;
