import axios from "axios";

const chzzkApi = axios.create({
  baseURL: "https://chzzk.naver.com/account-interlock",
});

export default chzzkApi;