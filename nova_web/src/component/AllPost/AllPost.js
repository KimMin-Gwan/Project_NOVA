import { useEffect, useState } from "react";
import style from "./AllPost.module.css";
import StoryFeed from "../StoryFeed/StoryFeed";

export default function AllPost({ brightMode, allFeed }) {
  // const [mode, setMode] = useState(brightMode); // 초기 상태는 부모로부터 받은 brightMode 값

  // useEffect(() => {
  //   setMode(brightMode); // brightMode 값이 바뀔 때마다 mode 업데이트
  // }, [brightMode]);

  return (
    <div className={`${style["wrap-container"]} ${style["allpost-container"]}`}>
      <div className={`${style["all-list"]} `}>
        {allFeed.map((feed, i) => {
          return <StoryFeed key={feed.feed.fid} feedData={feed} />;
        })}
      </div>
    </div>
  );
}
