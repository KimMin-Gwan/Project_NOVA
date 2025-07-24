import {useEffect, useState} from 'react';
import Feed from "./../../component/feed";
import style from "./../FeedList/FeedHashList.module.css";

import NavBar from "../../component/NavBar/NavBar.js";
import Banner from "../../component/Banner/Banner.js";
import SearchBox from "../../component/SearchBox.js";
import Header from "../../component/Header/Header.js";
import { fetchAllFeedList } from "../../services/getFeedApi.js";
import useIntersectionObserver from "../../hooks/useIntersectionObserver.js";
import MyPageLoading from "../LoadingPage/MypageLoading.js";
import NoneFeed from "../../component/NoneFeed/NoneFeed.js";

export default function NewHomePage () {
    const [feedData, setFeedData] = useState([]);
    const [nextData, setNextData] = useState(-1);
    const [hasMore, setHasMore] = useState(true);
    const [isLoading, setIsLoading] = useState(true);
    const [filterFclass, setFilterFclass] = useState(JSON.parse(localStorage.getItem("content")) || "");
    const [filterCategory, setFilterCategory] = useState( JSON.parse(localStorage.getItem("board")) || [""]);

    const fetchAllFeed = async () => {
      const data = await fetchAllFeedList(nextData, filterCategory, filterFclass);
      setFeedData(data.body.send_data);
      setNextData(data.body.key);
      setHasMore(data.body.send_data.length > 0);
      setIsLoading(false);
    }

    useEffect(() => {
        fetchAllFeed();

        return () => {
            setFeedData([]);
        };
    }, []);


    async function fetchFeedListType(fetchFunction, type, nextData, filterCategory, filterFclass) {
        const data = await fetchFunction(type, nextData, filterCategory, filterFclass);

        setFeedData((prevData) => {
            const newData = [...prevData, ...data.body.send_data];
            return newData;
        });
        setNextData(data.body.key);
        setIsLoading(false);
        setHasMore(data.body.send_data.length > 0);
    }

    async function fetchPlusData() {
        await fetchFeedListType(fetchAllFeedList, nextData, filterCategory, filterFclass);
    }

    const loadMoreCallBack = () => {
        if (!isLoading && hasMore) {
            fetchPlusData();
        }
    };

    const targetRef = useIntersectionObserver(loadMoreCallBack, { threshold: 0.5 }, hasMore);

    return(
        <div className={`all-box ${style["all_container"]}`}>
            <div className={style["container"]}>
                <div className={'top-area'}>
                    {/*<DisplayAds />*/}

                    <Header />
                    <SearchBox />
                </div>
                <div className="section-separator"></div>


                <section>
                    <div className={feedData.length > 0 ? style["scroll-area"] : style["none_feed_scroll"]}>
                    {
                        isLoading ? (
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
                </section>
                <NavBar brightMode={true}></NavBar>
            </div>
        </div>
    );
}



