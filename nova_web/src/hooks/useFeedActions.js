import { useNavigate } from "react-router-dom";
import mainApi from "../services/apis/mainApi";

export default function useFeedActions(setFeedData) {
  let navigate = useNavigate();

  function handleCheckStar(fid, e) {
    mainApi
      .get(`feed_explore/check_star?fid=${fid}`)
      .then((res) => {
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
