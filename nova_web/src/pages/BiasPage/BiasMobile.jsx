import { motion, AnimatePresence} from "framer-motion";
import style from "./BiasPage.module.css";
import Header from "../../component/Header/Header";
import background from "./icons/background.svg";
import AdComponent from "../../component/AdComponent/AdComponent";
import {
    getBiasStateStr, getStartTime,
    handlePreviewImage, defaultImage,
    ToggleSwitch, fetchChangeBiasIntro, fetchChangeBiasUploadMode, handleFileChange
} from "./BiasPageFunc";
import { useEffect, useRef, useState } from "react";
import { SCHEDULE_IMAGE_URL } from "../../constant/imageUrl";
import NavBar from "../../component/NavBar/NavBar";
import { BIAS_URL, DEFAULT_BIAS_URL } from "../../constant/biasUrl";
import ScheduleDetailMobile from "../../component/ScheduleDetail/ScheduleDetailMobile";

import follow from "./icons/follow.svg";
import share from "./icons/share.svg";
import chzzk_icon from "./icons/chzzk Icon_02.png";
import soop_icon from "./icons/soop Icon_02.png";
import edit1 from "./icons/edit1.svg";
import { useNavigate } from "react-router-dom";


const BiasPageMobile = ({
    scheduleList, targetBias, weekData, prevWeek,
     nextWeek, fetchTryFollowBias, is_following, isValidUser, todayIndex
}) => {
    const [isChecked, setIsChecked] = useState(false);
    const [targetSchedule, setTargetSchedule] = useState(null);
    const [showScheduleMoreOption, setShowScheduleMoreOption] = useState(false);
    const [isUploading, setIsUploading] = useState(false);

    const navigate = useNavigate();
    const [openInput, setOpenInput] = useState(false);
    const [introduce, setIntroduce] = useState("설명글 입니다.");
    const [introduceInput, setIntroduceInput] = useState(introduce);

    useEffect(()=>{
        setIsChecked(targetBias.open_content_mode);
        setIntroduce(targetBias.introduce);
        setIntroduceInput(targetBias.introduce);
    }, [targetBias])

    const handleChecked = async (checked) => {
        const res = await fetchChangeBiasUploadMode(targetBias.bid, !isChecked);
        setIsChecked(!isChecked);
    }

    const handleTargetSchedule = (schedule) => {
        setTargetSchedule(schedule.sid);
        toggleDetailOption();
    }

    const handleChangeIntroduce = async () => {
        const res = await fetchChangeBiasIntro(targetBias.bid, introduceInput);
        if (res){
            setIntroduce(introduceInput);
            setOpenInput(false);
        }
    }


    const toggleDetailOption = () => {
        setShowScheduleMoreOption(!showScheduleMoreOption);
    }

    function onChangeIntroduceInput(e) {
        setIntroduceInput(e.target.value);
    }

    // 부모 컨테이너 애니메이션 설정
    const containerVariants = {
        hidden: {},
        visible: {
            transition: {
                staggerChildren: 0.15, // 0.15초 간격으로 순차 등장
            },
        },
    };

    // 자식(각 아이템) 애니메이션 설정
    const itemVariants = {
        hidden: { opacity: 0, y: 20 }, // 아래에서 올라옴
        visible: { opacity: 1, y: 0 }, // 원래 위치
    };

    const handleCopy = () => {
        const currentUrl = window.location.href; // 현재 페이지 URL
        navigator.clipboard.writeText(currentUrl).then(() => {
            alert("URL이 클립보드에 복사되었습니다!");
        }).catch((err) => {
            console.error("클립보드 복사 실패:", err);
        });
    }


    const fileInputRef = useRef(null);
    const [imagePre, setImagePre] = useState(null);
    const [image, setImage] = useState(null);

    const handleButtonClick = () => {
        if (fileInputRef.current) {
            fileInputRef.current.click();
        }
    };

    const handlePreview = async (e) => {
        const file = e.target.files[0];
        const reader = new FileReader();
        reader.readAsDataURL(file);

        return new Promise((resolve) => {
        reader.onload = () => {
            setImagePre(reader.result || null);
            resolve();
        };
        });
    };

    return (
        <div className={style["frame"]}>
            {
                showScheduleMoreOption && 
                <ScheduleDetailMobile
                    sid={targetSchedule}
                    toggleDetailOption={toggleDetailOption}
                />
            }
            <div className={style["top-bar"]}>
                <Header/>
            </div>
            <AdComponent type={"link"}/>

            {
                isUploading && (
                    <div className={style["upload-feedback-background"]}>
                    <div className={style["upload-feedback"]}>
                        업로드 중입니다.
                    </div>
                    </div>
                )
            }

            <div className={style["inner-box"]}>
                <div className={style["inner-box-top-section"]}>
                    <div className={style["bias-meta-data-wrapper"]}>
                        <div className={style["bias-share-wrapper"]}>
                            <div className={style["bias-share-button"]}>
                                <div className={style["bias-share-icon"]}>
                                    <img src={share}/>
                                </div>
                                <div className={style["bias-share-text"]}
                                    onClick={handleCopy}
                                >
                                    이 페이지 공유
                                </div>
                            </div>
                        </div>

                        <div className={style["bias-image-outer-wrapper"]}>
                            <div className={style["bias-image-wrapper"]}
                                onClick={() => fileInputRef.current?.click()} // 클릭 시 input 열기
                            >
                                <img src={BIAS_URL + `${targetBias.bimage}.png`}
                                    onError={(e) => {
                                    e.currentTarget.onerror = null;
                                    e.currentTarget.src = DEFAULT_BIAS_URL;
                                    }}
                                    alt="bias"
                                />
                                {
                                    isValidUser && (
                                        <input
                                            type="file"
                                            accept="image/*"
                                            ref={fileInputRef}
                                            onChange={async(e) => {
                                                setIsUploading(true);
                                                await handleFileChange(e, targetBias.bid, setImage);
                                                await handlePreview(e);
                                                setIsUploading(false);
                                            }}
                                            style={{ display: "none" }} 
                                        />
                                    )
                                }
                            </div>
                            {
                                isValidUser && (
                                    <div className={style["image-change-meta-text"]}>
                                        이미지를 변경하려면 이미지를 터치하세요!
                                    </div>
                                )
                            }
                        </div>
                        <div className={style["bias-detail-container-wrapper"]}>
                            <div className={style["bias-name-container"]}>
                                <div className={style["bias-platform-icon"]}>
                                    {
                                        targetBias.platform == "치지직" ? (
                                            <img src={chzzk_icon}/>
                                        ):(
                                            <img src={soop_icon}/>
                                        )
                                    }
                                </div>
                                <div className={style["bias-name"]}>
                                    {targetBias.bname}
                                </div>
                            </div>

                            <div className={style["bias-introduce-wrapper"]}>
                                <div className={style["bias-introduce-myself"]}>
                                    {introduce}
                                </div>
                                {
                                    isValidUser && (
                                        <div className={style["platform-direct-follow-icon"]}
                                            onClick={()=>setOpenInput(!openInput)}
                                        >
                                            <img src={edit1}/>
                                        </div>
                                    )
                                }
                            </div>
                            {
                                openInput && (
                                    <div className={style["bias-introduce-input-wrapper"]}>
                                        <input className={style["bias-introduce-input"]}
                                            value={introduceInput}
                                            onChange={(e) => {
                                                onChangeIntroduceInput(e);
                                            }}
                                            placeholder={"자기소개를 입력하세요."}
                                            type="text"
                                            enterKeyHint="done"
                                        />
                                        <div className={style["fetch-intro-button"]}
                                            onClick={handleChangeIntroduce}
                                        >
                                            완료
                                        </div>
                                    </div>
                                )
                            }
                            {
                                isValidUser && (
                                    <div className={style["bias-option-wrapper"]}>
                                        <div className={style["bias-option-text"]}>
                                            열린 일정 모드
                                        </div>
                                        <div className={style["bias-option-toggle-button"]}>
                                            <ToggleSwitch
                                                id={"bias-option-input"}
                                                isChecked={isChecked}
                                                handleChecked={handleChecked}
                                            />
                                        </div>
                                    </div>
                                )
                            }
                        </div>
                    </div>
                    <div className={style["bias-meta-data-button-container"]}>
                        <div className={style["bias-meta-data-left-button"]}
                            onClick={()=>{fetchTryFollowBias(targetBias.bid)}}
                        >
                            <div className={style["platform-direct-follow-icon"]}>
                                <img src={follow}/>
                            </div>
                            <div className={style["platform-direct-follow-text"]}>
                                {
                                    is_following ?  "팔로우 중" : "팔로우"
                                }
                            </div>
                        </div>
                        <div className={style["bias-meta-data-right-button"]}
                            onClick={() => {
                                if (targetBias.platform_url != "https://supernova.io.kr"){
                                    window.open(targetBias.platform_url, "_blank")
                                } else{
                                    if (targetBias.platform == "치지직"){
                                        window.open(`https://chzzk.naver.com/search?query=${targetBias.bname}`, "_blank")
                                    }else{
                                        window.open(`https://www.sooplive.co.kr/search?szLocation=total_search&szSearchType=total&szKeyword=${targetBias.bname}&szStype=di&szActype=input_field`, "_blank")
                                    }
                                }
                            }}
                        >플랫폼 바로가기</div>
                    </div>
                </div>


                <div className={style["week-select-box"]}>
                    <div className={style["week-select-button-wrapper"]}>
                        <div className={style["prev-button"]}
                            onClick={prevWeek}
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 22 22" fill="none">
                                <rect width="22" height="22" rx="11" fill="white"/>
                                <path d="M14 5L7.06667 10.2C6.53333 10.6 6.53333 11.4 7.06667 11.8L14 17" stroke="#24272C" strokeWidth="1.5" strokeLinecap="round"/>
                            </svg>
                        </div>

                        <div className={style["week-data"]}>{`${weekData} 일정`}</div>

                        <div className={style["next-button"]}
                            onClick={nextWeek}
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 22 22" fill="none">
                                <rect width="22" height="22" rx="11" transform="matrix(-1 0 0 1 22 0)" fill="white"/>
                                <path d="M8 5L14.9333 10.2C15.4667 10.6 15.4667 11.4 14.9333 11.8L8 17" stroke="#24272C" strokeWidth="1.5" strokeLinecap="round"/>
                            </svg>
                        </div>
                    </div>
                </div>
                <motion.div
                    className={style["schedule-list-wrapper"]}
                    variants={containerVariants}
                    initial="hidden"
                    animate="visible"
                    key={scheduleList.map(s => s.schedule.sid || s.date).join("-")} 
                    // scheduleList가 바뀌면 key가 바뀌어 animate 재실행
                >
                    <AnimatePresence>
                        {scheduleList.map((schedule, index) => (
                            <motion.div
                                key={schedule.schedule.sid || schedule.date} // 고유 key
                                className={style["single-schedule-wrapper"]}
                                variants={itemVariants}
                                initial="hidden"
                                animate="visible"
                                exit={{ opacity: 0, y: 20 }}
                                transition={{ duration: 0.5, ease: "easeOut" }}
                            >
                                {schedule.schedule.sid !== "" ? (
                                    <ScheduleComponent 
                                        schedule={schedule.schedule}
                                        metaData={schedule}
                                        handleTargetSchedule={handleTargetSchedule} 
                                        index={index}
                                        todayIndex={todayIndex}
                                    />
                                ) : (
                                    <EmptyScheduleComponent 
                                        scheduleData={schedule}
                                        metaData={schedule}
                                        index={index}
                                        todayIndex={todayIndex}
                                        navigate={navigate}
                                    />
                                )}
                                {
                                    index != 6 && (
                                        <div className={style["schedule-connect-line"]}>
                                        </div>
                                    )
                                }

                            </motion.div>
                        ))}
                    </AnimatePresence>
                </motion.div>

                <div className={style["background-gradient"]}>
                    <img src={background}/>
                </div>
            </div>
            <div style={{height:"100px"}}> </div>
            <NavBar />
        </div>
    );
}



const EmptyScheduleComponent = ({scheduleData, metaData, index, todayIndex, navigate}) => {

    const navigateToMakeNew = () => {
        navigate(`/schedule/make_new?targetBias=${scheduleData.bid}&targetDate=${scheduleData.str_date}`)
    }

    if (index == todayIndex){
        return(
            <div className={style["single-schedule-container-today"]}
                onClick={navigateToMakeNew}
            >
                <div className={style["schedule-datetime-wrapper"]}>
                    <div className={style["schedule-datetime"]}>
                        {metaData.date || "날짜 없음"}
                    </div>
                    <div className={style["datetime-weekday"]}>
                        {metaData.weekday || ""}
                    </div>
                </div>
                <div className={style["empty-schedule"]}>휴방 / 미지정</div>
            </div>
        );
    }else{
        return(
            <div className={style["single-schedule-container"]}
                onClick={navigateToMakeNew}
            >
                <div className={style["schedule-datetime-wrapper"]}>
                    <div className={style["schedule-datetime"]}>
                        {metaData.date || "날짜 없음"}
                    </div>
                    <div className={style["datetime-weekday"]}>
                        {metaData.weekday || ""}
                    </div>
                </div>
                <div className={style["empty-schedule"]}>휴방 / 미지정</div>
            </div>
        );
    }
}


const ScheduleComponent = ({schedule, metaData, handleTargetSchedule, index, todayIndex}) => {
    const [image, setImage] = useState(null);

    useEffect(()=>{
        const url = `${SCHEDULE_IMAGE_URL}${schedule.simage}.png`;
        handlePreviewImage(url, setImage);
    }, [])

    if (index == todayIndex){
        return(
            <div className={style["single-schedule-container-today"]}
                onClick={()=>{handleTargetSchedule(schedule)}}
            >
                <div className={style["schedule-datetime-wrapper"]}>
                    <div className={style["schedule-datetime"]}>
                        {metaData.date || "날짜 없음"}
                    </div>
                    <div className={style["datetime-weekday"]}>
                        {metaData.weekday || ""}
                    </div>
                </div>
                <div className={style["single-schedule-container-wrapper"]}>
                    <div className={style["single-schedule-image"]}>
                        {
                            image != null ? (
                                <img src={image} alt="스케줄 이미지" />
                            ) : (
                                <img src={defaultImage} alt="스케줄 이미지" />
                            )
                        }   
                    </div>
                    <div className={style["single-schedule-detail-wrapper"]}>
                        <div className={style["single-schedule-title-wrapper"]}>
                            <div className={style["single-schedule-title"]}>
                                {schedule.title || "콘텐츠 없음"}
                            </div>
                            <div className={style["single-start-time"]}>
                                {
                                    getStartTime(schedule.datetime)
                                }
                            </div>
                        </div>
                        <div className={style["schedule-tag-wrapper"]}>
                            {schedule.tags.length > 0 ? (
                                schedule.tags.slice(0, 3).map((tag, tIdx) => (
                                    <div key={tIdx} className={style["tag"]}>
                                        {tag}
                                    </div>
                                ))
                            ) : (
                                <div className={style["tag"]}>-</div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        );
    }else{
        return(
            <div className={style["single-schedule-container"]}
                onClick={()=>{handleTargetSchedule(schedule)}}
            >
                <div className={style["schedule-datetime-wrapper"]}>
                    <div className={style["schedule-datetime"]}>
                        {metaData.date || "날짜 없음"}
                    </div>
                    <div className={style["datetime-weekday"]}>
                        {metaData.weekday || ""}
                    </div>
                </div>
                <div className={style["single-schedule-container-wrapper"]}>
                    <div className={style["single-schedule-image"]}>
                        {
                            image != null ? (
                                <img src={image} alt="스케줄 이미지" />
                            ) : (
                                <img src={defaultImage} alt="스케줄 이미지" />
                            )
                        }   
                    </div>
                    <div className={style["single-schedule-detail-wrapper"]}>
                        <div className={style["single-schedule-title-wrapper"]}>
                            <div className={style["single-schedule-title"]}>
                                {schedule.title || "콘텐츠 없음"}
                            </div>
                            <div className={style["single-start-time"]}>
                                {
                                    getStartTime(schedule.datetime)
                                }
                            </div>
                        </div>
                        <div className={style["schedule-tag-wrapper"]}>
                            {schedule.tags.length > 0 ? (
                                schedule.tags.slice(0, 3).map((tag, tIdx) => (
                                    <div key={tIdx} className={style["tag"]}>
                                        {tag}
                                    </div>
                                ))
                            ) : (
                                <div className={style["tag"]}>-</div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        );

    }

}




export default BiasPageMobile;