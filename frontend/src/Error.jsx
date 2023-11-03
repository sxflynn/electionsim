

function Error({error,onDismiss}){

return (
    <div>
        {error && (
            <div className="error-message">
                {error}
                <button onClick={onDismiss} className="dismiss-error-btn">X</button>
            </div>
        )}
    </div>
);
}

export default Error;