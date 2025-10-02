import BiasPageDesktop from "./BiasPageDesktop";
import BiasPageMobile from "./BiasMobile.jsx";
import DesktopLayout from "../../component/DesktopLayout/DeskTopLayout.jsx";
import useMediaQuery from "@mui/material/useMediaQuery";
import mainApi from "../../services/apis/mainApi";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

const BiasPage = () => {
    const isMobile = useMediaQuery('(max-width:1100px)');
    const { bid } = useParams();
    const [targetDate, setTargetDate] = useState(new Date());
    const navigate = useNavigate();
    const [scheduleList, setScheduleList] = useState([]);
    const [weekData, setWeekData] = useState("");

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

    //const bid = "203c35b9-dcd7-4a4f-bce9-96085a465446";

    const fetchBiasData = async (bid) => {
        const res = await mainApi.get(`/nova_sub_system/get_single_bias?bid=${bid}`);
        const bias = res.data.body.bias
        return bias
    }

    const fetchScheduleData = async ({bid, date}) => {
        const strDate = date.toISOString().split("T")[0];
        const res = await mainApi.get(`/time_table_server/get_bias_page_schedule?bid=${bid}&date=${strDate}`);
        const response = res.data.body;
        return response
    }

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
                 />
            </DesktopLayout>
        );
    }
}


export default BiasPage;
