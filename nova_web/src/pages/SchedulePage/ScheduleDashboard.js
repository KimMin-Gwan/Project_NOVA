import React from 'react';
import './style.css'; // Corrected import for CSS file
import vertical_line from './vertical_line.svg'; // Corrected import for SVG file
import EventComponent from './EventComponent'; // Corrected import for EventComponent`
import ScheduleTopic from '../../component/ScheduleTopic/ScheduleTopic';
import TimeChart from './TimeChart';

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


const tempScheduleData= [
    {   
        timeblocks: [
            {
                time : 0,
                start : 60,
                length : 180
            }
        ],
        schedule_detail : "저스트 채팅 짧방",
        bias_name : "도롱챠",
        color_code : "#FFC871"
    },
    {
        timeblocks: [
            {
                time : 0,
                start : 60,
                length : 300
            },
            {
                time : 1,
                start : 0,
                length : 360,
            },
            {
                time : 2,
                start : 0,
                length : 360,
            }
        ],
        schedule_detail : "런칭 하려는 날",
        bias_name : "김민관",
        color_code : "#B171FF"
    },
    {
        timeblocks: [
            {
                time : 1,
                start : 120,
                length : 120,
            },
        ],
        schedule_detail : "사무실 가는날",
        bias_name : "잠을못자",
        color_code : "#9CF6AA"
    },
    {
        timeblocks: [
            {
                time : 0,
                start : 240,
                length : 120 
            },
            {
                time : 1,
                start : 0,
                length : 120 
            }
        ],
        schedule_detail : "원펀맨 같이보기",
        bias_name : "허니츄러스",
        color_code : "#71C4FF"
    },
    {
        timeblocks: [
            {
                time : 0,
                start : 60,
                length :240
            }
        ],
        schedule_detail : "원딜 연습하는 날",
        bias_name : "아리사 Arisa",
        color_code : "#71FFCD"
    },
    {
        timeblocks: [
            {
                time : 0,
                start : 300,
                length : 60
            },
            {
                time : 1,
                start : 0,
                length :300 
            }
        ],
        schedule_detail : "생일 특별 방송!",
        bias_name : "허니츄러스",
        color_code : "#71D9FF"
    },
    {
        timeblocks: [
            {
                time : 0,
                start : 0,
                length :240 
            }
        ],
        schedule_detail : "행복한 합방 같은거 합니다요",
        bias_name : "다주",
        color_code : "#FFF371"
    },
]

const tempWeekDayData = [
    {
        date: 10,
        day: "월",
        num_schedule: 1
    },
    {
        date: 11,
        day: "화",
        num_schedule: 2
    },
    {
        date: 12,
        day: "수",
        num_schedule: 1
    },
    {
        date: 13,
        day: "목",
        num_schedule: 1
    },
    {
        date: 14,
        day: "금",
        num_schedule: 1
    },
    {
        date: 15,
        day: "토",
        num_schedule: 1
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
                {/* 타임차트를 만드는 핵심 구간 */}
                <TimeChart tempWeekDayData={tempWeekDayData} tempScheduleData={tempScheduleData} />
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
