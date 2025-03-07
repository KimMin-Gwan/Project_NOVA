import { useEffect, useState } from "react";
import mainApi from "../services/apis/mainApi";
import HEADER from "../constant/header";
import postApi from "../services/apis/postApi";
import { fetchDateFeedList, fetchAllFeedList, fetchBiasFeedList } from "../services/getFeedApi";

export default function useFetchFeedList(
  type,
  bid,
  bids,
  nextData,
  biasId,
  board,
  clickedFetch,
  updatedNextData,
  filterCategory,
  filterFclass
) {
  const [feedData, setFeedData] = useState([]);
  const [nextKey, setNextKey] = useState(-1);
  const [isLoading, setIsLoading] = useState(true);
  const [hasMore, setHasMore] = useState(true);

  async function fetchFeedList() {
    let data;
    console.log(bid, bids, board);
    if (type === "bias") {
      data = await fetchBiasFeedList(bid, bids, board, (nextData = -1));
    }

    setFeedData(data.body.send_data);
    setNextKey(data.body.key);
    setHasMore(data.body.send_data.length > 0);
    setIsLoading(false);
  }

  async function fetchPlusFeedList() {
    let data;
    if (type === "bias") {
      data = await fetchBiasFeedList(biasId, bids, board, nextData);
    }
    setFeedData((prevData) => [...prevData, ...data.body.send_data]);
    setNextKey(data.body.key);
    setHasMore(data.body.send_data.length > 0);
    setIsLoading(false);
  }
  return { feedData, nextKey, isLoading, hasMore, fetchFeedList, fetchPlusFeedList };
}

// async function fetchData() {
//   if (type === "today" || type === "weekly") {
//     const data = await fetchDateFeedList(type);
//     setFeedData(data.body.send_data);
//     setNextKey(data.body.key);
//     setIsLoading(false);
//   } else if (type === "all" || clickedFetch) {
//     let updatedNextData = -1;

//     //  만약 적용 버튼을 누르면 -1로 세팅
//     if (clickedFetch) {
//       updatedNextData = -1;
//       setNextKey(-1);
//     }
//     // 그게 아닌 상황에서는 기존의 nextData 를 사용
//     else {
//       updatedNextData = nextData;
//     }

//     const data = await fetchAllFeedList(updatedNextData, filterCategory, filterFclass);
//     console.log("ffff", data);
//     setFeedData(data.body.send_data);
//     setNextKey(data.body.key);
//     setIsLoading(false);
//   }
// }

// useEffect(() => {
//   fetchData();
// }, [type, nextKey]);

// return { feedData, nextKey, isLoading, fetchFeedList };
