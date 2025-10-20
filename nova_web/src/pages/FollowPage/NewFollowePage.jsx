import { useEffect, useState, useRef } from "react";
import { useLocation } from "react-router-dom";
import FollowPageDesktop from "./NewFollowPageDesktop.jsx";
import DesktopLayout from "../../component/DesktopLayout/DeskTopLayout";
import useMediaQuery from "@mui/material/useMediaQuery";
import FollowPageMobile from "./NewFollowPageMobile.jsx";
import useBiasStore from "../../stores/BiasStore/useBiasStore.js";
import mainApi from "../../services/apis/mainApi.js";


const NewFollowPage = () => {
    const isMobile = useMediaQuery('(max-width:1100px)');
    const tags= ["모두", "치지직", "SOOP"];
    const [searchResult, setSearchResult] = useState([]);
    const [searchWord, setSearchWord] = useState("");
    const [targetPlatform, setTargetPlatform] = useState("모두");
    const location = useLocation();
    const { biasId, biasList, setBiasId, fetchBiasList} = useBiasStore();

    const handleSearchWord = (e) => {
        setSearchWord(e.target.value);
    }

    const handleKeyDown = (event) => {
        if (event.key === "Enter") {
            fetchSearchBias(searchWord, targetPlatform);
        }
    }

    const fetchSearchBias = async (keyword, platform, lenBias, isMore) => {
        const res = await mainApi.get(`/nova_sub_system/try_search_bias?keyword=${keyword}&category=${platform}&len_bias=${lenBias}`);
        if (isMore){
            setSearchResult((prev) => [...prev, ...res.data.body.biases]);
        }else{
            setSearchResult(res.data.body.biases);
        }
        return res.data.body.biases.length;
    }

    const fetchSearchBiasInit = async (keyword, platform) => {
        const res = await mainApi.get(`/nova_sub_system/try_search_bias?keyword=${keyword}&category=${platform}&len_bias=${0}`);
        setSearchResult(res.data.body.biases);
        return res.data.body.biases.length;
    }

    const [initialLoaded, setInitialLoaded] = useState(false);
    const initFollowPageSeachResult = async () =>{
        try {
            const count = await fetchSearchBias(searchWord, targetPlatform, 0, false);

            // ✅ 숫자면 (0 포함) 초기 로드 완료로 간주
            if (typeof count === "number" && !isNaN(count)) {
                setInitialLoaded(true);
            } 
        } catch (err) {
            console.error("❌ 초기 검색 실패:", err);
        }
    }


    // ✅ 세션에서 복원
    useEffect(() => {
        fetchBiasList();

        if(!isMobile){
            const savedState = sessionStorage.getItem("followPageState");
            if (savedState) {
                const parsed = JSON.parse(savedState);
                setSearchResult(parsed.searchResult);
                setSearchWord(parsed.searchWord);
                setTargetPlatform(parsed.targetPlatform);
                // 복원 후 스크롤 이동
                        // 복원 후 스크롤 이동 (내부 컨테이너)
                setTimeout(() => {
                    const scrollContainer = document.getElementById("desktop-scroll-container");
                    if (scrollContainer) {
                        scrollContainer.scrollTop = parsed.scrollY || 0;  // ✅ 여기서 내부 컨테이너 scrollTop 설정
                    } else {
                        window.scrollTo(0, parsed.scrollY || 0);  // fallback
                    }
                }, 0);
                sessionStorage.removeItem("followPageState");
            } else {
                initFollowPageSeachResult(searchWord, targetPlatform, 0);
            }
        }else{
            const savedState = sessionStorage.getItem("followPageState");
            if (savedState) {
                const parsed = JSON.parse(savedState);
                setSearchResult(parsed.searchResult);
                setSearchWord(parsed.searchWord);
                // 복원 후 스크롤 이동
                setTimeout(() => window.scrollTo(0, parsed.scrollY || 0), 0);
                sessionStorage.removeItem("followPageState");
            } else {
                initFollowPageSeachResult(searchWord, targetPlatform, 0);
            }
        }
    }, []);

    if(isMobile){
        return(
            <FollowPageMobile
                tags={tags}
                targetPlatform={targetPlatform}
                setTargetPlatform={setTargetPlatform}
                biasList={biasList}
                searchResult={searchResult}
                searchWord={searchWord}
                handleSearchWord={handleSearchWord}
                handleKeyDown={handleKeyDown}
                fetchSearchBias={fetchSearchBias}
                initialLoaded={initialLoaded}
            />
        )
    }else{
        return(
            <DesktopLayout>
                <FollowPageDesktop
                    tags={tags}
                    targetPlatform={targetPlatform}
                    setTargetPlatform={setTargetPlatform}
                    biasList={biasList}
                    searchResult={searchResult}
                    searchWord={searchWord}
                    handleSearchWord={handleSearchWord}
                    handleKeyDown={handleKeyDown}
                    fetchSearchBias={fetchSearchBias}
                />
            </DesktopLayout>
        )
    }
}


export default NewFollowPage;