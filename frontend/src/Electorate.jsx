import NumberInput from './NumberInput';

function Electorate({ data, setData }) {
    return (
        <div>
            <h2>Electorate</h2>
            {Object.entries(data.electorate).map(([party, value]) => (
                <div key={party}>
                    <NumberInput
                        label={party}
                        value={value}
                        min={0}
                        max={1}
                        step={0.01}
                        onChange={e => setData(prev => {
                            let updatedElectorate = {...prev.electorate};
                            updatedElectorate[party] = parseFloat(e.target.value);
                            return {
                                ...prev,
                                electorate: updatedElectorate
                            };
                        })}
                    />
                </div>
            ))}
        </div>
    );
}

export default Electorate;
