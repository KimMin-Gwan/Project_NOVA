export default function Input({ id, type, value, onChange, placeholder, onFocus, onClick }) {
  return (
    <input
      id={id}
      type={type}
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      onFocus={onFocus}
      onClick={onClick}
    />
  );
}
