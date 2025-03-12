import style from "./EventMore.module.css";
import ModalRectangle from "./../../img/ModalRectangle.png";
import { useState, useEffect } from "react";
import ScheduleBundle from "../ScheduleEvent/ScheduleBundle";
import ScheduleEvent from "../EventCard/EventCard";
import { ScheduleMoreAdd } from "../ScheduleMore/ScheduleMore";

const exdata = [0, 1];

export default function EventMore({ closeSchedule, isOpen }) {
  const [backgroundColor, setBackgroundColor] = useState("");
  const [selectBack, setSelectBack] = useState({});
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

  // 선택하면 배경색 변화하게 해주는 거
  function handleSelect(key) {
    console.log(key);
    setSelectBack((prev) => ({
      ...prev,
      [key]: prev[key] === "" ? "#F1F7FF" : "",
    }));
  }

  // 일정 선택 하기, 취소하기 토클
  const selectToggle = () => {};
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
        <ScheduleBundle />
        <ScheduleMoreAdd selectToggle={selectToggle} />
        {exdata.map((key, index) => (
          <ScheduleEvent
            key={index}
            toggleClick={() => {
              handleSelect(key);
            }}
            selectBack={selectBack[index]}
          />
        ))}
      </section>
    </div>
  );
}
