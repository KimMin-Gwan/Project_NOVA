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
import { BundleScheduleDetail, ScheduleDetail } from "../../component/EventMore/EventMore";
import { MakeSingleSchedule, EditSingleSchedule } from "../../component/EventMore/EventMore";
import { ScheduleMore, ScheduleAdd, ScheduleRemove, ScheduleEdit} from "../../component/ScheduleMore/ScheduleMore";
import { ScheduleBundle} from "../../component/ScheduleEvent/ScheduleBundle";
import useToggleMore from "../../hooks/useToggleMore";
import ScheduleCard from "../../component/EventCard/EventCard";
import NoneSchedule from "../../component/NoneFeed/NoneSchedule";

export default function SearchResultPage() {
  let [searchParams] = useSearchParams();
  let keyword = searchParams.get("keyword");
  let navigate = useNavigate();

  // 검색어 상태
  let [searchWord, setSearchWord] = useState(keyword);
  let [searchHistory, setSearchHistory] = useState([]);

  // 탭 및 데이터 타입 상태
  const [activeIndex, setActiveIndex] = useState(0);
  const [type, setType] = useState("post");

  const [targetSchedule, setTargetSchedule] = useState({});
  const [targetScheduleBundle, setTargetScheduleBundle] = useState({});

  // 데이터 관련 상태
  let [feedData, setFeedData] = useState([]);
  const [comments, setComments] = useState([]);
  const [scheduleBundleData, setScheduleBundleData] = useState([]);
  const [scheduleData, setScheduleData] = useState([]);
  let [isLoading, setIsLoading] = useState(true);
  const [hasMore, setHasMore] = useState(true);

  const [addScheduleModal, setAddScheduleModal] = useState(false);
  const [addScheduleBundleModal, setAddScheduleBundleModal] = useState(false);
  const [editScheduleModal, setEditScheduleModal] = useState(false);

  // 페이지네이션 키
  const [feedNextKey, setFeedNextKey] = useState(-1);
  const [commentNextKey, setCommentNextKey] = useState(-1);
  const [scheduleBundleKey, setScheduleBundleKey] = useState(-1);
  const [scheduleKey, setScheduleKey] = useState(-1);

  useEffect(() => {
    let historyList = JSON.parse(localStorage.getItem("history")) || [];
    setSearchHistory(historyList);
  }, []);

  useEffect(() => {
    setIsLoading(true);
  }, [activeIndex]);

  useEffect(() => {
    setFeedNextKey(-1);
    setCommentNextKey(-1);
    setFeedData([]);
    setComments([]);

    if (type === "post") {
      fetchSearchKeyword();
    } else if (type === "comment") {
      fetchCommentKeyword();
    } else if (type === "schedule") {
      fetchScheduleKeyword();
    } else if (type === "schedule_bundle") {
      fetchScheduleBundleKeyword();
    }


  }, [type]);

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


  async function fetchCommentKeyword() {
    await mainApi
      .get(`feed_explore/search_comment_with_keyword?keyword=${keyword}&key=${commentNextKey}`)
      .then((res) => {
        setComments((prev) => [...prev, ...res.data.body.feeds]);
        setHasMore(res.data.body.feeds.length > 0);
        setIsLoading(false);
        setCommentNextKey(res.data.body.key);
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


  async function fetchScheduleBundleKeyword() {
    await mainApi
      .get(
        `time_table_server/try_search_schedule_with_keyword?keyword=${keyword}&key=${scheduleBundleKey}&type=schedule_bundle`
      )
      .then((res) => {
          setScheduleBundleData((prev) => [...prev, ...res.data.body.schedule_bundles]);
          setHasMore(res.data.body.schedule_bundles.length > 0);
          setIsLoading(false);
          setScheduleBundleKey(res.data.body.key);
      });
  }


  function loadMoreCallBack() {
    if (!hasMore || isLoading) return;

    if (type === "post") {
      fetchSearchKeyword();
    } else if (type === "comment") {
      fetchCommentKeyword();
    } else if (type === "schedule") {
      fetchScheduleKeyword();
    } else if (type === "schedule_bundle") {
      fetchScheduleBundleKeyword();
    }
  }


  const targetRef = useIntersectionObserver(loadMoreCallBack, { threshold: 0.5 }, hasMore);

  function handleNavigate() {
    const updateHistory = [...searchHistory, searchWord];
    setSearchHistory(updateHistory);
    localStorage.setItem("history", JSON.stringify(updateHistory));
    navigate(`/search_result?keyword=${searchWord}`);
    navigate(0);
    setSearchWord("");
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
    console.log("검색어:", history, searchWord);
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
    else if (data === "댓글"){
      setType("comment");
    }
    else if (data === "일정"){
      setType("schedule");
    }
    //else if (data === "일정 번들"){
      //setType("schedule_bundle");
    //}
    else{
      setType("post");
    }
  };


  const toggleEditScheduleModal = (target) => {
    setEditScheduleModal((editScheduleModal) => !editScheduleModal);
    setTargetSchedule(target);
  };


  // 일정 추가하기 버튼 누르면 동작하는애
  const toggleAddScheduleModal = (target) => {
    setAddScheduleModal((addScheduleModal) => !addScheduleModal);
    setTargetSchedule(target);
  };

  // 일정 번들 추가하기 버튼 누르면 동작하는 애
  const toggleAddScheduleBundleModal = (target) => {
    setAddScheduleBundleModal((addScheduleBundleModal) => !addScheduleBundleModal);
    setTargetScheduleBundle(target);
  };

  return (
    <div className="container search_result_page">
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
      <Tabs activeIndex={activeIndex} handleClick={handleClick} onClickType={onClickType} />
      {type === "comment" && <Comments comments={comments} isLoading={isLoading} />}
      {type === "post" && <FeedSection feedData={feedData} setFeedData={setFeedData} isLoading={isLoading} /> }
      {type === "schedule" && <Schedules scheduleData={scheduleData}
       type={type} toggleAddScheduleBundleModal={toggleAddScheduleBundleModal} toggleEditScheduleModal={toggleEditScheduleModal} />}

      <div ref={targetRef} style={{ height: "1px" }}></div>
      <NavBar />

      {/* 자세히 보기 모달창 */}
      <BundleScheduleDetail
        closeSchedule={toggleAddScheduleBundleModal}
        isOpen={addScheduleBundleModal}
        target={targetScheduleBundle}
      />

      {/*여기도 target 추가해야될 듯 */}
      <ScheduleDetail
        closeSchedule={toggleAddScheduleModal}
        isOpen={addScheduleModal}
        target={targetSchedule}
      />

      <EditSingleSchedule
        closeSchedule={toggleEditScheduleModal}
        isOpen={editScheduleModal}
        target={targetSchedule}
        isSingleSchedule={true}
      />

    </div>
  );
}

function Schedules ({scheduleData, type, toggleAddScheduleBundleModal, toggleAddScheduleModal, toggleEditScheduleModal, fetchTryAddSchedule, fetchTryRejectSchedule}) {
  const { moreClick, handleToggleMore } = useToggleMore();
  let navigate = useNavigate();
  // 게시판으로 이동
  const navBoard = () => {
    navigate("/");
  };

  return(
        <ul className="scheduleList" style={{ display: "flex", flexDirection: "column", gap: "4px", paddingLeft:"0px"}}>
        {scheduleData.length === 0 && <NoneSchedule/>}
        {type=== "schedule_bundle"
          ? scheduleData.map((item) => (
              <div key={item.sbid}>
                <ScheduleBundle
                  item={item}
                  toggleClick={() => handleToggleMore(item.sbid)} // id 전달
                />
                {moreClick[item.sbid] && ( // 해당 id의 상태만 확인
                  <ScheduleMore
                    target={item}
                    navBoardClick={navBoard}
                    scheduleClick={toggleAddScheduleBundleModal}
                  />
                )}
              </div>
            ))
          : scheduleData.map((item) => (
            <div key={item.sid}>
              <ScheduleCard
                {...item}
                toggleClick={() => handleToggleMore(item.sid)} // id 전달
              />

              {moreClick[item.sid] && (
                item.is_already_have === false ? (
                  <ScheduleAdd
                    target={item}
                    detailClick={toggleAddScheduleModal}
                    navBoardClick={navBoard}
                    addClick={fetchTryAddSchedule}
                  />
                ) : item.is_owner === false? (
                  <ScheduleRemove
                    target={item}
                    navBoardClick={navBoard}
                    removeClick={fetchTryRejectSchedule}
                  />
                ) : (
                  <ScheduleEdit
                    target={item}
                    navBoardClick={navBoard}
                    editClick={toggleEditScheduleModal}
                  />
                )
              )}
            </div>
 
            ))}
          <div style={{height:"48px"}}></div>

      </ul>
  );
}


