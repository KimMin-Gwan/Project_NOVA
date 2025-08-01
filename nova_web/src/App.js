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
// import NavBar from "./component/NavBar/NavBar.js";
// import NovaFunding from "./pages/NovaFunding/NovaFunding.js";
// import LikeFunding from "./pages/NovaFunding/LikeFunding/LikeFunding.js";
// import DuckFunding from "./pages/NovaFunding/DuckFunding/DuckFunding.js";
// import SuccessFunding from "./pages/NovaFunding/DuckFunding/SuccessFunding.js";
// import RankingFunding from "./pages/NovaFunding/FundingRanking/FundingRanking.js";
// import OpenRanking from "./pages/NovaFunding/FundingRanking/OpenRanking.js";
// import BiasFunding from "./pages/NovaFunding/BiasFunding/BiasFunding.js";
// import MoreProjects from "./pages/NovaFunding/BiasFunding/MoreProjects.js";
// import EventCard from "./component/EventCard/EventCard.js";
import FollowPage from "./pages/FollowPage/FollowPage.js";
import FeedDetail from "./pages/FeedDetail/FeedDetail.js";
import Write from "./pages/Write/Write.js";
import SearchPage from "./pages/SearchPage/SearchPage.js";
import SearchResultPage from "./pages/SearchResultPage/SearchResultPage.js";
import NoticePage from "./pages/NoticePage/NoticePage.js";
import HomePage from "./pages/HomePage/HomePage.js";
import ReportPage from "./pages/ReportPage/ReportPage.js";
import SearchSchedulePage from "./pages/SearchSchedulePage/SearchSchedulePage.js";
import TestPage from "./pages/TestPage/TestPage.js";
import ScheduleDashboard from "./pages/SchedulePage/ScheduleDashboard.js";
import SearchTopicPage from "./pages/SearchTopicPage/SearchTopicPage.js";
import MySchedulePage from "./pages/MySchedulePage/MySchedulePage.js";
import ScheduleExplore from "./pages/ScheduleExplore/ScheduleExplore.js";
import PaymentPage from "./pages/NOVAADPage/paymentpage.js";
import NovaADHomepage from "./pages/NOVAADPage/novaADHomepage.js";
import ScheduleMakePage from "./pages/SchedulePage/ScheduleMakePage.js";
import { NewFeedWritePage } from "./pages/Write/newWrite.js";
import NewFeedDetail from "./pages/FeedDetail/NewFeedDetail.js";
import BrandPage from "./pages/BrandPage/brandPage.jsx";
import YouTubePlayer from "./pages/BrandContent/TestPage.jsx";
import ImageChecker from "./pages/BrandContent/ImageChecker.jsx";
import ContentPage from "./pages/BrandContent/ContentPage.jsx";
import ContentTestPage from "./pages/BrandContent/ContentTestPage.jsx";
import NewHomePage from "./pages/NewHomePage/NewHomePage.jsx";
import DesktopLayout from "./component/DesktopLayout/DeskTopLayout.jsx";

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
      <Route path="/follow_page" element={<FollowPage />}></Route>

      {/* 검색 페이지 */}
      <Route path="/search" element={<SearchPage />}></Route>
      <Route path="/search_result" element={<SearchResultPage />}></Route>

      {/* 스케줄 페이지 */}
      <Route path="/schedule" element={<ScheduleDashboard />}></Route>
      <Route path="/search/topic" element={<SearchTopicPage />}></Route>
      <Route path="/explore/schedule" element={<ScheduleExplore />}></Route>
      <Route path="/schedule/make_new" element={<ScheduleMakePage/>}></Route>


      {/* 광고 페이지 */}
      {/**
      <Route path="/nova_ad/home" element={<NovaADHomepage/>}></Route>
      <Route path="/nova_ad/charging" element={<PaymentPage/>}></Route>
      */}

      {/* 이벤트는 다다음 버전에 추가 */}
      {/*<Route path="/search/event" element={<ScheduleResearch />}></Route>/*}

      {/* 펀딩 페이지 목록 */}
      {/* 
      <Route path="/like_funding" element={<LikeFunding />}></Route>
      <Route path="/duck_funding" element={<DuckFunding />}></Route>
      <Route path="/funding_project/:type" element={<SuccessFunding />}></Route>
      <Route path="/funding_ranking" element={<RankingFunding />}></Route>
      <Route path="/open_ranking" element={<OpenRanking />}></Route>
      <Route path="/bias_funding" element={<BiasFunding />}></Route>
      <Route path="/bias_funding/:type" element={<MoreProjects />}></Route> */}

      {/* 테스트 페이지 및 에러 페이지 */}
      {/* <Route path="/test2" element={<TestPage />}></Route> */}
      <Route path="*" element={<div>404 Error</div>}></Route>

      {/* 홈 화면 */}
      <Route path="/" element={<NewHomePage/>} />
      <Route path="/home_test" element={<HomePage/>}/>

      <Route path="/desktop_test" element={<DesktopLayout/>} />


      <Route path="/welcome" element={<BrandPage/>} />
      <Route path="/temp_test2" element={<YouTubePlayer/>} />
      <Route path="/content" element={<ContentPage/>} />

      <Route path="/content_test" element={<ContentTestPage/>} />
    </Routes>
  );
}


export default App;
