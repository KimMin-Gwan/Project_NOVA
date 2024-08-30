import React, { useState, useEffect } from "react";
import Loundspeaker from "./loundspeaker";
// import "./App.css";

function FloatingButton({ showSpeaker, setShowSpeaker }) {

  // let [showSpeaker, setShowSpeaker] = useState(false);
  const [chattingData, setChattingData] = useState([]);
  let chattingList = [];

  useEffect(() => {
    fetch('http://nova-platform.kr/chatting_list')
      .then(res => res.json())
      .then(data => {
        chattingList = [...data.body.chatting_list];
        setChattingData(chattingList);
        console.log(chattingData);
      })
  }, [])

  const handleClick = () => {
    setShowSpeaker(!showSpeaker);
  };

  return (
    <>
      {
        !showSpeaker &&
        <button className="floating-button speaker-button" onClick={handleClick}>
          확성기
        </button>
      }
      {
        showSpeaker && (
          <div>
            <Loundspeaker chattingData={chattingData}></Loundspeaker>
          </div>
        )
      }
    </>
  );
}

export default FloatingButton;