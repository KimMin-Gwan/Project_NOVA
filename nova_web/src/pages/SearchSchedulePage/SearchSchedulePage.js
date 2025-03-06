import EventCard from "../../component/EventCard/EventCard";
import ScheduleTopic from "../../component/ScheduleTopic/ScheduleTopic";
import "./index.css";
import search_icon from "./../../img/search_icon.png";
const mockData = [
  {
    id: 0,
    name: "한결",
    job: "인터넷 방송인",
    platform: "SOOP",
    tag: ["버추얼", "노래", "신입"],
    time: ["저녁", "새벽"],
  },
  {
    id: 1,
    name: "한결1",
    job: "인터넷 방송인",
    platform: "SOOP",
    tag: ["버추얼", "노래", "신입"],
    time: ["저녁", "새벽"],
  },
  {
    id: 2,
    name: "한결2",
    job: "인터넷 방송인",
    platform: "SOOP",
    tag: ["버추얼", "노래", "신입"],
    time: ["저녁", "새벽"],
  },
];

const eventData = [
  {
    id: 0,
    name: "한결 3월 1주차 방송 스케줄",
    topic: "한결",
    date: "25년 03월 01일",
  },
  {
    id: 1,
    name: "플레이브 미니 3집",
    topic: "플레이브",
    date: "25년 03월 01일",
  },
  {
    id: 2,
    name: "한결 3월 1주차 방송 스케줄",
    topic: "한결1",
    date: "25년 03월 01일",
  },
];

export default function SearchSchedulePage() {
  return (
    <div className="container SearchSchedulePage">
      <div className="Search_section">
        <div className="section_top">
          <div>일정 탐색</div>
          <button>일정 등록</button>
        </div>
        <div className={"search-fac"}>
          <div className={"search-box"}>
            <input
              type="text"
              //   onKeyDown={onKeyDown}
              //   value={searchBias}
              //   onChange={(e) => {
              //     onChangeSearchBias(e);
              //   }}
              placeholder="팔로우 하고 싶은 주제를 검색해보세요"
            />
            <img
              src={search_icon}
              // onClick={fetchSearchBias}
              alt="검색바"
            />
          </div>
        </div>
      </div>
      {mockData.map((item, i) => {
        return <ScheduleTopic key={item.id} {...item} />;
      })}
      {eventData.map((event, i) => {
        return <EventCard key={event.id} {...event} />;
      })}
    </div>
  );
}
