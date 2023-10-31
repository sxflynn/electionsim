function TextArea({value, onChange}){

    return (
        <textarea 
        rows ="7"
        value = {value}
        onChange={onChange}
        placeholder = "Enter candidates, one per line"
        />
    );

}

export default TextArea;