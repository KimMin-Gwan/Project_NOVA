import "../button/button.css";
export default function Button({ text, onClick }) {
  return (
    <div>
      <button onClick={onClick}>{text}</button>
    </div>
  );
}
