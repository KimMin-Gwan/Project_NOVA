import { useEffect, useRef, useState } from "react";

export default function BiasBoxes() {
  const URL = "https://nova-platform.kr/home/";
  let bias_url = "https://kr.object.ncloudstorage.com/nova-images/";

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

  useEffect(() => {
    fetch(URL + "my_bias", {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        setMyBias(data.body.bias_list);
      })
      .catch((error) => {
        console.error("Fetch error:", error);
      });
  }, []);

  return (
    <div
      ref={scrollRef}
      onMouseDown={onMouseDown}
      onMouseMove={onMouseMove}
      onMouseUp={onMouseUp}
      className="bias-container"
    >
      <div className="bias-wrapper">
        {Array.from({ length: totalBiasBoxes }).map((_, i) => {
          const bias = myBias[i];
          return (
            <div key={i} className="bias-info">
              <div className="bias-box">
                {bias && <img src={bias_url + `${bias.bid}.PNG`} alt="bias" />}
              </div>
              <div className="b-name">{bias?.bname || <span>&nbsp;</span>}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
