import { useState, useEffect } from 'react';
import configData from './config.json';
import './App.css';
import TextArea from './TextArea';
import ElectionSettingsInput from './ElectionSettingsInput';
import ElectorateInput from './ElectorateInput';
import VoterProfilesInput from './VoterProfilesInput';
import ResponseSection from './ResponseSection';

function App() {
    // Initial state
    
    const [response, setResponse] = useState(null);

    const [isSubmitted, setIsSubmitted] = useState(false);

    const loadFromLocalStorage = () => {
        try {
            const serializedData = localStorage.getItem('electionData');
            if (serializedData == null)
            return configData;
        return JSON.parse(serializedData);
        } catch (error){
            console.error("Failed to load from local storage", error);
            return configData;
        }
    }


    const saveToLocalStorage = (data) => {
        try {
            const serializedData = JSON.stringify(data);
            localStorage.setItem('electionData',serializedData);
        } catch (error) {
            console.error("Failed to save to local storage", error);
        }
    }

    const [data, setData] = useState(loadFromLocalStorage());

    useEffect(() => {
        saveToLocalStorage(data);
    }, [data]);


    const handleSubmit = async (event) => {
      event.preventDefault();
    //   const apiUrl = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000'; this breaks the fetch
  
      try {
        // const response = await fetch(`${apiUrl}/election`, { for setting environment variable
          const response = await fetch('http://10.0.0.132:8000/election', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify(data)
          });
  
          const responseData = await response.json();
          setResponse(responseData);
          console.log('Successful fetch'); 
          setIsSubmitted(true);
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
    }

    const resetToDefaults = () => {
        setData(configData);
        localStorage.removeItem('electionData');

  };
  
//   Rendering Logic
    return (
        <>
            <h1>UA Election Predictor</h1>
            {!isSubmitted ? (
            <form onSubmit={handleSubmit}>
                <button type="button" onClick={resetToDefaults}>Reset to Default Values</button>
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
                <ElectorateInput data={data} setData={setData}/>

            {/* ElectionSettingsInput component */}
                <ElectionSettingsInput 
                    data={data} 
                    updateNestedObject={updateNestedObject}
                    maxBallotWinners = {numCandidates - 1}
                />

                <button type="submit">Submit</button>
            </form>
            ) : (
            // ResponseSection component
            <>
            {response && <ResponseSection responseData={response} />}
            <button onClick={() => setIsSubmitted(false)}>New form</button>
            </>
            )}
        </>
    );
}

export default App;
