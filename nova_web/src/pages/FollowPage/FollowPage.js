import React from "react";

import { useEffect, useLocation, useMemo, useRef, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import style from "./FollowPage.module.css";
import { getModeClass } from "./../../App.js";
import BiasBoxes from "../../component/BiasBoxes.js";
import logo2 from "./../../img/logo2.png";
import search_icon from "./../../img/search_icon.png";
import Stackframe from "./../../img/Stackframe.png";
import mainApi from "../../services/apis/mainApi.js";

const bias_url = "https://kr.object.ncloudstorage.com/nova-images/";
export default function FollowPage() {
  const navigate = useNavigate();

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

  const openModal = (bid, bname) => {
    setClickedBname(bname);
    setClickedBid(bid);
    setIsModalOpen(true);
  };
  const closeModal = () => setIsModalOpen(false);

  const [biasDataList, setBiasDataList] = useState([]);
  const [clickedBid, setClickedBid] = useState();
  const [clickedBname, setClickedBname] = useState();

  function fetchBiasFollowList() {
    mainApi.get("nova_sub_system/get_bias_follow_page_data").then((res) => {
      console.log(res.data);
      setBiasDataList(res.data.body);
      setIsLoading(false);
    });
  }

  useEffect(() => {
    fetchBiasFollowList();
  }, []);

  if (isLoading) {
    return <div>loading...</div>;
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
          <BiasBoxes setBiasId={setBiasId} />
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
          <h4>아티스트</h4>
          <span className={style["streamer-list"]}>
            {biasDataList.artist.map((bias, i) => {
              return (
                <button
                  key={bias.bid}
                  onClick={() => {
                    openModal(bias.bid, bias.bname);
                  }}
                  className={style["streamer-img"]}
                >
                  <div>
                    <img src={bias_url + `${bias.bid}.PNG`} />
                  </div>
                  <p>{bias.bname}</p>
                </button>
              );
            })}
          </span>
          <button className={style["more-see"]}>더보기</button>
        </div>

        {biasDataList.chzzk.length > 0 && (
          <div className={style["streamer-box"]}>
            <h4>치지직 스트리머</h4>
            <span className={style["streamer-list"]}>
              {biasDataList.chzzk.map((bias, i) => {
                return (
                  <button
                    key={bias.bid}
                    onClick={() => {
                      openModal(bias.bid, bias.bname);
                    }}
                    className={style["streamer-img"]}
                  >
                    <div>
                      <img src={bias_url + `${bias.bid}.PNG`} />
                    </div>
                    <p>{bias.bname}</p>
                  </button>
                );
              })}
            </span>
            <button className={style["more-see"]}>더보기</button>
          </div>
        )}

        <div className={style["streamer-box"]}>
          <h4>SOOP 스트리머</h4>
          <span className={style["streamer-list"]}>
            {biasDataList.soop.map((bias, i) => {
              return (
                <button
                  key={bias.bid}
                  onClick={() => {
                    openModal(bias.bid, bias.bname);
                  }}
                  className={style["streamer-img"]}
                >
                  <div>
                    <img src={bias_url + `${bias.bid}.PNG`} />
                  </div>
                  <p>{bias.bname}</p>
                </button>
              );
            })}
          </span>
          <button className={style["more-see"]}>더보기</button>
        </div>

        <div className={style["streamer-box"]}>
          <h4>유튜버</h4>
          <span className={style["streamer-list"]}>
            {biasDataList.youtube.map((bias, i) => {
              return (
                <button
                  key={bias.bid}
                  onClick={() => {
                    openModal(bias.bid, bias.bname);
                  }}
                  className={style["streamer-img"]}
                >
                  <div>
                    <img src={bias_url + `${bias.bid}.PNG`} />
                  </div>
                  <p>{bias.bname}</p>
                </button>
              );
            })}
          </span>
          <button className={style["more-see"]}>더보기</button>
        </div>

        {isModalOpen && (
          <div className={style["modal-overlay"]} onClick={closeModal}>
            <div className={style["modal"]} onClick={(e) => e.stopPropagation()}>
              <button className={style["streamer-img"]}>
                <div>
                  <img src={bias_url + `${clickedBid}.PNG`} />
                </div>
              </button>
              <p>
                {clickedBname}님을 <b>팔로우</b>합니다
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
  );
}
