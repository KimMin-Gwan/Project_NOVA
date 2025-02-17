import React from "react";

import { useEffect, useLocation, useMemo, useRef, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import style from "./FollowPage.module.css";
import { getModeClass } from "./../../App.js";
import FollowBoxes from "../../component/FollowBoxes.js";
import logo2 from "./../../img/logo2.png";
import search_icon from "./../../img/search_icon.png";
import Stackframe from "./../../img/Stackframe.png";
import mainApi from "../../services/apis/mainApi.js";
import postApi from "../../services/apis/postApi.js";
import useBiasStore from "../../stores/BiasStore/useBiasStore.js";

const bias_url = "https://kr.object.ncloudstorage.com/nova-images/";
export default function FollowPage() {
  const navigate = useNavigate();
  let { biasList } = useBiasStore();

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
  let header = {
    "request-type": "default",
    "client-version": "v1.0.1",
    "client-ip": "127.0.0.1",
    uid: "1234-abcd-5678",
    endpoint: "/user_system/",
  };

  let send_data = {
    header: header,
    body: {
      bid: clickedBid,
    },
  };
  function fetchTryFollowBias() {
    console.log(clickedBid);
    fetch("https://nova-platform.kr/nova_sub_system/try_select_my_bias", {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(send_data),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        if (biasList.some((item) => item.bid === clickedBid)) {
          alert("팔로우 취소 완료");
        } else {
          alert("팔로우 완료!");
        }
        setIsModalOpen(false);
        window.location.reload();
      })
      .catch((err) => {
        console.log("err", err);
      });

    // postApi
    //   .post("nova_sub_system/try_select_my_bias", {
    //     send_data,
    //   })
    //   .then((res) => {
    //     console.log(res.data);
    //   });
  }
  const [searchBias, setSearchBias] = useState("");
  const [resultBias, setResultBias] = useState([]);
  const [resultLength, setResultLength] = useState(1);

  function fetchSearchBias() {
    mainApi.get(`nova_sub_system/try_search_bias?bname=${searchBias}`).then((res) => {
      let biasCount = res.data.body.biases.length;
      setResultLength(biasCount);
      setResultBias(res.data.body.biases);
    });
  }
  // useEffect(() => {
  //   fetchSearchBias();
  // }, [searchBias]);
  function onKeyDown(e) {
    if (e.key === "Enter") {
      fetchSearchBias();
    }
  }

  function onChangeSearchBias(e) {
    setSearchBias(e.target.value);
  }

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

        <h2 className={style["fav-title"]}>주제 팔로우</h2>
        <h3>
          <b>노바</b>에 등록된 <b>주제</b>를 소개합니다.
        </h3>

        <div className={style["following"]}>
          <h4>
            <b>팔로우</b> 중인 주제
          </h4>
          <FollowBoxes setBiasId={setBiasId} />
        </div>

        <div className={style["search-fac"]}>
          <div className={style["search-box"]}>
            <input
              type="text"
              onKeyDown={onKeyDown}
              value={searchBias}
              onChange={(e) => {
                onChangeSearchBias(e);
              }}
              placeholder="팔로우 하고 싶은 주제를 검색해보세요"
            />
            <img src={search_icon} onClick={fetchSearchBias} alt="검색바" />
          </div>
          {resultLength !== 0 ? (
            <div className={style["streamer-box"]}>
              <span className={style["streamer-list"]}>
                {resultBias.map((bias, i) => {
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
            </div>
          ) : (
            <p>검색 결과 없음 {resultLength}</p>
          )}

          <button className={style["fav-apply"]}>
            <img src={Stackframe} alt="" />
            <span>
              <p>찾는 주제가 없다면 간편하게 신청해요!</p>
              <b>1분만에 주제 신청하기</b>
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
                <button className={style["follow-button"]} onClick={fetchTryFollowBias}>
                  {biasList.some((item) => {
                    return item.bid === clickedBid;
                  })
                    ? "팔로우 취소"
                    : "팔로우"}
                </button>
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
