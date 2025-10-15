import BiasPageDesktop from "./BiasPageDesktop";
import BiasPageMobile from "./BiasMobile.jsx";
import DesktopLayout from "../../component/DesktopLayout/DeskTopLayout.jsx";
import useMediaQuery from "@mui/material/useMediaQuery";
import mainApi from "../../services/apis/mainApi";
import { useEffect, useState } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { fetchIsValidUser } from "./BiasPageFunc.jsx";

const BiasPage = () => {
    const isMobile = useMediaQuery('(max-width:1100px)');
    const { bid } = useParams();
    const [targetDate, setTargetDate] = useState(new Date());
    const navigate = useNavigate();
    const location = useLocation();
    const [scheduleList, setScheduleList] = useState([]);
    const [weekData, setWeekData] = useState("");
    const [is_following, setIsFollowing] = useState(false);
    const [isValidUser, setIsValidUser] = useState(false);

    const [targetBias, setTargetBias] = useState({
        bname :"",
        bid: "",
        state: "TEMP",
        plaform : "치지직"
    })
    const [targetSchedule, setTargetSchedule] = useState({
        sid : "",
        title : "",
        datetime : "",
        tags : []
    })

    const fetchBiasData = async (bid) => {
        const res = await mainApi.get(`/nova_sub_system/get_single_bias?bid=${bid}`);
        const bias = res.data.body.bias
        const is_following = res.data.body.is_following
        setIsFollowing(is_following);
        return bias
    }

    const fetchScheduleData = async ({bid, date}) => {
        const strDate = date.toISOString().split("T")[0];
        const res = await mainApi.get(`/time_table_server/get_bias_page_schedule?bid=${bid}&date=${strDate}`);
        const response = res.data.body;
        return response
    }

    const fetchTryFollowBias = async (bid) => {
        try {
            const res = await mainApi.get(`nova_sub_system/try_follow_bias?bid=${bid}`);

            if (res.status === 401) {
                alert("로그인이 필요한 서비스입니다.");
                navigate("/novalogin", { state: { from: location.pathname } });
            }

            const result = res.data.body.now_following;

            if (result){
                alert("팔로우 완료!");
            }else{
                alert("팔로우 취소 완료");
            }

            setIsFollowing(result);
            return result;
        } catch (err) {
            const status = err.response.status;
            if (status === 401) {
                alert("로그인이 필요한 서비스입니다.");
                navigate("/novalogin", { state: { from: location.pathname } });
            }else{
                alert("오류가 발생했습니다. 잠시 후 다시 시도해주세요.");
            }
        }
    };

    useEffect(() => {
        const loadData = async () => {
            if (bid) {
                try {
                    const bias = await fetchBiasData(bid);  // await 추가
                    if (!bias || bias.bid === "") {
                        alert("스트리머를 찾을 수 없습니다.");
                        navigate("/");
                        return;
                    }
                    
                    setTargetBias(bias);

                    const response = await fetchScheduleData({ bid: bias.bid, date: targetDate}); // await 추가
                    setScheduleList(response.schedule_data);
                    setWeekData(response.week_data);
                } catch (err) {
                    console.error("데이터 로딩 실패:", err);
                    alert("데이터를 불러오는 중 오류가 발생했습니다.");
                    navigate("/");
                }

                try{
                    const validResult = await fetchIsValidUser(bid);
                    setIsValidUser(validResult)
                } catch (err) {
                    console.error("알 수 없는 오류", err);
                }
            } else {
                alert("잘못된 경로 입니다.");
                navigate("/");
            }
        };

        loadData();
    }, [bid, navigate]);

    // 이전 주
    const prevWeek = () => {
        setTargetDate(prevDate => {
            const newDate = new Date(prevDate);
            newDate.setDate(newDate.getDate() - 7);
            return newDate;
        });
    };

    // 다음 주
    const nextWeek = () => {
        setTargetDate(prevDate => {
            const newDate = new Date(prevDate);
            newDate.setDate(newDate.getDate() + 7);
            return newDate;
        });
    };

    useEffect(()=>{
        const loadScheduleData = async () => {
            const response = await fetchScheduleData({ bid: targetBias.bid, date: targetDate }); // await 추가
            setScheduleList(response.schedule_data);
            setWeekData(response.week_data);
        }
        loadScheduleData()
    }, [targetDate])

    const handleInitTargetSchedule = () => {
        if (!scheduleList || scheduleList.length === 0) return;

        // sid가 ""가 아닌 첫 번째 데이터 찾기
        const firstValid = scheduleList.find(item => item.schedule.sid !== "");

        // 없으면 맨 첫 번째 데이터
        const target = firstValid || scheduleList[0];

        setTargetSchedule(target.schedule);
    };

    useEffect(()=>{
        handleInitTargetSchedule()
    }, [scheduleList])


    if (isMobile){
        return(
            <BiasPageMobile 
                scheduleList={scheduleList}
                targetBias={targetBias}
                weekData={weekData}
                prevWeek={prevWeek}
                nextWeek={nextWeek}
                fetchTryFollowBias={fetchTryFollowBias}
                is_following={is_following}
                isValidUser={isValidUser}
            />
        );
    }else{
        return(
            <DesktopLayout>
                <BiasPageDesktop
                    scheduleList={scheduleList}
                    targetBias={targetBias}
                    weekData={weekData}
                    prevWeek={prevWeek}
                    nextWeek={nextWeek}
                    targetSchedule={targetSchedule}
                    setTargetSchedule={setTargetSchedule}
                    fetchTryFollowBias={fetchTryFollowBias}
                    is_following={is_following}
                    isValidUser={isValidUser}
                 />
            </DesktopLayout>
        );
    }
}


export default BiasPage;
