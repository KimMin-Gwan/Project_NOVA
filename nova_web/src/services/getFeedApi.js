import HEADER from "../constant/header";
import mainApi from "./apis/mainApi";
import postApi from "./apis/postApi";

// 주간, 오늘 피드 데이터
export async function fetchDateFeedList(type, nextData = -1) {
  const res = await mainApi.get(`feed_explore/${type}_best?key=${nextData}`);
  return res.data;
}

// 전체 피드 데이터 추가 받기
export async function fetchAllFeedList(nextData, filterCategory, filterFclass) {
  const res = await postApi.post(`feed_explore/all_feed`, {
    header: HEADER,
    body: {
      key: nextData,
      category: filterCategory || [""],
    },
  });
  return res.data;
}

// 태그 클릭 시 피드 받기
export async function fetchFeedListWithTag(tag, time) {
  const res = await mainApi.get(
    `feed_explore/search_feed_with_hashtag?hashtag=${tag}&key=-1&target_time=${time}`
  );
  return res.data;
}

// 주제별 피드 리스트
export async function fetchBiasFeedList(bid, bids, board, nextData) {
  let bodyData = {
    bid: bid || bids?.[0] || "",
    board: board || "",
    key: nextData || -1,
  };

  const res = await postApi.post(`feed_explore/feed_with_community`, {
    header: HEADER,
    body: bodyData,
  });

  return res.data;
}
