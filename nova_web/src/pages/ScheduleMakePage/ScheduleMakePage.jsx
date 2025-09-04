import React, { useEffect, useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import style from "./ScheduleMakePage.module.css";
import useMediaQuery from "@mui/material/useMediaQuery";
import DesktopLayout from "../../component/DesktopLayout/DeskTopLayout.jsx";
import chzzklogo from "./chzzklogo_kor(Green).svg";

import { Swiper, SwiperSlide } from 'swiper/react';
import { FreeMode, Pagination } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/free-mode';
import 'swiper/css/pagination';

const ScheduleMakePage = () => {
    const isMobile = useMediaQuery('(max-width:1100px)');
    const navigate = useNavigate();
    const defaultDate = {
      year : "",
      month: "",
      day : ""
    }

    const [selectedBias, setSelectedBias] = useState("");
    const [selectedDate, setSelectedDate] = useState(defaultDate);

    const handleSelectBias = (bid) => {
        console.log(bid);
        if (selectedBias == bid){
            setSelectedBias("");
        }else{
            setSelectedBias(bid);
        }
    }

    const handleSelectDate = (date) => {
      if (
        date.year === selectedDate.year &&
        date.month === selectedDate.month &&
        date.day === selectedDate.day
      ) {
        setSelectedDate({ ...defaultDate }); // 새 객체로 초기화
      } else {
        setSelectedDate({ ...date }); // 새 객체로 설정
      }
    };


    const tempBiasList = [
        {
            bid: "1",
            bname: "도롱햄",
            platform: "chzzk"
        },
        {
            bid: "2",
            bname: "유콩콩",
            platform: "chzzk"
        },
        {
            bid: "3",
            bname: "쿠레나이 나츠키",
            platform: "chzzk"
        },
        {
            bid: "4",
            bname: "모아",
            platform: "chzzk"
        },
        {
            bid: "5",
            bname: "어다감?",
            platform: "chzzk"
        }
    ]

    if (!isMobile){
        return(
            <DesktopLayout>
                <div className={style["frame"]}>
                    <BiasSelectSection
                      biasList={tempBiasList}
                      selectedBias={selectedBias}
                      handleSelectBias={handleSelectBias}
                    />
                    <div 
                      className={style["desktop-section-wrapper"]}
                      style={{
                        height: selectedBias ? "960px" : "0px",
                      }}
                    >
                      <DesktopCalender 
                        // event={eventList}
                        selectedDate={selectedDate}
                        handleSelectDate={handleSelectDate}
                      />
                    </div>
                    <div 
                      className={style["desktop-section-wrapper"]}
                      style={{
                        height: selectedDate.day ? "800px" : "0px",
                      }}
                    >
                      <ScheduleSelectSection/>
                    </div>
                </div>
            </DesktopLayout>
        );
    }
}


const BiasSelectSection = ({ biasList,
     selectedBias, handleSelectBias 
    }) => {


    return (
        <div className={style["bias-select-section"]}>
            <span className={style["bias-select-section-title"]}>스트리머 선택</span>
            <div className={style["bias-selection-wrapper"]} >
                <Swiper
                    slidesPerView={3}
                    spaceBetween={30}
                    freeMode={true}
                    modules={[Pagination]}
                >
                    {biasList.map((bias) => (
                        <SwiperSlide
                                key={bias.bid}
                        >
                            <BiasComponent
                                bias={bias}
                                selectedBias={selectedBias}
                                handleSelectBias={handleSelectBias}
                            />
                        </SwiperSlide>
                    ))}
                </Swiper>
            </div>
        </div>
    );
};

const BiasComponent = ({
    bias,
    selectedBias, handleSelectBias
}) => {

    return(
        <div className={style["bias-component-wrapper"]}>
            <div className={style["bias-component"]}
                onClick={()=>handleSelectBias(bias.bid)}
                style={{ border: selectedBias == bias.bid ? "2px solid #8CFF99" : "2px solid #fff" }}
            >
                <div className={style["bias-image"]}></div>
                <div className={style["bias-detail-wrapper"]}>
                    <span className={style["bias-name"]}> {bias.bname}</span>
                    <img className={style["bias-platform-logo"]} src={chzzklogo}/>
                </div>
            </div>
            {
                selectedBias == bias.bid &&
                 <span className={style["bias-selected-span"]}> 선택 </span> 
            }
        </div>
    );
}



const DesktopCalender = ({
  selectedDate, handleSelectDate
}) => {
  const weekDays = ["일", "월", "화", "수", "목", "금", "토"];

  // 현재 년/월 상태
  const today = new Date();
  const [year, setYear] = useState(today.getFullYear());
  const [month, setMonth] = useState(today.getMonth() + 1); // JS는 0부터 시작 → +1
  const [weeks, setWeeks] = useState([]);
  const [day, setDay] = useState("");

  // 임시 일정 데이터
  const events = {
    1: "33원정대",
    2: "33원정대",
    3: "DK vs KT",
    4: "롤, 오버워치 시참 데이",
    8: "저챗 뱅",
    9: "발로란트",
    10: "카페탐방",
    12: "클립 이상..",
    15: "33원정대",
    16: "저챗 뱅",
    19: "롤 시참 데..",
  };

  // 달력 생성
  useEffect(() => {
    generateCalendar(year, month);
  }, [year, month]);

  const generateCalendar = (y, m) => {
    const firstDay = new Date(y, m - 1, 1).getDay(); // 시작 요일
    const lastDate = new Date(y, m, 0).getDate(); // 마지막 날짜

    const days = [];
    // 앞쪽 빈칸
    for (let i = 0; i < firstDay; i++) {
      days.push({ day: null });
    }
    // 날짜 채우기
    for (let d = 1; d <= lastDate; d++) {
      days.push({ day: d, body: events[d] });
    }
    // 뒤쪽 빈칸
    while (days.length % 7 !== 0) {
      days.push({ day: null });
    }

    // 7일 단위로 끊기
    const weekChunks = [];
    for (let i = 0; i < days.length; i += 7) {
      weekChunks.push(days.slice(i, i + 7));
    }

    setWeeks(weekChunks);
  };

  // 이전달 이동
  const handlePrevMonth = () => {
    if (month === 1) {
      setYear((prev) => prev - 1);
      setMonth(12);
    } else {
      setMonth((prev) => prev - 1);
    }
  };

  // 다음달 이동
  const handleNextMonth = () => {
    if (month === 12) {
      setYear((prev) => prev + 1);
      setMonth(1);
    } else {
      setMonth((prev) => prev + 1);
    }
  };

  const trySelectDay = (day) =>{
    setDay(day);
    handleSelectDate({ 
      year:year,
      month: month,
      day:day
    })
  }

  useEffect(()=>{
    handleSelectDate({ 
      year:year,
      month: month,
      day:day
    })
  },[year, month])

  return (
    <div>
      <div className={style["desktop-calendar-component"]}>
        <div className={style["calendar-wrapper"]}>
          {/* 헤더 */}
          <div className={style["calendar-header-wrapper"]}>
            <div className={style["month-select-button"]}onClick={handlePrevMonth}> 이전</div>
            <div className={style["calendar-header"]}>
              <span className={style["calendar-header-span"]}>
                {year}년 {month}월
              </span>
            </div>
            <div className={style["month-select-button"]}onClick={handleNextMonth}> 다음</div>
          </div>

          {/* 요일 헤더 */}
          <div className={style["weekday-wrapper"]}>
            {weekDays.map((day, idx) => (
              <WeekDayComponent key={idx} body={day} />
            ))}
          </div>

          {/* 주차별 */}
          {weeks.map((week, idx) => (
            <div key={idx} className={style["week-component"]}>
              {week.map((item, i) => (
                <DayComponent 
                key={i}
                day={item.day}
                body={item.body}
                dayState={day}
                trySelectDay={trySelectDay}
                />
              ))}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

const WeekDayComponent = ({ body }) => {
  const [color, setColor] = useState("transparent");

  useEffect(() => {
    if (body === "일") setColor("#FFD2D2");
    else if (body === "토") setColor("#D2FFD3");
    else{
      setColor("#fff");
    }
  }, [body]);

  return (
    <div
      className={style["week-day-component"]}
      style={{ backgroundColor: color }}
    >
      <span className={style["week-day-component-span"]}>{body}</span>
    </div>
  );
};

const DayComponent = ({ day, dayState, body, trySelectDay}) => {
  if (!day) {
    return <div className={style["day-component"]}></div>; // 빈칸
  }

  return (
    <div
      className={style["day-component"]}
      style={{
        justifyContent: body ? "space-between" : "center", 
        backgroundColor: day == dayState ? "#83b5ff" : "transparent"
        }}
      onClick={()=>trySelectDay(day)}
    >
      <span className={style["day-component-title-span"]}
        style={{fontSize: body ? "30px" : "42px"}}
      >{day}</span>
      {body && (
        <div className={style["day-component-body"]}>
          <span className={style["day-component-body-span"]}>{body}</span>
        </div>
      )}
    </div>
  );
};



const ScheduleSelectSection = () => {

  // 실제로 선택한 종료 시간
  const [timePickerValue, setTimePickerValue] = useState({
    hour: 0,
    minute: 0,
  });

  const sampleTags= ["게임", "저챗", "음악", "그림", "스포츠", "시참"];
  const [tagsInput, setTagsInput] = useState("");
  const [tagsArrayData, setTagsArrayData] = useState([]);

  const defaultSchedule = {
    sid : "",
    sname : "어떤데",
    tags : tagsArrayData,
    time : "",
    duration: ""
  }

  const [detailInput, setDetailInput] = useState("");
  const [scheduleDetail, setScheduleDetail] = useState(defaultSchedule);
  const [durationInput, setDurationInput] = useState("");

  const initEditTag = (tags) => {
    if (!Array.isArray(tags) || tags.length === 0) return; // 유효성 검사

    setTagsArrayData((prev) => {
      // 기존 태그와 병합 후 중복 제거
      const uniqueTags = Array.from(new Set([...prev, ...tags]));
      return uniqueTags;
    });

    setTagsInput((prevInput) => {
      // 기존 입력값과 병합 후 쉼표로 구분된 문자열 생성
      const updatedTags = prevInput ? `${prevInput}, ${tags.join(", ")}` : tags.join(", ");
      return updatedTags;
    });
  };

  const removeTag = (index) => {
    // 특정 태그 제거
    setTagsArrayData((prevTags) => {
      const updatedTags = prevTags.filter((_, i) => i !== index);

      // `tagsInput` 업데이트: 삭제된 태그를 제외한 나머지 태그를 쉼표로 결합
      setTagsInput(updatedTags.join(", "));
      return updatedTags;
    });
  };

  const addSampleTag = (tag) => {
    if (!tagsArrayData.includes(tag)) {
      // 중복 방지
      setTagsArrayData((prev) => [...prev, tag]);
      setTagsInput((prevInput) => (prevInput ? `${prevInput}, ${tag}` : tag));
    }
  };

  const onChangeTagsInput = (e) => {
    const value = e.target.value
    setTagsInput(value)

    // 공백 제거 .filter(item => item !== ""); // 빈 항목 제거
    const splitData = value.split(",").map(item => item.trim()) 
    setTagsArrayData(splitData)

    if (value == ""){
      setTagsArrayData([])
    }
  };

  // 스케줄 상세 바꾸기
  const onChangeDetailInput = (e) => {
    setDetailInput(e.target.value);
  };

  const onChangeDurationInput = (e) => {
    // 숫자만 허용
    const onlyNumbers = e.target.value.replace(/\D/g, "");
    setDurationInput(onlyNumbers);
  };

  const [selectedAmPm, setSelectedAmPm] = useState("am"); // 기본 선택
  // 높이 결정
  const height = selectedAmPm === "am" ? 40 : 120;

  const [hours, setHours] = useState(10);
  const [minutes, setMinutes] = useState(10);

  const intervalRef = useRef(null); // setInterval ID 저장

  // === 시간 함수 ===
  const changeHours = (delta) => {
    setHours(prev => {
      let next = (prev + delta) % 12;
      if (next === 0) next = 12; // 0이면 12로 변환

      // am/pm 전환 조건
      if ((prev === 12 && delta === 1) || (prev === 1 && delta === -1)) {
        setSelectedAmPm(prevAmPm => (prevAmPm === "am" ? "pm" : "am"));
      }

      return next;
    });
  };

  // === 분 함수 ===
  const changeMinutes = (delta) => {
    setMinutes(prev => (prev + delta + 60) % 60);
  };

  // === 버튼 눌렀을 때 반복 시작 ===
  const handleMouseDown = (type, delta) => {
    if (type === "hours") changeHours(delta);
    if (type === "minutes") changeMinutes(delta);

    intervalRef.current = setInterval(() => {
      if (type === "hours") changeHours(delta);
      if (type === "minutes") changeMinutes(delta);
    }, 150); // 150ms마다 반복
  };



  // === 버튼 뗄 때 반복 종료 ===
  const handleMouseUp = () => {
    clearInterval(intervalRef.current);
  };


  useEffect(()=>{
    initEditTag(scheduleDetail.tags);
  },[])

  return(
    <div className={style["schedule-select-section-frame"]}>
      <span className={style["bias-select-section-title"]}>콘텐츠 일정 작성 </span>
      <div className={style["schedule-detail-frame"]}>
        <div className={style["schedule-detail-input-wrapper"]}>
            <div className={style["searchFac"]}>
              <span>*이름</span>
              <div className={style["searchBoxMargin"]}>
                <div className={style["searchBox"]}>
                  <input
                    type="text"
                    value={detailInput}
                    onChange={onChangeDetailInput}
                    placeholder="일정의 이름"
                  />
                </div>
              </div>
            </div>

            <div className={style["searchFac"]}>
              <span>태그</span>
              <div className={style["sampleTagsContainer"]}>
                {sampleTags.map((tag, index) => (
                  <div
                    className={style["sampleTag"]}
                    key={index}
                    onClick={() => addSampleTag(tag)}
                  >
                    {tag}
                  </div>
                ))}
              </div>

              <div className={style["searchBoxMargin"]}>
                <div className={style["searchBox"]}>
                  <input
                    type="text"
                    value={tagsInput}
                    onChange={onChangeTagsInput}
                    placeholder="각 태그의 뒤에 쉼표를 입력하세요"
                  />
                </div>
              </div>

              <div className={style["tagsContainer"]}>
                {tagsArrayData.map((tag, index) => (
                    <div className={style["tag"]} key={index}>
                      {tag}
                      <button
                        className={style["removeButton"]}
                        onClick={() => removeTag(index)}
                      >
                        &times;
                      </button>
                    </div>
                  ))}
              </div>
            </div>
        </div>
        <div className={style["schedule-detail-time-selector-wrapper"]}>
          <div className={style["schedule-time-select-box"]}>
            {/* 시간 */}

            <div className={style["time-select-part-wrapper"]}
              style={{
                height: `${height}px`,
                transition: "height 0.3s ease" // 부드럽게 변화
              }}
            >
              <div className={style["time-select-part"]}
                onClick={() => setSelectedAmPm("pm")}
                style={{ color : selectedAmPm === "am" ? "#6C6C6C" : "#111" }}
              >
                am
              </div>
              <div className={style["time-select-part"]}
                onClick={() => setSelectedAmPm("am")}
                style={{ color : selectedAmPm === "pm" ? "#6C6C6C" : "#111" }}
              >
                pm
              </div>
            </div>

            <div className={style["time-select-button-wrapper"]}>
              <div
                className={style["time-select-button"]}
                onMouseDown={() => handleMouseDown("hours", 1)}
                onMouseUp={handleMouseUp}
                onMouseLeave={handleMouseUp}
              >+</div>
              <div className={style["time-select-intager"]}>{hours.toString().padStart(2, "0")}</div>
              <div
                className={style["time-select-button"]}
                onMouseDown={() => handleMouseDown("hours", -1)}
                onMouseUp={handleMouseUp}
                onMouseLeave={handleMouseUp}
              >-</div>
            </div>

            <div className={style["time-select-intager"]}>:</div>

            {/* 분 */}
            <div className={style["time-select-button-wrapper"]}>
              <div
                className={style["time-select-button"]}
                onMouseDown={() => handleMouseDown("minutes", 10)}
                onMouseUp={handleMouseUp}
                onMouseLeave={handleMouseUp}
              >+</div>
              <div className={style["time-select-intager"]}>{minutes.toString().padStart(2, "0")}</div>
              <div
                className={style["time-select-button"]}
                onMouseDown={() => handleMouseDown("minutes", -10)}
                onMouseUp={handleMouseUp}
                onMouseLeave={handleMouseUp}
              >-</div>
            </div>
          </div>

          <div className={style["searchFac"]}>
            <span>예상 방송 시간</span>
            <div className={style["searchBoxMargin"]}>
              <div className={style["searchBox"]}>
                <input
                  type="text"
                  value={durationInput ? durationInput + "시간" : ""}
                  onChange={onChangeDurationInput}
                  placeholder="2시간"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ScheduleMakePage;