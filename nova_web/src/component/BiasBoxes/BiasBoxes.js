import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import toast, { Toaster } from "react-hot-toast";

import { BIAS_URL, DEFAULT_BIAS_URL } from "../../constant/biasUrl";
import useBiasStore from "../../stores/BiasStore/useBiasStore";
import useLoginStore from "../../stores/LoginStore/useLoginStore";
import useDragScroll from "../../hooks/useDragScroll";
import add_bias_icon from "./../../img/add_bias.png";
import tempBias from "./../../img/tempBias.png";
import biasBadge from "./bias_badge.svg";

import "./index.css";

export default function BiasBoxes({ fetchBiasCategoryData, fecthDefaultSetting }) {
  const navigate = useNavigate();
  const location = useLocation();
  const { scrollRef, hasDragged, dragHandlers } = useDragScroll();
  let { biasList, biasId, setBiasId, loading, fetchBiasList } = useBiasStore();

  const { isLogin } = useLoginStore();
  useEffect(() => {
    fetchBiasList();
    if (isLogin === "done") {
      fetchBiasList();
    }
  }, []);

  const [clickedBias, setClickedBias] = useState(-1);

  function onClickBiasId(bid) {
    setBiasId(bid);
  }

  function onClickCurrentBias(i) {
    setClickedBias(i);
  }

  let [isUserState, setIsUserState] = useState(false);
  function handleValidCheck() {
    fetch("https://supernova.io.kr/home/is_valid", {
      credentials: "include",
    })
      .then((response) => {
        if (response.status === 200) {
          setIsUserState(true);
          return response.json();
        } else {
          setIsUserState(false);
          return Promise.reject();
        }
      })
      .catch((error) => {
        setIsUserState(false);
      });
  }

  useEffect(() => {
    handleValidCheck();
  }, []);

  const defaultBoxes = 1;
  const totalBiasBoxes = Math.max(defaultBoxes, biasList.length);

  function onClickAddButton() {
    if (isUserState) {
      navigate("/follow_page");
    } else {
      navigate("/novalogin", { state: { from: location.pathname } });
    }
  }

  useEffect(() => {
    if (loading) {
      toast.loading("loading...");
    } else {
      toast.dismiss();
    }
  }, [loading]);

  if(biasList.length === 0){
    return (
      <div
        ref={scrollRef}
        onMouseDown={dragHandlers.onMouseDown}
        onMouseMove={dragHandlers.onMouseMove}
        onMouseUp={dragHandlers.onMouseUp}
        className="bias-container"
      >
        <Toaster position="bottom-center" />
        <div className="bias-wrapper">
          <AddBiasButton onClickAddButton={onClickAddButton} add_bias_icon={add_bias_icon} />
        </div>
      </div>
    );
  }else{
    return (
      <div
        ref={scrollRef}
        onMouseDown={dragHandlers.onMouseDown}
        onMouseMove={dragHandlers.onMouseMove}
        onMouseUp={dragHandlers.onMouseUp}
        className="bias-container"
      >
        <Toaster position="bottom-center" />
        <div className="bias-wrapper">
          {Array.from({ length: totalBiasBoxes }).map((_, i) => {
            const bias = biasList[i];
            return (
              <div key={i} className="bias-info">
                <div className={clickedBias === i ? "clicked_bias" : "bias-box"}>
                  {bias && (
                    <img
                      src={BIAS_URL + `${bias.bid}.png`}
                        onError={(e) => {
                            e.currentTarget.onerror = null; // 무한 루프 방지
                            e.currentTarget.src = DEFAULT_BIAS_URL;
                        }}
                      alt="bias"
                      onClick={() => {
                        if (hasDragged) return;
                        if (clickedBias == i){
                          onClickCurrentBias(-1);
                          onClickBiasId("");
                          fecthDefaultSetting();
                        }else{
                          onClickCurrentBias(i);
                          onClickBiasId(bias.bid);
                          fetchBiasCategoryData && fetchBiasCategoryData(bias.bid);
                        }
                      }}
                    />
                  )}
                </div>
                <div className={"bias-info-wrapper"}>
                  <img className={"bias-badge-svg"} src={biasBadge}
                    style={{ display: bias.state == "CONFIRMED" ? "" : "none"  }}
                   />
                  <div className="b-name">{bias?.bname || <span>&nbsp;</span>}</div>
                </div>
                <div className={clickedBias === i ? "clicked-box" : "non-clicked-box"}></div>
              </div>
            );
          })}
          <AddBiasButton onClickAddButton={onClickAddButton} add_bias_icon={add_bias_icon} />
        </div>
      </div>
    );
  }
}

function AddBiasButton({ onClickAddButton, add_bias_icon }) {
  return (
    <div className="bias-info">
      <button
        className="add-bias-box"
        onClick={() => {
          onClickAddButton();
        }}
      >
        <img src={add_bias_icon} alt="add-bias" />
      </button>
      <div className="b-name"></div>
    </div>
  );
}
