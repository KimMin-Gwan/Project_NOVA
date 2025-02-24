import mainApi from "./apis/mainApi";

export default function getFeedList({ type }) {
  return mainApi.get(`/feed_explore/${type}`);
}
