import "./index.css";
import React, { useEffect, useState } from "react";
import heart_icon from "./../../img/heart.png";

export default function LoadingComponent() {
  const [dots, setDots] = useState("");

  useEffect(() => {
    const interval = setInterval(() => {
      setDots((prev) => (prev.length >= 3 ? "" : prev + " ."));
    }, 500);

    return () => clearInterval(interval); // 컴포넌트 언마운트 시 정리
  }, []);

  return (
    <div className="NoneFeed">
      <div className="heart-icon">
        <img src={heart_icon} alt="heart" />
      </div>
      <p
        style={{
          color: '#767676',
          fontSize: '15px',
          fontStyle: 'normal',
          fontWeight: '600',
          lineHeight: '140%', /* 21px */
          letterSpacing: '-0.375px',
        }}
      >불러오는 중입니다{dots}</p>
    </div>
  );
}