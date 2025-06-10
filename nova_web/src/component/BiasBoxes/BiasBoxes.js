import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import toast, { Toaster } from "react-hot-toast";

import { BIAS_URL } from "../../constant/biasUrl";
import useBiasStore from "../../stores/BiasStore/useBiasStore";
import useLoginStore from "../../stores/LoginStore/useLoginStore";
import useDragScroll from "../../hooks/useDragScroll";
import add_bias_icon from "./../../img/add_bias.png";
import tempBias from "./../../img/tempBias.png";

import "./index.css";

export default function BiasBoxes({ fetchBiasCategoryData }) {
  const navigate = useNavigate();
  const { scrollRef, hasDragged, dragHandlers } = useDragScroll();
  let { biasList, biasId, setBiasId, loading, fetchBiasList } = useBiasStore();

  const { isLogin } = useLoginStore();
  useEffect(() => {
    fetchBiasList();
    if (isLogin === "done") {
      fetchBiasList();
    }
  }, []);

  const [clickedBias, setClickedBias] = useState(0);

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
      navigate("/novalogin");
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
    return null;
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
                <div className="bias-box">
                  {bias && (
                    <img
                      className={clickedBias === i ? "clicked-img" : ""}
                      src={BIAS_URL + `${bias.bid}.png`}
                      onError={(e) => (e.target.src = tempBias)}
                      alt="bias"
                      onClick={() => {
                        if (hasDragged) return;
                        onClickCurrentBias(i);
                        onClickBiasId(bias.bid);
                        fetchBiasCategoryData && fetchBiasCategoryData(bias.bid);
                      }}
                    />
                  )}
                </div>
                <div className="b-name">{bias?.bname || <span>&nbsp;</span>}</div>
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
      <div className="b-name">주제 추가하기</div>
    </div>
  );
}
