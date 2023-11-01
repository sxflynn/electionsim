import MultiElectionResponse from "./MultiElectionResponse";
import SingleElectionResponse from "./SingleElectionResponse";

function ResponseSection({ responseData, predictionType }) {
    // const [showDetails, setShowDetails] = useState(false);

    return (
        <>
        {predictionType === 'multi' && <MultiElectionResponse responseData={responseData} />}
        {predictionType === 'single' && <SingleElectionResponse responseData={responseData} />}
        </>
        
    );
}

export default ResponseSection;
