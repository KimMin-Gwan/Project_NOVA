import "./index.css";
import heart_icon from "./../../img/heart.png";

export default function NoneFindFeed() {
  return (
    <div className="NoneFeed">
      <div className="heart-icon">
        <img src={heart_icon} alt="heart" />
      </div>
      <p>발견된 댓글이 없어요</p>
    </div>
  );
}