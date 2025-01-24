import axios from "axios";

const mainApi = axios.create({
  baseURL: "https://nova-platform.kr/",
  withCredentials: true,
});

export default mainApi;
