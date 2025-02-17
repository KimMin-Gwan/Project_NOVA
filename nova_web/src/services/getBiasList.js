import axios from "axios";
import mainApi from "./apis/mainApi";

async function getBiasList() {
  return await mainApi
    .get("/home/my_bias")
    .then((res) => {
      console.log("biasListzzzz", res.data);
      return res.data;
    })
    .catch((err) => {
      console.log(err);
    });
}

export default getBiasList;
