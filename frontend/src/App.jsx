import { useState } from 'react';
import configData from './config.json';
import './App.css';

function App() {
    // Initial state
    const [data, setData] = useState(configData);
  
    const [response, setResponse] = useState(null);

    const handleSubmit = async (event) => {
      event.preventDefault();
  
      try {
          const response = await fetch('http://127.0.0.1:8000/election', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify(data)
          });
  
          const responseData = await response.json();
          setResponse(responseData);
      } catch (error) {
          console.error('Error making POST request:', error);
      }
  };

    return (
        <>
            <h1>UA Election Predictor</h1>

            <form onSubmit={handleSubmit}>
                <h2>Candidates</h2>
                <textarea rows = "7"
                    value={data.candidates.join('\n')}
                    onChange={(e) => setData({
                        ...data,
                        candidates: e.target.value.split('\n')
                    })}
                    placeholder="Enter candidates, one per line"
                />

                <h2>Voter Profiles</h2>
                {Object.entries(data.voterProfiles).map(([party, profiles]) => (
                    <div key={party}>
                        <h3>{party}</h3>
                        {data.candidates.map(candidate => (
                            <div key={candidate}>
                                <label>
                                    {candidate}:
                                    <input
                                        type="number"
                                        min="0"
                                        max="1"
                                        step="0.01"
                                        value={profiles[candidate] || ''}
                                        onChange={e => setData(prev => {
                                            let updatedProfiles = {...prev.voterProfiles};
                                            updatedProfiles[party][candidate] = parseFloat(e.target.value);
                                            return {
                                                ...prev,
                                                voterProfiles: updatedProfiles
                                            };
                                        })}
                                    />
                                </label>
                            </div>
                        ))}
                    </div>
                ))}

                <h2>Electorate</h2>
                {Object.entries(data.electorate).map(([party, value]) => (
                    <div key={party}>
                        <label>
                            {party}:
                            <input
                                type="number"
                                min="0"
                                max="1"
                                step="0.01"
                                value={value}
                                onChange={e => setData(prev => {
                                    let updatedElectorate = {...prev.electorate};
                                    updatedElectorate[party] = parseFloat(e.target.value);
                                    return {
                                        ...prev,
                                        electorate: updatedElectorate
                                    };
                                })}
                            />
                        </label>
                    </div>
                ))}

                <h2>Election Settings</h2>
                <div>
                    <label>
                        Number of Simulations:
                        <input
                            type="number"
                            value={data.electionSettings.numOfSims}
                            onChange={(e) => setData({
                                ...data,
                                electionSettings: {
                                    ...data.electionSettings,
                                    numOfSims: parseInt(e.target.value, 10)
                                }
                            })}
                        />
                    </label>
                </div>
                <div>
                    <label>
                        Total Voters:
                        <input
                            type="number"
                            value={data.electionSettings.totalVoters}
                            onChange={(e) => setData({
                                ...data,
                                electionSettings: {
                                    ...data.electionSettings,
                                    totalVoters: parseInt(e.target.value, 10)
                                }
                            })}
                        />
                    </label>
                </div>
                <div>
                    <label>
                        Ballot Winners:
                        <input
                            type="number"
                            value={data.electionSettings.ballotWinners}
                            onChange={(e) => setData({
                                ...data,
                                electionSettings: {
                                    ...data.electionSettings,
                                    ballotWinners: parseInt(e.target.value, 10)
                                }
                            })}
                        />
                    </label>
                </div>

                <button type="submit">Submit</button>
            </form>

            {response && (
    <div className="response-section">
        <h2>Simulation Results</h2>

        <p><strong>Datetime:</strong> {response.datetime}</p>

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
                {Object.entries(response.candidates).map(([name, results]) => (
                    <tr key={name}>
                        <td>{name}</td>
                        <td>{results.numberOfWins}</td>
                        <td>{results.probabilityToWin}</td>
                    </tr>
                ))}
            </tbody>
        </table>
        <h2>Election Settings</h2>
        <h3>Voter Profiles</h3>
        {Object.entries(response.voterProfiles).map(([party, profiles]) => (
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
            {Object.entries(response.electorate).map(([party, value]) => (
                <li key={party}>
                    {party}: {value.toFixed(2)}
                </li>
            ))}
        </ul>

        <h3>Election Settings</h3>
        <ul>
            <li>Number of Simulations: {response.electionSettings.numOfSims}</li>
            <li>Total Voters: {response.electionSettings.totalVoters}</li>
            <li>Ballot Winners: {response.electionSettings.ballotWinners}</li>
        </ul>
    </div>
)}

        </>
    );
}

export default App;
