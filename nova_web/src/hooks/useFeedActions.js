import { useNavigate } from "react-router-dom";
import mainApi from "../services/apis/mainApi";

export default function useFeedActions(setFeedData, type) {
  let navigate = useNavigate();

  function handleCheckStar(fid, e) {
    mainApi
      .get(`feed_explore/check_star?fid=${fid}`)
      .then((res) => {
        console.log(res.data);
        if (type === "myPage") {
          setFeedData((prevFeeds) =>
            prevFeeds.map((feed) =>
              feed.fid === fid
                ? {
                    ...feed,
                    star: res.data.body.feed[0].star,
                    star_flag: res.data.body.feed[0].star_flag,
                  }
                : feed
            )
          );
        } else {
          setFeedData((prevFeeds) => {
            return prevFeeds.map((feed) => {
              return feed.feed.fid === fid
                ? {
                    ...feed,
                    feed: res.data.body.feed[0],
                  }
                : feed;
            });
          });
        }
      })
      .catch((err) => {
        console.log(err);
        if (err.response.status === 401) {
          navigate("/novalogin");
        } else {
          console.error("Error checking star:", err);
        }
      });
  }

  return { handleCheckStar };
}
