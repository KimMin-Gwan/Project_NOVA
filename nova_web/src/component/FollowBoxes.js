import { useEffect, useRef, useState } from "react";
import useBiasStore from "../stores/BiasStore/useBiasStore";
import useLoginStore from "../stores/LoginStore/useLoginStore";
import add_bias_icon from "./../img/add_bias.png";
import { useNavigate } from "react-router-dom";
import style from "./FollowBoxes.module.css";
import tempBias from "./../img/tempBias.png";

export default function FollowBoxes({ setBiasId }) {
  let bias_url = "https://kr.object.ncloudstorage.com/nova-images/";

  const navigate = useNavigate();
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
  const { isLogin, isLogout } = useLoginStore();
  let { biasList, loading, fetchBiasList } = useBiasStore();

  useEffect(() => {
    //console.log(biasList.length);
    fetchBiasList();
    if (isLogin === "done") {
      fetchBiasList();
      //console.log("isLogin", isLogin);
    }
  }, []);

  const [clickedBias, setClickedBias] = useState(0);

  function onClickBiasId(bid) {
    setBiasId(bid);
  }

  function onClickCurrentBias(i) {
    setClickedBias(i);
  }

  const defaultBoxes = 1;
  const totalBiasBoxes = Math.max(defaultBoxes, biasList.length);

  let scrollRef = useRef(null);
  let [isDrag, setIsDrag] = useState(false);
  let [dragStart, setDragStart] = useState("");
  let [hasDragged, setHasDragged] = useState(false);

  function onMouseDown(e) {
    e.preventDefault();
    setIsDrag(true);
    setDragStart(e.pageX + scrollRef.current.scrollLeft);
    setHasDragged(false);
  }

  function onMouseUp(e) {
    if (hasDragged) {
      e.stopPropagation();
      e.preventDefault();
    }
    setIsDrag(false);
  }

  function onMouseMove(e) {
    if (isDrag) {
      scrollRef.current.scrollLeft = dragStart - e.pageX;
      setHasDragged(true);
    }
  }

  if (loading) {
    return <div>loading...</div>;
  }
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

  async function fetchTryFollowBias() {
    await mainApi.get( `nova_sub_system/try_follow_bias?bid=${clickedBid}`
    ).then((res) => {
      if (res.status === 401) {
        alert("로그인이 필요한 서비스입니다.");
        navigate("/novalogin");
        return Promise.reject("Unauthorized: 로그인 필요");
      }
      return res.data;
    }).then((data) =>{
        if (biasList.some((item) => item.bid === clickedBid)) {
          alert("팔로우 취소 완료");
        } else {
          alert("팔로우 완료!");
        }
        setIsModalOpen(false);
        window.location.reload();
    }) .catch(err => {
        console.error("Error | ", err);
    });
  }

  if (biasList.length === 0) {
    return (
      <div className="bias-container">
        <div style={{display:"flex", margin:"20px", width:"100%", height:"60px", justifyContent:"center", alignItems:"center",}}>
          <div style={{fontSize:"16px", fontWeight:"600", color:"#111"}}>
            팔로우한 주제가 없어요!
          </div>
        </div>
      </div>
    );
  }

  return (
    <div >
    <div
      ref={scrollRef}
      onMouseDown={onMouseDown}
      onMouseMove={onMouseMove}
      onMouseUp={onMouseUp}
      className="bias-container"
    >
      <div className="bias-wrapper">
        {Array.from({ length: totalBiasBoxes }).map((_, i) => {
          const bias = biasList[i];
          return (
            <div key={i} className="bias-info">
              <div className={style["bias-box"]}>
                {bias && (
                  <img
                    src={bias_url + `${bias.bid}.png`}
                    alt="bias"
                    onError={(e) => (e.target.src = tempBias)}
                    onClick={() => {
                      onClickCurrentBias(i);
                      onClickBiasId(bias.bid);
                      openModal(bias.bid, bias.bname);
                    }}
                  />
                )}
              </div>
              <div className="b-name">{bias?.bname || <span>&nbsp;</span>}</div>
            </div>
          );
        })}

        {isModalOpen && (
          <div className={style["modal-overlay"]} onClick={closeModal}>
            <div className={style["modal"]} onClick={(e) => e.stopPropagation()}>
              <button className={style["streamer-img"]}>
                <div>
                  <img src={bias_url + `${clickedBid}.png`} />
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

    </div>
  );
}
