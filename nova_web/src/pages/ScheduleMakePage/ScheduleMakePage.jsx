import { useEffect, useState, useRef } from "react";
import { useNavigate, useParams } from "react-router-dom";
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
import mainApi from "../../services/apis/mainApi.js";
import HEADER from "../../constant/header.js";
import useBiasStore from "../../stores/BiasStore/useBiasStore";

const ScheduleMakePage = () => {
    const isMobile = useMediaQuery('(max-width:1100px)');
    const { sid } = useParams();
    const navigate = useNavigate();
    const [isUserState, setIsUserState] = useState(false);
    const { biasList, biasId, setBiasId, loading, fetchBiasList } = useBiasStore();
    const [scheduleList, setScheduleList] = useState({});
    const [initDate, setInitDate] = useState();

    function handleValidCheck() {
        fetch("https://supernova.io.kr/home/is_valid", {
        credentials: "include",
        })
        .then((response) => {
            if (response.status === 200) {
              setIsUserState(true);
            return response.json();
            } else {
              setIsUserState(false);
            return Promise.reject();
            }
        })
        .catch((error) => {
          setIsUserState(false);
          alert("로그인이 필요한 서비스입니다.");
          navigate("/novalogin");
        });
    }


    function fetchScheduleList(bid, year, month) {
      mainApi.get(`/time_table_server/get_monthly_bias_schedule?bid=${bid}&year=${year}&month=${month}`).then((res)=>{
        const body = res.data.body;
        if (body.result){
          const scheduleData = body.schedules;
          const formattedSchedule = {};
          scheduleData.forEach((schedule) => {
            const date = new Date(schedule.datetime);
            const day = date.getDate();
            formattedSchedule[day] = {
              ...schedule,
              datetime: date
            };
          });
          setScheduleList(formattedSchedule);
        } else{
          alert("스케줄 정보를 불러오지 못했습니다.");
          setScheduleList({});
        }
      }).catch((error)=>{
        console.error("Error fetching schedule list:", error);
        setScheduleList({});
      });
    }
    



    useEffect(() => {
      fetchBiasList();
    }, [isUserState]);

   
    const now = new Date(); // 현재 시각
    const defaultDate = {
      year : now.getFullYear(),
      month: now.getMonth() + 1, // 월은 0부터 시작하므로 +1 
      day : ""
    }

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
      duration: 1,
      is_owner : true,
    };


    const [selectedBias, setSelectedBias] = useState("");
    const [selectedDate, setSelectedDate] = useState(defaultDate);
    const [selectedSchedule, setSelectedSchedule] = useState(defaultSchedule);

    const handleSelectBias = (bid) => {
        if(initDate){
          setInitDate();
        }

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

    useEffect(()=>{
      if(!initDate){
        handleSelectDate(defaultDate);
      }
      if (selectedBias){
        fetchScheduleList(selectedBias, now.getFullYear(), now.getMonth()+1);
      }
    }, [selectedBias])

    function selectedDateToDate(selectedDate, hour = 22, minute = 0) {
      if (!selectedDate?.year || !selectedDate?.month || !selectedDate?.day) {
        return null;
      }
      return new Date(
        selectedDate.year,
        selectedDate.month - 1, // JS Date는 month가 0부터 시작
        selectedDate.day,
        hour,
        minute
      );
    }

    useEffect(()=>{
      if(!initDate){
        if (selectedDate.day !== "") {
          const schedule = scheduleList[selectedDate.day];
          if (schedule) {
            setSelectedSchedule(schedule);
          } else {
            const newSchedule = {
              sid: "",
              bid: "",
              title: "",
              tags: [],
              datetime: selectedDateToDate(selectedDate, 22, 0), // 22:00 고정
              duration: 1,
              is_owner: true,
            };
            setSelectedSchedule(newSchedule);
          }
        } else {
          setSelectedSchedule(defaultSchedule); // 날짜가 빈 값일 때도 초기화
        }
      }
    }, [selectedDate])


    async function tryFetchNewSchedule(newSchedule) {
      if (initDate) {
        setInitDate();
      }

      setSelectedSchedule(newSchedule);

      try {
        const res = await postApi.post('/time_table_server/try_make_new_schedule', {
          header: HEADER,
          body: {
            schedule: newSchedule,
          },
        });

        // ✅ sid 안전하게 반환
        if (res?.data?.body?.sid) {
          return res.data.body.sid;
        } else {
          console.error("❌ 서버 응답에 sid가 없습니다:", res.data);
          return null;
        }
      } catch (error) {
        if (error.response) {
          // 서버에서 에러 응답을 받은 경우
          console.error("❌ 서버 에러:", error.response.status, error.response.data);
        } else if (error.request) {
          // 요청은 전송됐지만 응답이 없는 경우
          console.error("❌ 네트워크 에러: 응답 없음", error.request);
        } else {
          // 요청 설정 문제 등
          console.error("❌ 요청 에러:", error.message);
        }
        return null; // 실패 시 안전하게 null 반환
      }
    }

    const fetchSingleScheduleData = (sid) => {
      mainApi.get(`/time_table_server/try_get_written_schedule?sid=${sid}`).then((res)=>{
        const schedule = res.data.body.schedules[0];
        setSelectedBias(schedule.bid);
        const date = new Date(schedule.datetime);
        setInitDate(date);
        setSelectedSchedule({
          ...schedule,
          datetime: date
        })
      })
    }

    // init
    useEffect(() => {
      handleValidCheck();
      if (sid){
        fetchSingleScheduleData(sid);
      }
    }, []);

    const resetAll = () => {
      setSelectedBias("");
      setSelectedDate(defaultDate);
      setSelectedSchedule(defaultSchedule);
      setScheduleList({});
    }


    if (!isMobile){
      return(
        <DesktopLayout>
          <div className={style["frame"]}>
            <DesktopBiasSelectSection
              biasList={biasList}
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
                fetchScheduleList={fetchScheduleList}
                initDate={initDate}
                setInitDate={setInitDate}
              />
            </div>
            <div 
              className={style["desktop-section-wrapper"]}
              style={{
                height: selectedDate.day && selectedBias ? "fit-content" : "0px",
              }}
            >
              <DesktopScheduleSelectSection
                selectedSchedule={selectedSchedule}
                selectedBias={selectedBias}
                setSelectedSchedule={setSelectedSchedule}
                tryFetchNewSchedule={tryFetchNewSchedule}
                resetAll={resetAll}
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
              <div className={style2["mobile-top-bar-wrapper"]}>
                <div className={style2["backword-button"]}
                  onClick={()=>{
                    navigate('/');
                  }}
                > 취소 </div>
                <span className={style2["mobile-top-bar-title"]}> 콘텐츠 일정 작성</span>
                <div
                style={{width: "24px"}}
                ></div>
              </div>

              <div className={style2["mobile-section-wrapper"]} 
                style={{
                  padding : "10px 4%"
                }}
              >
                <MobileBiasSelectSection
                  biasList={biasList}
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
                  fetchScheduleList={fetchScheduleList}
                  initDate={initDate}
                  setInitDate={setInitDate}
                />
              </div>
              <div 
                className={style2["mobile-section-wrapper"]}
                style={{
                  height: selectedDate.day && selectedBias ? "fit-content" : "0px",
                }}
              >
                <MobileScheduleSelectSection
                  selectedSchedule={selectedSchedule}
                  selectedBias={selectedBias}
                  setSelectedSchedule={setSelectedSchedule}
                  tryFetchNewSchedule={tryFetchNewSchedule}
                  resetAll={resetAll}
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

