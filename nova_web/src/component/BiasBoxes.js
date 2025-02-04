import { useEffect, useRef, useState } from "react";
import useBiasStore from "../stores/BiasStore/useBiasStore";
import useLoginStore from "../stores/LoginStore/useLoginStore";

export default function BiasBoxes({ setBiasId, fetchBiasCategoryData, writeCommunity }) {
  const URL = "https://nova-platform.kr/home/";
  let bias_url = "https://kr.object.ncloudstorage.com/nova-images/";

  const { isLogin, isLogout } = useLoginStore();
  let { biasList, loading, fetchBiasList } = useBiasStore();

  useEffect(() => {
    if (isLogin === "done") {
      fetchBiasList();
      console.log("isLogin", isLogin);
    }
  }, []);

  function onClickBiasId(bid) {
    setBiasId(bid);
  }

  const defaultBoxes = 4;
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

  return (
    <div
      ref={scrollRef}
      onMouseDown={onMouseDown}
      onMouseMove={onMouseMove}
      onMouseUp={onMouseUp}
      className="bias-container"
    >
      <div className="bias-wrapper">
        {writeCommunity && (
          <div className="bias-info">
            <div className="bias-box">
              <div
                className="non-bias"
                onClick={() => {
                  // onClickBiasId(bias.bid);
                  // fetchBiasCategoryData && fetchBiasCategoryData(bias.bid);
                }}
              >
                선택 없음
              </div>
            </div>
            <div className="b-name">
              <span>&nbsp;</span>
            </div>
          </div>
        )}

        {Array.from({ length: totalBiasBoxes }).map((_, i) => {
          const bias = biasList[i];
          return (
            <div key={i} className="bias-info">
              <div className="bias-box">
                {bias && (
                  <img
                    src={bias_url + `${bias.bid}.PNG`}
                    alt="bias"
                    onClick={() => {
                      onClickBiasId(bias.bid);
                      fetchBiasCategoryData && fetchBiasCategoryData(bias.bid);
                    }}
                  />
                )}
              </div>
              <div className="b-name">{bias?.bname || <span>&nbsp;</span>}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
