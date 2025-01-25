import mainApi from "./apis/mainApi";

function getTagList() {
  return mainApi
    .get("https://nova-platform.kr/home/realtime_best_hashtag")
    .then((res) => {
      return res.data;
    })
    .catch((err) => {
      console.log(err);
    });
}

export default getTagList;
