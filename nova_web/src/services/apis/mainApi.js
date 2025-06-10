import axios from "axios";

const mainApi = axios.create({
  baseURL: "https://supernova.io.kr/",
  withCredentials: true,
});

export default mainApi;
