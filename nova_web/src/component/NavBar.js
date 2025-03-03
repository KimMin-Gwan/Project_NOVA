import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import { getModeClass } from "./../App.js";
import WriteMoment from "../pages/Write/Writemoment.js";

import more_see from "./../img/more_see.png";
import moment from "./../img/moment_img.png";
import post from "./../img/post_img.png";
import short_form from "./../img/short_form_icon.png";
import feed_write from "./../img/feed_nav.png";
import search from "./../img/search_nav.png";

const NavBar = ({ brightMode }) => {
  const navBarList = [
    {
      id: 0,
      title: "최애 게시판",
      src: short_form,
      alt: "bias_board",
      end_point: "/feed_list?type=bias",
      type: "navigate",
      onClick: (endPoint) => handleNavigate(endPoint),
    },
    {
      id: 1,
      title: "피드 작성",
      src: feed_write,
      alt: "write",
      end_point: "/feed_list?type=bias",
      type: "write",
      onClick: () => onClickWrite(),
    },
    {
      id: 2,
      title: "검색",
      src: search,
      alt: "search",
      end_point: "/search",
      type: "navigate",
      onClick: (endPoint) => handleNavigate(endPoint),
    },
    {
      id: 3,
      title: "더보기",
      src: more_see,
      alt: "bias_board",
      end_point: "/more_see",
      type: "navigate",
      onClick: (endPoint) => handleNavigate(endPoint),
    },
  ];

  let navigate = useNavigate();

  let [writeOptions, setWriteOptions] = useState(false);

  const [writeMoment, setWriteMoment] = useState(false);

  const onClickWrite = () => {
    setWriteOptions(!writeOptions);
  };

  function handleNavigate(path) {
    navigate(path);
  }

  function handleAction(type, endPoint) {
    if (type === "write") {
      onClickWrite();
    } else {
      handleNavigate(endPoint);
    }
  }

  const onClickMoment = () => {
    setWriteMoment(!writeMoment);
  };

  const [mode, setMode] = useState(brightMode); // 초기 상태는 부모로부터 받은 brightMode 값
  useEffect(() => {
    setMode(brightMode); // brightMode 값이 바뀔 때마다 mode 업데이트
  }, [brightMode]);

  return (
    <div className={` ${writeOptions || writeMoment ? "nav-back" : ""}`}>
      <div className={`bottom_bar ${getModeClass(mode)}`}>
        {writeOptions && (
          <div className={`write_select ${writeOptions ? "active" : ""}`}>
            <h4>새로운 게시글 작성하기</h4>

            <section>
              <button
                onClick={() => {
                  setWriteOptions(!writeOptions);
                  onClickMoment();
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

            <section>
              <button>주제 팔로우</button>
              <button>추가 기능</button>
            </section>
          </div>
        )}

        {writeMoment && <WriteMoment onClickMoment={onClickMoment} />}

        {navBarList.map((item) => (
          <div className="nav_button_box">
            <button
              className="nav_button"
              onClick={(e) => {
                handleAction(item.type, item.end_point);
              }}
            >
              <img src={item.src} alt={item.alt} className="btn_img" />
              <p className="btn_text">{item.title}</p>
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default NavBar;
