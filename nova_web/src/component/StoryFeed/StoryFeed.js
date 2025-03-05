import { useNavigate } from "react-router-dom";
import style from "./StoryFeed.module.css";
export default function StoryFeed({ feedData, type, hasDragged }) {
  let navigate = useNavigate();

  function onClickFeed(fid) {
    navigate(`/feed_detail/${fid}`, { state: { commentClick: false } });
  }

  if (!feedData) {
    return <div>loading...</div>;
  }

  return (
    <div
      className={`${style["story_feed"]} ${style[`story_feed_${type}`]}`}
      onClick={() => {
        if (hasDragged) return;
        onClickFeed(feedData.feed.fid);
      }}
    >
      <div className={style["all-img"]}>
        <img
          src={
            feedData.feed?.image.length > 0
              ? feedData.feed.image[0]
              : "https://kr.object.ncloudstorage.com/nova-feed-images/nova-platform.png"
          }
          alt="이미지"
        />
      </div>
      <div className={style["all-text"]}>
        <p>{feedData.feed.body}</p>
      </div>
    </div>
  );
}
