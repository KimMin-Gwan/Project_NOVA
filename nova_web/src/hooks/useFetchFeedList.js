import { useEffect, useState } from "react";
import mainApi from "../services/apis/mainApi";

export default function useFetchFeedList(type) {
  const [feedDatas, setFeedDatas] = useState([]);
  const [nextKey, setNextKey] = useState(-1);
  const [isLoadings, setIsLoadings] = useState(true);

  async function fetchFeedList() {
    await mainApi.get(`feed_explore/${type}_best`).then((res) => {
      console.log(`${type} feed`, res.data.body);
      //   console.log("dsdad", res.data);
      setFeedDatas(res.data.body.send_data);
      setNextKey(res.data.body.key);
      setIsLoadings(false);
    });
  }

  useEffect(() => {
    fetchFeedList();
  }, [type]);

  return { feedDatas, nextKey, isLoadings, fetchFeedList };
}
