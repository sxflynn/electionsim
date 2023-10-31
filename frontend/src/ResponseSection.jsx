function ResponseSection({ responseData }) {
    return (
        <div className="response-section">
            <h2>Simulation Results</h2>

            <p><strong>Datetime:</strong> {responseData.datetime}</p>

            <h3>Candidate Results</h3>
            <table>
                <thead>
                    <tr>
                        <th>Candidate</th>
                        <th>Number of Wins</th>
                        <th>Probability to Win</th>
                    </tr>
                </thead>
                <tbody>
                    {Object.entries(responseData.candidates).map(([name, results]) => (
                        <tr key={name}>
                            <td>{name}</td>
                            <td>{results.numberOfWins}</td>
                            <td>{results.probabilityToWin}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
            
            <h3>Voter Profiles</h3>
            {Object.entries(responseData.voterProfiles).map(([party, profiles]) => (
                <div key={party}>
                    <h4>{party}</h4>
                    <ul>
                        {Object.entries(profiles).map(([candidate, value]) => (
                            <li key={candidate}>
                                {candidate}: {value.toFixed(2)}
                            </li>
                        ))}
                    </ul>
                </div>
            ))}
            
            <h3>Electorate</h3>
            <ul>
                {Object.entries(responseData.electorate).map(([party, value]) => (
                    <li key={party}>
                        {party}: {value.toFixed(2)}
                    </li>
                ))}
            </ul>
            
            <h3>Election Settings</h3>
            <ul>
                <li>Number of Simulations: {responseData.electionSettings.numOfSims}</li>
                <li>Total Voters: {responseData.electionSettings.totalVoters}</li>
                <li>Ballot Winners: {responseData.electionSettings.ballotWinners}</li>
            </ul>
        </div>
    );
}

export default ResponseSection;
