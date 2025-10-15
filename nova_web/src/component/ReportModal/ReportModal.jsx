import React, { useState } from "react";
import style from "./ReportModal.module.css";

const ReportModal = ({ type, target, toggleReportOption }) => {
  const reportOption = {
    1: "1번 사유",
    2: "2번 사유",
    3: "3번 사유",
    4: "4번 사유",
    5: "5번 사유",
    6: "6번 사유",
    7: "7번 사유",
  };


  const [selected, setSelected] = useState(null);

  const handleReport = (key) => {
    setSelected(key);
    console.log("신고 사유 선택:", key);
    console.log("목표:", target.fid);
  };

  return (
    <div
      className={style["modal-frame"]}
      onClick={() => toggleReportOption(false)}
    >
      <div
        className={style["modal-container"]}
        onClick={(e) => e.stopPropagation()}
      >
        <div className={style["modal-title-wrapper"]}>
            <div className={style["modal-title"]}>신고 사유 선택</div>
            <div className={style["modal-sub-title"]}>신고된 게시물은 비활성화 됩니다.</div>
        </div>
        <div className={style["option-list"]}>
            {Object.entries(reportOption).map(([key, value]) => (
                <div
                key={key}
                className={style["option-item"]}
                onClick={() => handleReport(key)}
                >
                <div className={style["radio-circle"]}>
                    {selected === key && <div className={style["radio-selected"]} />}
                </div>
                <span>{value}</span>
                </div>
            ))}
        </div>
      </div>
    </div>
  );
};

export default ReportModal;
