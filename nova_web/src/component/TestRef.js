import { useEffect, useState } from "react";
import { useRef } from "react";
import ProgressBar from "./ProgressBar";

export default function TestRef() {
  return (
    <div className={"long-form-container"}>
      <div className="action-container">
        <div className="action-box">
          <div className="action-result" style={{ width: "100%" }}>
            갑니다
          </div>
          <div className="action-points">%</div>
        </div>

        <div className="action-box">
          <div className="action-result" style={{ width: "10%" }}>
            갑니다
          </div>
          <div className="action-points">%</div>
        </div>

        <div className="action-box">
          <div className="action-result" style={{ width: "100%" }}></div>
          <div className="action-points">%</div>
        </div>

        <div className="action-box">
          <div className="action-result" style={{ width: "100%" }}></div>
          <div className="action-points">%</div>
        </div>
      </div>

      {/* 
          <div className="action-result" style={{ width: "100%" }}>
            <div className="action-points">%</div>1
        </div>
        <ProgressBar />

        <div className={"action-box"}>
          22
        </div>
      <div></div> */}
    </div>
  );
}
