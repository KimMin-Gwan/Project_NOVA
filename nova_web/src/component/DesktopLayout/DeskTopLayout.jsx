import { useState, useEffect } from 'react';
import style from './DeskTopLayout.module.css';

import top_logo from "./logo.svg";
import feed_icon from "./feed_icon.svg";
import date_icon from "./date_icon.svg";
import search_icon from "./search_icon.svg";
import right_arrow from "./right_arrow.svg";
import { useLocation, useNavigate } from 'react-router-dom';

export default function DesktopLayout({ children }) {
  const navigate = useNavigate();
  const [targetMenu, setTargetMenu] = useState("");

  const location = useLocation();

  function handleNavigate(path) {
    navigate(path);
  }

  useEffect(()=>{
    setTargetMenu(location.pathname);
  }, [location.pathname])

  const actionButtons = [
    {
        title: "게시글 작성",
        end_point : "/write_feed",
        alt: "write_feed"
    },
    {
        title: "컨텐츠 일정 등록",
        end_point : "/schedule/make_new",
        alt: "schedule_make_new"
    }
  ];

  const menuData = [
    {
      title: "게시판",
      icon: feed_icon,
      end_point : "/",
      alt: "bias_board",
      items: [],
    },
    {
      title: "콘텐츠 일정",
      icon: date_icon,
      items: [
            {
                title: "구독 중인 콘텐츠", 
                end_point : "/schedule",
                alt: "schedule"
            },
            {
                title: "콘텐츠 탐색",
                end_point : "/explore/schedule",
                alt: "bias_board"
            }
      ],
    },
    {
      title: "검색",
      icon: search_icon,
      end_point: "/search",
      items: [],
    },
    {
      title: "기타",
      icon: null,
      end_point: "/etc",
      items: [
            {
                title: "주제 팔로우",
                end_point : "/follow_page",
                alt: "follow_page"
            },
            {
                title: "공지 사항",
                end_point : "/notice",
                alt: "notice"
            },
            {
                title: "이용 약관",
                end_point : "/terms_page",
                alt: "terms_page"
            },
    ],
      isSub: true,
    },
  ];

  const renderMenuGroup = (title, end_point, icon, items, isSub = false) => (
    <div className={style["side-bar-menu-wrapper"]}>
      {title && icon && (
        <div 
            className={`${style["side-bar-menu-title"]} ${end_point === targetMenu ? style["active"] : ""}`}
            style={{
                background : end_point==targetMenu? "#D9ECFE" : "none"
            }}
            onClick={() => {
              handleNavigate(end_point);
            }}
        >
          <img src={icon} className={style["side-bar-icon"]} />
          {title}
        </div>
      )}
      {isSub && <div className={style["side-bar-sub-menu-separater"]}></div>}
      {items.map((item, idx) => (
        <div
          key={idx}
          className={`
            ${style[isSub ? "side-bar-sub-menu" : "side-bar-menu"]}
            ${item.end_point === targetMenu ? style["active"] : ""}
          `}
          onClick={() => {
            handleNavigate(item.end_point);
          }}
        >
          {item.title}
          <div className={style["side-bar-icon"]}>
            <img src={right_arrow} />
          </div>
        </div>
      ))}
    </div>
  );

  return (
    <div className={style["desktop-page-background"]}>
      {/* Top bar */}
      <div className={style["top-bar-frame"]}>
        <div className={style["top-bar-inner"]}>
            <div className={style["top-bar-logo-box"]}>
                <img src={top_logo} />
            </div>
            <div className={style["sign-button-wrapper"]}>
                <div className={style["sign-up-button"]}>회원가입</div>
                <div className={style["sign-in-button"]}>로그인</div>
            </div>
        </div>
      </div>

      {/* Main layout */}
      <div className={style["middle-frame"]}>
        {/* Sidebar */}
        <div className={style["side-bar-frame"]}>
          <div className={style["side-bar-top-component"]}>
            {/* Action buttons */}
            <div className={style["add-new-button-wrapper"]}>
              {actionButtons.map((btn, i) => (
                <div key={btn.title} 
                  className={`${style["add-new-button"]} ${btn.end_point == targetMenu ? style["active"] : ""}`}
                  onClick={() => {
                    handleNavigate(btn.end_point);
                  }}
                >
                  {btn.title}
                </div>
              ))}
            </div>

            <div className={style["separate-line"]}></div>

            {/* Menu groups */}
            {menuData.map((group, i) =>
              renderMenuGroup(group.title, group.end_point, group.icon, group.items, group.isSub)
            )}
          </div>

          {/* Footer */}
          <div className={style["side-bar-footer-wrapper"]}>
            <div className={style["side-bar-footer-box"]}>
              <div className={style["team-name"]}>Team SUPERNOVA</div>
              <div className={style["footer-body-wrapper"]}>
                <div className={style["footer-body"]}>대표 : 김민관</div>
                <div className={style["footer-body"]}>youth0828@naver.com</div>
              </div>
            </div>
            <div className={style["copyright"]}>
              @ 2025 TEAM SUPERNOVA. All rights reserved.
            </div>
          </div>
        </div>

        {/* Main content */}
        <div className={style["main-frame"]}>
          {children}
        </div>
      </div>
    </div>
  );
}

