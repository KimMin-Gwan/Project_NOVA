import axios from "axios";

const justPostApi = axios.create({
  baseURL: "https://supernova.io.kr/",
  withCredentials: true,
  headers: {
  },
});

export default justPostApi;
