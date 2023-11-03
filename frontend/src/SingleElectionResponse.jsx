function SingleElectionResponse({responseData, isEdited}){

    const totalVotes = Object.values(responseData.results).reduce((accumulator, votes) => accumulator + votes, 0);

    return(
        <div className="response-section">
        <h2>{isEdited ? "Your Simulated Election Results" : "Simulated Election Results"}</h2>

            <h3>Turnout: {responseData.electionSettings.totalVoters} voters</h3>
            <table>
                <thead>
                    <tr>
                        <th>Candidate</th>
                        <th>Votes</th>
                        <th>Percentage</th>
                    </tr>
                </thead>
                <tbody>
                    {Object.entries(responseData.results).map(([name, votes]) => (
                        <tr key={name}>
                            <td>{name}</td>
                            <td>{votes}</td>
                            <td>{((votes / totalVotes) * 100).toFixed(2)}%</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>


    );

}

export default SingleElectionResponse;