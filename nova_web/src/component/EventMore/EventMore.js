import style from "./EventMore.module.css";
import ModalRectangle from "./../../img/ModalRectangle.png";
import { useState, useEffect } from "react";
import { EventBundle } from "../ScheduleEvent/ScheduleBundle";
import ScheduleEvent from "../EventCard/EventCard";
import { ScheduleMoreAdd } from "../ScheduleMore/ScheduleMore";
import TimeChart from "../../pages/SchedulePage/TimeChart";
import {
  tempWeekDayData,
  tempScheduleData,
} from "../../pages/SchedulePage/TestScheduleData";
const exdata = [0, 1];

export default function EventMore({ closeSchedule, isOpen, children }) {
  const [backgroundColor, setBackgroundColor] = useState("");

  // 애니메이션 올라오면 배경색 변화도록 해주는 이펙트
  useEffect(() => {
    if (!isOpen) {
      setBackgroundColor("transparent"); //닫혀있을 때는 배경색 없애기
    } else {
      setTimeout(() => {
        setBackgroundColor("rgba(0, 0, 0, 0.5)"); //일정시간 지난 후에 뒤에 배경색 주기
      }, 500);
    }

    return () => {
      clearTimeout();
    };
  }, [isOpen]);

  return (
    <div
      className={`${style["EventMoreContainer"]} ${isOpen ? style["see"] : ""}`}
      onClick={closeSchedule}
      style={{ backgroundColor }}
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

export function BundleEventMore({ closeSchedule, isOpen }) {
  const [selectBack, setSelectBack] = useState({});
  const [isSelect, setIsSelect] = useState(1);
  // 취소했을 때 모두 취소되어서 변화하도록함
  useEffect(() => {
    if (isSelect === 1) {
      handleReset();
    }
  }, [isSelect]);

  // 선택하면 배경색 변화하게 해주는 거
  function handleSelect(key) {
    setSelectBack((prev) => {
      const newState = {
        ...prev,
        [key]: prev[key] === "" || prev[key] === undefined ? "#F1F7FF" : "",
        // 처음에 초기 값이 ""이나 undefined여도 눌렀을 때 바로 색이 변하도록 함
      };

      return newState;
      // 새로운 값에 할당하여 값을 설정해주어서 상태가 즉시 업데이트 되도록 해준다
    });
  }

  // 선택한 일정 리셋하기
  function handleReset() {
    setSelectBack({});
  }

  // 일정 모두 선택
  function handleAllSelect() {
    console.log("모두선택");

    // 색상변화
    // setSelectBack((prev) => {
    //   const isAllSelected = exdata.every((key) => prev[key] === "#F1F7FF");

    //   return exdata.reduce((acc, key) => {
    //     acc[key] = isAllSelected ? "" : "#F1F7FF";
    //     return acc;
    //   }, {});
    // });
  }

  // 일정 선택 하기, 취소하기 토클
  const selectToggle = () => {
    // 왜 4냐면 button 배열에 선택됐을 때 텍스트가 배열[4]이기 때문임
    setIsSelect((prev) => (prev === 1 ? 4 : 1));
  };

  return (
    <EventMore closeSchedule={closeSchedule} isOpen={isOpen}>
      <EventBundle />
      <ScheduleMoreAdd
        selectToggle={selectToggle}
        selectText={isSelect}
        allSelect={isSelect === 1 ? () => handleAllSelect() : undefined}
      />
      {exdata.map((key, index) => (
        <ScheduleEvent
          key={index}
          toggleClick={isSelect === 4 ? () => handleSelect(key) : undefined}
          selectBack={selectBack[index] || ""}
        />
      ))}
      <TimeChart
        tempWeekDayData={tempWeekDayData}
        tempScheduleData={tempScheduleData}
      />
    </EventMore>
  );
}

export function ScheduleEventMore({ closeSchedule, isOpen }) {
  return (
    <EventMore closeSchedule={closeSchedule} isOpen={isOpen}>
      <EventBundle />
    </EventMore>
  );
}
