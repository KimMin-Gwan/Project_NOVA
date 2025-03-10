import MyPageLoading from "../../pages/LoadingPage/MypageLoading";
import Feed from "../feed";
import NoneFeed from "../NoneFeed/NoneFeed";
import style from "./FeedSection.module.css";

export default function FeedSection({ feedData, isLoading }) {
  if (isLoading) {
    return <MyPageLoading />;
  }

  if (feedData.length === 0) {
    return <NoneFeed />;
  }

  return (
    <section className={style["feed_section"]}>
      {feedData.map((feed, i) => {
        return <Feed key={feed.feed.fid} feed={feed.feed} />;
      })}
    </section>
  );
}
