import style from "./Comments.module.css";
import arrow from "./../../img/comment_arrow.svg";
import reArrow from "./../../img/recomment.svg";
import { useState } from "react";
import MyPageLoading from "../../pages/LoadingPage/MypageLoading";
import NoneFeed from "../NoneFeed/NoneFeed";

export default function Comments({ comments, isLoading }) {
  const [clickedComments, setClickedComments] = useState({});
  const [isClickedComment, setIsClickedComment] = useState(false);
  const handleCommentToggle = (id) => {
    setClickedComments((prev) => ({
      ...prev,
      [id]: !prev[id],
    }));
  };

  if (isLoading) {
    return <MyPageLoading />;
  }

  if (comments.length === 0) {
    return <NoneFeed />;
  }
  return (
    <>
      {comments.map((feed, i) => {
        return (
          <div key={feed.fid} className={style["MyPage_Comment_Box"]}>
            <div className={style["Feed_title"]} onClick={() => handleCommentToggle(feed.fid)}>
              <img src={arrow} alt="화살표" />
              <p>{feed.body}</p>
            </div>

            {clickedComments[feed.fid] && Array.isArray(feed.cid) && feed.cid.length > 0 && (
              <ul className={style["comment_box"]}>
                {feed.cid.map((comment, j) => (
                  <li key={j}>
                    <img src={reArrow} alt="대댓글" />
                    <p className={style["Comment_content"]}>{comment.body}</p>
                    <span>{comment.date}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        );
      })}
    </>
  );
}
