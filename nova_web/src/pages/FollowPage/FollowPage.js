import React from "react";
import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";

import { getModeClass } from "./../../App.js";
import useBiasStore from "../../stores/BiasStore/useBiasStore.js";
import mainApi from "../../services/apis/mainApi.js";

import logo2 from "./../../img/logo2.png";

import FollowBoxes from "../../component/FollowBoxes.js";
import search_icon from "./../../img/search_icon.png";
import Stackframe from "./../../img/Stackframe.png";
import style from "./FollowPage.module.css";
import HEADER from "../../constant/header.js";
import { REQUEST_URL } from "../../constant/biasUrl.js";

const bias_url = "https://kr.object.ncloudstorage.com/nova-images/";
export default function FollowPage() {
  const navigate = useNavigate();
  let { biasList } = useBiasStore();

  const [params] = useSearchParams();
  let [biasId, setBiasId] = useState();

  const brightModeFromUrl = params.get("brightMode");
  const initialMode = brightModeFromUrl || localStorage.getItem("brightMode") || "bright"; // URL에서 가져오고, 없으면 로컬 스토리지에서 가져옴
  const [mode, setMode] = useState(initialMode);

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
      setBiasDataList(res.data.body);
      setIsLoading(false);
    });
  }

  useEffect(() => {
    fetchBiasFollowList();
  }, []);

  let send_data = {
    header: HEADER,
    body: {
      bid: clickedBid,
    },
  };
  function fetchTryFollowBias() {
    //console.log(clickedBid);
    fetch("https://nova-platform.kr/nova_sub_system/try_select_my_bias", {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(send_data),
    })
      .then((res) => {
        console.log(res);
        if (res.status === 401) {
          alert("로그인이 필요한 서비스입니다.");
          navigate("/novalogin");
          return Promise.reject();
        }
        return res.json();
      })
      .then((data) => {
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

  function handleRequestURL(url) {
    window.open(url, "_blank", "noopener, noreferrer");
  }

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
            <b>팔로우</b>중인 주제
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
            <p className={style["no_result"]}>검색 결과가 없어요</p>
          )}

          <button
            className={style["fav-apply"]}
            onClick={() => {
              handleRequestURL(REQUEST_URL);
            }}
          >
            <img src={Stackframe} alt="" />
            <span>
              <p>찾는 주제가 없다면 간편하게 신청해요!</p>
              <b>1분만에 주제 신청하기</b>
            </span>
          </button>
        </div>

        <Streamer title={"아티스트"} platform={biasDataList.artist} openModal={openModal} />
        <Streamer title={"치지직 스트리머"} platform={biasDataList.chzzk} openModal={openModal} />
        <Streamer title={"SOOP 스트리머"} platform={biasDataList.soop} openModal={openModal} />
        <Streamer title={"유튜버"} platform={biasDataList.youtube} openModal={openModal} />

        {isModalOpen && (
          <div className={style["modal-overlay"]} onClick={closeModal}>
            <div className={style["modal"]} onClick={(e) => e.stopPropagation()}>
              <button className={style["streamer-img"]}>
                <div>
                  <img src={bias_url + `${clickedBid}.PNG`} />
                </div>
              </button>
              <p>
                {clickedBname}님을{" "}
                <b>
                  {biasList.some((item) => {
                    return item.bid === clickedBid;
                  })
                    ? "팔로우 취소"
                    : "팔로우"}
                </b>
                합니다
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

function Streamer({ title, platform, openModal }) {
  if (platform.length === 0) {
    return null;
  }

  return (
    <div className={style["streamer-box"]}>
      <h4>{title}</h4>
      <span className={style["streamer-list"]}>
        {platform.map((bias, i) => {
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
  );
}
