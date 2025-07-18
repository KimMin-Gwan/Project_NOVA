import Styles from "./Card.module.css";
import React, { useState } from "react";
import { useSpring, animated } from "react-spring";

function Card({ imagen, title, body }) {
  const url = "https://supernova.io.kr/content";
  const [show, setShown] = useState(false);

  const props3 = useSpring({
    transform: show ? "scale(1.03)" : "scale(1)",
    boxShadow: show
      ? "0 20px 25px rgb(0 0 0 / 25%)"
      : "0 2px 10px rgb(0 0 0 / 8%)"
  });
  return (
    <animated.div
      className={Styles.card}
      style={props3}
      onMouseEnter={() => setShown(true)}
      onMouseLeave={() => setShown(false)}
    >
      <img src={imagen} alt="" />
      <h2>{title}</h2>
      <p>
        {body}
      </p>
      <div className={Styles.btnn}>
        <div className={Styles.customButton}
          onClick={() => window.open(url, "_blank")}
        >
          바로가기
        </div>
      </div>
    </animated.div>
  );
}

export default Card;