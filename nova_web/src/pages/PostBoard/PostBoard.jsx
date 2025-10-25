import {useEffect, useState, useRef} from 'react';
import useMediaQuery from '@mui/material/useMediaQuery';
import Feed from "../../component/feed.js";
import style from "./../FeedList/FeedHashList.module.css";
import style2 from "./PostBoard.module.css";

import NavBar from "../../component/NavBar/NavBar.js";
import BiasBoxes from "../../component/BiasBoxes/BiasBoxes.js";
import SearchBox from "../../component/SearchBox.js";
import Header from "../../component/Header/Header.js";
import { fetchAllFeedList } from "../../services/getFeedApi.js";
import useIntersectionObserver from "../../hooks/useIntersectionObserver.js";
import MyPageLoading from "../LoadingPage/MypageLoading.js";
import NoneFeed from "../../component/NoneFeed/NoneFeed.js";
import useBiasStore from "../../stores/BiasStore/useBiasStore.js";
import HEADER from "../../constant/header.js";
import postApi from "../../services/apis/postApi.js";
import DesktopLayout from "../../component/DesktopLayout/DeskTopLayout.jsx";
import AdComponent from '../../component/AdComponent/AdComponent.jsx';
import { useNavigate } from 'react-router-dom';
import ReportModal from '../../component/ReportModal/ReportModal.jsx';

export default function PostBoard () {
    const navigate = useNavigate();
    const isMobile = useMediaQuery('(max-width:1100px)');
    const [feedData, setFeedData] = useState([]);
    const [nextData, setNextData] = useState(-1);
    const [hasMore, setHasMore] = useState(true);
    const [initialLoaded, setInitialLoaded] = useState(false);
    const [filterFclass, setFilterFclass] = useState(JSON.parse(localStorage.getItem("content")) || "");
    const [filterCategory, setFilterCategory] = useState( JSON.parse(localStorage.getItem("board")) || [""]);
    const { biasId, biasList, setBiasId, fetchBiasList} = useBiasStore();

    const [targetFeed, setTargetFeed] = useState({fid:""});
    const [reportModal, setReportModal] = useState(false);

    const handleReport = (target) => {
        setTargetFeed(target);
        setReportModal(true);
    }

    let bids = biasList.map((item, i) => {
        return item.bid;
    });

    const fetchAllFeed = async () => {

        try {
            const data = await fetchAllFeedList(-1, filterCategory);
            setFeedData(data.body.send_data);
            setNextData(data.body.key);
            setInitialLoaded(true);
            return data.body.send_data.length;
        } catch (err) {
            console.error(err);
        } 
        return 0;
    }


    const fetchBiasCategoryData = async (targetBid) => {
        try {
            const res = await postApi.post(`feed_explore/feed_with_community`, {
                header: HEADER,
                body: {
                bid: targetBid || bids?.[0] || "",
                board: "",
                key: -1,
                },
            })

            const body = res.data.body;
            setFeedData(body.send_data);
            setNextData(body.key);
            setInitialLoaded(true);
        } catch (err) {
            setInitialLoaded(false);
        }
    }

    const fetchInitialData = async () => {
        const res = await fetchAllFeed();
        if (!res) setHasMore(false);
    }

    useEffect(() => {
        setInitialLoaded(false);
        const targetBias = biasId;
        setFeedData([]);
        setNextData(-1);
        setHasMore(true);

        const initNow = async () => {
            if (biasId){
                await fetchBiasCategoryData(targetBias);
            }else{
                await fetchAllFeed();
            }
        }
        initNow();

    }, [biasId])

    useEffect(() => {
        fetchBiasList();

        if(!isMobile){
            const savedState = sessionStorage.getItem("postBoardState");
            if (savedState) {
                const parsed = JSON.parse(savedState);

                setFeedData(parsed.feedData);
                setNextData(parsed.nextData);
                setBiasId(parsed.biasId);

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
                fetchInitialData();
            }
        }else{
            const savedState = sessionStorage.getItem("postBoardState");
            if (savedState) {
                const parsed = JSON.parse(savedState);

                setFeedData(parsed.feedData);
                setNextData(parsed.nextData);
                setBiasId(parsed.biasId);

                // 복원 후 스크롤 이동
                setTimeout(() => window.scrollTo(0, parsed.scrollY || 0), 0);
                sessionStorage.removeItem("postBoardState");
                setInitialLoaded(true);
            } else {
                fetchInitialData();
            }
        }

        return () => {
            setFeedData([]);
        };
    }, []);


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
            biasId,
            scrollY: currentScroll,
            })
        );

        // ✅ 페이지 이동
        navigate(`/feed_detail/${feed.fid}`, {
            state: { fromBoard: true } 
        });
    }


    const fetchPlusAllFeed = async () => {
        try {
            const data = await fetchAllFeedList(nextData, filterCategory);

            setFeedData((prevData) => {
                const combined = [...prevData, ...data.body.send_data];

                // 중복 제거 (feed_id 기준)
                const unique = Array.from(
                    new Map(combined.map((item) => [item.feed.fid, item])).values()
                );

                return unique;
            });

            setNextData(data.body.key);
            return data.body.send_data.length;
        } catch (err) {
        } 
        return 0;
    }

    const fetchPlusCategoryFeed = async (targetBid, key) => {
        try {
            const res = await postApi.post(`feed_explore/feed_with_community`, {
                header: HEADER,
                body: {
                bid: targetBid || bids?.[0] || "",
                board: "",
                key: key,
                },
            })

            const body = res.data.body;


            setFeedData((prevData) => {
                const combined = [...prevData, ...body.send_data];

                // 중복 제거 (feed_id 기준)
                const unique = Array.from(
                    new Map(combined.map((item) => [item.feed.fid, item])).values()
                );

                return unique;
            });
            setNextData(body.key);

            return res.data.body.send_data.length;
        } catch (err) {
        }
        return 0;
    }



    const loadMoreCallBack = async () => {
        if (initialLoaded){
            if (biasId) {
                const targetBias = biasId;
                const key = nextData;
                const res = await fetchPlusCategoryFeed (targetBias, key);
                if (!res) setHasMore(false);
            }else{
                const res = await fetchPlusAllFeed()
                if (!res) setHasMore(false);
            }
        }
    };

    const scrollRef = useRef(null);
    const targetRef = useIntersectionObserver2(loadMoreCallBack, 
        { root:scrollRef.current, threshold: 0.5 }, hasMore);

    
    if (isMobile){
        return(
            <div className={`all-box ${style["all_container"]}`}>
                <div className={style["container"]}>
                    {
                        reportModal && (
                            <ReportModal type={"feed"} target={targetFeed} toggleReportOption={setReportModal} />
                        )
                    }
                    <div className={style['top-area']}>
                        {/*<DisplayAds />*/}

                        <Header />
                        <SearchBox />
                        <AdComponent type={"link"}/>
                    </div>
                    <BiasBoxes fecthDefaultSetting={fetchAllFeed}/>
                    <div className="section-separator"></div>
                    <div className={feedData.length > 0 ? style["scroll-area"] : style["none_feed_scroll"]}
                        style={{columnCount:2, columnGap: "20px"}}
                        >
                    {
                        !initialLoaded ? (
                            <MyPageLoading />
                        ) : feedData.length > 0 ? (
                            feedData.map((feed, i) => {
                            return (
                                <Feed
                                    key={`feed_${feed.feed.fid}`}
                                    className={style["feed-box"]}
                                    feed={feed.feed}
                                    setFeedData={setFeedData}
                                    onClickComponent={onClickComponent}
                                    handleReport={handleReport}
                                    hideReport={false}
                                ></Feed>
                            );
                            })
                        ) : (
                            <NoneFeed />
                    )}
                    <div ref={targetRef} style={{ height: "1px" }}></div>
                    </div>
                    <NavBar brightMode={true}></NavBar>
                </div>
            </div>
        );
    }else{
        return(
            <DesktopLayout>
                <div className={style2["desktop_feed_list_outer_frame"]}>
                    {
                        reportModal && (
                            <ReportModal type={"feed"} target={targetFeed} toggleReportOption={setReportModal} />
                        )
                    }
                    <div className={style2["desktop-ad-section-style"]}>
                        <AdComponent type={"image_32x60"}/>
                    </div>
                    <div className={style2["desktop_feed_list_inner_frame"]}>
                        <BiasBoxes setBiasId={setBiasId} fetchBiasCategoryData={fetchBiasCategoryData}  fecthDefaultSetting={fetchAllFeed}/>
                        <div className={feedData.length > 0 ? style["scroll-area"] : style["none_feed_scroll"]}
                        >
                        {
                            !initialLoaded ? (
                                <MyPageLoading />
                            ) : feedData.length > 0 ? (
                                feedData.map((feed, i) => {
                                return (
                                    <Feed
                                        key={`feed_${feed.feed.fid}`}
                                        className={style["feed-box"]}
                                        feed={feed.feed}
                                        setFeedData={setFeedData}
                                        onClickComponent={onClickComponent}
                                        handleReport={handleReport}
                                        hideReport={false}
                                    ></Feed>
                                );
                                })
                            ) : (
                                <NoneFeed />
                        )}
                        </div>
                        <div ref={targetRef} style={{ height: "1px" }}></div>
                    </div>
                    <div className={style2["desktop-ad-section-style"]}>
                        <AdComponent type={"image_32x60"}/>
                    </div>
                </div>
            </DesktopLayout>
        );
    }
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