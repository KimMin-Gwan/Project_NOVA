import React from 'react';
import './style.css'; // Corrected import for CSS file
import vertical_line from './vertical_line.svg'; // Corrected import for SVG file
import EventComponent from './EventComponent'; // Corrected import for EventComponent`
import arrow_drop_left from './Arrow_drop_left.svg'; // Corrected import for SVG file
import arrow_drop_right from './Arrow_drop_right.svg'; // Corrected import for SVG file
import TimeWeekComponent from './TImeWeekComponent';
import ChartScheduleComponent from './ChartScheduleComponent';
import ScheduleTopic from '../../component/ScheduleTopic/ScheduleTopic';

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

const timeSectionList = [
    ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00"],
    ["06:00", "07:00", "08:00", "09:00", "10:00", "11:00"],
    ["12:00", "13:00", "14:00", "15:00", "16:00", "17:00"],
    ["18:00", "19:00", "20:00", "21:00", "22:00", "23:00"],
]

const tempScheduleData= [
    {
        schedule_detail : "저스트 채팅 짧방",
        bias_name : "도롱챠",
        start : 60,
        length : 180,
        color_code : "#FFC871"
    },
    {
        schedule_detail : "런칭 하려는 날",
        bias_name : "김민관",
        start : 60,
        length : 300,
        color_code : "#B171FF"
    },
    {
        schedule_detail : "원펀맨 같이보기",
        bias_name : "허니츄러스",
        start : 240,
        length : 120,
        color_code : "#71C4FF"
    },
    {
        schedule_detail : "원딜 연습하는 날",
        bias_name : "아리사 Arisa",
        start : 60,
        length : 240,
        color_code : "#71FFCD"
    },
    {
        schedule_detail : "생일 특별 방송!",
        bias_name : "허니츄러스",
        start : 240,
        length : 120,
        color_code : "#71D9FF"
    },
    {
        schedule_detail : "행복한 합방 같은거 합니다요",
        bias_name : "다주",
        start : 0,
        length : 240,
        color_code : "#FFF371"
    },
]

const tempWeekDayData = [
    {
        date: 10,
        day: "월",
        num_shedule: 1
    },
    {
        date: 11,
        day: "화",
        num_shedule: 1
    },
    {
        date: 12,
        day: "수",
        num_shedule: 1
    },
    {
        date: 13,
        day: "목",
        num_shedule: 1
    },
    {
        date: 14,
        day: "금",
        num_shedule: 1
    },
    {
        date: 15,
        day: "토",
        num_shedule: 1
    }
]



const ScheduleDashboard = () => {
    return (
        <div className="container">
            <div className='section-box'>
                <div className='dashboard-section'>
                    <div className='section-title'>
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
                            <span>주제 탐색</span>
                            <img src={vertical_line} alt="vertical line" />
                            <span>일정 등록</span>
                        </div>
                    </div>
                </div>
                <div className='dashboard-section'>
                    <div className='section-title'>
                        <p className="element">
                            <span className="text-wrapper">예정된 이벤트</span>
                        </p>
                    </div>
                    <div className="my-dashboard">
                        <div className='day-tittle'>
                            <span >오늘</span>
                        </div>
                        <div className='event-list'>
                            <EventComponent/>
                            <EventComponent/>
                            <EventComponent/>
                        </div>
                    </div>
                </div>
            </div>
            <div className='section-line'></div>
            <div className='section-box'>
                <div className='dashboard-section'>
                    <div className='section-title'>
                        <p className="element">
                            <span className="text-wrapper">타임 차트</span>
                        </p>
                    </div>
                </div>
                <div className="time-chart-box">
                    <div className='day-week-list'>
                        <div className='chart-etc-box'> </div>
                        <div>
                            {tempWeekDayData.map((item, i) => {
                                return <TimeWeekComponent key={item.id} {...item} />;
                            })}
                        </div>
                    </div>
                    <div className='chart-box'>
                        <div className='time-select-box'>
                            <img src={arrow_drop_left} alt="vertical line" />
                            <span> 오전 타임 </span>
                            <img src={arrow_drop_right} alt="vertical line" />
                        </div>
                        <div  className='time-line-box'>
                            {timeSectionList[0].map((time, i) => {
                                return <span key={i}>{time}</span>
                            })}
                        </div>
                        <div className='schedule-box-list'>
                            {tempScheduleData.map((item, i) => {
                                return <ChartScheduleComponent key={item.id} {...item} />;
                            })}
                        </div>
                    </div>
                </div>
            </div>
            <div className='section-line'></div>
            <div className='section-box'>
                <div className='dashboard-section'>
                    <div className='section-title'>
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
