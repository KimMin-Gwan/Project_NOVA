import MyPageLoading from "../../pages/LoadingPage/MypageLoading";
import Feed from "../feed";
import NoneFindFeed from "../NoneFeed/NoneFindFeed";
import style from "./FeedSection.module.css";

export default function FeedSection({ feedData, setFeedData,
  isLoading, onClickComponent, handleReport}) {
  if (isLoading) {
    return <MyPageLoading />;
  }

  if (feedData.length === 0) {
    return <NoneFindFeed/>;
  }

  return (
    <section className={style["feed_section"]}>
      {feedData.map((feed, i) => {
        return <Feed 
        key={feed.feed.fid} setFeedData={setFeedData} feed={feed.feed} 
        onClickComponent={onClickComponent} handleReport={handleReport}
        hideReport={false}
        />;
      })}
    </section>
  );
}
