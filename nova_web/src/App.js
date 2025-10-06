import "./App.css";
import { useEffect, useState } from "react";
import { useNavigate, Routes, Route } from "react-router-dom";
import MyPage from "./pages/MyPage/Mypage";
import MyPageEdit from "./pages/MyPage/MypageEdit";
import NOVALogin from "./pages/NovaLogin/NovaLogin";
import MoreSee from "./pages/MoreSee/MoreSee";
import SignUp from "./pages/SignUp/SignUp.js";
import Temrs from "./pages/Temrs/Temrs.js";
import FindPw from "./pages/FindPw/FindPw.js";
import FindPwChange from "./pages/FindPw/FindPwChange.js";
import FeedList from "./pages/FeedList/FeedList.js";
import Write from "./pages/Write/Write.js";
import SearchPage from "./pages/SearchPage/SearchPage.js";
import SearchResultPage from "./pages/SearchResultPage/SearchResultPage.js";
import NoticePage from "./pages/NoticePage/NoticePage.js";
import ReportPage from "./pages/ReportPage/ReportPage.js";
import ScheduleDashboard from "./pages/SchedulePage/ScheduleDashboard.js";
import ScheduleExplore from "./pages/ScheduleExplore/ScheduleExplore.js";
import ScheduleMakePage from "./pages/ScheduleMakePage/ScheduleMakePage.jsx";
import NewFeedDetail from "./pages/FeedDetail/NewFeedDetail.js";
import BrandPage from "./pages/BrandPage/brandPage.jsx";
import ContentPage from "./pages/BrandContent/ContentPage.jsx";
import ContentTestPage from "./pages/BrandContent/ContentTestPage.jsx";
import NewHomePage from "./pages/NewHomePage/NewHomePage.jsx";
import SubmitNewBiasPage from "./pages/SubmitNewBias/SubmitNewBias.jsx";
import ErrorPage from "./pages/error_page.js";
import NotYet from "./pages/NotYet.jsx";
import AdComponent from "./component/AdComponent/AdComponent.jsx";
import BiasPage from "./pages/BiasPage/BiasPage.jsx";
import NewFollowPage from "./pages/FollowPage/NewFollowePage.jsx";

// 다크 모드 클래스 반환 함수
export function getModeClass(mode) {
  return mode === "dark" ? "dark-mode" : "bright-mode";
}
function App() {
  const navigate = useNavigate();

  useEffect(() => {
    const visited = localStorage.getItem("visited");

    if (!visited) {
      // 첫 방문인 경우
      localStorage.setItem("visited", "true");
      // /welcome 페이지로 이동
      navigate("/welcome", { replace: true });
    }
  }, [navigate]);

  // // brightMode 상태가 변경될 때마다 body 클래스 업데이트
  const [brightMode, setBrightMode] = useState(() => {
    return localStorage.getItem("brightMode") || "bright"; // 기본값은 'bright'
  });
  useEffect(() => {
    document.body.className =
      brightMode === "dark" ? "dark-mode" : "bright-mode";
  }, [brightMode]);

  const handleModeChange = (newMode) => {
    setBrightMode(newMode); // MoreSee에서 전달받은 상태 업데이트
  };

  if (
    window.innerWidth <= 768 ||
    /Mobi|Android|iPhone|iPad|iPod|Windows Phone/i.test(navigator.userAgent)
  ) {
    document.body.style.zoom = 100 + "%";
  } else {
    document.body.style.zoom = 100 + "%";
  }

  return (
    <Routes>
      {/* 더보기 페이지 / 마이페이지 */}
      <Route
        path="/more_see"
        element={<MoreSee onModeChange={handleModeChange} />}
      ></Route>
      <Route path="/mypage" element={<MyPage />}></Route>
      <Route path="/mypage_edit" element={<MyPageEdit />}></Route>

      {/* 로그인 및 비밀번호 및 회원가입 */}
      <Route
        path="/novalogin"
        element={<NOVALogin brightMode={brightMode} />}
      ></Route>
      <Route path="/find_pw" element={<FindPw />}></Route>
      <Route path="/find_pw_change" element={<FindPwChange />}></Route>
      <Route path="/signup" element={<SignUp />}></Route>

      {/* 이용약관 및 공지사항 */}
      <Route path="/terms_page" element={<Temrs />}></Route>
      <Route path="/notice" element={<NoticePage />} />
      <Route path="/report" element={<ReportPage />} />
      {/* <Route path="/notice/:nid" element={<Notice />} /> */}

      {/* 피드 페이지 */}
      <Route path="/write_feed" element={<Write />}>
        <Route path=":fid" element={<Write />}></Route>
      </Route>
      <Route
        path="/feed_list"
        element={<FeedList brightMode={brightMode} />}
      ></Route>
      <Route path="/feed_list/:fid" element={<FeedList />}></Route>
      {/*<Route path="/feed_detail/:fid" element={<FeedDetail />}></Route>*/}
      <Route path="/feed_detail/:fid" element={<NewFeedDetail/>}></Route>

      {/* 스트리머 관련 페이지*/}
      <Route path="/follow_page" element={<NewFollowPage/>}></Route>
      <Route path="/submit_new" element={<SubmitNewBiasPage/>} />

      {/* 검색 페이지 */}
      <Route path="/search" element={<SearchPage />}></Route>
      <Route path="/search_result" element={<SearchResultPage />}></Route>

      {/* 컨텐츠  페이지 */}
      <Route path="/temp" element={<ScheduleDashboard />}></Route>
      <Route path="/explore/schedule" element={<ScheduleExplore />}></Route>
      <Route path="/schedule/make_new" element={<ScheduleMakePage/>}>
        <Route path=":sid" element={<ScheduleMakePage/>}></Route>
      </Route>
      <Route path="/bias" element={<BiasPage/>}>
        <Route path=":bid" element={<BiasPage/>}></Route>
      </Route>

      {/* 테스트 페이지 및 에러 페이지 */}
      {/* <Route path="/test2" element={<TestPage />}></Route> */}
      <Route path="*" element={<ErrorPage/>} />
      <Route path="/" element={<NotYet/>} />

      {/* 홈 화면 */}
      <Route path="/post_board" element={<NewHomePage/>} />
      <Route path="/welcome" element={<BrandPage/>} />
      <Route path="/content" element={<ContentPage/>} />

      <Route path="/test_component" element={<AdComponent type={"image_50x32"}/>} />

      <Route path="/content_test" element={<ContentTestPage/>} />
    </Routes>
  );
}


export default App;

      //{/* 광고 페이지 */}
      //{/**
      //<Route path="/nova_ad/home" element={<NovaADHomepage/>}></Route>
      //<Route path="/nova_ad/charging" element={<PaymentPage/>}></Route>
      //*/}
