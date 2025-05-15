import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";

import { getModeClass } from "../../App.js";
import WriteMoment from "../../pages/Write/Writemoment.js";

import more_see from "./../../img/more_see.png";
import moment from "./../../img/moment_img.png";
import post from "./../../img/post_img.png";
import short_form from "./../../img/short_form_icon.png";
import feed_write from "./../../img/feed_nav.png";
import search from "./../../img/search_nav.png";
import searchSchedule from "./../../img/search_schedule.svg";

import "./index.css";

const NavBar = ({ brightMode }) => {
  const navBarList = [
    {
      id: 0,
      title: "게시글",
      src: short_form,
      alt: "bias_board",
      // end_point: "/feed_list?type=bias",
      end_point: "/",
      type: "navigate",
      onClick: (endPoint) => handleNavigate(endPoint),
    },
    {
      id: 1,
      title: "일정",
      src: searchSchedule,
      alt: "schedule",
      end_point: "/schedule",
      type: "navigate",
      onClick: (endPoint) => handleNavigate(endPoint),
    },
    {
      id: 2,
      title: "추가",
      src: feed_write,
      alt: "write",
      end_point: "/feed_list?type=bias",
      type: "write",
      onClick: () => onClickWrite(),
    },
    {
      id: 3,
      title: "검색",
      src: search,
      alt: "search",
      end_point: "/search",
      type: "navigate",
      onClick: (endPoint) => handleNavigate(endPoint),
    },
    {
      id: 4,
      title: "더보기",
      src: more_see,
      alt: "bias_board",
      end_point: "/more_see",
      type: "navigate",
      onClick: (endPoint) => handleNavigate(endPoint),
    },
  ];

  let navigate = useNavigate();
  const location = useLocation(); //현재 경로 감지

  const [activeIndex, setActiveIndex] = useState(() => {
    return Number(sessionStorage.getItem("activeNav")) || 0;
  });
  let [writeOptions, setWriteOptions] = useState(false);

  const [writeMoment, setWriteMoment] = useState(false);
  useEffect(() => {
    const currentIndex = navBarList.findIndex((item) => item.end_point === location.pathname);
    setActiveIndex(currentIndex !== -1 ? currentIndex : 0);
    sessionStorage.setItem("activeNav", currentIndex !== -1 ? currentIndex : 0);
  }, [location.pathname]);

  useEffect(() => {
    const currentIndex = navBarList.findIndex((item) => item.end_point === location.pathname);

    if (!writeOptions && !writeMoment) {
      setActiveIndex(currentIndex);
      sessionStorage.removeItem("activeNav");
    }
  }, [writeOptions, writeMoment]);

  const onClickWrite = () => {
    setWriteOptions(!writeOptions);
  };

  function handleNavigate(path) {
    navigate(path);
  }

  function handleClickNav(index) {
    setActiveIndex(index);
    sessionStorage.setItem("activeNav", index);
  }

  // type이 write일 때만 다른 동작
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
    <div
      className={` ${writeOptions || writeMoment ? "nav-back" : ""}`}
      onClick={(e) => {
        if (writeMoment) {
          e.stopPropagation();
          e.preventDefault();
          setWriteMoment(false);
        } else if (writeOptions) {
          setWriteOptions(false);
        }
      }}
    >
      <div className={`bottom_bar ${getModeClass(mode)}`}>
        {writeOptions && (
          <div
            className={`write_select`}
            onClick={(e) => {
              e.stopPropagation();
            }}
          >
            <h4>새로운 게시글 작성하기</h4>

            <section>
              <button
                onClick={() => {
                  //onClickMoment();
                  handleNavigate("/write_feed");
                }}
              >
                <div className="img-box">
                  <img src={moment} alt="moment" />
                </div>
                새 게시글
              </button>

              <button
                onClick={() => {
                  handleNavigate("/schedule/make_new");
                }}
              >
                <div className="img-box">
                  <img src={post} alt="post" />
                </div>
                새 일정
              </button>
            </section>

            <section className="button_container">
              <button
                onClick={() => {
                  navigate("/follow_page");
                }}
              >
                주제 팔로우
              </button>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                }}
              >
                추가 기능
              </button>
            </section>
          </div>
        )}

        {writeMoment && <WriteMoment onClickMoment={onClickMoment} />}

        {navBarList.map((item, index) => (
          <div
            key={item.id}
            className={`nav_button_box ${activeIndex === index ? "btn_clicked" : ""}`}
          >
            <button
              className="nav_button"
              onClick={() => {
                handleClickNav(index);
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
