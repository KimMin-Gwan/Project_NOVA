import EventCard from "../../component/EventCard/EventCard";
import ScheduleTopic from "../../component/ScheduleTopic/ScheduleTopic";

export default function SearchSchedulePage() {
  return (
    <div className="container">
      <ScheduleTopic />
      <EventCard />
    </div>
  );
}
