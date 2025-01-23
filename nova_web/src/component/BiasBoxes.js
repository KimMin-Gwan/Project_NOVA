import { useEffect, useRef, useState } from "react";

export default function BiasBoxes({ setBiasId, fetchBiasCategoryData, writeCommunity }) {
  const URL = "https://nova-platform.kr/home/";
  let bias_url = "https://kr.object.ncloudstorage.com/nova-images/";
  let [isLoading, setIsLoading] = useState(true);

  async function fetchBiasData() {
    await fetch(`${URL}my_bias`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("bias_data", data);
        setMyBias(data.body.bias_list);
        setIsLoading(false);
      })
      .catch((error) => {
        console.error("Fetch error:", error);
      });
  }

  useEffect(() => {
    fetchBiasData();
  }, []);

  function onClickBiasId(bid) {
    setBiasId(bid);
  }

  let [myBias, setMyBias] = useState([]);
  const defaultBoxes = 4;
  const totalBiasBoxes = Math.max(defaultBoxes, myBias.length);

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

  if (isLoading) {
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
              {" "}
              <span>&nbsp;</span>
            </div>
          </div>
        )}

        {Array.from({ length: totalBiasBoxes }).map((_, i) => {
          const bias = myBias[i];
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
