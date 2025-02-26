import { useEffect, useRef } from "react";
import "./index.css";
import { useNavigate } from "react-router-dom";

export default function ReportPage() {
  const navigate = useNavigate();

  return (
    <div className="container ReportPage">
      <div className="ReportPage_title">
        <button
          onClick={() => {
            navigate(-1);
          }}
        >
          돌아가기
        </button>
        <div>버그 리포트</div>
      </div>

      <div className="Report_notice">
        <p>
          불편을 드려 죄송합니다.
          <br />
          발생한 문제를 신속하게 해결하기 위해 귀하의 도움이 필요합니다. <br />
          버그에 대한 자세한 설명과 함께 어떻게 발생했는지에 대한 정보를 제공해 주시면 더욱 신속하고
          정확한 조치를 취할 수 있습니다.
          <br />
          감사합니다.
        </p>
      </div>

      <div className="Report_notice">
        <div className="Report_image">
          <div className="img_box">img</div>
          <button>이미지 첨부</button>
        </div>
        <textarea className="Report_input" placeholder="어떤 버그를 만나셨나요?" />
      </div>

      <div className="Report_button_container">
        <button className="Report_button">리포트</button>
      </div>
    </div>
  );
}
