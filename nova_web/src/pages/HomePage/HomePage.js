import { useEffect, useState } from "react";

import Banner from "../../component/Banner/Banner.js";
import NavBar from "../../component/NavBar/NavBar.js";
import AllPost from "../../component/AllPost/AllPost.js";
import all_post from "../../img/all_post.png";
import best from "../../img/best.png";
import new_pin from "../../img/new_pin.png";

import FeedThumbnail from "../../component/feed-list/FeedThumbnail.js";
import useFetchData from "../../hooks/useFetchData.js";
import BiasBoxes from "../../component/BiasBoxes/BiasBoxes.js";
import SearchBox from "../../component/SearchBox.js";
import useTagStore from "../../stores/TagStore/useTagStore.js";
import useBiasStore from "../../stores/BiasStore/useBiasStore.js";
import Header from "../../component/Header/Header.js";
import postApi from "../../services/apis/postApi.js";
import GoogleAD from "../../component/display_google_ad.js";
import DisplayAds from "../../component/display_google_ad.js";
import LoadingPage from "../LoadingPage/LoadingPage.js";
import HEADER from "../../constant/header.js";
import { useNavigate } from "react-router-dom";
import addBias from "../../img/search_nav.png";

import "./index.css";
import { use } from "react";

export function getModeClass(mode) {
  return mode === "dark" ? "dark-mode" : "bright-mode";
}

export default function HomePage() {
  const navigate = useNavigate();

  // 네비게이션 함수
  const handleNavigate = (path) => {
    navigate(`${path}`);
  };


  //let todayBestFeed = useFetchData(`/home/today_best`);
  // /let weeklyFeed = useFetchData(`/home/weekly_best`);
  //let allFeed = useFetchData(`/home/all_feed`);

  const { data: allFeed, loading: allFeedLoading } = useFetchData(`/home/all_feed`);
  const { data: weeklyFeed, loading: weeklyFeedLoading } = useFetchData(`/home/weekly_best`);
  const { data: todayBestFeed, loading: todayBestFeedLoading } = useFetchData(`/home/today_best`);

  let { biasId, biasList, setBiasId, fetchBiasList} = useBiasStore();
  let [feedData, setFeedData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [topSectionLoading, setTopSectionLoading] = useState(false);

  useEffect(() => {
    fetchBiasList();
  }, []);


  let bids = biasList.map((item, i) => {
    return item.bid;
  });

  useEffect(() => {
    if (bids.length > 0 && !biasId) {
      setBiasId(bids[0]);
    }
  }, [bids]);

  async function fetchBiasCategoryData(targetBid) {
    setTopSectionLoading(true);
    await postApi
      .post(`feed_explore/feed_with_community`, {
        header: HEADER,
        body: {
          bid: targetBid || bids?.[0] || "",
          board: "자유게시판",
          key: -1,
        },
      })
      .then((res) => {
        setFeedData(res.data.body.send_data);
        setIsLoading(false);
        setTopSectionLoading(false);
      });
  }

  useEffect(() => {
    setFeedData([]);
    fetchBiasCategoryData(biasId);
  }, [biasId]);

  const [brightMode, setBrightMode] = useState(() => {
    return localStorage.getItem("brightMode") || "bright"; // 기본값은 'bright'
  });
  useEffect(() => {
    document.body.className = brightMode === "dark" ? "dark-mode" : "bright-mode";
  }, [brightMode]);

  const handleModeChange = (newMode) => {
    setBrightMode(newMode); // MoreSee에서 전달받은 상태 업데이트
  };

  if (isLoading) {
    return <LoadingPage />;
  }
  return (
    <div className={`container ${getModeClass(brightMode)}`}>
      <div className={'top-area'}>
        {/*<DisplayAds />*/}

        <Header />
        <SearchBox />
        {
          bids.length > 0 ? (
            <>
              <BiasBoxes setBiasId={setBiasId} fetchBiasCategoryData={fetchBiasCategoryData} />
              <FeedThumbnail
                img_src={new_pin}
                feedData={feedData}
                brightMode={brightMode}
                type={"bias"}
                endPoint={`/feed_list?type=bias`}
                customClassName="custom-height"
                loading={topSectionLoading}
              />
            </>
          ):(
            <div className="bias-container">
              <div 
                style={{
                  display: "flex",
                  margin: "20px",
                  width: "100%",
                  height: "60px",
                  background: "linear-gradient(135deg, rgba(255, 255, 255, 0.4) 0%, rgba(255, 255, 255, 0.6) 100%)",
                  border: "2px solid #ffffff",
                  boxShadow: "3px 3px 8px rgba(0, 0, 0, 0.08)",
                  borderRadius: "15px",
                  alignItems: "center",
                  justifyContent: "center",
                  cursor: "pointer",
                }}
                  onClick={()=>{handleNavigate("/follow_page")}}
                >
                  <img src={addBias}  style={{
                    width: "30px",
                    height: "30px",
                    marginRight: "20px"
                  }}/>

                <div style={{fontSize:"16px", fontWeight:"500", color:"#111"}}>
                  주제 팔로우 하러 가기
                </div>
              </div>
            </div>
          )

        }
      </div>

        <Banner />
      <div className="section-separator"></div>

      <section className="contents">
        {/**
         * 
        <FeedThumbnail
          title={
            <>
              오늘의 베스트 <span className="title-color">게시글</span>
            </>
          }
          img_src={best}
          feedData={todayBestFeed}
          brightMode={brightMode}
          endPoint={`/feed_list?type=today`}
        />
         * 
         */}
        <FeedThumbnail
          title={
            <>
              주간 <span className="title-color">TOP 100</span>
            </>
          }
          img_src={best}
          feedData={weeklyFeed}
          brightMode={brightMode}
          endPoint={`/feed_list?type=weekly`}
          loading={weeklyFeedLoading}
        />

          <div className="section-separator"></div>
        <FeedThumbnail
          title={"모든 게시글"}
          img_src={all_post}
          feedData={allFeed}
          brightMode={brightMode}
          allPost={<AllPost allFeed={allFeed} />}
          endPoint={"/feed_list?type=all"}
          loading={allFeedLoading}
        />
      </section>
      <NavBar brightMode={brightMode}></NavBar>
    </div>
  );
}
