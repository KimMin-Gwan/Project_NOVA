import {useEffect, useState, useRef} from 'react';
import useMediaQuery from '@mui/material/useMediaQuery';
import Feed from "./../../component/feed";
import style from "./../FeedList/FeedHashList.module.css";
import style2 from "./NewHomePage.module.css";

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

export default function NewHomePage () {
    const isMobile = useMediaQuery('(max-width:1100px)');
    const [feedData, setFeedData] = useState([]);
    const [nextData, setNextData] = useState(-1);
    const [hasMore, setHasMore] = useState(true);
    const [initialLoaded, setInitialLoaded] = useState(false);
    const [filterFclass, setFilterFclass] = useState(JSON.parse(localStorage.getItem("content")) || "");
    const [filterCategory, setFilterCategory] = useState( JSON.parse(localStorage.getItem("board")) || [""]);
    const { biasId, biasList, setBiasId, fetchBiasList} = useBiasStore();

    let bids = biasList.map((item, i) => {
        return item.bid;
    });


    const fetchAllFeed = async () => {
        try {
            const data = await fetchAllFeedList(nextData, filterCategory);
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
                board: "자유게시판",
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
        fetchBiasCategoryData(targetBias);
    }, [biasId])

    useEffect(() => {
        fetchBiasList();
        fetchInitialData();

        return () => {
            setFeedData([]);
        };
    }, []);


    const fetchPlusAllFeed = async () => {
        try {
            const data = await fetchAllFeedList(nextData, filterCategory);
            setFeedData((prevData) => [...prevData, ...data.body.send_data]);
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
                board: "자유게시판",
                key: key,
                },
            })

            const body = res.data.body;
            setFeedData((prevData) => [...prevData, ...body.send_data]);
            setNextData(body.key);
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
    const targetRef = useIntersectionObserver(loadMoreCallBack, 
        { root:scrollRef.current, threshold: 0.5 }, hasMore);



    if (isMobile){
        return(
            <div className={`all-box ${style["all_container"]}`}>
                <div className={style["container"]}>
                    <div className={style['top-area']}>
                        {/*<DisplayAds />*/}

                        <Header />
                        <SearchBox />
                        <AdComponent type={"link"}/>
                    </div>
                    <BiasBoxes setBiasId={setBiasId} fetchBiasCategoryData={fetchBiasCategoryData}  fecthDefaultSetting={fetchAllFeed}/>
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
                                    ></Feed>
                                );
                                })
                            ) : (
                                <NoneFeed />
                        )}
                        <div ref={targetRef} style={{ height: "1px" }}></div>
                        </div>
                    </div>
                    <div className={style2["desktop-ad-section-style"]}>
                        <AdComponent type={"image_32x60"}/>
                    </div>
                </div>
            </DesktopLayout>
        );
    }
}



