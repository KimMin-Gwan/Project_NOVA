import "./index.css";

export default function ScheduleTopic({ name, job, tag, platform, time }) {
  return (
    <div className="ScheduleTopic">
      <div>
        <h3>{name}</h3>
        <div>{platform}</div>
        <div>{job}</div>
        <div>{tag}</div>
        <div>{time}</div>
      </div>

      <div className="bias_img">img</div>
    </div>
  );
}
