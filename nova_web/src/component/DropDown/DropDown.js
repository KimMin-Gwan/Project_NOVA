import { useState } from "react";
import "./index.css";

export default function DropDown({ options, setBiasId, setCategory }) {
  const [showTopic, setShowTopic] = useState(false);
  const [currentTopic, setCurrentTopic] = useState("선택 없음");

  function onClickTopic() {
    setShowTopic(!showTopic);
  }

  function onClickSelectTopic(e, bid, category) {
    setCurrentTopic(e.target.innerText);
    setShowTopic(!showTopic);
    if (setBiasId) {
      setBiasId(bid);
    } else if (setCategory) {
      setCategory(category);
    }
  }

  return (
    <>
      <label className="Select_box" onClick={onClickTopic}>
        {currentTopic}
      </label>
      <ul className={`${showTopic ? "Select_options_on" : "Select_options"}`}>
        <li onClick={onClickSelectTopic}>선택 없음</li>
        {options &&
          options.map((option, i) => {
            return (
              <li
                key={option.bid || option.key}
                value={option.bid || option.category}
                onClick={(e) => {
                  onClickSelectTopic(e, option.bid, option.category);
                }}
              >
                {option.bname || option.category}
              </li>
            );
          })}
      </ul>
    </>
  );
}
