import axios from "axios";

const feedApi = axios.create({
  baseURL: "https://supernova.io.kr/charlie/",
  withCredentials: true,
});

// 인터셉터 설정
feedApi.interceptors.request.use((config) => {
  // 이미 .html이 있으면 중복 방지
  if (typeof config.url === "string" && !config.url.endsWith(".html")) {
    config.url = `${config.url}.html`;
  }
  return config;
});

export default feedApi;
