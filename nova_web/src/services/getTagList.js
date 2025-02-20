import mainApi from "./apis/mainApi";

function getTagList() {
  return mainApi
    .get("home/realtime_best_hashtag")
    .then((res) => {
      console.log("rea", res.data);
      return res.data;
    })
    .catch((err) => {
      console.log(err);
    });
}

export default getTagList;
