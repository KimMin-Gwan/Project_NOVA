import React from "react";
// import "./App.css";

function FloatingButton() {
  const handleClick = () => {
    alert("Floating button clicked!");
  };

  return (
    <button className="floating-button" onClick={handleClick}>
      +
    </button>
  );
}

export default FloatingButton;