import { useEffect, useState } from "react";

import Banner from "../../component/banner.js";
import NavBar from "../../component/NavBar/NavBar.js";
import AllPost from "../../component/AllPost/AllPost.js";
import all_post from "../../img/all_post.png";
import best from "../../img/best.png";
import new_pin from "../../img/new_pin.png";

import FeedThumbnail from "../../component/feed-list/FeedThumbnail.js";
import useFetchData from "../../hooks/useFetchData.js";
import BiasBoxes from "../../component/BiasBoxes.js";
import SearchBox from "../../component/SearchBox.js";
import useTagStore from "../../stores/TagStore/useTagStore.js";
import useBiasStore from "../../stores/BiasStore/useBiasStore.js";
import Header from "../../component/Header/Header.js";
import postApi from "../../services/apis/postApi.js";
import GoogleAD from "../../component/display_google_ad.js";
import DisplayAds from "../../component/display_google_ad.js";
import LoadingPage from "../LoadingPage/LoadingPage.js";
import HEADER from "../../constant/header.js";

export function getModeClass(mode) {
  return mode === "dark" ? "dark-mode" : "bright-mode";
}

export default function HomePage() {
  let todayBestFeed = useFetchData(`/home/today_best`);
  let weeklyFeed = useFetchData(`/home/weekly_best`);
  let allFeed = useFetchData(`/home/all_feed`);

  let { biasList } = useBiasStore();
  let { tagList, loading, fetchTagList } = useTagStore();

  // 실시간 랭킹 받아오기
  //   useEffect(() => {
  //     fetchTagList();
  //   }, []);
  // const [currentIndex, setCurrentIndex] = useState(0); // 현재 표시 중인 태그 인덱스
  // const intervalTime = 3000; // 2초마다 태그 변경
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
  let [feedData, setFeedData] = useState([]);

  let { biasId, setBiasId } = useBiasStore();
  // let [biasId, setBiasId] = useState(null);

  const [isLoading, setIsLoading] = useState(true);
  let bids = biasList.map((item, i) => {
    return item.bid;
  });
  useEffect(() => {
    if (bids.length > 0 && !biasId) {
      setBiasId(bids[0]);
    }
  }, [bids]);

  async function fetchBiasCategoryData(bid) {
    await postApi
      .post(`feed_explore/feed_with_community`, {
        header: HEADER,
        body: {
          bid: biasId || bids?.[0] || "",
          board: "자유게시판",
          key: -1,
        },
      })
      .then((res) => {
        ////console.log("first bias data", res.data);
        setFeedData(res.data.body.send_data);
        setIsLoading(false);
      });
  }

  useEffect(() => {
    setFeedData([]);
    fetchBiasCategoryData();
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

  if (loading || isLoading) {
    return <LoadingPage />;
  }
  return (
    <div className="all-box">
      <div className={`container ${getModeClass(brightMode)}`}>
        <div className={`top-area ${getModeClass(brightMode)}`}>
          <DisplayAds />

          <Header />
          <SearchBox />
          <h4 className="main-title">최애가 가장 빛날 수 있는 공간</h4>
          <Banner />

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
            endPoint={`/feed_list?type=bias`}
            customClassName="custom-height"
          >
            <BiasBoxes setBiasId={setBiasId} fetchBiasCategoryData={fetchBiasCategoryData} />
          </FeedThumbnail>
        </div>

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
            endPoint={`/feed_list?type=today`}
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
            endPoint={`/feed_list?type=weekly`}
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
  );
}

{
  /* <section className="up-container">
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
              </section> */
}
