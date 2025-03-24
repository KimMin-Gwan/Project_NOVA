import EventComponent from "./EventComponent.jsx";
import "./style.css";
import vertical_line from "./../../img/vertical_line.svg";
import ScheduleTopic from "../../component/ScheduleTopic/ScheduleTopic.js";
import { useNavigate } from "react-router-dom";
import React, { useEffect, useState } from "react";
import TimeChart from "./TimeChart/TimeChart.jsx";
import Header from "../../component/Header/Header.js";

import mainApi from "../../services/apis/mainApi.js";
import NavBar from "../../component/NavBar/NavBar.js";
import { MakeSingleSchedule } from "../../component/EventMore/EventMore.js";

const ScheduleDashboard = () => {
  const navigate = useNavigate();

  const [makeScheduleModal, setMakeScheduleModal] = useState(false);

  // 일정 추가하기 버튼 누르면 동작하는애
  const toggleMakeScheduleModal = (target) => {
    setMakeScheduleModal((makeScheduleModal) => !makeScheduleModal);
  };

  let [weekDayData, setWeekDayData] = useState([]);
  let [scheduleData, setScheduleData] = useState([]);
  //let [eventData, setEventData] = useState([]);

  let [targetMonth, setTargetMonth] = useState("00년 00월");
  let [targetWeek, setTargetWeek] = useState("0주차");
  let [numBias, setNumBias] = useState(0);

  let [biasData, setBiasData] = useState([]);

  const [pageIndex, setPageIndex] = useState(0);
  const [todayDate, setTodayDate] = useState(new Date());

  const onChangeIndex = (param) => {
    const index = pageIndex + param;
    setPageIndex(index);

    const targetDate = new Date(todayDate); // 기존 날짜 복사
    const daysToAdd = index * 7; // 일수를 계산
    targetDate.setDate(targetDate.getDate() + daysToAdd); // 날짜를 계산
    setTodayDate(targetDate);
  };

  const brightMode = "brigthMode";

  // 네비게이션 함수
  const handleNavigate = (path) => {
    navigate(`${path}`);
  };

  // 주간 날짜 받기
  function fetchTargetMonthWeek(date) {
    mainApi.get(`time_table_server/try_get_dashboard_data?date=${date}`).then((res) => {
      setTargetMonth(res.data.body.target_month);
      setTargetWeek(res.data.body.target_week);
      setNumBias(res.data.body.num_bias);
    });
  }

  // 시간 차트 데이터 받기
  function fetchTimeChartData(date) {
    mainApi.get(`time_table_server/try_get_today_time_chart?date=${date}`).then((res) => {
      setScheduleData(res.data.body.schedule_blocks);
      setWeekDayData(res.data.body.week_day_datas);
    });
  }

  // 추천 주제 데이터 받기
  function fetchBiasData() {
    mainApi.get("time_table_server/try_get_recommended_bias_list").then((res) => {
      setBiasData(res.data.body.biases);
    });
  }

  useEffect(() => {
    const dateString = todayDate.toISOString().split('T')[0]; // 'YYYY-MM-DD' 형식으로 변환
    fetchTargetMonthWeek(dateString);
    fetchTimeChartData(dateString);
  }, [todayDate]);


  useEffect(() => {
    fetchBiasData();
    const dateString = todayDate.toISOString().split('T')[0]; // 'YYYY-MM-DD' 형식으로 변환
    fetchTargetMonthWeek(dateString);
    fetchTimeChartData(dateString);
  }, []);

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
                <button onClick={() => handleNavigate("/schedule/my_schedule")}>내 일정</button>
                <img src={vertical_line} alt="vertical line" />
                <button onClick={()=>toggleMakeScheduleModal()}>일정 등록</button>
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
              <span className="add-schedule" onClick={() => handleNavigate("/search/topic")}>
                주제 탐색
              </span>
            </div>
          </div>
          {biasData.map((item, i) => {
            return <ScheduleTopic key={i} {...item} />;
          })}
        </div>
      </div>
      <NavBar brightMode={brightMode} />


      <MakeSingleSchedule
        closeSchedule={toggleMakeScheduleModal}
        isOpen={makeScheduleModal}
      />

    </div>
  );
};

export default ScheduleDashboard;

//  // 오늘짜 이벤트 데이터 받아오고
//// 이것도 나중에 오늘 말고 내일, 이틀 후 사흘 후 이런걸로 해야될 듯
//function fetchEventData() {
//mainApi.get("time_table_server/try_get_event_board_data").then((res) => {
//setEventData(res.data.body.schedule_events);
//});
//}
