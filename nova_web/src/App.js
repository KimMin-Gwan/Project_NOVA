import "./App.css";
import { useEffect, useRef, useState } from "react";
import { Routes, Route, useNavigate, Link } from "react-router-dom";
import Banner from "./component/banner";
import MyBias from "./Container/myBiasContainer";
import MyPage from "./pages/MyPage/Mypage";
import MyPageEdit from "./pages/MyPage/MypageEdit";
import menu from "./img/menu-burger.png";
import NOVALogin from "./pages/NovaLogin/NovaLogin";
import SelectBias from "./component/selectBias/SelectBias";
import BiasDetail from "./pages/BiasDetail/biasDetail";
import BiasCertify from "./pages/BiasCertify/biasCertify";
import NameCard from "./pages/NameCard/nameCard";
import MoreSee from "./pages/MoreSee/MoreSee";
import NoticeList from "./pages/Notice/NoticeList";
import Notice from "./pages/Notice/Notice";
import LeaguePage from "./pages/LeaguePage/LeaguePage";
import SignUp from "./pages/SignUp/SignUp.js";
import FeedPage from "./pages/FeedPage/FeedPage.js";
import GalaxyList from "./pages/GalaxyPage/GalaxyList.js";
import NavBar from "./component/NavBar.js";
import WriteFeed from "./pages/WriteFeed/WriteFeed.js";
import MyWriteFeed from "./pages/MyPage/MyWriteFeed/MyWriteFeed.js";
import MyInterestFeed from "./pages/MyPage/MyInterestFeed/MyInterestFeed.js";
import MyCommentFeed from "./pages/MyPage/MyCommentFeed/MyCommentFeed.js";
import MyActiveFeed from "./pages/MyPage/MyActiveFeed/MyActiveFeed.js";
import MyAlert from "./pages/MyPage/Alert/MyAlert.js";
import Temrs from "./pages/Temrs/Temrs.js";
import FindPw from "./pages/FindPw/FindPw.js";
import FindPwChange from "./pages/FindPw/FindPwChange.js";
import MainPart from "./pages/MainPage/MainPart.js";
import PopularFeed from "./pages/MainPage/PopularFeed.js";
import IncreaseTag from "./pages/MainPage/IncreaseTag.js";
import AllPost from "./pages/MainPage/AllPost.js";
import FeedHashList from "./pages/FeedList/FeedHashList.js";
import FeedList from "./pages/FeedList/FeedList.js";
import NovaFunding from "./pages/NovaFunding/NovaFunding.js";
import LeftBar from "./pages/WideVer/LeftBar.js";
import RightBar from "./pages/WideVer/RightBar.js";
import LikeFunding from "./pages/NovaFunding/LikeFunding/LikeFunding.js";
import Week100 from "./pages/MainPage/Week100.js";
import DuckFunding from "./pages/NovaFunding/DuckFunding/DuckFunding.js";
import SuccessFunding from "./pages/NovaFunding/DuckFunding/SuccessFunding.js";
import RankingFunding from "./pages/NovaFunding/FundingRanking/FundingRanking.js";
import OpenRanking from "./pages/NovaFunding/FundingRanking/OpenRanking.js";
import BiasFunding from "./pages/NovaFunding/BiasFunding/BiasFunding.js";
import RecommendAll from "./pages/NovaFunding/BiasFunding/MoreProjects.js";
import FollowPage from "./pages/FollowPage/FollowPage.js";

import all_post from "./img/all_post.png";
import best from "./img/best.png";
import new_pin from "./img/new_pin.png";
import hashtag from "./img/hashtag.png";
import logo from "./img/NOVA_Platform.png";
import logo2 from "./img/logo2.png";
import FeedThumbnail from "./component/feed-list/FeedThumbnail.js";
import useFetchData from "./hooks/useFetchData.js";
import MoreProjects from "./pages/NovaFunding/BiasFunding/MoreProjects.js";
import BiasBoxes from "./component/BiasBoxes.js";
import { ContentFeed } from "./component/feed.js";
import FeedDetail from "./pages/FeedDetail/FeedDetail.js";
import TestRef from "./component/TestRef.js";
import FilterModal from "./component/FilterModal/FilterModal.js";
import LongFormWrite from "./pages/LongFormWrite/LongFormWrite.js";
import NoticeBox from "./component/NoticeBox/NoticeBox.js";
import CategoryModal from "./component/CategoryModal/CategoryModal.js";
import SearchBox from "./component/SearchBox.js";
import Write from "./pages/Write/index.js";

import { Editor } from "@toast-ui/react-editor";
import "@toast-ui/editor/dist/toastui-editor.css";
import "tui-color-picker/dist/tui-color-picker.css";
import "@toast-ui/editor/dist/i18n/ko-kr";
import "@toast-ui/editor-plugin-color-syntax/dist/toastui-editor-plugin-color-syntax.css";
import SearchPage from "./pages/SearchPage/SearchPage.js";
import getTagList from "./services/getTagList.js";
import useTagStore from "./stores/tagList/useTagStore.js";
import SearchResultPage from "./pages/SearchResultPage/SearchResultPage.js";

// 다크 모드 클래스 반환 함수
export function getModeClass(mode) {
  return mode === "dark" ? "dark-mode" : "bright-mode";
}
function App() {
  const URL = "https://nova-platform.kr/home/";
  // let url = 'http://127.0.0.1:5000/home/';

  let [isUserState, setIsUserState] = useState(false);
  let todayBestFeed = useFetchData(`${URL}today_best`);
  let weeklyFeed = useFetchData(`${URL}weekly_best`);
  let allFeed = useFetchData(`${URL}all_feed`);
  // let bias_url = "https://kr.object.ncloudstorage.com/nova-images/";
  let [isLoading, setIsLoading] = useState(true);

  // let [myBias, setMyBias] = useState([]);

  // async function fetchBiasData() {
  //   await fetch(`${URL}my_bias`, {
  //     credentials: "include",
  //   })
  //     .then((response) => response.json())
  //     .then((data) => {
  //       console.log("bias_data", data);
  //       setMyBias(data.body.bias_list);
  //       setIsLoading(false);
  //     })
  //     .catch((error) => {
  //       console.error("Fetch error:", error);
  //     });
  // }

  // useEffect(() => {
  //   fetchBiasData();
  // }, []);
  // let [allFeed, setAllFeed] = useState([]);
  // let header = {
  //   "request-type": "default",
  //   "client-version": "v1.0.1",
  //   "client-ip": "127.0.0.1",
  //   uid: "1234-abcd-5678",
  //   endpoint: "/user_system/",
  // };
  // let send_form = {
  //   header: header,
  //   body: {
  //     key: -1,
  //     category: ["자유게시판"],
  //     fclass: "short",
  //   },
  // };

  // function fetchAllFeed() {
  //   fetch("https://nova-platform.kr/feed_explore/all_feed", {
  //     method: "POST",
  //     credentials: "include",
  // headers: {
  //   "Content-Type": "application/json",
  // },
  //     body: JSON.stringify(send_form),
  //   })
  //     .then((response) => response.json())
  //     .then((data) => {
  //       console.log("all", data);
  //     });
  // }

  // useEffect(() => {
  //   fetchAllFeed();
  // }, []);

  let bias_url = "https://kr.object.ncloudstorage.com/nova-images/";

  let [myBias, setMyBias] = useState([]);
  const defaultBoxes = 4;
  const totalBiasBoxes = Math.max(defaultBoxes, myBias.length);

  useEffect(() => {
    fetch(URL + "my_bias", {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        setMyBias(data.body.bias_list);
        setIsLoading(false);
        console.log("bias_list", data);
      })
      .catch((error) => {
        console.error("Fetch error:", error);
      });
  }, []);

  function handleValidCheck() {
    fetch("https://nova-platform.kr/home/is_valid", {
      credentials: "include", // 쿠키를 함께 포함한다는 것
    })
      .then((response) => {
        if (!response.ok) {
          if (response.status === 401) {
            setIsUserState(false);
          } else if (response.status === 200) {
            setIsUserState(true);
          } else {
            throw new Error(`status: ${response.status}`);
          }
        } else {
          // console.log("로그인  확인");
          setIsUserState(true);
        }
        return response.json();
      })
      .then((data) => {
        // console.log(data);
      });
  }

  useEffect(() => {
    handleValidCheck();
  }, []);

  // let [tagList, setTagList] = useState([]);

  // console.log("ada", tagLists);
  // function fetchTagData() {
  //   fetch("https://nova-platform.kr/home/realtime_best_hashtag", {
  //     credentials: "include",
  //   })
  //     .then((response) => response.json())
  //     .then((data) => {
  //       setTagList(data.body.hashtags);
  //     });
  //   }

  let { tagList, loading, fetchTagList } = useTagStore();

  useEffect(() => {
    fetchTagList();
    // fetchTagData();
    // getTagList().then((data) => {
    //   setTagList(data.body.hashtags);
    // });
  }, []);

  const [currentIndex, setCurrentIndex] = useState(0); // 현재 표시 중인 태그 인덱스
  const intervalTime = 3000; // 2초마다 태그 변경
  let [biasId, setBiasId] = useState();

  // useEffect(() => {
  //   const timer = setInterval(() => {
  //     setCurrentIndex((prevIndex) => {
  //       const nextIndex = (prevIndex + 1) % tagList.length;
  //       return nextIndex;
  //     }, intervalTime);

  //     return clearInterval(timer);
  //   }, 3000);
  //   return () => clearInterval(timer); // 컴포넌트 언마운트 시 타이머 정리
  // });

  let [showBox, setShowBox] = useState(false);
  let [blackBox, setBlackBox] = useState("");

  let navigate = useNavigate();

  // // brightMode 상태가 변경될 때마다 body 클래스 업데이트
  const [brightMode, setBrightMode] = useState(() => {
    return localStorage.getItem("brightMode") || "bright"; // 기본값은 'bright'
  });
  useEffect(() => {
    document.body.className = brightMode === "dark" ? "dark-mode" : "bright-mode";
  }, [brightMode]);

  const handleModeChange = (newMode) => {
    setBrightMode(newMode); // MoreSee에서 전달받은 상태 업데이트
  };
  return (
    <Routes>
      {/* 더보기 페이지 / 마이페이지 */}
      <Route path="/more_see" element={<MoreSee onModeChange={handleModeChange} />}></Route>
      <Route path="/mypage" element={<MyPage />}></Route>
      <Route path="/mypage_edit" element={<MyPageEdit />}></Route>

      {/* 로그인 및 비밀번호 및 회원가입 */}
      <Route path="/novalogin" element={<NOVALogin brightMode={brightMode} />}></Route>
      <Route path="/find_pw" element={<FindPw />}></Route>
      <Route path="/find_pw_change" element={<FindPwChange />}></Route>
      <Route path="/signup" element={<SignUp />}></Route>

      {/* 이용약관 및 공지사항 */}
      <Route path="/terms_page" element={<Temrs />}></Route>
      <Route path="/notice_list" element={<NoticeList />}></Route>
      <Route path="/notice" element={<NoticeList />} />
      <Route path="/notice/:nid" element={<Notice />} />

      {/* 피드 페이지 */}
      <Route path="/feed_page" element={<FeedPage brightMode={brightMode} />}></Route>
      <Route path="/write_feed" element={<Write />}>
        <Route path=":type" element={<Write />}></Route>
      </Route>
      <Route path="/select_bias" element={<SelectBias />}></Route>
      <Route path="/feed_hash_list" element={<FeedHashList />}></Route>
      <Route path="/feed_hash_list/:fid" element={<FeedHashList />}></Route>
      <Route path="/feed_list" element={<FeedList brightMode={brightMode} />}></Route>
      <Route path="/feed_list/:fid" element={<FeedList />}></Route>
      <Route path="/feed_detail/:fid" element={<FeedDetail />}></Route>
      <Route path="/follow_page" element={<FollowPage />}></Route>
      <Route path="/search" element={<SearchPage />}></Route>
      <Route path="/search_result" element={<SearchResultPage />}></Route>

      {/* 펀딩 페이지 목록 */}
      <Route path="/nova_funding" element={<NovaFunding brightMode={brightMode} />}></Route>
      <Route path="/like_funding" element={<LikeFunding />}></Route>
      <Route path="/duck_funding" element={<DuckFunding />}></Route>
      <Route path="/funding_project/:type" element={<SuccessFunding />}></Route>
      <Route path="/funding_ranking" element={<RankingFunding />}></Route>
      <Route path="/open_ranking" element={<OpenRanking />}></Route>
      <Route path="/bias_funding" element={<BiasFunding />}></Route>
      <Route path="/bias_funding/:type" element={<MoreProjects />}></Route>

      {/* 테스트 페이지 및 에러 페이지 */}
      <Route path="/test" element={<LongFormWrite />}></Route>
      <Route path="/test1" element={<NavBar />}></Route>
      <Route path="*" element={<div>404 Error</div>}></Route>

      {/* 미사용 페이지 */}
      {/* <Route path="/planet" element={<PlanetList />}></Route> */}
      {/* <Route path='/league_detail' element={<LeagueDetail />}></Route> */}
      {/* <Route path="/namecard" element={<NameCard />}></Route> */}
      {/* <Route path="/bias_certify" element={<BiasCertify />}></Route> */}
      {/* <Route path="/bias_info/user_contribution" element={<BiasDetail />}></Route> */}
      {/* <Route path="/my_write_feed" element={<MyWriteFeed brightMode={brightMode} />}/> */}
      {/* <Route path="/my_comment_feed" element={<MyCommentFeed />} /> */}
      {/* <Route path="/my_active_feed" element={<MyActiveFeed />} /> */}
      {/* <Route path="/my_alerts" element={<MyAlert />} /> */}
      {/* <Route path="/week100" element={<Week100 />}></Route> */}
      {/* <Route path="/my_interest_feed" element={<MyInterestFeed />} /> */}
      {/* <Route path="/galaxy" element={<GalaxyList />}></Route> */}
      {/* <Route path="/league_detail" element={<LeaguePage />}></Route> */}

      {/* 홈 화면 */}
      <Route
        path="/"
        element={
          <div className="all-box">
            {/* <section className="contents com1">
              <LeftBar brightMode={brightMode} />
            </section> */}
            <div
              onClick={(e) => {
                e.stopPropagation();
                if (showBox) {
                  setShowBox(false);
                }
              }}
              className={`container ${blackBox} ${getModeClass(brightMode)}`}
            >
              <div className={`top-area ${getModeClass(brightMode)}`}>
                <header className="header">
                  <div
                    className="logo"
                    onClick={() => {
                      navigate("/");
                    }}
                  >
                    <img
                      src={logo2}
                      alt="logo"
                      className={`logo-st ${getModeClass(brightMode)}`}
                    ></img>
                  </div>
                  {/* <Link to="/write_feed/long">롱폼작성 페이지지</Link>
                  <Link to="/test1">test page</Link> */}
                </header>
                <SearchBox />
                <h4 className="main-title">최애가 가장 빛날 수 있는 공간</h4>

                <div className="banner-box">
                  <Banner url={URL}></Banner>
                </div>

                <FeedThumbnail
                  title={
                    <>
                      <span className="title-color">최애 </span>몰아보기
                    </>
                  }
                  biasList={myBias}
                  img_src={new_pin}
                  feedData={weeklyFeed}
                  brightMode={brightMode}
                  type={"bias"}
                  children={<BiasBoxes setBiasId={setBiasId} />}
                  endPoint={`/feed_list?type=bias`}
                  customClassName="custom-height"
                />
                {/* <section className="my-bias">
                  <MyBias url={URL} showBox={showBox} blackBox={blackBox}></MyBias>
                </section> */}
              </div>

              <section>
                <ul className="rt-ranking ">
                  {tagList.map((tag, i) => {
                    return (
                      <li
                        key={i}
                        style={{
                          display: i === currentIndex ? "flex" : "none",
                        }}
                      >
                        {i + 1}. {tag}
                      </li>
                    );
                  })}
                </ul>
              </section>

              <section className="contents">
                {/* <MainPart brightMode={brightMode} /> */}
                {/* <PopularFeed brightMode={brightMode} /> */}
                {/* <div className="narrow-page">
                  <IncreaseTag brightMode={brightMode} />
                </div> */}
                {/* <Week100 brightMode={brightMode} /> */}
                {/* <hr className={`hr-line ${getModeClass(brightMode)}`}></hr> */}

                <FeedThumbnail
                  title={
                    <>
                      오늘의 베스트 <span className="title-color">피드</span>
                    </>
                  }
                  img_src={best}
                  feedData={todayBestFeed}
                  brightMode={brightMode}
                  hasSearchBox
                  endPoint={`/feed_list?type=best`}
                />
                <FeedThumbnail
                  title={
                    <>
                      주간 <span className="title-color">TOP 100</span>
                    </>
                  }
                  img_src={best}
                  feedData={weeklyFeed}
                  brightMode={brightMode}
                  endPoint={`/feed_list?type=weekly_best`}
                />

                <FeedThumbnail
                  title={"전체 글"}
                  img_src={all_post}
                  feedData={allFeed}
                  brightMode={brightMode}
                  allPost={<AllPost allFeed={allFeed} />}
                  endPoint={"/feed_list?type=all"}
                />
                {/* <AllPost brightMode={brightMode} /> */}
              </section>
              <NavBar brightMode={brightMode}></NavBar>

              <div className="narrow-page">
                <NavBar brightMode={brightMode}></NavBar>
              </div>
            </div>
            {/* <section className="contents com1">
              <RightBar brightMode={brightMode} />
            </section> */}
          </div>
        }
      />
    </Routes>
  );
}

export default App;
