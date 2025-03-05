import { useEffect, useState } from "react";
import useDragScroll from "../../hooks/useDragScroll";
import mainApi from "../../services/apis/mainApi";
import style from "./KeywordBox.module.css";
import useFetchFeedList from "../../hooks/useFetchFeedList";
import useFeedStore from "../../stores/FeedStore/useFeedStore";

export default function KeywordBox({ type, title, subTitle, onClickTagButton }) {
  const { scrollRef, hasDragged, dragHandlers } = useDragScroll();

  let [bestTags, setBestTags] = useState([]);
  let [isLoading, setIsLoading] = useState(true);

  // const { feedDatas, nextKey, fetchFeedList } = useFetchFeedList({ type });
  const { fetchFeedList, loadings } = useFeedStore();

  async function fetchHashTags() {
    await mainApi.get(`home/${type}_spiked_hot_hashtag`).then((res) => {
      setBestTags(res.data.body.hashtags);
      setIsLoading(false);
      //console.log(`${type}`, res.data);
    });
  }

  useEffect(() => {
    fetchHashTags();
  }, []);

  let [currentTag, setCurrentTag] = useState();

  function onClickTags(index, tag) {
    if (currentTag === index) {
      setCurrentTag(null);
      fetchFeedList(type);
    } else {
      setCurrentTag(index);
      onClickTagButton(tag);
    }
  }

  if (isLoading || loadings) {
    return <div>loading...</div>;
  }

  return (
    <div className={style["keyword-container"]}>
      <div className={style["title-container"]}>
        {title} <span className={style["sub-title"]}>{subTitle}</span>
      </div>

      <div
        className={style["tags-container"]}
        ref={scrollRef}
        onMouseDown={dragHandlers.onMouseDown}
        onMouseMove={dragHandlers.onMouseMove}
        onMouseUp={dragHandlers.onMouseUp}
      >
        <div className={style["tags-wrapper"]}>
          {bestTags.map((tag, i) => {
            return (
              <div
                key={i}
                onClick={() => {
                  if (hasDragged) return;
                  onClickTags(i, tag);
                }}
                className={`${style["tags"]} ${currentTag === i ? style["click-tag"] : ""}`}
              >
                #{tag}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
