import { useEffect, useState } from "react";
import style from "./AllPost.module.css";
import StoryFeed from "../StoryFeed/StoryFeed";

export default function AllPost({ allFeed }) {
  return (
    <div className={`${style["wrap-container"]} ${style["allpost-container"]}`}>
      <div className={`${style["all-list"]} `}>
        {allFeed.map((feed, i) => {
          return <StoryFeed key={feed.feed.fid} feedData={feed} type={"home"} />;
        })}
      </div>
    </div>
  );
}
