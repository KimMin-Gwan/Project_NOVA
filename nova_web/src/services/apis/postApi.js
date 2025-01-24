import axios from "axios";

let header = {
  "request-type": "default",
  "client-version": "v1.0.1",
  "client-ip": "127.0.0.1",
  uid: "1234-abcd-5678",
  endpoint: "/user_system/",
};

const postApi = axios.create({
  baseURL: "https://nova-platform.kr/",
  withCredentials: true,
  headers: {
    header,
    "Content-Type": "application/json",
  },
});

export default postApi;
