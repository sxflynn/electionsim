import MultiElectionResponse from "./MultiElectionResponse";
import SingleElectionResponse from "./SingleElectionResponse";

function ResponseSection({ responseData, predictionType, isEdited }) {
    // const [showDetails, setShowDetails] = useState(false);

    return (
        <>
        {predictionType === 'multi' && <MultiElectionResponse responseData={responseData} isEdited = {isEdited}/>}
        {predictionType === 'single' && <SingleElectionResponse responseData={responseData} isEdited = {isEdited} />}
        <p><strong>Datetime:</strong> {responseData.datetime}</p>
        </>
        
    );
}

export default ResponseSection;
