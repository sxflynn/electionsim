import NumberInput from './NumberInput';

function ElectorateInput({ data, setData, setIsEdited }) {

    const handleElectorateChange = (party, key, value) => {
        setData(prevData => ({
            ...prevData,
            electorate: {
                ...prevData.electorate,
                [party]: {
                    ...prevData.electorate[party],
                    [key]: parseFloat(value)
                }
            }
        }));
        setIsEdited(true);
    };

    return (
        <div>
            <h2>Electorate</h2>
            <table>
                <thead>
                    <tr>
                        <th>Party</th>
                        <th>Size</th>
                        <th>Percent Strict Preference</th>
                    </tr>
                </thead>
                <tbody>
                    {Object.entries(data.electorate).map(([party, values]) => (
                        <tr key={party}>
                            <td>{party}</td>
                            <td>
                                <NumberInput
                                    value={values.size}
                                    min={0}
                                    max={1}
                                    step={0.01}
                                    onChange={e => handleElectorateChange(party, 'size', e.target.value)}
                                />
                            </td>
                            <td>
                                <NumberInput
                                    value={values.percentStrictPreference}
                                    min={0}
                                    max={1}
                                    step={0.01}
                                    onChange={e => handleElectorateChange(party, 'percentStrictPreference', e.target.value)}
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
