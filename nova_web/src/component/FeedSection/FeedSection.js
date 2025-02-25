import Feed from "../feed";
import style from "./FeedSection.module.css";

export default function FeedSection({ feedData }) {
  return (
    <section className={style["feed_section"]}>
      {feedData.map((feed, i) => {
        return <Feed key={feed.feed.fid} feed={feed.feed} />;
      })}
    </section>
  );
}
