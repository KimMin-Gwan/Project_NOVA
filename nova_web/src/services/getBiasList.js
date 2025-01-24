import axios from "axios";

function getBiasList() {
  return axios
    .get("https://nova-platform.kr/home/my_bias", {
      withCredentials: true,
    })
    .then((res) => {
      console.log("biasListzzzz", res.data);
      return res.data;
    })
    .catch((err) => {
      console.log(err);
    });
}

export default getBiasList;
