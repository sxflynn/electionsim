function NumberInput({ label, value, min, max, step, onChange }) {
    return (
      <label>
        {label}:
        <input
          type="number"
          value={value}
          min={min}
          max={max}
          step={step}
          onChange={onChange}
        />
      </label>
    );
  }
  
  export default NumberInput;  