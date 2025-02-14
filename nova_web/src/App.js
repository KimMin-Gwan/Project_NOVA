import "./App.css";
import { useEffect, useState } from "react";
import { Routes, Route, useNavigate } from "react-router-dom";
import Banner from "./component/banner";
import MyPage from "./pages/MyPage/Mypage";
import MyPageEdit from "./pages/MyPage/MypageEdit";
import NOVALogin from "./pages/NovaLogin/NovaLogin";
import MoreSee from "./pages/MoreSee/MoreSee";
import NoticeList from "./pages/Notice/NoticeList";
import Notice from "./pages/Notice/Notice";
import SignUp from "./pages/SignUp/SignUp.js";
import NavBar from "./component/NavBar.js";
import Temrs from "./pages/Temrs/Temrs.js";
import FindPw from "./pages/FindPw/FindPw.js";
import FindPwChange from "./pages/FindPw/FindPwChange.js";
import AllPost from "./pages/MainPage/AllPost.js";
import FeedList from "./pages/FeedList/FeedList.js";
import NovaFunding from "./pages/NovaFunding/NovaFunding.js";
import LikeFunding from "./pages/NovaFunding/LikeFunding/LikeFunding.js";
import DuckFunding from "./pages/NovaFunding/DuckFunding/DuckFunding.js";
import SuccessFunding from "./pages/NovaFunding/DuckFunding/SuccessFunding.js";
import RankingFunding from "./pages/NovaFunding/FundingRanking/FundingRanking.js";
import OpenRanking from "./pages/NovaFunding/FundingRanking/OpenRanking.js";
import BiasFunding from "./pages/NovaFunding/BiasFunding/BiasFunding.js";
import FollowPage from "./pages/FollowPage/FollowPage.js";

import all_post from "./img/all_post.png";
import best from "./img/best.png";
import new_pin from "./img/new_pin.png";
import logo2 from "./img/logo2.png";
import logo from "./img/NOVA_Platform.png";
import upIcon from "./img/up-ranking.png";

import FeedThumbnail from "./component/feed-list/FeedThumbnail.js";
import useFetchData from "./hooks/useFetchData.js";
import MoreProjects from "./pages/NovaFunding/BiasFunding/MoreProjects.js";
import BiasBoxes from "./component/BiasBoxes.js";
import FeedDetail from "./pages/FeedDetail/FeedDetail.js";
import LongFormWrite from "./pages/LongFormWrite/LongFormWrite.js";
import SearchBox from "./component/SearchBox.js";
import Write from "./pages/Write/Write.js";
import SearchPage from "./pages/SearchPage/SearchPage.js";
import useTagStore from "./stores/TagStore/useTagStore.js";
import SearchResultPage from "./pages/SearchResultPage/SearchResultPage.js";
import useBiasStore from "./stores/BiasStore/useBiasStore.js";

// 다크 모드 클래스 반환 함수
export function getModeClass(mode) {
  return mode === "dark" ? "dark-mode" : "bright-mode";
}
function App() {
  let navigate = useNavigate();
  let todayBestFeed = useFetchData(`/home/today_best`);
  let weeklyFeed = useFetchData(`/home/weekly_best`);
  let allFeed = useFetchData(`/home/all_feed`);

  let { biasList, fetchBiasList } = useBiasStore();
  let { tagList, loading, fetchTagList } = useTagStore();

  // 최애 리스트 받아오기
  useEffect(() => {
    fetchBiasList();
  }, []);

  const FETCH_URL = "https://nova-platform.kr/feed_explore/";

  // 실시간 랭킹 받아오기
  useEffect(() => {
    fetchTagList();
  }, []);

  let [feedData, setFeedData] = useState([]);

  let [biasId, setBiasId] = useState();

  let header = {
    "request-type": "default",
    "client-version": "v1.0.1",
    "client-ip": "127.0.0.1",
    uid: "1234-abcd-5678",
    endpoint: "/user_system/",
  };
  const [isLoading, setIsLoading] = useState(true);
  let bids = biasList.map((item, i) => {
    return item.bid;
  });
  async function fetchBiasCategoryData(bid) {
    let send_data = {
      header: header,
      body: {
        bids: bid === undefined ? [bids] : [bid],
        board: "자유게시판",
        key: -1,
      },
    };

    await fetch(`${FETCH_URL}feed_with_community`, {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(send_data),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("first bias data", data);
        setFeedData(data.body.send_data);
        setIsLoading(false);
      });
  }

  useEffect(() => {
    setFeedData([]);
    fetchBiasCategoryData();
  }, [biasId]);

  // function handleValidCheck() {
  //   fetch("https://nova-platform.kr/home/is_valid", {
  //     credentials: "include", // 쿠키를 함께 포함한다는 것
  //   })
  //     .then((response) => {
  //       if (!response.ok) {
  //         if (response.status === 401) {
  //           setIsUserState(false);
  //         } else if (response.status === 200) {
  //           setIsUserState(true);
  //         } else {
  //           throw new Error(`status: ${response.status}`);
  //         }
  //       } else {
  //         // console.log("로그인  확인");
  //         setIsUserState(true);
  //       }
  //       return response.json();
  //     })
  //     .then((data) => {
  //       // console.log(data);
  //     });
  // }

  // useEffect(() => {
  //   handleValidCheck();
  // }, []);

  const [currentIndex, setCurrentIndex] = useState(0); // 현재 표시 중인 태그 인덱스
  const intervalTime = 3000; // 2초마다 태그 변경
  // let [biasId, setBiasId] = useState();

  // 실시간 랭킹 동작(꺼놓음)
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

  if (loading || isLoading) {
    return <div>loading...</div>;
  }
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
      {/* <Route path="/feed_page" element={<FeedPage brightMode={brightMode} />}></Route> */}
      {/* <Route path="/select_bias" element={<SelectBias />}></Route> */}

      <Route path="/write_feed" element={<Write />}>
        <Route path=":type" element={<Write />}></Route>
      </Route>
      <Route path="/feed_list" element={<FeedList brightMode={brightMode} />}></Route>
      <Route path="/feed_list/:fid" element={<FeedList />}></Route>
      <Route path="/feed_detail/:fid" element={<FeedDetail />}></Route>
      <Route path="/follow_page" element={<FollowPage />}></Route>

      {/* 검색 페이지 */}
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

      {/* 홈 화면 */}
      <Route
        path="/"
        element={
          <div className="all-box">
            <div className={`container ${getModeClass(brightMode)}`}>
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
                </header>
                <SearchBox />
                <h4 className="main-title">최애가 가장 빛날 수 있는 공간</h4>

                <Banner></Banner>

                <FeedThumbnail
                  title={
                    <>
                      최애<span className="title-color">주제</span>
                    </>
                  }
                  img_src={new_pin}
                  feedData={feedData}
                  brightMode={brightMode}
                  type={"bias"}
                  children={
                    <BiasBoxes
                      setBiasId={setBiasId}
                      fetchBiasCategoryData={fetchBiasCategoryData}
                    />
                  }
                  endPoint={`/feed_list?type=bias`}
                  customClassName="custom-height"
                />
              </div>

              <section className="up-container">
                <div>
                  <img src={upIcon} alt="급상승 해시태그" />
                  <h3>급상승 해시태그</h3>
                </div>
                <ul className="rt-ranking ">
                  {tagList.map((tag, i) => {
                    return (
                      <li
                        key={i}
                        style={{
                          display: i === currentIndex ? "flex" : "none",
                        }}
                      >
                        <p>{i + 1}</p>
                        {tag}
                      </li>
                    );
                  })}
                </ul>
              </section>

              <section className="contents">
                <FeedThumbnail
                  title={
                    <>
                      오늘의 베스트 <span className="title-color">게시글</span>
                    </>
                  }
                  img_src={best}
                  feedData={todayBestFeed}
                  brightMode={brightMode}
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
                  title={"모든 게시글"}
                  img_src={all_post}
                  feedData={allFeed}
                  brightMode={brightMode}
                  allPost={<AllPost allFeed={allFeed} />}
                  endPoint={"/feed_list?type=all"}
                />
              </section>
              <NavBar brightMode={brightMode}></NavBar>
            </div>
          </div>
        }
      />
    </Routes>
  );
}

export default App;
