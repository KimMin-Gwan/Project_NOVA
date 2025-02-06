import "./index.css";
import heart_icon from "./../../img/heart.png";

export default function NoneFeed() {
  return (
    <div className="NoneFeed">
      <div className="heart-icon">
        <img src={heart_icon} alt="heart" />
      </div>
      <p>아직 작성된 게시물이 없어요</p>
    </div>
  );
}
