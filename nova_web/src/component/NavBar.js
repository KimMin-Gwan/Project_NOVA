import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import fund_img from "./../img/funding.png";
import menuBtn_img from "./../img/menuBtn.png";
import galaxy_img from "./../img/galaxy3.png";
import shortForm_img from "./../img/short_form2.png";
import new_feed from "./../img/new_feed2.png";
import moment from "./../img/moment_img.png";
import post from "./../img/post_img.png";

import home_icon from "./../img/home_icon.png";
import menu3 from "./../img/menu3.png";
import feed_write from "./../img/feed_write.png";
import search from "./../img/search.png";
import { getModeClass } from "./../App.js";

const NavBar = ({ isUserState, brightMode }) => {
  const [isVisible, setIsVisible] = useState(false);

  let navigate = useNavigate();

  let [writeOptions, setWriteOptions] = useState(false);

  const onClickWrite = () => {
    setWriteOptions(!writeOptions);
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
        <button
          className="nav_button"
          onClick={(e) => {
            handleNavigate("/feed_list?type=bias");
            handleStopClick(e);
          }}
        >
          <img src={menu3} alt="make" className="btn_img" />
          <p className="btn_text">최애 게시판</p>
        </button>
      </div>

      <div className="nav_button_box write_button_hover">
        {writeOptions && (
          <div className="write_select">
            <div
              onClick={() => {
                handleNavigate("/write_feed/short");
              }}
            >
              <div className="img-box">
                <img src={moment} alt="moment" />
              </div>
              모멘트
            </div>
            <div
              onClick={() => {
                handleNavigate("/write_feed/long");
              }}
            >
              <div className="img-box">
                <img src={post} alt="post" />
              </div>
              포스트
            </div>
          </div>
        )}
        <button
          className="nav_button"
          onClick={(e) => {
            onClickWrite();
            handleStopClick(e);
          }}
        >
          <img src={feed_write} alt="make" className="btn_img" />
          <p className="btn_text">피드 작성</p>
        </button>
      </div>

      <div className="nav_button_box">
        <button
          className="nav_button"
          onClick={(e) => {
            handleNavigate("/search");
            handleStopClick(e);
          }}
        >
          <img src={search} alt="make" className="btn_img" />
          <p className="btn_text">검색</p>
        </button>
      </div>

      <div className="nav_button_box">
        <button
          className="nav_button"
          onClick={(e) => {
            handleNavigate("/more_see");
            handleStopClick(e);
          }}
        >
          <img src={shortForm_img} alt="shorts" className="btn_img" />
          <p className="btn_text">더보기</p>
        </button>
      </div>
    </div>
  );
};

export default NavBar;
