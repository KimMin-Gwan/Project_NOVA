import { useLocation, useNavigate } from "react-router-dom";
import mainApi from "../services/apis/mainApi";

export default function useFeedActions(setFeedData, type) {
  const navigate = useNavigate();
  const location = useLocation()

  function handleCheckStar(fid, e) {
    mainApi
      .get(`feed_explore/check_star?fid=${fid}`)
      .then((res) => {
        if (type === "myPage") {
          setFeedData((prevFeeds) =>
            prevFeeds.map((feed) =>
              feed.fid === fid
                ? {
                    ...feed,
                    like: res.data.body.feed[0].like,
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
        if (err.response.status === 401) {
          navigate("/novalogin", { state: { from: location.pathname } });
        } else {
          console.error("Error checking like:", err);
        }
      });
  }

  return { handleCheckStar };
}
