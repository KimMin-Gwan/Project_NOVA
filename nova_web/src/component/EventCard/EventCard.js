import "./index.css";

export default function EventCard({ name, topic, date }) {
  return (
    <div className="EventCard">
      <div>
        <div>{name}</div>
        <div>{topic}</div>
        <div>{date}</div>
      </div>
    </div>
  );
}
