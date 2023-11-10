import { useState, useEffect } from 'react';
import configData from './config.json';
import './App.css';
import TextArea from './TextArea';
import ElectionSettingsInput from './ElectionSettingsInput';
import ElectorateInput from './ElectorateInput';
import VoterProfilesInput from './VoterProfilesInput';
import ResponseSection from './ResponseSection';
import Loading from './Loading';
import { randomizeData } from './randomize';
import About from './About';
import Error from './Error';



function App() {
    // Initial state
    
    const [response, setResponse] = useState(null);
   
    const [isLoading, setIsLoading] = useState(false); //false

    const [isSubmitted, setIsSubmitted] = useState(false);

    const [isEdited, setIsEdited] = useState(false);

    const [predictionType, setPredictionType] = useState(''); // multi or single

    const [showAbout, setShowAbout] = useState(false);

    const [error, setError] = useState(null);


    const loadFromLocalStorage = () => {
        try {
            const serializedData = localStorage.getItem('electionData');
            if (serializedData == null)
            return configData;
        return JSON.parse(serializedData);
        } catch (error){
            console.error("Failed to load from local storage", error);
            setError("Failed to load from local storage");
            return configData;
        }
    }


    const saveToLocalStorage = (data) => {
        try {
            const serializedData = JSON.stringify(data);
            localStorage.setItem('electionData',serializedData);
        } catch (error) {
            console.error("Failed to save to local storage", error);
            setError("Failed to save to local storage");
        }
    }

    const [data, setData] = useState(loadFromLocalStorage());

    useEffect(() => {
        saveToLocalStorage(data);
    }, [data]);


    const performSimulation = async () => {

        console.log('Load submit animation');
    //   const apiUrl = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000'; this breaks the fetch
    
    let endpoint;

    if (predictionType === 'single') {
        endpoint = '/one_election';
        console.log('single election');
    } else if (predictionType === 'multi') {
        endpoint = '/election';
        console.log('multi election');
    }
  
      try {
        // const response = await fetch(`${apiUrl}/election`, { for setting environment variable
        if (predictionType === 'single') {
            endpoint = '/one_election';
            console.log('single election');
        } else if (predictionType === 'multi') {
            endpoint = '/election';
            console.log('multi election');
        }

        // const response = await fetch(`https://fastapi-staging.fly.dev${endpoint}`, {
        const response = await fetch(`http://localhost:8000${endpoint}`, {
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
          setError('Error making POST request. Please try again.');
      }
      setIsLoading(false);
      console.log('Loading state ended');

    }



    const handleSubmit = async (event) => {
      event.preventDefault();
      setIsLoading(true);
      performSimulation();
  };
  const numCandidates = data.candidates.length;
  const candidatesValue = data.candidates.join('\n');
  const handleCandidatesChange = (e) => {
    // Updating the candidates in state based on the TextArea value
    setData({
      ...data,
      candidates: e.target.value.split('\n'),
    });
    setIsEdited(true);
  };

  const updateNestedObject = (path, value) => {
    setData(prevData => {
      // Create a deep clone of the previous state
      const updatedData = JSON.parse(JSON.stringify(prevData));
  
      // Use reduce to navigate to the deepest object
      path.slice(0, -1).reduce((obj, key) => obj[key], updatedData)[path.slice(-1)[0]] = value;
        
      return updatedData;
    });
    setIsEdited(true);
    console.log("Values edited")
    }

    const resetToDefaults = () => {
        setData(configData);
        localStorage.removeItem('electionData');
        setIsEdited(false);
        console.log("Edited set to false");

  };
  
//   Rendering Logic
    return (
        <>
            <div className="navbar">
                <div><a href = "/"><img src="/bearicon.svg" alt="Bear Icon" className="website-icon" /></a></div>
                <div><a href="/about" onClick={(e) => { e.preventDefault(); setShowAbout(!showAbout); }}>About</a></div>
                <div><a href = "https://github.com/sxflynn/electionsim">GitHub Source</a></div>
                <div><a href = "https://github.com/sxflynn">Contact</a></div>
            </div>

            {error && <Error error={error} onDismiss={() => setError(null)} />}

            {showAbout && <About onClose={() => setShowAbout(false)} />}



            

            <h1 className="reduced-padding">Ballot Bear</h1>
            <h2 className="h2-italics">Simulate local election results</h2>
            
            {!isSubmitted ? (
                
            <form onSubmit={handleSubmit}>
                
                <button className={`app-button ${isLoading ? 'loading' : ''}`} type="submit" disabled={isLoading} onClick={() => setPredictionType('multi')}>Simulate Multiple Elections</button>
                <button className={`app-button ${isLoading ? 'loading' : ''}`} type="submit" disabled={isLoading} onClick={() => setPredictionType('single')}>Simulate One Election</button>
                <div>{isLoading && <Loading/>}</div>
                <h2>Candidates</h2>
                
                
            {/* TextArea component */}
                <TextArea value={candidatesValue} onChange={handleCandidatesChange} setIsEdited={setIsEdited} />
            
            {/* VoterProfilesInput component */}
                <VoterProfilesInput 
                    voterProfilesData = {data.voterProfiles}
                    candidates = {data.candidates}
                    updateNestedObject={updateNestedObject}
                    setIsEdited={setIsEdited}
                    />

            {/* ElectorateInput component */}
                <ElectorateInput data={data} setData={setData} setIsEdited={setIsEdited}/>

            {/* ElectionSettingsInput component */}
                <ElectionSettingsInput 
                    data={data} 
                    updateNestedObject={updateNestedObject}
                    maxBallotWinners = {numCandidates - 1}
                    setIsEdited={setIsEdited}
                />
             
             <button className="app-button" type="button" onClick={resetToDefaults}>Reset to Default Values</button>
             <button className="app-button" type="button" onClick={() => randomizeData(configData, setData, setIsEdited)}>Randomize</button>
             
             <div>Created by <a href ="https://www.linkedin.com/in/sxflynn/">Stephen Flynn</a></div>
            </form>
            ) : (
            // ResponseSection component
            <>
            {response && <ResponseSection responseData={response} predictionType={predictionType} isEdited={isEdited} />}
            <button className="app-button" onClick={() => setIsSubmitted(false)}>Edit numbers</button>
            <button className={`app-button ${isLoading ? 'loading' : ''}`} disabled={isLoading} onClick={() => {setIsLoading(true);performSimulation();}}>Simulate again</button>
            <div>{isLoading && <Loading/>}</div>
            
            </>
            )}
            
        </>
    );
}

export default App;
