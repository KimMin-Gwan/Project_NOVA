import { useEffect, useRef, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import SearchBox from "../../component/SearchBox";
import "./index.css";
import back from "./../../img/search_back.png";
import NavBar from "../../component/NavBar/NavBar";
import mainApi from "../../services/apis/mainApi";
import Header from "../../component/Header/Header";
import Comments from "../../component/Comments/Comments";
import Tabs from "../../component/Tabs/Tabs";
import FeedSection from "../../component/FeedSection/FeedSection";
import NoneSchedule from "../../component/NoneFeed/NoneSchedule";
import useMediaQuery from "@mui/material/useMediaQuery";
import DesktopLayout from "../../component/DesktopLayout/DeskTopLayout";
import style from "./SearchResultPageDesktop.module.css";
import SearchBoxDesktop from "../../component/SearchBoxDesktop";
import ScheduleGrid from "../ScheduleExplore/ScheduleGrid";
import ScheduleComponentMobile from "../ScheduleExplore/ScheduleComponentMobile";
import ScheduleDetailMobile from "../../component/ScheduleDetail/ScheduleDetailMobile";
import ScheduleDetailDekstop from "../../component/ScheduleDetail/ScheduleDetailDesktop";
import AdComponent from "../../component/AdComponent/AdComponent";
import ReportModal from "../../component/ReportModal/ReportModal";

export default function SearchResultPage() {
  const isMobile = useMediaQuery('(max-width:1100px)');
  const [searchParams] = useSearchParams();
  const keyword = searchParams.get("keyword");
  const navigate = useNavigate();

  // 검색어 상태
  const [searchWord, setSearchWord] = useState(keyword);
  const [searchHistory, setSearchHistory] = useState([]);

  // 탭 및 데이터 타입 상태
  const [activeIndex, setActiveIndex] = useState(0);
  const [type, setType] = useState("post");

  // 데이터 관련 상태
  const [feedData, setFeedData] = useState([]);
  const [scheduleData, setScheduleData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [hasMore, setHasMore] = useState(false);
  const [reportModal, setReportModal] = useState(false);
  const [targetFeed, setTargetFeed] = useState({fid:""});
  const [initialLoaded, setInitialLoaded] = useState(false);

  const handleReport = (target) => {
      setTargetFeed(target);
      setReportModal(true);
  }
  // 페이지네이션 키
  const [feedNextKey, setFeedNextKey] = useState(-1);
  const [scheduleKey, setScheduleKey] = useState(-1);

  //useEffect(() => {
    //setIsLoading(true);
  //}, [activeIndex]);

  useEffect(() => {
    setInitialLoaded(false);

    const initData = async() => {
      if (type == "post"){
        const res = await fetchInitSearchKeyword();
        if (!res){
          setInitialLoaded(false);
          setHasMore(false);
        }else{
          setInitialLoaded(true);
          setHasMore(true);
        }
      } else if (type == "schedule") {
        const res = await fetchInitScheduleKeyword();
        if (!res){
          setInitialLoaded(false);
          setHasMore(false);
        }else{
          setInitialLoaded(true);
          setHasMore(true);
        }
      }
    }

    initData();
  }, [type]);

  async function fetchInitSearchKeyword() {
    try{
      const res = await mainApi.get(`feed_explore/search_feed_with_keyword?keyword=${keyword}&key=${-1}`)

      const data = res.data;

      setFeedData((prevData) => {
        const combined = [...prevData, ...data.body.send_data];

        // 중복 제거 (feed_id 기준)
        const unique = Array.from(
            new Map(combined.map((item) => [item.feed.fid, item])).values()
        );

        return unique;
      });

      setFeedNextKey(res.data.body.key);
      setIsLoading(false);

      return res.data.body.send_data.length;
    }catch{
      return 0
    }
  }

  async function fetchInitScheduleKeyword() {
    try{
      const res = await mainApi.get(`time_table_server/try_search_schedule_with_keyword?keyword=${keyword}&key=${-1}&type=schedule`)
      setScheduleData(res.data.body.schedules);
      setScheduleKey(res.data.body.key);
      setIsLoading(false);

      return res.data.body.schedules.length;
    }catch{
      return 0;
    }
  }


  async function fetchSearchKeyword() {
    try{
      const res = await mainApi.get(`feed_explore/search_feed_with_keyword?keyword=${keyword}&key=${feedNextKey}`)

      const data = res.data;

      setFeedData((prevData) => {
        const combined = [...prevData, ...data.body.send_data];

        // 중복 제거 (feed_id 기준)
        const unique = Array.from(
            new Map(combined.map((item) => [item.feed.fid, item])).values()
        );

        return unique;
      });

      setFeedNextKey(res.data.body.key);
      setIsLoading(false);

      return res.data.body.send_data.length;
    }catch{
      return 0
    }
  }

  async function fetchScheduleKeyword() {
    try{
      const res = await mainApi.get(`time_table_server/try_search_schedule_with_keyword?keyword=${keyword}&key=${scheduleKey}&type=schedule`)
      setScheduleData((prev) => [...prev, ...res.data.body.schedules]);
      setScheduleKey(res.data.body.key);
      setIsLoading(false);

      return res.data.body.schedules.length;
    }catch{
      return 0;
    }
  }


  // 다른 버튼 눌러서 동작할때 파라미터를 사용함
  function handleNavigate(searchDetail) {
    if (searchDetail){
      const updateHistory = [...searchHistory, searchDetail];
      setSearchHistory(updateHistory);
      localStorage.setItem("history", JSON.stringify(updateHistory));
      navigate(`/search_result?keyword=${searchDetail}`);
      navigate(0);
      setSearchWord("");
    }else{
      const updateHistory = [...searchHistory, searchWord];
      setSearchHistory(updateHistory);
      localStorage.setItem("history", JSON.stringify(updateHistory));
      navigate(`/search_result?keyword=${searchWord}`);
      navigate(0);
      setSearchWord("");
    }
  }

  function handleSearchWord(e) {
    setSearchWord(e.target.value);
  }

  function handleKeyDown(event) {
    if (event.key === "Enter") {
      handleNavigate();
    }
  }

  const handleClick = (index) => {
    setActiveIndex(index);
  };

  function handleSearch(history) {
    if (history) {
      navigate(`/search_result?keyword=${history}`);
    } else if (searchWord) {
      navigate(`/search_result?keyword=${searchWord}`);
    } else {
      alert("검색어를 입력해주세요.");
    }
  }

  const onClickType = (data) => {
    if (data === "후기글"){
      setType("post");
    }
    else if (data === "콘텐츠"){
      setType("schedule");
    }
    else{
      setType("post");
    }
  };


  function getTapStyle(isActive) {
    return {
      border: isActive ? "2px solid transparent" : "2px solid #D8E9FF",
      backgroundImage: isActive
        ? "linear-gradient(#fff, #fff), linear-gradient(135deg, #FFE9E9 -0.5%, #91FF94 25.38%, #8981FF 83.1%)"
        : "none",
      backgroundOrigin: isActive ? "border-box" : "initial",
      backgroundClip: isActive ? "content-box, border-box" : "initial",
    };
  }

  const [showScheduleMoreOption, setShowScheduleMoreOption] = useState(false);
  const [targetSchedule, setTargetSchedule] = useState("");

  const toggleDetailOption = (targetSchedule) => {
      setTargetSchedule(targetSchedule);
      setShowScheduleMoreOption(!showScheduleMoreOption);
  }

  const onClickComponent = (feed) => {
      // ✅ 페이지 이동
      navigate(`/feed_detail/${feed.fid}`);
  }

  useEffect(() => {
    const historyList = JSON.parse(localStorage.getItem("history")) || [];
    setSearchHistory(historyList);

    return () => {
        setFeedData([]);
    };
  }, []);


  const loadMoreCallBack = async() => {
    if (initialLoaded){
      if (type === "post") {
        const result = await fetchSearchKeyword();
        if (!result) setHasMore(false);
      }
      else if (type === "schedule") {
        const result = await fetchScheduleKeyword();
        if (!result) setHasMore(false);
      } 
    }
  }


  const scrollRef = useRef(null);
  const targetRef = useIntersectionObserver2(loadMoreCallBack, 
    { root:scrollRef.current, threshold: 0.5 }, hasMore);

  if(isMobile){
    return (
      <div className="container search_result_page">
        {
            reportModal && (
                <ReportModal type={"feed"} target={targetFeed} toggleReportOption={setReportModal} />
            )
        }
        <Header />
        <div className="top-bar ">
          <div
            className="back"
            onClick={() => {
              navigate("/search");
            }}
          >
            <img src={back} />
          </div>
          <SearchBox
            type="search"
            searchWord={searchWord}
            onClickSearch={handleSearch}
            onChangeSearchWord={handleSearchWord}
            onKeyDown={handleKeyDown}
          />
        </div>

        {
          showScheduleMoreOption && 
          <ScheduleDetailMobile
              sid={targetSchedule}
              toggleDetailOption={toggleDetailOption}
            />
        }
        <Tabs activeIndex={activeIndex} handleClick={handleClick} onClickType={onClickType} />
        <div
          style={{marginBottom: "100px"}}
        >
          {type === "post" && 
          <FeedSection feedData={feedData} setFeedData={setFeedData} isLoading={isLoading} 
            onClickComponent={onClickComponent} handleReport={handleReport}
            /> }
          {type === "schedule" && <ScheduleListMobile toggleDetailOption={toggleDetailOption} scheduleData={scheduleData}
          />}
          {
            (hasMore && initialLoaded) && (
              <div>
                더 불러오기
              </div>
            )
          }
          <div ref={targetRef} style={{ height: "1px" }}></div>
        </div>
        <NavBar />
      </div>
    );
  }else{
    return(
      <DesktopLayout>
        <div className={style["desktop_search_result_page_outer_frame"]}>
            {
                reportModal && (
                    <ReportModal type={"feed"} target={targetFeed} toggleReportOption={setReportModal} />
                )
            }
          <div className={style["desktop_search_result_page_inner_frame"]}>
          <div className={style["desktop-search-meta-data-wrapper"]}>
            <SearchBoxDesktop
              type="search"
              searchWord={searchWord}
              onClickSearch={handleSearch}
              onChangeSearchWord={handleSearchWord}
              onKeyDown={handleKeyDown}
            />

            <div className={style["taps_wrapper"]}>
              <div
                className={style["single_tap"]}
                onClick={() => onClickType("후기글")}
                style={getTapStyle(type === "post")}
              >
                후기글
              </div>
              <div
                className={style["single_tap"]}
                onClick={() => onClickType("콘텐츠")}
                style={getTapStyle(type === "schedule")}
              >
                콘텐츠
              </div>
            </div>
          </div>
          {
            showScheduleMoreOption && 
            <ScheduleDetailDekstop
                sid={targetSchedule}
                toggleDetailOption={toggleDetailOption}
              />
          }

          <div
            style={{width: type == "post" ? "800px" : "1020px"}}
          >
            {type === "post" && <FeedSection 
                feedData={feedData} setFeedData={setFeedData}
                isLoading={isLoading}
                 onClickComponent={onClickComponent} 
                handleReport={handleReport}
                /> }
            {type === "schedule" && (
              scheduleData.length === 0 ? (
                <div className={style["none_schedule_frame"]}>
                  <NoneSchedule />
                </div>
              ) : (
                <ScheduleGrid scheduleData={scheduleData} toggleDetailOption={toggleDetailOption} />
              )
            )}

            <div ref={targetRef} style={{ height: "1px" }}></div>
          </div>
          </div>
          <div className={style["desktop-ad-section-style"]}>
            <AdComponent type={"image_32x60"}/>
          </div>
        </div>
      </DesktopLayout>
    );
  }
}



const ScheduleListMobile = ({toggleDetailOption, scheduleData}) => {
  return (
    <>
      {scheduleData.length === 0 && <NoneSchedule/>}


      {scheduleData.map((singleSchedule, index) => (
        <ScheduleComponentMobile
          key={index}
          toggleDetailOption={toggleDetailOption}
          {...singleSchedule}
        />
        ))}
    </>
  );
}



const useIntersectionObserver2 = (callback, options = {}, hasMore) => {
  const targetRef = useRef(null);

  useEffect(() => {
    if (!hasMore || !targetRef.current) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          callback();
        }
      });
    }, options);

    observer.observe(targetRef.current);

    return () => {
      observer.disconnect();
    };
  }, [callback, options, hasMore, targetRef.current]); // 👈 핵심 수정

  return targetRef;
}