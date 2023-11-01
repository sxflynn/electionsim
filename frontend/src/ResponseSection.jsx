function ResponseSection({ responseData }) {
    // const [showDetails, setShowDetails] = useState(false);

    return (
        <div className="response-section">
            <h2>Prediction Results</h2>

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
        </div>
    );
}

export default ResponseSection;
