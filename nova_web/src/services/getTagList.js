import axios from "axios";

function getTagList() {
  return axios
    .get("https://nova-platform.kr/home/realtime_best_hashtag", {
      withCredentials: true,
    })
    .then((res) => {
      return res.data;
    })
    .catch((err) => {
      console.log(err);
    });
}

export default getTagList;
