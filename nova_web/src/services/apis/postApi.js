import axios from "axios";

const postApi = axios.create({
  baseURL: "https://nova-platform.kr/",
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

export default postApi;
