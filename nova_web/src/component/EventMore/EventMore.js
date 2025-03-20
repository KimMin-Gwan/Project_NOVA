import style from "./EventMore.module.css";
import ModalRectangle from "./../../img/ModalRectangle.png";
import { useState, useEffect } from "react";
import BaseBundle, { EventBundle } from "../ScheduleEvent/ScheduleBundle";
import ScheduleEvent from "../EventCard/EventCard";
import HEADER from "../../constant/header";
import postApi from "../../services/apis/postApi";
import { ScheduleEventAdd, ScheduleDetailAdd, ScheduleAdd } from "../ScheduleMore/ScheduleMore";
import TimeChart from "../../pages/SchedulePage/TimeChart/TimeChart";
import { tempWeekDayData, tempScheduleData } from "../../pages/SchedulePage/TestScheduleData";
import ScheduleCalendar from "../ScheduleCalendar/ScheduleCalendar";
import { ScheduleBundle } from "../../component/ScheduleEvent/ScheduleBundle";
import { MakeScheduleDetail } from "../ScheduleSelect/ScheduleSelect";

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

export function BundleScheduleDetail({ closeSchedule, isOpen, target }) {
  const [selectBack, setSelectBack] = useState({});
  const [isSelect, setIsSelect] = useState(1);
  const [sids, setSids] = useState([]);
  const [schedules, setSchedules] = useState([]);

  // 내 스케줄에 등록하는 함수 (추가하기 버튼 누르면 동작해야됨)
  // 완료하면 성공했다고 알려주면 좋을듯
  async function fetchTryAddSchedule(dummy) {
    await postApi.post("time_table_server/try_add_schedule", {
      header: HEADER,
      body: {
        sids: sids,
      },
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
      handleReset();
      fetchSchedules();
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

    console.log(sids);
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
    console.log("모두선택");

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
      <TimeChart weekDayData={tempWeekDayData} scheduleData={tempScheduleData} />
    </DetailModal>
  );
}

// 이건 스케줄 목록에서 추가하기 버튼 누르면 나오는 자세히 모달창(밑에서 위로 올라오는애)
export function ScheduleDetail({ closeSchedule, isOpen, target }) {
  const [sids, setSids] = useState([]);

  // 내 스케줄에 등록하는 함수 (추가하기 버튼 누르면 동작해야됨)
  async function fetchTryAddSchedule() {
    await postApi.post("time_table_server/try_add_schedule", {
      header: HEADER,
      body: {
        sids: sids,
      },
    });
  }

  useEffect(() => {
    // 토글창 열리면 패치 받아오기
    if (isOpen) {
      setSids([target.sid]);
    }
  }, [isOpen]);

  return (
    <DetailModal closeSchedule={closeSchedule} isOpen={isOpen}>
      <ScheduleEvent {...target} />
      <ScheduleAdd target={target} addClick={fetchTryAddSchedule} />
      <TimeChart weekDayData={tempWeekDayData} scheduleData={tempScheduleData} />
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
  //const [sids, setSids] = useState([]);

  // 내 스케줄에 등록하는 함수 (추가하기 버튼 누르면 동작해야됨)
  async function fetchTryAddSchedule() {
    await postApi.post("time_table_server/try_add_schedule", {
      header: HEADER,
      body: {},
    });
  }

  return (
    <DetailModal closeSchedule={closeSchedule} isOpen={isOpen}>
      <MakeScheduleDetail></MakeScheduleDetail>
    </DetailModal>
  );
}
