import { useEffect, useState } from "react";
import mainApi from "../services/apis/mainApi";
import HEADER from "../constant/header";
import postApi from "../services/apis/postApi";

export default function useFetchFeedList(type, updatedNextData, filterCategory, filterFclass) {
  const [feedDatas, setFeedDatas] = useState([]);
  const [nextKey, setNextKey] = useState(-1);
  const [isLoadings, setIsLoadings] = useState(true);

  async function fetchFeedList() {
    if (type === "today" || type === "weekly") {
      await mainApi.get(`feed_explore/${type}_best`).then((res) => {
        console.log(`${type} feed`, res.data.body);
        setFeedDatas(res.data.body.send_data);
        setNextKey(res.data.body.key);
        setIsLoadings(false);
      });
    }

    // if (type === "all") {
    //   await postApi
    //     .post(`feed_explore/all_feed`, {
    //       header: HEADER,
    //       body: {
    //         key: updatedNextData, // 여기에서  사용됨
    //         category: filterCategory || [""],
    //         fclass: filterFclass || "",
    //       },
    //     })
    //     .then((res) => {
    //       setFeedDatas(res.data.body.send_data);
    //       setNextKey(res.data.body.key);
    //       setIsLoadings(false);
    //     });
    // }
  }

  useEffect(() => {
    fetchFeedList();
  }, [type, nextKey, updatedNextData, filterCategory, filterFclass]);

  return { feedDatas, nextKey, isLoadings, fetchFeedList };
}
