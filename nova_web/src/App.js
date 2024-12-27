import "./App.css";
import { useEffect, useState } from "react";
import { Routes, Route, useNavigate } from "react-router-dom";
import Banner from "./component/banner";
import MyBias from "./Container/myBiasContainer";
import MyPage from "./pages/MyPage/Mypage";
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
import MoreSeeFunding from "./pages/NovaFunding/MoreSeeFunding/MoreSeeFunding.js";
import RecommendAll from "./pages/NovaFunding/MoreSeeFunding/RecommendAll.js";

import logo from "./img/NOVA_Platform.png";
import FeedThumbnail from "./component/feed-list/FeedThumbnail.js";
import useFetchData from "./hooks/useFetchData.js";
// 401 이면 바이어스 격자 무늬로 띄우기
// 401 이면 alert - 로그인 필요 문구 띄우기
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
  let allFeed = useFetchData(`${URL}/all_feed`);

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

  let [showBox, setShowBox] = useState(false);
  let [blackBox, setBlackBox] = useState("");

  let navigate = useNavigate();

  function toNavigate() {}

  // 다크모드 버튼이 눌리면 바뀌도록
  // true면 다크모드 , false면 컬러
  // let [changeMode, setChangeMode] = useState(true);
  // let [brightMode, setBrightMode] = useState("");
  // function handleChangeMode() {
  //   if (changeMode) {
  //     setBrightMode("");
  //     setChangeMode(false);
  //   } else {
  //     setBrightMode("bright-mode");
  //     setChangeMode(true);
  //   }
  // }

  // // 초기 상태를 localStorage에서 불러오거나 기본값으로 설정
  // const [brightMode, setBrightMode] = useState(() => {
  //   return localStorage.getItem("brightMode") || "bright"; // 기본값은 'bright'
  // });

  // // 다크 모드 전환 함수
  // const handleChangeMode = () => {
  //   const newMode = brightMode === "dark" ? "bright" : "dark";
  //   setBrightMode(newMode);
  //   localStorage.setItem("brightMode", newMode); // 상태를 localStorage에 저장
  // };

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
      <Route path="/write_feed" element={<WriteFeed />}></Route>
      <Route path="/more_see" element={<MoreSee onModeChange={handleModeChange} />}></Route>
      <Route path="/galaxy" element={<GalaxyList />}></Route>
      <Route path="/feed_page" element={<FeedPage brightMode={brightMode} />}></Route>
      <Route path="/signup" element={<SignUp />}></Route>
      <Route path="/terms_page" element={<Temrs />}></Route>
      <Route path="/league_detail" element={<LeaguePage />}></Route>
      <Route path="/notice" element={<NoticeList />} />
      {/* Dynamic Route for Notice Details */}
      <Route path="/notice/:nid" element={<Notice />} />
      <Route path="/my_write_feed" element={<MyWriteFeed brightMode={brightMode} />} />
      <Route path="/my_interest_feed" element={<MyInterestFeed />} />
      <Route path="/my_comment_feed" element={<MyCommentFeed />} />
      <Route path="/my_active_feed" element={<MyActiveFeed />} />
      <Route path="/my_alerts" element={<MyAlert />} />
      <Route path="/notice_list" element={<NoticeList />}></Route>
      <Route path="/select_bias" element={<SelectBias />}></Route>
      <Route path="/namecard" element={<NameCard />}></Route>
      <Route path="/mypage" element={<MyPage />}></Route>
      <Route path="/bias_certify" element={<BiasCertify />}></Route>
      <Route path="/bias_info/user_contribution" element={<BiasDetail />}></Route>
      <Route path="/novalogin" element={<NOVALogin brightMode={brightMode} />}></Route>
      <Route path="/find_pw" element={<FindPw />}></Route>
      <Route path="/find_pw_change" element={<FindPwChange />}></Route>
      <Route path="/feed_hash_list" element={<FeedHashList />}></Route>
      <Route path="/feed_hash_list/:fid" element={<FeedHashList />}></Route>
      <Route path="/feed_list" element={<FeedList brightMode={brightMode} />}></Route>
      <Route path="/feed_list/:fid" element={<FeedList />}></Route>
      <Route path="/nova_funding" element={<NovaFunding brightMode={brightMode} />}></Route>
      <Route path="/like_funding" element={<LikeFunding />}></Route>
      <Route path="/week100" element={<Week100 />}></Route>
      <Route path="/duck_funding" element={<DuckFunding />}></Route>
      <Route path="/funding_project/:type" element={<SuccessFunding />}></Route>
      <Route path="/funding_ranking" element={<RankingFunding />}></Route>
      <Route path="/open_ranking" element={<OpenRanking />}></Route>
      <Route path="/moresee_funding" element={<MoreSeeFunding />}></Route>
      <Route path="/recommend_all" element={<RecommendAll />}></Route>
      <Route path="*" element={<div>404 Error</div>}></Route>
      {/* <Route path="/test" element={<Box />}></Route> */}
      {/* <Route path="/planet" element={<PlanetList />}></Route> */}
      {/* <Route path='/league_detail' element={<LeagueDetail />}></Route> */}
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
                      src={logo}
                      alt="logo"
                      className={`logo-st ${getModeClass(brightMode)}`}
                    ></img>
                  </div>

                  <div className="buttons">
                    <button className="tool-button">
                      <img
                        src={menu}
                        alt="menu"
                        className={`logo-st ${getModeClass(brightMode)}`}
                        onClick={() => {
                          navigate("/more_see");
                        }}
                      ></img>
                    </button>
                  </div>
                </header>
                <h4 className="main-title">최애가 가장 빛날 수 있는 공간</h4>

                <Banner url={URL}></Banner>

                <FeedThumbnail
                  title={"내가 가장 보고싶은 최애"}
                  feedData={weeklyFeed}
                  brightMode={brightMode}
                  children={
                    <div className="bias-container">
                      <div className="bias-wrapper">
                        {Array.from({ length: totalBiasBoxes }).map((_, i) => {
                          const bias = myBias[i];
                          return (
                            <div key={i} className="bias-info">
                              <div className="bias-box">
                                {bias && <img src={bias_url + `${bias.bid}.PNG`} alt="bias" />}
                              </div>
                              <div className="b-name">{bias?.bname || <span>&nbsp;</span>}</div>
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  }
                />
                {/* <section className="my-bias">
                  <MyBias url={URL} showBox={showBox} blackBox={blackBox}></MyBias>
                </section> */}
              </div>

              <section>
                <div className="rt-ranking">{"<실시간랭킹>"}들어갈 와이어프레임</div>
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
                  title={"오늘의 베스트 피드"}
                  feedData={todayBestFeed}
                  brightMode={brightMode}
                  hasSearchBox
                  endPoint={`/feed_list?type=best`}
                />
                <FeedThumbnail
                  title={"주간 TOP 100"}
                  feedData={weeklyFeed}
                  brightMode={brightMode}
                  endPoint={`/feed_list?type=weekly_best`}
                />

                <FeedThumbnail
                  title={"전체 글"}
                  feedData={allFeed}
                  brightMode={brightMode}
                  allPost={<AllPost />}
                  endPoint={"/feed_list?type=all"}
                />
                {/* <AllPost brightMode={brightMode} /> */}
              </section>

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
