import NumberInput from "./NumberInput";

function VoterProfilesInput({ voterProfilesData, candidates, updateNestedObject }) {
    return (
        <div>
            <h2>Voter Profiles</h2>
            {Object.entries(voterProfilesData).map(([party, profiles]) => (
                <div key={party}>
                    <h3>{party}</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Candidate</th>
                                <th>Probability</th>
                            </tr>
                        </thead>
                        <tbody>
                            {candidates.map(candidate => (
                                <tr key={candidate}>
                                    <td>{candidate}</td>
                                    <td>
                                        <NumberInput
                                            value={profiles[candidate] || ''} 
                                            min="0" 
                                            max="1" 
                                            step="0.01"
                                            onChange={e => updateNestedObject(
                                                ['voterProfiles', party, candidate],
                                                parseFloat(e.target.value))
                                            }
                                        />
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            ))}
        </div>
    );
}

export default VoterProfilesInput;
