function TextArea({value, onChange}){

    return (
        <textarea 
        rows ="10"
        value = {value}
        onChange={onChange}
        placeholder = "Enter candidates, one per line"
        />
    );

}

export default TextArea;