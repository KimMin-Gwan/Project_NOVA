import "./style.css";
import vertical_line from "./../../img/vertical_line.svg";
import EventComponent from "./EventComponent.jsx";
import ScheduleTopic from "../../component/ScheduleTopic/ScheduleTopic.js";
import { useNavigate } from "react-router-dom";
import React, { useEffect, useState } from "react";
import TimeChart from "./TimeChart/TimeChart.jsx";
import Header from "../../component/Header/Header.js";

import mainApi from "../../services/apis/mainApi.js";
import NavBar from "../../component/NavBar/NavBar.js";

const ScheduleDashboard = () => {
  let [weekDayData, setWeekDayData] = useState([]);
  let [scheduleData, setScheduleData] = useState([]);
  //let [eventData, setEventData] = useState([]);

  let [targetMonth, setTargetMonth] = useState("00년 00월");
  let [targetWeek, setTargetWeek] = useState("0주차");
  let [numBias, setNumBias] = useState(0);

  let [biasData, setBiasData] = useState([]);

  const brightMode = "brigthMode";

  // 목표 날짜를 받아오고
  function fetchTargetMonthWeek() {
    mainApi.get("time_table_server/try_get_dashboard_data").then((res) => {
      setTargetMonth(res.data.body.target_month);
      setTargetWeek(res.data.body.target_week);
      setNumBias(res.data.body.num_bias);
    });
  }

  //  // 오늘짜 이벤트 데이터 받아오고
  //// 이것도 나중에 오늘 말고 내일, 이틀 후 사흘 후 이런걸로 해야될 듯
  //function fetchEventData() {
  //mainApi.get("time_table_server/try_get_event_board_data").then((res) => {
  //setEventData(res.data.body.schedule_events);
  //});
  //}

  // 시간 차트 받아오고
  function fetchTimeChartData() {
    mainApi.get("time_table_server/try_get_today_time_chart").then((res) => {
      setScheduleData(res.data.body.schedule_blocks);
      setWeekDayData(res.data.body.week_day_datas);
    });
  }

  // 오늘짜 이벤트 데이터 받아오고
  // 이것도 나중에 오늘 말고 내일, 이틀 후 사흘 후 이런걸로 해야될 듯
  function fetchBiasData() {
    mainApi.get("time_table_server/try_get_recommended_bias_list").then((res) => {
      setBiasData(res.data.body.biases);
    });
  }

  useEffect(() => {
    fetchTargetMonthWeek();
    //fetchEventData();
    fetchBiasData();
    fetchTimeChartData();
  }, []);

  const navigate = useNavigate();
  const handleNavigate = (path) => {
    navigate(`${path}`);
  };

  return (
    <div className="container">
      <div className="body-box">
        <Header />

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
                <button onClick={() => handleNavigate("/search/topic")}>주제 탐색</button>
                <img src={vertical_line} alt="vertical line" />
                <button>일정 등록</button>
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
              <span className="add-schedule" onClick={() => handleNavigate("/search/schedule")}>
                일정 탐색
              </span>
            </div>
          </div>
          {/* 타임차트를 만드는 핵심 구간 */}
          <TimeChart weekDayData={weekDayData} scheduleData={scheduleData} />
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
          {biasData.map((item, i) => {
            return <ScheduleTopic key={i} {...item} />;
          })}
        </div>
      </div>
      <NavBar brightMode={brightMode}></NavBar>
    </div>
  );
};

export default ScheduleDashboard;
