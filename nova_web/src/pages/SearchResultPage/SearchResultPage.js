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
import useIntersectionObserver from "../../hooks/useIntersectionObserver";
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
  let [searchParams] = useSearchParams();
  let keyword = searchParams.get("keyword");
  let navigate = useNavigate();

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

  useEffect(() => {
    setIsLoading(true);
  }, [activeIndex]);

  useEffect(() => {
    if (type == "post"){
      if(!feedData){ 
        fetchSearchKeyword();
      }
    } else if (type = "schedule") {
      if(!scheduleData){
        fetchScheduleKeyword();
      }
    }
  }, [type]);

  const InitSearchResult = async () => {
    setFeedNextKey(-1);
    setFeedData([]);
    setScheduleKey(-1);
    setScheduleData([]);

    if (type === "post") {
      await fetchSearchKeyword();
    } 
    else if (type === "schedule") {
      await fetchScheduleKeyword();
    } 
    setInitialLoaded(true);
  }

  async function fetchSearchKeyword() {
    await mainApi
      .get(`feed_explore/search_feed_with_keyword?keyword=${keyword}&key=${feedNextKey}`)
      .then((res) => {
        setFeedData((prev) => {
          return [...prev, ...res.data.body.send_data];
        });
        setHasMore(res.data.body.send_data.length > 0);
        setFeedNextKey(res.data.body.key);
        setIsLoading(false);
      });
  }

  async function fetchScheduleKeyword() {
    await mainApi
      .get(
        `time_table_server/try_search_schedule_with_keyword?keyword=${keyword}&key=${scheduleKey}&type=schedule`
      )
      .then((res) => {
          setScheduleData((prev) => [...prev, ...res.data.body.schedules]);
          setHasMore(res.data.body.schedules.length > 0);
          setIsLoading(false);
          setScheduleKey(res.data.body.key);
      });
  }

  function loadMoreCallBack() {
    if (!initialLoaded || hasMore || isLoading) return;

    if (type === "post") {
      fetchSearchKeyword();
    }
     //else if (type === "comment") {
      //fetchCommentKeyword();
    //}
     else if (type === "schedule") {
      fetchScheduleKeyword();
    } 
  }


  const targetRef = useIntersectionObserver(loadMoreCallBack, { threshold: 0.5 }, hasMore);

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
    if (data === "게시글"){
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
      let currentScroll = 0;

      if (isMobile){
          currentScroll = window.scrollY;
      }else{
          const scrollContainer = document.getElementById("desktop-scroll-container");
          currentScroll = scrollContainer ? scrollContainer.scrollTop : window.scrollY;
      }

      // ✅ 세션 저장
      sessionStorage.setItem(
          "postBoardState",
          JSON.stringify({
          feedData,
          nextData,
          scheduleData,
          nextData,
          activeIndex,
          type,
          scrollY: currentScroll,
          })
      );

      // ✅ 페이지 이동
      navigate(`/feed_detail/${feed.fid}`, {
          state: { fromBoard: true } 
      });
  }

  useEffect(() => {
    let historyList = JSON.parse(localStorage.getItem("history")) || [];
    setSearchHistory(historyList);

    if(!isMobile){
        const savedState = sessionStorage.getItem("postBoardState");
        if (savedState) {
            const parsed = JSON.parse(savedState);

            setFeedData(parsed.feedData);
            setFeedNextKey(parsed.nextData);
            setScheduleData(parsed.scheduleData);
            setScheduleKey(parsed.nextData);
            setActiveIndex(parsed.activeIndex);
            setType(parsed.type);

            // 복원 후 스크롤 이동
            setTimeout(() => {
                const scrollContainer = document.getElementById("desktop-scroll-container");
                if (scrollContainer) {
                    scrollContainer.scrollTop = parsed.scrollY || 0;  // ✅ 여기서 내부 컨테이너 scrollTop 설정
                } else {
                    window.scrollTo(0, parsed.scrollY || 0);  // fallback
                }
            }, 0);

            sessionStorage.removeItem("postBoardState");
            setInitialLoaded(true);
        } else {
          InitSearchResult();
        }
    }else{
        const savedState = sessionStorage.getItem("postBoardState");
        if (savedState) {
            const parsed = JSON.parse(savedState);

            setFeedData(parsed.feedData);
            setFeedNextKey(parsed.nextData);
            setScheduleData(parsed.scheduleData);
            setScheduleKey(parsed.nextData);
            setActiveIndex(parsed.activeIndex);
            setType(parsed.type);

            // 복원 후 스크롤 이동
            setTimeout(() => window.scrollTo(0, parsed.scrollY || 0), 0);
            sessionStorage.removeItem("postBoardState");
            setInitialLoaded(true);
        } else {
          InitSearchResult();
        }
    }

    return () => {
        setFeedData([]);
    };
}, []);


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
        {type === "post" && 
        <FeedSection feedData={feedData} setFeedData={setFeedData} isLoading={isLoading} 
          onClickComponent={onClickComponent} handleReport={handleReport}
          /> }
        {type === "schedule" && <ScheduleListMobile toggleDetailOption={toggleDetailOption} scheduleData={scheduleData}
        />}
        <div ref={targetRef} style={{ height: "1px" }}></div>
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
                onClick={() => onClickType("게시글")}
                style={getTapStyle(type === "post")}
              >
                게시글
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
