import React, { useState } from "react";
import style from "./ReportModal.module.css";
import mainApi from "../../services/apis/mainApi";

const ReportModal = ({ type, target, toggleReportOption }) => {

  const reportOption = {
    1: "성적인 콘텐츠",
    2: "폭력적 또는 혐오스러운 콘텐츠",
    3: "증오 또는 악의적인 콘텐츠",
    4: "유해하거나 위험한 행위",
    5: "잘못된 정보",
    6: "부적절한 프로필 또는 닉네임",
    7: "커뮤니티 지침 위반",
  };

  const [selected, setSelected] = useState(null);
  const [targetOption, setTargetOption] = useState("");

  const handleReport = async (key) => {
    setSelected(key);
    setTargetOption(reportOption[key]);
  };

  const fetchViolationReport = async () => {
    let id = "";

    if (type == "feed") {
      id = target.fid;
    }else if (type=="schedule"){
      id = target.sid;
    }else if (type=="comment"){
      id = target.cid;
    }else{
      return null;
    }

    try{
      const res = await mainApi.get(`/nova_sub_system/try_report_violation?report_type=${type}&target_id=${id}&report_option=${targetOption}`)
      if (res.data.body.result) {
        alert("신고 제출이 완료 되었습니다.");
      }else{
        alert("신고 제출 중 문제가 생겼습니다.");
      }
    }
    catch{
      alert("신고 제출 중 문제가 생겼습니다. 관리자에게 문의하세요.");
    }
    return;
  }

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
            <div className={style["modal-sub-title"]}>신고된 게시물은 검토 후 비활성화 됩니다.</div>
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
        {
          selected && (
            <div className={style["button-wrapper"]}>
              <div className={style["submit-button"]}
                onClick={async ()=>{
                  await fetchViolationReport();
                  toggleReportOption();
                }}
              >
                제출하기
              </div>
            </div>
          )
        }
      </div>
    </div>
  );
};

export default ReportModal;
