import React from "react";

import { useEffect, useLocation, useMemo, useRef, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import style from "./FollowPage.module.css";
import { getModeClass } from "./../../App.js";
import BiasBoxes from "../../component/BiasBoxes.js";
import logo2 from "./../../img/logo2.png";
import search_icon from "./../../img/search_icon.png";
import Stackframe from "./../../img/Stackframe.png";

export default function FollowPage() {
  const navigate = useNavigate(); // useNavigate 훅 사용

  const [params] = useSearchParams();
  const type = params.get("type");
  let [biasId, setBiasId] = useState();

  const brightModeFromUrl = params.get("brightMode");
  const initialMode = brightModeFromUrl || localStorage.getItem("brightMode") || "bright"; // URL에서 가져오고, 없으면 로컬 스토리지에서 가져옴
  const [mode, setMode] = useState(initialMode);

  let [feedData, setFeedData] = useState([]);
  let [nextData, setNextData] = useState([]);
  let [isLoading, setIsLoading] = useState(true);

  const [isModalOpen, setIsModalOpen] = useState(false);

  const openModal = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);

  let header = {
    "request-type": "default",
    "client-version": "v1.0.1",
    "client-ip": "127.0.0.1",
    uid: "1234-abcd-5678",
    endpoint: "/user_system/",
  };
  const FETCH_URL = "https://nova-platform.kr/feed_explore/";
  function fetchBiasCategoryData(bid) {
    let send_data = {
      header: header,
      body: {
        bid: bid || "",
        board: "",
        last_fid: "",
      },
    };
    // setIsLoading(true);
    if (type === "bias") {
      fetch(`${FETCH_URL}feed_with_community`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(send_data),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("first bias data", data);
          setFeedData(data.body.send_data);
          setNextData(data.body.last_fid);
          setIsLoading(false);
        });
    }
  }

  return (
    <div className="all-box">
      <div className={`${style["container"]} ${style[getModeClass(mode)]}`}>
        <header className={style.header}>
          <div className="logo">
            <img src={logo2} alt="logo" onClick={() => navigate("/")} />
          </div>
        </header>

        <h2 className={style["fav-title"]}>최애 팔로우</h2>
        <h3>
          <b>노바</b>에 등록된 <b>최애</b>를 소개합니다.
        </h3>

        <div className={style["following"]}>
          <h4>
            <b>팔로우</b> 중인 최애
          </h4>
          <BiasBoxes setBiasId={setBiasId} fetchBiasCategoryData={fetchBiasCategoryData} />
        </div>

        <div className={style["search-fac"]}>
          <div className={style["search-box"]}>
            <input type="text" placeholder="팔로우 하고 싶은 최애를 검색해보세요" />
            <img src={search_icon} alt="검색바" />
          </div>

          <button className={style["fav-apply"]}>
            <img src={Stackframe} alt="" />
            <span>
              <p>찾는 최애가 없다면 간편하게 신청해요!</p>
              <b>1분만에 최애 신청하기</b>
            </span>
          </button>
        </div>

        <div className={style["streamer-box"]}>
          <h4>치지직 스트리머</h4>
          <span className={style["streamer-list"]}>
            <button onClick={openModal} className={style["streamer-img"]}>
              <div>이미지</div>
              <p>우정잉</p>
            </button>
            <button onClick={openModal} className={style["streamer-img"]}>
              <div>이미지</div>
              <p>우정잉</p>
            </button>
            <button onClick={openModal} className={style["streamer-img"]}>
              <div>이미지</div>
              <p>우정잉</p>
            </button>
          </span>
          <span className={style["streamer-list"]}>
            <button onClick={openModal} className={style["streamer-img"]}>
              <div>이미지</div>
              <p>우정잉</p>
            </button>
            <button onClick={openModal} className={style["streamer-img"]}>
              <div>이미지</div>
              <p>우정잉</p>
            </button>
            <button onClick={openModal} className={style["streamer-img"]}>
              <div>이미지</div>
              <p>우정잉</p>
            </button>
          </span>
          <span className={style["streamer-list"]}>
            <button onClick={openModal} className={style["streamer-img"]}>
              <div>이미지</div>
              <p>우정잉</p>
            </button>
            <button onClick={openModal} className={style["streamer-img"]}>
              <div>이미지</div>
              <p>우정잉</p>
            </button>
            <button onClick={openModal} className={style["streamer-img"]}>
              <div>이미지</div>
              <p>우정잉</p>
            </button>
          </span>

          <button className={style["more-see"]}>더보기</button>

          {isModalOpen && (
            <div className={style["modal-overlay"]} onClick={closeModal}>
              <div className={style["modal"]} onClick={(e) => e.stopPropagation()}>
                <button onClick={openModal} className={style["streamer-img"]}>
                  <div>이미지</div>
                </button>
                <p>
                  라디유님을 <b>팔로우</b>합니다
                </p>
                <span>
                  <button onClick={closeModal}>취소</button>
                  <button className={style["follow-button"]}>팔로우</button>
                </span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
