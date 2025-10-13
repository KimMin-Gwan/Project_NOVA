import { useLocation, useNavigate } from "react-router-dom";
import  { useEffect, useRef, useState } from "react";
import style from "./Mypage.module.css";
import style2 from "./MypageMobile.module.css";
import style3 from "./MypageDesktop.module.css";
import user_icon from "./../../img/user_profile.svg";
import mainApi from "../../services/apis/mainApi";
import Feed from "../../component/feed";
import arrow from "./../../img/comment_arrow.svg";
import reArrow from "./../../img/recomment.svg";

import reArrow1 from "./../../img/reArrow1.svg";
import reArrow2 from "./../../img/reArrow2.svg";
import reArrow3 from "./../../img/reArrow3.svg";
import reArrow4 from "./../../img/reArrow4.svg";
import MyPageLoading from "../LoadingPage/MypageLoading";
import useMediaQuery from "@mui/material/useMediaQuery";
import DesktopLayout from "../../component/DesktopLayout/DeskTopLayout";
import useIntersectionObserver from "../../hooks/useIntersectionObserver";
import NoneFeed from "../../component/NoneFeed/NoneFeed";

function MyPage() {
  const isMobile = useMediaQuery('(max-width:1100px)');
  const navigate = useNavigate();
  const location = useLocation();
  const [isUserState, setIsUserState] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [categoryLoading, setCategoryLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [myData, setMyData] = useState(
    {
      num_comment : 0,
      num_like : 0,
      num_feed : 0,
      uid : "",
      uname : ''
    }
  );
  const [feedData, setFeedData] = useState([]);
  const [nextKey, setNextKey] = useState(-1);

  const handleValidCheck = async () => {
    mainApi.get("https://supernova.io.kr/home/is_valid?only_token=n").then((res) => {
        if (res.status === 200) {
          setIsUserState(true);
        } else {
          if (window.confirm("로그인이 필요합니다.")){
            navigate("/novalogin", { state: { from: location.pathname } });
          }else{
            navigate("/");
          }
          setIsUserState(false);
        }
        return 
      })
      .catch((error) => {
        if (error.response.status == 401){
          if (window.confirm("로그인이 필요합니다.")){
            navigate("/novalogin", { state: { from: location.pathname } });
          }else{
            navigate("/");
          }
          setIsUserState(false);
        }
        setIsUserState(false);
      });
  }

  useEffect(() => {
    if (!isUserState) {
      handleValidCheck();
    }else{
      fetchMyPage();
      initMyPageResult();
    }
  }, [isUserState]);

  const [initialLoaded, setInitialLoaded] = useState(false);

  const initMyPageResult = async () =>{
      try {
          const count = await fetchInitFeed();

          // ✅ 숫자면 (0 포함) 초기 로드 완료로 간주
          if (typeof count === "number" && !isNaN(count)) {
              setInitialLoaded(true);
          } 
      } catch (err) {
          console.error("❌ 초기 검색 실패:", err);
      }
  }

  const fetchMyPage = async () => {
    await mainApi.get("user_home/get_my_page_data").then((res) => {
      setMyData(res.data.body);
      setIsLoading(false);
    });
  }

  const fetchInitFeed = async() => {
    setIsLoading(true);
    const res = await mainApi.get(`user_home/get_my_feed?type=post&key=${nextKey}`);

    setCategoryLoading(false);
    setFeedData(res.data.body.feed);
    setHasMore(res.data.body.feed.length > 0);
    setNextKey(res.data.body.key);
    setIsLoading(false);
    return res.data.body.feed.length;
  }

  const fetchMyFeedMore = async() => {
    const res = await mainApi.get(`user_home/get_my_feed?type=post&key=${nextKey}`);
    setCategoryLoading(false);
    setFeedData((prevData) => [...prevData, ...res.data.body.feed]);
    setHasMore(res.data.body.feed.length > 0);
    setNextKey(res.data.body.key);
    setIsLoading(false);
    return res.data.body.feed.length;
  }

  const handleFetchMore = async () => {
    if (initialLoaded){
        const res = await fetchMyFeedMore();
        if (!res) setHasMore(false);
    }
  }

  const handleMovePage = (e, page) =>{
    e.preventDefault();
    navigate(page);
  }

  const scrollRef = useRef(null);
  const targetRef = useIntersectionObserver(handleFetchMore,
      { root:scrollRef.current, threshold: 0.5 }, hasMore);

  const profile = `https://kr.object.ncloudstorage.com/nova-profile-bucket/${myData.uid}.png`;

  if(isMobile){
    return (
      <div className={style2["frame"]}>
        <div className={style2["inner-box"]}>
          <div className={style2["top_area"]}>
            <div className={style2["backword-button"]}
              onClick={() => { navigate(-1); }}
            >
              뒤로
            </div>
            <div className={style2["page-title"]} >
              마이페이지
            </div>
            <div className={style2["backword-button"]}
              onClick={(e) => handleMovePage(e, "/mypage_edit")} style={{ cursor: "pointer" }}
            >
              프로필 수정
            </div>
          </div>
          <div className={style2["user-profile-wrapper"]}>
            <div className={style2["user-image-container"]}>
              <div className={style2["user-image"]}>
                <img src={profile} />
              </div>
              <div className={style2["user-name"]}>
                {myData.uname}
              </div>
            </div>

            <div className={style2["user-detail-container"]}>
              <div className={style2["user-detail-wrapper"]}>
                <div className={style2["user-data-number"]}>
                  {myData.num_feed}
                </div>
                <div className={style2["user-data-type"]}>
                  게시글
                </div>
              </div>
              <div className={style2["user-detail-wrapper"]}>
                <div className={style2["user-data-number"]}>
                  {myData.num_comment}
                </div>
                <div className={style2["user-data-type"]}>
                  댓글
                </div>
              </div>
              <div className={style2["user-detail-wrapper"]}>
                <div className={style2["user-data-number"]}>
                  {myData.num_like}
                </div>
                <div className={style2["user-data-type"]}>
                  좋아요
                </div>
              </div>
            </div>
          </div>

          <div className={
              feedData.length > 0 ? style2["scroll-area"] : style2["none_feed_scroll"]}
              ref={scrollRef}
          >
          {
              isLoading ? (
                  <MyPageLoading />
              ) : feedData.length > 0 ? (
                  feedData.map((feed, i) => {
                  return (
                      <Feed
                        key={`feed_${feed.fid}`}
                        className={style["feed-box"]}
                        feed={feed}
                        setFeedData={setFeedData}
                      ></Feed>
                  );
                  })
              ) : (
                <div className={style2["none-feed-container"]}>
                  <NoneFeed />
                </div>
          )}
          <div ref={targetRef} style={{ height: "1px" }}></div>
          </div>
        </div>
      </div>
    );
  }else{
    return (
      <DesktopLayout>
      <div className={style3["frame"]}>
          <div className={style3["user-profile-wrapper"]}>
            <div className={style3["user-image-container"]}>
              <div className={style3["user-image"]}>
                <img src={profile} />
              </div>
            </div>

            
            <div className={style3["user-detail-wrapper"]}>
              <div className={style3["user-name-container"]}>
                <div className={style3["user-name"]}>
                  {myData.uname}
                </div>
                <div className={style3["profile-edit-button"]}
                  onClick={(e) => handleMovePage(e, "/mypage_edit")} style={{ cursor: "pointer" }}
                >
                  프로필 수정
                </div>
              </div>

              <div className={style3["user-detail-container"]}>
                <div className={style3["user-info-wrapper"]}>
                  <div className={style3["user-data-type"]}>
                    게시글
                  </div>
                  <div className={style3["user-data-number"]}>
                    {myData.num_feed}
                  </div>
                </div>
                <div className={style3["user-info-wrapper"]}>
                  <div className={style3["user-data-type"]}>
                    댓글
                  </div>
                  <div className={style3["user-data-number"]}>
                    {myData.num_comment}
                  </div>
                </div>
                <div className={style3["user-info-wrapper"]}>
                  <div className={style3["user-data-type"]}>
                    좋아요
                  </div>
                  <div className={style3["user-data-number"]}>
                    {myData.num_like}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className={
              feedData.length > 0 ? style2["scroll-area"] : style2["none_feed_scroll"]}
              ref={scrollRef}
          >
          {
              isLoading ? (
                  <MyPageLoading />
              ) : feedData.length > 0 ? (
                  feedData.map((feed, i) => {
                  return (
                      <Feed
                      key={`feed_${feed.fid}`}
                      className={style["feed-box"]}
                      feed={feed}
                      setFeedData={setFeedData}
                      ></Feed>
                  );
                  })
              ) : (
                <div className={style2["none-feed-container"]}>
                  <NoneFeed />
                </div>
          )}
          <div ref={targetRef} style={{ height: "1px" }}></div>
          </div>
      </div>
      </DesktopLayout>
    );
  }
}

export default MyPage;
