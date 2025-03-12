import { useEffect, useState } from "react";
import mainApi from "../services/apis/mainApi";
import HEADER from "../constant/header";
import postApi from "../services/apis/postApi";
import {
  fetchDateFeedList,
  fetchAllFeedList,
  fetchBiasFeedList,
  fetchFeedListWithTag,
} from "../services/getFeedApi";

export default function useFetchFeedList(
  type,
  bid,
  bids,
  biasId,
  board,
  clickedFetch,
  filterCategory,
  filterFclass
) {
  const [feedData, setFeedData] = useState([]);
  const [nextKey, setNextKey] = useState(-1);
  const [isLoading, setIsLoading] = useState(true);
  const [hasMore, setHasMore] = useState(true);

  // 피드 요청
  async function fetchFeedList() {
    let data;
    let updatedNextData = -1;

    //  만약 적용 버튼을 누르면 -1로 세팅
    if (clickedFetch) {
      updatedNextData = -1;
      setNextKey(-1);
    }
    // 그게 아닌 상황에서는 기존의 nextData 를 사용
    else {
      updatedNextData = nextKey;
    }

    if (type === "bias") {
      data = await fetchBiasFeedList(bid, bids, board, nextKey);
    } else if (type === "today" || type === "weekly") {
      data = await fetchDateFeedList(type);
    } else if (type === "all" || clickedFetch) {
      data = await fetchAllFeedList(updatedNextData, filterCategory, filterFclass);
    }

    setFeedData(data.body.send_data);
    setNextKey(data.body.key);
    setHasMore(data.body.send_data.length > 0);
    setIsLoading(false);
  }

  // 피드 추가 요청
  async function fetchPlusFeedList() {
    let data;
    let updatedNextData = -1;

    //  만약 적용 버튼을 누르면 -1로 세팅
    if (clickedFetch) {
      updatedNextData = -1;
      setNextKey(-1);
    }
    // 그게 아닌 상황에서는 기존의 nextData 를 사용
    else {
      updatedNextData = nextKey;
    }

    if (type === "bias") {
      data = await fetchBiasFeedList(biasId, bids, board, nextKey);
    } else if (type === "today" || type === "weekly") {
      data = await fetchDateFeedList(type, nextKey);
    } else if (type === "all" || clickedFetch) {
      data = await fetchAllFeedList(updatedNextData, filterCategory, filterFclass);
    }

    setFeedData((prevData) => [...prevData, ...data.body.send_data]);
    setNextKey(data.body.key);
    setHasMore(data.body.send_data.length > 0);
    setIsLoading(false);
  }

  // 태그 클릭 시 피드 요청
  async function fetchFeedWithTag(tag) {
    let time;
    if (type === "today") {
      time = "day";
    } else if (type === "weekly") {
      time = "weekly";
    }

    const data = await fetchFeedListWithTag(tag, time);
    setFeedData(data.body.send_data);
    setIsLoading(false);
  }

  return {
    feedData,
    nextKey,
    isLoading,
    hasMore,
    fetchFeedList,
    fetchPlusFeedList,
    fetchFeedWithTag,
  };
}
