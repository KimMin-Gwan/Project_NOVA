import { useState } from "react";
import style from "./ProgressBar.module.css";

function ProgressBar({ point, type }) {
  let [value, setValue] = useState(0);

  function updateValue(p) {
    setValue(p);
  }

  return (
    <div className={`${style["progress-container"]} ${style[`progress-container-${type}`]}`}>
      <div
        className={style["progress-bar"]}
        style={{ width: `${point}%` }}
        onChange={() => updateValue(point)}
      ></div>
    </div>
  );
}

export default ProgressBar;
