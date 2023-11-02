function MultiElectionResponse({responseData}){


    return(
        <div className="response-section">
            <h2>Data from {responseData.electionSettings.numOfSims} elections simulations</h2>
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
        </div>


    );

}

export default MultiElectionResponse;