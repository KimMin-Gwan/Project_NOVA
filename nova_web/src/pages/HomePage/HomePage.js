import { useEffect, useState } from "react";

import Banner from "../../component/banner.js";
import NavBar from "../../component/NavBar.js";
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

export function getModeClass(mode) {
  return mode === "dark" ? "dark-mode" : "bright-mode";
}

export default function HomePage() {
  let todayBestFeed = useFetchData(`/home/today_best`);
  let weeklyFeed = useFetchData(`/home/weekly_best`);
  let allFeed = useFetchData(`/home/all_feed`);

  let { biasList, fetchBiasList } = useBiasStore();
  let { tagList, loading, fetchTagList } = useTagStore();

  // 최애 리스트 받아오기
  useEffect(() => {
    console.log("새로고침");
    fetchBiasList();
  }, []);

  const FETCH_URL = "https://nova-platform.kr/feed_explore/";

  // 실시간 랭킹 받아오기
  //   useEffect(() => {
  //     fetchTagList();
  //   }, []);
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
        bids: biasId === undefined ? [bids] : [biasId],
        board: "자유게시판",
        key: -1,
      },
    };

    console.log("2222", send_data.body);

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
    <div className="all-box">
      <div className={`container ${getModeClass(brightMode)}`}>
        <div className={`top-area ${getModeClass(brightMode)}`}>
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
            children={
              <BiasBoxes setBiasId={setBiasId} fetchBiasCategoryData={fetchBiasCategoryData} />
            }
            endPoint={`/feed_list?type=bias`}
            customClassName="custom-height"
          />
        </div>

        {/* <section className="up-container">
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
              </section> */}

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
  );
}
