function NumberInput({ label, value, onChange }) {
    return (
      <label>
        {label}
        <input
          type="number"
          value={value}
          onChange={onChange}
          min="0"
          max="1"
          step="0.01"
        />
      </label>
    );
  }
  
  export default NumberInput;