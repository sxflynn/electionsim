import NumberInput from "./NumberInput";

function VoterProfiles({voterProfilesData, candidates, updateNestedObject}){

    return (

    <div>
    <h2>Voter Profiles</h2>
                {Object.entries(voterProfilesData).map(([party, profiles]) => (
                    <div key={party}>
                        <h3>{party}</h3>
                        {candidates.map(candidate => (
                            <div key={candidate}>
                                {/* NumberInput component */}  
                                <NumberInput 
                                    label={candidate} value={profiles[candidate] || ''} min="0" max="1" step="0.01"
                                    onChange={e => updateNestedObject(
                                        ['voterProfiles', party, candidate],
                                         parseFloat(e.target.value))
                                        }
                                    />
                            </div>
                        ))}
                    </div>
                ))}
    </div>

    )

}


export default VoterProfiles;