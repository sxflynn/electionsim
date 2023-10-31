import { useState } from 'react';
import configData from './config.json';
import './App.css';
import TextArea from './TextArea';
import ElectionSettingsInput from './ElectionSettingsInput';
import ElectorateInput from './ElectorateInput';
import VoterProfilesInput from './VoterProfilesInput';
import ResponseSection from './ResponseSection';

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

            {/* VoterProfilesInput component */}
                <VoterProfilesInput 
                    voterProfilesData = {data.voterProfiles}
                    candidates = {data.candidates}
                    updateNestedObject={updateNestedObject}
                    />

            {/* ElectorateInput component */}
                <ElectorateInput data={data} setData={setData}/>;

            {/* ElectionSettingsInput component */}
                <ElectionSettingsInput 
                    data={data} 
                    updateNestedObject={updateNestedObject}
                    maxBallotWinners = {numCandidates - 1}
                />

                <button type="submit">Submit</button>
            </form>

            {/* ResponseSection component */}
            {response && <ResponseSection responseData={response} />}

        </>
    );
}

export default App;
