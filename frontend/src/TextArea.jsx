function TextArea({value, onChange, setIsEdited}){

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