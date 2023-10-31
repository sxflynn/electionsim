import { useState } from 'react';
import configData from './config.json';
import './App.css';
import TextArea from './TextArea';
import NumberInput from './NumberInput';
import ElectionSettings from './ElectionSettings';
import Electorate from './Electorate';
import VoterProfiles from './VoterProfiles';

function App() {
    // Initial state
    const [data, setData] = useState(configData);
  
    const [response, setResponse] = useState(null);

    const handleSubmit = async (event) => {
      event.preventDefault();
    //   const apiUrl = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000'; this breaks the fetch
  
      try {
        // const response = await fetch(`${apiUrl}/election`, { for setting environment variable
          const response = await fetch('http://127.0.0.1:8000/election', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify(data)
          });
  
          const responseData = await response.json();
          setResponse(responseData);
          console.log('Successful fetch'); 
      } catch (error) {
          console.error('Error making POST request:', error);
      }
  };
  const numCandidates = data.candidates.length;
  const candidatesValue = data.candidates.join('\n');
  const handleCandidatesChange = (e) => {
    // Updating the candidates in state based on the TextArea value
    setData({
      ...data,
      candidates: e.target.value.split('\n'),
    });
  };

  const updateNestedObject = (path, value) => {
    setData(prevData => {
      // Create a deep clone of the previous state
      const updatedData = JSON.parse(JSON.stringify(prevData));
  
      // Use reduce to navigate to the deepest object
      path.slice(0, -1).reduce((obj, key) => obj[key], updatedData)[path.slice(-1)[0]] = value;
  
      return updatedData;
    });
  };
  
    return (
        <>
            <h1>UA Election Predictor</h1>

            <form onSubmit={handleSubmit}>
                <h2>Candidates</h2>
                {/* TextArea component */}
                <TextArea value={candidatesValue} onChange={handleCandidatesChange} />

                {/* VoterProfiles component */}
                <VoterProfiles 
                    voterProfilesData = {data.voterProfiles}
                    candidates = {data.candidates}
                    updateNestedObject={updateNestedObject}
                    />

                {/* Electorate component */}
                <Electorate data={data} setData={setData}/>;

                {/* ElectionSettings component */}
                <ElectionSettings 
                    data={data} 
                    updateNestedObject={updateNestedObject}
                    maxBallotWinners = {numCandidates - 1}
                />

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
