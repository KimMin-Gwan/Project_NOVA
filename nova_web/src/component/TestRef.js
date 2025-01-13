import { useEffect, useState } from "react";
import { useRef } from "react";
import ProgressBar from "./ProgressBar";

export default function TestRef() {
  return (
    <div className="notice-container">
      <div>
        <div className="notice-box">
          <div className="notice-img">
            <img alt="img" />
          </div>

          <div className="notice-content">
            <b>게시글 작성할 때 요zzzz령</b>
            <p>전체 공지사항</p>
          </div>
        </div>
      </div>
    </div>
  );
}
