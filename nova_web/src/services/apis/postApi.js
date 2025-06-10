import axios from "axios";

const postApi = axios.create({
  baseURL: "https://supernova.io.kr/",
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

export default postApi;
