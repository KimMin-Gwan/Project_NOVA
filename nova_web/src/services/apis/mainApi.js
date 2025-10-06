import axios from "axios";

const mainApi = axios.create({
  baseURL: "https://supernova.io.kr/",
  withCredentials: true,
});

//// ✅ 401 에러 전역 처리 인터셉터 추가
//mainApi.interceptors.response.use(
  //(response) => response, // 정상 응답은 그대로 통과
  //(error) => {
    //if (error.response?.status === 401) {
      //// 콘솔에 에러 안 찍히게
      //console.clear();

      //// 로그인 안내
      //alert("로그인이 필요한 서비스입니다.");

      //// 페이지 이동 (React Router 대신 전역 이동)
      //window.location.href = "/novalogin";

      //// catch로 전달되지 않게 막음
      //return Promise.resolve({ status: 401, data: null });
    //}

    //// 그 외 에러는 그대로 던짐
    //return Promise.reject(error);
  //}
//);

export default mainApi;
