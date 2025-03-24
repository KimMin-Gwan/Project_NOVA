import style from "./EventMore.module.css";
import ModalRectangle from "./../../img/ModalRectangle.png";
import { useState, useEffect } from "react";
import ScheduleEvent from "../EventCard/EventCard";
import HEADER from "../../constant/header";
import postApi from "../../services/apis/postApi";
import { ScheduleDetailAdd, ScheduleAdd } from "../ScheduleMore/ScheduleMore";
import TimeChart, {TimeChartPreview} from "../../pages/SchedulePage/TimeChart/TimeChart";
import { tempWeekDayData, tempScheduleData } from "../../pages/SchedulePage/TestScheduleData";
import { ScheduleBundle } from "../../component/ScheduleEvent/ScheduleBundle";
import ScheduleSelect, { MakeScheduleDetail } from "../ScheduleSelect/ScheduleSelect";
import useBiasStore from "../../stores/BiasStore/useBiasStore";
import DropDown from "../DropDown/DropDown";

export function DetailModal({ closeSchedule, isOpen, children }) {
  const [backgroundColor, setBackgroundColor] = useState("");
  const [displaySt, setdisplaySt] = useState("");
  const [upAnimation, setUpAnimation] = useState(false);
  // 애니메이션 올라오면 배경색 변화도록 해주는 이펙트
  useEffect(() => {
    if (!isOpen) {
      setBackgroundColor("transparent"); //닫혀있을 때는 배경색 없애기
      setUpAnimation(false); // see 클래스 없애주기 위해서 닫히면 false 되도록 바꿔줌
      // 5초 뒤에 닫기도록
      setTimeout(() => {
        setdisplaySt("none");
      }, 500);
    } else {
      setdisplaySt("block");

      // 열렸다는 block 후에 애니메이션 적용 되도록 함
      setTimeout(() => {
        setUpAnimation(true);
      }, 10);

      //애니메이션 다하고 뒤에 배경색 주기
      setTimeout(() => {
        setBackgroundColor("rgba(0, 0, 0, 0.5)");
      }, 500);
    }

    return () => {
      clearTimeout();
    };
  }, [isOpen]);

  return (
    <div
      className={`${style["EventMoreContainer"]} ${upAnimation ? style["see"] : ""}`}
      onClick={closeSchedule}
      style={{ display: displaySt, backgroundColor }}
    >
      <section
        className={`${style["eventMain"]} ${isOpen ? style["on"] : ""}`}
        onClick={(e) => e.stopPropagation()}
      >
        <div className={style["topImage"]}>
          <img src={ModalRectangle} alt="모달 사각형" />
        </div>
        {children}
      </section>
    </div>
  );
}

async function fetchTimeTableData(sids) {
  try {
    const response = await postApi.post("time_table_server/get_time_chart_with_other_schedule", {
      header: HEADER,
      body: {
        sids: sids,
      },
    });
    return response.data.body; // 데이터 반환
  } catch (error) {
    return {schedule_blocks:[], week_day_datas:[]}; // 에러 발생 시 null 또는 다른 처리
  }
}


export function BundleScheduleDetail({ closeSchedule, isOpen, target }) {
  const [selectBack, setSelectBack] = useState({});
  const [isSelect, setIsSelect] = useState(1);
  const [sids, setSids] = useState([]);  // 선택한 schedule의 sid 리스트임
  const [schedules, setSchedules] = useState([]); // 이건 표시되는 모든 schedule임

  const [timeWeekDayData, setTimeWeekDayData] = useState([]);
  const [timeChartData, setTimeChartData] = useState([]);

  // 내 스케줄에 등록하는 함수 (추가하기 버튼 누르면 동작해야됨)
  // 완료하면 성공했다고 알려주면 좋을듯
  async function fetchTryAddSchedule(dummy) {
    await postApi.post("time_table_server/try_add_schedule", {
      header: HEADER,
      body: {
        sids: sids,
      },
    }).then((res) => {
      alert("일정을 추가했습니다.");
      closeSchedule()
    });
  }


  // 스케줄 번들에 있는 스케줄들 받아오는 함수
  async function fetchSchedules() {
    // 패치 받기 전에 스케줄 초기화 부터하기
    setSchedules([]);
    await postApi
      .post("time_table_server/get_schedule_with_sids", {
        header: HEADER,
        body: {
          sids: target.sids,
        },
      })
      .then((res) => {
        setSchedules((prev) => [...prev, ...res.data.body.schedules]);
      });
  }

  // 타임 차트 데이터를 받아오는 비동기 함수
  const fetchData = async (sids) => {
    let fetchBody = {}
    fetchBody = await fetchTimeTableData(sids);
    setTimeChartData(fetchBody.schedule_blocks);
    setTimeWeekDayData(fetchBody.week_day_datas);
  }

  // 선택이 되면 패치 받아야됨
  useEffect(() => {
    fetchData(sids)
  }, [sids]);

  // 취소했을 때 모두 취소되어서 변화하도록함
  useEffect(() => {
    if (isSelect === 1) {
      handleReset();
    }
  }, [isSelect]);

  // 취소했을 때 모두 취소되어서 변화하도록함
  useEffect(() => {
    // 토글창 열리면 패치 받아오기
    if (isOpen) {
      let fetchBody = {}
      handleReset();
      fetchSchedules();
      fetchData([])
    }
  }, [isOpen]);

  // 선택하면 배경색 변화하게 해주는 거
  function handleSelect(item, key) {
    setSelectBack((prev) => {
      // 클릭한 key가 이미 존재하는지 확인
      if (prev[key]) {
        // 이미 존재할 경우, 해당 key를 제외하고 새로운 객체를 반환
        const { [key]: omit, ...rest } = prev;
        return rest;
      } else {
        // 존재하지 않을 경우, 새로운 key와 초기값 추가
        return { ...prev, [key]: "#F1F7FF" };
      }
    });

    // 전송에 사용할 sid도 추가
    setSids((prev) => {
      // 클릭한 item.sid가 배열에 이미 존재하는지 확인
      if (prev.includes(item.sid)) {
        // 이미 존재할 경우, 해당 item.sid를 배열에서 제거
        return prev.filter((sid) => sid !== item.sid);
      } else {
        // 존재하지 않을 경우, 배열에 추가
        return [...prev, item.sid];
      }
    });
    // 새로운 값에 할당하여 값을 설정해주어서 상태가 즉시 업데이트 되도록 해준다
  }

  // 선택한 일정 리셋하기
  //
  function handleReset() {
    // 선택 초기화 하기
    setSelectBack({});
    setSids([]);
    setIsSelect(1);
  }

  // 일정 모두 선택
  function handleAllSelect() {
    ////색상변화
    schedules.map((item, index) => handleSelect(item, index));
    setIsSelect(4);
    //setSelectBack((prev) => {
    //const isAllSelected = exdata.every((key) => prev[key] === "#F1F7FF");

    //return exdata.reduce((acc, key) => {
    //acc[key] = isAllSelected ? "" : "#F1F7FF";
    //return acc;
    //}, {});
    //});
  }

  // 일정 선택 하기, 취소하기 토클
  const selectToggle = () => {
    // 왜 4냐면 button 배열에 선택됐을 때 텍스트가 배열[4]이기 때문임
    setIsSelect((prev) => (prev === 1 ? 4 : 1));
  };

  return (
    <DetailModal closeSchedule={closeSchedule} isOpen={isOpen}>
      <ScheduleBundle item={target} />
      <ScheduleDetailAdd
        selectToggle={selectToggle}
        selectText={isSelect}
        allSelect={isSelect === 1 ? () => handleAllSelect() : fetchTryAddSchedule}
      />
      {schedules.map((item, index) => (
        <ScheduleEvent
          key={index}
          {...item}
          toggleClick={isSelect === 4 ? () => handleSelect(item, index) : undefined}
          selectBack={selectBack[index] || ""}
        />
      ))}

      <div className={style["modal-title"]}>
        미리보기
      </div>
      <TimeChartPreview weekDayData={timeWeekDayData} scheduleData={timeChartData} />
    </DetailModal>
  );
}

// 이건 스케줄 목록에서 추가하기 버튼 누르면 나오는 자세히 모달창(밑에서 위로 올라오는애)
export function ScheduleDetail({ closeSchedule, isOpen, target }) {
  const [sids, setSids] = useState([]);
  const [timeWeekDayData, setTimeWeekDayData] = useState([]);
  const [timeChartData, setTimeChartData] = useState([]);

  // 내 스케줄에 등록하는 함수 (추가하기 버튼 누르면 동작해야됨)
  async function fetchTryAddSchedule() {
    await postApi.post("time_table_server/try_add_schedule", {
      header: HEADER,
      body: {
        sids: sids,
      },
    });
  }

  // 타임 차트 데이터를 받아오는 비동기 함수
  const fetchData = async (sids) => {
    let fetchBody = {}
    fetchBody = await fetchTimeTableData(sids);
    setTimeChartData(fetchBody.schedule_blocks);
    setTimeWeekDayData(fetchBody.week_day_datas);
  }

  //// 선택이 되면 패치 받아야됨
  //useEffect(() => {
    //fetchData(sids)
  //}, [sids]);

  useEffect(() => {
    // 토글창 열리면 패치 받아오기
    if (isOpen) {
      setSids([target.sid])
      fetchData([target.sid])
    }
  }, [isOpen]);

  return (
    <DetailModal closeSchedule={closeSchedule} isOpen={isOpen}>
      <ScheduleEvent {...target} />
      <ScheduleAdd target={target} addClick={fetchTryAddSchedule} />
      <div className={style["modal-title"]}>
        미리보기
      </div>
      <TimeChartPreview weekDayData={timeWeekDayData} scheduleData={timeChartData} />
    </DetailModal>
  );
}

//export function EventDetail ({ closeSchedule, isOpen }) {
//return (
//<DetailModal closeSchedule={closeSchedule} isOpen={isOpen}>
//<BaseBundle />
//<ScheduleEventAdd />
//<EventBundle />
//<section className={style["previewBox"]}>
//<h3>이벤트 미리보기</h3>
//<ScheduleCalendar />
//</section>
//</DetailModal>
//);
//}

// 단일 스케줄 만들기
export function MakeSingleSchedule({ closeSchedule, isOpen }) {
  // 스케줄 만들기 모드
  // single vs bundle

  const scheduleFormat = {
    id: Date.now(), 
    sname : '',
    location : '',
    bid : '',
    start_date : '',
    start_time : '',
    end_date : '',
    end_time : ''
  }

  const [scheduleArray, setScheduleArray] = useState([scheduleFormat]);

  const bundleFormat = {
    sname : '',
    bid : '',
    schedules : scheduleArray
  }

  const [addMode, setAddMode] = useState('single');
  const [numSchedule, setNumSchedule] = useState(1);
  const [sendScheduleData, setSendScheduleData] = useState(bundleFormat)

  let { biasList } = useBiasStore();
  let [biasId, setBiasId] = useState();



  // 번들 이름 
  const [bundleNameInput, setBundleNameInput] = useState("");

  // 번들 이름 바꾸기
  const onChangeBundleName= (e) => {
    setBundleNameInput(e.target.value);
  };

  // 단일 스케줄 만들기
  async function fetchTryMakeSingleSchedule() {
    await postApi.post("time_table_server/try_make_new_single_schedule", {
      header: HEADER,
      body: sendScheduleData.schedules[0],
    });
  }

  // 번들 스케줄 만들기
  async function fetchTryMakeBundleSchedule() {
    await postApi.post("time_table_server/try_make_new_multiple_schedule", {
      header: HEADER,
      body: sendScheduleData,
    });
  }

  // 전송하는 함수 (모드를 보고 번들로 보낼지 싱글로 보낼지 확인)
  function tryFetchMakeSchedule(){
    if (addMode == 'single') {
      fetchTryMakeSingleSchedule()
    }
    else if (addMode == 'bundle'){
      fetchTryMakeBundleSchedule()
    }
  }

  const addSchedule = () => {
    setNumSchedule((prev) => prev + 1);
    const newSchedule = { ...scheduleFormat, id: Date.now() };
    const updatedSchedules = [...sendScheduleData.schedules, newSchedule];
    setSendScheduleData((prev) => ({
      ...prev,
      schedules: updatedSchedules,
    }));
  };


  const removeSchedule = (index) => {
    setNumSchedule((prev) => (prev-1))
    const updatedSchedules = sendScheduleData.schedules.filter((_, i) => i !== index);
    setSendScheduleData((prev) => ({
    ...prev,
    schedules: updatedSchedules,
    }));
  }

  useEffect(()=>{
    if(numSchedule == 1){
      setAddMode("single")
    }
    else{
      setAddMode("bundle")
    }
  }, [numSchedule])

  useEffect(()=>{
    setSendScheduleData(prevState => ({
      ...prevState,
      bid: biasId, // bundleNameInput 값으로 sname 업데이트
    }));
  }, [biasId])

  useEffect(() => {
    setSendScheduleData(prevState => ({
      ...prevState,
      sname: bundleNameInput, // bundleNameInput 값으로 sname 업데이트
    }));
  }, [bundleNameInput]);

  useEffect( () => {
    if (isOpen) {
      // 스케줄 초기화
      setScheduleArray([scheduleFormat]);

      // 번들 이름 초기화
      setBundleNameInput('');

      // 추가 모드 설정
      setAddMode('single');
      setNumSchedule(1);

      // 전송 데이터 초기화
      setSendScheduleData(bundleFormat);
    }
  }, [isOpen])


  return (
    <DetailModal closeSchedule={closeSchedule} isOpen={isOpen}>
      <div className={style["modal-title"]}>
        일정 등록
      </div>
      {
        addMode === "bundle" ? (
          <div className="ScheduleSelect">
            <div className={style["searchFac"]}>
              <div className={style["searchBox"]}>
                <input
                  type="text"
                  value={bundleNameInput}
                  onChange={onChangeBundleName}
                  placeholder="일정 번들 이름"
                />
              </div>
            </div>
          </div>
        ) : null
      }
      <div className={style["bias-container"]}>
        <DropDown options={biasList} setBiasId={setBiasId} />
      </div>
      {
       sendScheduleData.schedules.map((schedule, index) => (
          <ScheduleSelect
            key={schedule.id}
            index={index}
            setSendScheduleData={setSendScheduleData}
            sendScheduleData={sendScheduleData}
            removeSchedule={removeSchedule}
          />
        ))
      }
      <div className={style["additional-schedule-button"]}>
        <p
          className={style["additional-schedule-text"]}
          onClick={addSchedule}
        >
          일정 추가
        </p>
      </div>
      <div className={style["moreContainer"]}>
        <button onClick={() => {tryFetchMakeSchedule()}}>일정 등록</button>
      </div>
    </DetailModal>
  );
}
