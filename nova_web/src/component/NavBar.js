import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import fund_img from "./../img/funding.png";
import menuBtn_img from "./../img/menuBtn.png";
import galaxy_img from "./../img/galaxy3.png";
import shortForm_img from "./../img/short_form2.png";
import new_feed from "./../img/new_feed2.png";

import home_icon from "./../img/home_icon.png";
import menu3 from "./../img/menu3.png";
import feed_write from "./../img/feed_write.png";
import search from "./../img/search.png";
import { getModeClass } from "./../App.js";

const NavBar = ({ isUserState, brightMode }) => {
  const [isVisible, setIsVisible] = useState(false);

  let navigate = useNavigate();

  const toggleNavBar = () => {
    setIsVisible(!isVisible);
  };

  function handleNavigate(path) {
    navigate(path);
  }

  function handleStopClick(e) {
    e.stopPropagation();
  }

  const [mode, setMode] = useState(brightMode); // 초기 상태는 부모로부터 받은 brightMode 값
  useEffect(() => {
    setMode(brightMode); // brightMode 값이 바뀔 때마다 mode 업데이트
  }, [brightMode]);
  return (
    <div className={`bottom_bar ${getModeClass(mode)}`}>
      <div className="nav_button_box">
        <button className="nav_button" onClick={() => window.location.reload()}>
          <img src={home_icon} alt="home" className="btn_img" />
          <p className="btn_text">홈</p>
        </button>
      </div>

      <div className="nav_button_box">
        <button
          className="nav_button"
          onClick={(e) => {
            handleNavigate("/feed_list?type=all");
            handleStopClick(e);
          }}
        >
          <img src={menu3} alt="make" className="btn_img" />
          <p className="btn_text">전체 피드</p>
        </button>
      </div>

      <div className="nav_button_box">
        <button
          className="nav_button"
          onClick={(e) => {
            handleNavigate("/write_feed");
            handleStopClick(e);
          }}
        >
          <img src={feed_write} alt="make" className="btn_img" />
          <p className="btn_text">피드 작성</p>
        </button>
      </div>

      <div className="nav_button_box">
        <button className="nav_button">
          <img src={search} alt="make" className="btn_img" />
          <p className="btn_text">탐색</p>
        </button>
      </div>

      <div className="nav_button_box">
        <button
          className="nav_button"
          onClick={(e) => {
            handleNavigate("/feed_page");
            handleStopClick(e);
          }}
        >
          <img src={shortForm_img} alt="shorts" className="btn_img" />
          <p className="btn_text">숏피드</p>
        </button>
      </div>
    </div>
  );
};

export default NavBar;
