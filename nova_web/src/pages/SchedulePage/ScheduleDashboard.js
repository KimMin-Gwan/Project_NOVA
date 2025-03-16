import "./style.css"; // Corrected import for CSS file
import vertical_line from "./vertical_line.svg"; // Corrected import for SVG file
import EventComponent from "./EventComponent"; // Corrected import for EventComponent`
import ScheduleTopic from "../../component/ScheduleTopic/ScheduleTopic";
import { useNavigate } from "react-router-dom";
import React, { useEffect, useRef, useState } from "react";
import TimeChart from "./TimeChart";
import {
  tempWeekDayData,
  tempScheduleData,
  mockData,
} from "../../pages/SchedulePage/TestScheduleData";
import mainApi from "../../services/apis/mainApi";

const ScheduleDashboard = () => {
  let [weekDayData, setWeekDayData] = useState([]);
  let [scheduleData, setScheduleData] = useState([]);
  let [eventData, setEventData] = useState([]);

  let [targetMonth, setTargetMonth] = useState("00년 00월")
  let [targetWeek, setTargetWeek] = useState("0주차")
  let [numBias, setNumBias] = useState(0)

  let [biasData, setBiasData] = useState([])

  // 목표 날짜를 받아오고
  function fetchTargetMonthWeek() {
    mainApi.get("time_table_server/try_get_dashboard_data").then((res) => {
      setTargetMonth(res.data.body.target_month);
      setTargetWeek(res.data.body.target_week);
      setNumBias(res.data.body.num_bias);
    });
  }

  // 오늘짜 이벤트 데이터 받아오고
  // 이것도 나중에 오늘 말고 내일, 이틀 후 사흘 후 이런걸로 해야될 듯
  function fetchEventData() {
    mainApi.get("time_table_server/try_get_event_board_data").then((res) => {
      setEventData(res.data.body.schedule_events);
    });
  }

  // 시간 차트 받아오고
  function fetchTimeChartData() {
    mainApi.get("time_table_server/try_get_today_time_chart").then((res) => {
      setScheduleData(res.data.body.schedule_blocks);
      setWeekDayData(res.data.body.week_day_datas);
    });
  }

  // 오늘짜 이벤트 데이터 받아오고
  // 이것도 나중에 오늘 말고 내일, 이틀 후 사흘 후 이런걸로 해야될 듯
  function fetchEventData() {
    mainApi.get("time_table_server/try_get_recommended_bias_list").then((res) => {
      setBiasData(res.data.body.biases);
    });
  }

  useEffect(() => {
    fetchTargetMonthWeek();
    fetchEventData();
    fetchTimeChartData();
  }, []);

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
              <span className="text-wrapper">{targetMonth} </span>
              <span className="span">{targetWeek}</span>
            </p>
          </div>
          <div className="my-dashboard">
            <div className="left-group">
              <span>선택중인 주제</span>
              <span className="num-bias">{numBias}</span>
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
              {eventData.length === 0 ? <span>오늘 일정 없음</span> : <span>오늘</span>}
            </div>
            <div className="event-list">
              {eventData.map((item, i) => {
                return <EventComponent key={item.id} {...item} />;
              })}
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
          tempWeekDayData={weekDayData}
          tempScheduleData={scheduleData}
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
        {timeChartData.map((item, i) => {
          return <ScheduleTopic key={item.id} {...item} />;
        })}
      </div>
    </div>
  );
};

export default ScheduleDashboard;
