import { useEffect, useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import style from "./ScheduleMakePage.module.css";
import style2 from "./ScheduleMakePageMobile.module.css";
import useMediaQuery from "@mui/material/useMediaQuery";
import DesktopLayout from "../../component/DesktopLayout/DeskTopLayout.jsx";
import DesktopScheduleSelectSection from "./DesktopScheduleSelector.jsx";
import DesktopBiasSelectSection from "./DesktopBiasSelector.jsx";
import DesktopCalender from "./DesktopCalendar.jsx";
import MobileBiasSelectSection from "./MobileBiasSelecotr.jsx";
import MobileCalender from "./MobileCalendar.jsx";
import MobileScheduleSelectSection from "./MobileScheduleSelector.jsx";
import postApi from "../../services/apis/postApi.js";
import HEADER from "../../constant/header.js";

const ScheduleMakePage = () => {
    const isMobile = useMediaQuery('(max-width:1100px)');
    const navigate = useNavigate();
    const defaultDate = {
      year : "",
      month: "",
      day : ""
    }
    const now = new Date(); // 현재 시각
    const datetime = new Date(
      now.getFullYear(),
      now.getMonth(),   // 0~11
      now.getDate(),    // 오늘 날짜
      22,               // 시
      0,                // 분
      0                 // 초
    );

    const defaultSchedule = {
      sid: "",
      bid: "",
      title: "",
      tags: [],
      datetime: datetime, // 오늘 22:00
      duration: 60
    };


    const [selectedBias, setSelectedBias] = useState("");
    const [selectedDate, setSelectedDate] = useState(defaultDate);
    const [selectedSchedule, setSelectedSchedule] = useState(defaultSchedule);

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

    const scheduleList = {
      1: {
        title : "33원정대",
        datetime : new Date("2025-09-01T14:00:00"),
        tags: ["게임"],
        duration: 120,
      },
      2: {
        title : "33원정대",
        datetime : new Date("2025-09-02T14:00:00"),
        tags: ["게임"],
        duration: 120,
      },
      3: {
        title : "DK vs KT",
        datetime : new Date("2025-09-03T14:00:00"),
        tags: ["저챗", "LCK같이보기"],
        duration: 180,
      },
      4:{
        title : "롤, 오버워치 시참 데이",
        datetime : new Date("2025-09-04T14:00:00"), 
        tags: ["게임", "롤", "오버워치"],
        duration: 300,
      },
      8: {
        title : "저챗 뱅",
        datetime : new Date("2025-09-08T14:00:00"),
        tags: ["저챗"],
        duration: 120,
      },
      9: {
        title : "발로란트", 
        datetime : new Date("2025-09-09T14:00:00"),
        tags: ["게임", "발로란트"],
        duration: 120,  
      },
      10: {
        title : "카페탐방", 
        datetime : new Date("2025-09-10T14:00:00"),
        tags: ["일상", "먹방"],
        duration: 180,
      },
      12: {
        title : "클립 이상형월드컵",  
        datetime : new Date("2025-09-12T14:00:00"),
        tags: ["게임"],
        duration: 120,
      },
      15: {
        title : "33원정대", 
        datetime : new Date("2025-09-15T14:00:00"),
        tags: ["게임"],
        duration: 120,
      },
      16: {
        title : "저챗 뱅", 
        datetime : new Date("2025-09-16T14:00:00"),
        tags: ["저챗"],
        duration: 120,
      },
      19: {
        title : "롤 시참 데이", 
        datetime : new Date("2025-09-19T14:00:00"),
        tags: ["게임", "롤"],
        duration: 300,
      },
    };

    useEffect(()=>{
      setSelectedDate(defaultDate);
    }, [selectedBias])

    useEffect(()=>{
      if (selectedDate.day !== "") {
        const schedule = scheduleList[selectedDate.day];
        if (schedule) {
          setSelectedSchedule(schedule);
        } else {
          setSelectedSchedule(defaultSchedule);
        }
      } else {
        setSelectedSchedule(defaultSchedule); // 날짜가 빈 값일 때도 초기화
      }
    }, [selectedDate])


  async function tryFetchNewSchedule(newSchedule) {
    try {
      const res = await postApi.post('/time_table_server/try_make_new_schedule', {
        header: HEADER,
        body: {
          schedule: {
            ...newSchedule,
            bid: selectedBias,
          },
        },
      });

      console.log(res.data);

      return res.data;
    } catch (error) {
      if (error.response) {
        // 서버에서 응답을 준 경우
        console.error("❌ 서버 에러:", error.response.status, error.response.data);
      } else if (error.request) {
        // 요청은 갔는데 응답이 없는 경우
        console.error("❌ 네트워크 에러: 응답 없음", error.request);
      } else {
        // 요청 설정 문제 등
        console.error("❌ 요청 에러:", error.message);
      }
    }
  }


    if (!isMobile){
      return(
        <DesktopLayout>
          <div className={style["frame"]}>
            <DesktopBiasSelectSection
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
                selectedBias={selectedBias}
                selectedDate={selectedDate}
                handleSelectDate={handleSelectDate}
                scheduleList={scheduleList}
              />
            </div>
            <div 
              className={style["desktop-section-wrapper"]}
              style={{
                height: selectedDate.day && selectedBias ? "900px" : "0px",
              }}
            >
              <DesktopScheduleSelectSection
                selectedSchedule={selectedSchedule} setSelectedSchedule={setSelectedSchedule}
                tryFetchNewSchedule={tryFetchNewSchedule}
              />
            </div>
            <div className={style["schedule-make-info"]}>
              <div className={style["schedule-make-info-title"]}>주의사항</div>
              <span>1. 작성된 콘텐츠 일정은 스트리머 요청으로 삭제될 수 있습니다.</span>
              <span>2. 악의적의 의도로 콘텐츠 일정을 작성할 경우 커뮤니티 지침에 따라 제제될 수 있습니다.</span>
              <span>3. 작성된 컨텐츠 일정은 대상 스트리머와 작성자가 수정할 수 있습니다.</span>
            </div>
          </div>
        </DesktopLayout>
      );
    }else{
      return(
        <div className="container">
            <div className={style2["mobile-frame"]} >
              <div className={style2["mobile-section-wrapper"]} 
                style={{
                  padding : "10px 4%"
                }}
              >
                <MobileBiasSelectSection
                  biasList={tempBiasList}
                  selectedBias={selectedBias}
                  handleSelectBias={handleSelectBias}
                />
              </div>
              <div 
                className={style2["mobile-section-wrapper"]}
                style={{
                  height: selectedBias ? "720px" : "0px",
                }}
              >
                <MobileCalender
                  // event={eventList}
                  selectedBias={selectedBias}
                  selectedDate={selectedDate}
                  handleSelectDate={handleSelectDate}
                  scheduleList={scheduleList}
                />
              </div>
              <div 
                className={style2["mobile-section-wrapper"]}
                style={{
                  height: selectedDate.day && selectedBias ? "900px" : "0px",
                }}
              >
                <MobileScheduleSelectSection
                  selectedSchedule={selectedSchedule} setSelectedSchedule={setSelectedSchedule}
                  tryFetchNewSchedule={tryFetchNewSchedule}
                />
              </div>
              <div className={style["schedule-make-info"]}>
                <div className={style["schedule-make-info-title"]}>주의사항</div>
                <span>1. 작성된 콘텐츠 일정은 스트리머 요청으로 삭제될 수 있습니다.</span>
                <span>2. 악의적의 의도로 콘텐츠 일정을 작성할 경우 커뮤니티 지침에 따라 제제될 수 있습니다.</span>
                <span>3. 작성된 컨텐츠 일정은 대상 스트리머와 작성자가 수정할 수 있습니다.</span>
              </div>
          </div>
        </div>
      );
  } 
}




export default ScheduleMakePage;