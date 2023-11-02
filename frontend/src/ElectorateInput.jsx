import NumberInput from './NumberInput';

function ElectorateInput({ data, setData }) {
    return (
        <div>
            <h2>Electorate</h2>
            <table>
                <thead>
                    <tr>
                        <th>Party</th>
                        <th>Size</th>
                    </tr>
                </thead>
                <tbody>
                    {Object.entries(data.electorate).map(([party, value]) => (
                        <tr key={party}>
                            <td>{party}</td>
                            <td>
                                <NumberInput
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
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default ElectorateInput;
