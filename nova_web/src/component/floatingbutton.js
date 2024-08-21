import React, { useState } from "react";
import Loundspeaker from "./loundspeaker";
// import "./App.css";

function FloatingButton({showSpeaker, setShowSpeaker}) {

  // let [showSpeaker, setShowSpeaker] = useState(false);

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
            <Loundspeaker></Loundspeaker>
          </div>
        )
      }
    </>
  );
}

export default FloatingButton;