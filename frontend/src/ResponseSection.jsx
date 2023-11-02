import MultiElectionResponse from "./MultiElectionResponse";
import SingleElectionResponse from "./SingleElectionResponse";

function ResponseSection({ responseData, predictionType }) {
    // const [showDetails, setShowDetails] = useState(false);

    return (
        <>
        {predictionType === 'multi' && <MultiElectionResponse responseData={responseData} />}
        {predictionType === 'single' && <SingleElectionResponse responseData={responseData} />}
        <p><strong>Datetime:</strong> {responseData.datetime}</p>
        </>
        
    );
}

export default ResponseSection;
