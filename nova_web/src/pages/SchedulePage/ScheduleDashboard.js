import React from "react";
import "./style.css"; // Corrected import for CSS file
import vertical_line from "./vertical_line.svg"; // Corrected import for SVG file
import EventComponent from "./EventComponent"; // Corrected import for EventComponent`
import ScheduleTopic from "../../component/ScheduleTopic/ScheduleTopic";
import { useNavigate } from "react-router-dom";
import TimeChart from "./TimeChart";
import {
  tempWeekDayData,
  tempScheduleData,
  mockData,
} from "../../pages/SchedulePage/TestScheduleData";

const ScheduleDashboard = () => {
  const navigate = useNavigate();
  const handleNavigate = (path) => {
    navigate(`${path}`);
  };
  return (
    <div className="container">
      <div className="section-box">
        <div className="dashboard-section">
          <div className="section-title">
            <p className="element">
              <span className="text-wrapper">25년 2월 </span>
              <span className="span">3주차</span>
            </p>
          </div>
          <div className="my-dashboard">
            <div className="left-group">
              <span>선택중인 주제</span>
              <span className="num-bias">4</span>
              <span>개</span>
            </div>
            <div className="right-group">
              <button onClick={() => handleNavigate("/search/topic")}>
                주제 탐색
              </button>
              <img src={vertical_line} alt="vertical line" />
              <button>일정 등록</button>
            </div>
          </div>
        </div>
        <div className="dashboard-section">
          <div className="section-title">
            <p className="element">
              <span className="text-wrapper">예정된 이벤트</span>
            </p>
          </div>
          <div className="my-dashboard">
            <div className="day-tittle">
              <span>오늘</span>
            </div>
            <div className="event-list">
              <EventComponent />
              <EventComponent />
              <EventComponent />
            </div>
          </div>
        </div>
      </div>
      <div className="section-line"></div>
      <div className="section-box">
        <div className="dashboard-section">
          <div className="section-title">
            <p className="element">
              <span className="text-wrapper">타임 차트</span>
            </p>
          </div>
        </div>
        {/* 타임차트를 만드는 핵심 구간 */}
        <TimeChart
          tempWeekDayData={tempWeekDayData}
          tempScheduleData={tempScheduleData}
        />
      </div>
      <div className="section-line"></div>
      <div className="section-box">
        <div className="dashboard-section">
          <div className="section-title">
            <p className="element">
              <span className="text-wrapper">이런 최애는 어때요?</span>
            </p>
          </div>
        </div>
        {mockData.map((item, i) => {
          return <ScheduleTopic key={item.id} {...item} />;
        })}
      </div>
    </div>
  );
};

export default ScheduleDashboard;
