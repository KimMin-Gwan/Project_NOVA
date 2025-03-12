import style from "./EventMore.module.css";
import ModalRectangle from "./../../img/ModalRectangle.png";
import { useState, useEffect } from "react";

export default function EventMore({ closeSchedule, isOpen }) {
  const [backgroundColor, setBackgroundColor] = useState("");
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
        메인
      </section>
    </div>
  );
}
