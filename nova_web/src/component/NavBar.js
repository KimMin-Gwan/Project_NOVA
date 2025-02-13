import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import shortForm_img from "./../img/short_form2.png";
import moment from "./../img/moment_img.png";
import post from "./../img/post_img.png";
import menu3 from "./../img/fav_nav.png";
import feed_write from "./../img/feed_nav.png";
import search from "./../img/search_nav.png";
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
      {writeOptions && (
        <div className={`write_select ${writeOptions ? "active" : ""}`}>
          <h4>새로운 게시글 작성하기</h4>

          <section>
            <button
              onClick={() => {
                handleNavigate("/write_feed/short");
              }}
            >
              <div className="img-box">
                <img src={moment} alt="moment" />
              </div>
              모멘트
            </button>
            <button
              onClick={() => {
                handleNavigate("/write_feed/long");
              }}
            >
              <div className="img-box">
                <img src={post} alt="post" />
              </div>
              포스트
            </button>
          </section>

          <hr />

          <section>
            <button>주제 팔로우</button>
            <button>추가 기능</button>
          </section>
        </div>
      )}

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
