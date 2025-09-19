import { useEffect, useState, useRef } from "react";
import style from "./ScheduleMakePage.module.css";
import HEADER from "../../constant/header";
import justPostApi from "../../services/apis/imagePostApi";

const DesktopScheduleSelectSection = ({
  selectedSchedule, setSelectedSchedule, selectedBias,
  tryFetchNewSchedule, resetAll
}) => {

  // 실제로 선택한 종료 시간
  const [timePickerValue, setTimePickerValue] = useState({
    hour: 0,
    minute: 0,
  });

  const sampleTags= ["게임", "저챗", "음악", "그림", "스포츠", "시참"];
  const [tagsInput, setTagsInput] = useState("");
  const [tagsArrayData, setTagsArrayData] = useState([]);

  const defaultSchedule = {
    sid : "",
    title: "어떤데",
    tags : tagsArrayData,
    datetime : "",
    duration: 60
  }

  const [detailInput, setDetailInput] = useState("");
  const [durationInput, setDurationInput] = useState("");
  const [isValid, setIsValid] = useState(false);
  const [isImageUpload, setIsImageUpload] = useState(false);

  const initEditTag = (tags) => {
    if (!Array.isArray(tags) || tags.length === 0) return; // 유효성 검사

    setTagsArrayData((prev) => {
      // 기존 태그와 병합 후 중복 제거
      const uniqueTags = Array.from(new Set([...prev, ...tags]));
      return uniqueTags;
    });

    setTagsInput((prevInput) => {
      // 기존 입력값과 병합 후 쉼표로 구분된 문자열 생성
      const updatedTags = prevInput ? `${prevInput}, ${tags.join(", ")}` : tags.join(", ");
      return updatedTags;
    });
  };

  const removeTag = (index) => {
    // 특정 태그 제거
    setTagsArrayData((prevTags) => {
      const updatedTags = prevTags.filter((_, i) => i !== index);

      // `tagsInput` 업데이트: 삭제된 태그를 제외한 나머지 태그를 쉼표로 결합
      setTagsInput(updatedTags.join(", "));
      return updatedTags;
    });
  };

  const addSampleTag = (tag) => {
    if (!tagsArrayData.includes(tag)) {
      // 중복 방지
      setTagsArrayData((prev) => [...prev, tag]);
      setTagsInput((prevInput) => (prevInput ? `${prevInput}, ${tag}` : tag));
    }
  };

  const onChangeTagsInput = (e) => {
    const value = e.target.value
    setTagsInput(value)

    // 공백 제거 .filter(item => item !== ""); // 빈 항목 제거
    const splitData = value.split(",").map(item => item.trim()) 
    setTagsArrayData(splitData)

    if (value == ""){
      setTagsArrayData([])
    }
  };

  // 스케줄 상세 바꾸기
  const onChangeDetailInput = (e) => {
    setDetailInput(e.target.value);
  };

  const onChangeDurationInput = (e) => {
    // 숫자만 허용
    const onlyNumbers = e.target.value.replace(/\D/g, "");
    setDurationInput(onlyNumbers);
  };

  const [selectedAmPm, setSelectedAmPm] = useState("am"); // 기본 선택
  // 높이 결정
  const height = selectedAmPm === "pm" ? 40 : 120;

  const [hours, setHours] = useState(10);
  const [minutes, setMinutes] = useState(10);

  const intervalRef = useRef(null); // setInterval ID 저장

  // === 시간 함수 ===
  const changeHours = (delta) => {
    setHours(prev => {
      let next = (prev + delta) % 12;
      if (next === 0) next = 12; // 0이면 12로 변환

      // am/pm 전환 조건
      if ((prev === 12 && delta === 1) || (prev === 1 && delta === -1)) {
        setSelectedAmPm(prevAmPm => (prevAmPm === "am" ? "pm" : "am"));
      }

      return next;
    });
  };

  // === 분 함수 ===
  const changeMinutes = (delta) => {
    setMinutes(prev => (prev + delta + 60) % 60);
  };

  // === 버튼 눌렀을 때 반복 시작 ===
  const handleMouseDown = (type, delta) => {
    if (type === "hours") changeHours(delta);
    if (type === "minutes") changeMinutes(delta);

    intervalRef.current = setInterval(() => {
      if (type === "hours") changeHours(delta);
      if (type === "minutes") changeMinutes(delta);
    }, 150); // 150ms마다 반복
  };



  // === 버튼 뗄 때 반복 종료 ===
  const handleMouseUp = () => {
    clearInterval(intervalRef.current);
  };

  useEffect(() => {
    setDetailInput(selectedSchedule.title);
    setTagsArrayData(selectedSchedule.tags || []);
    setTagsInput((selectedSchedule.tags || []).join(", "));
    setDurationInput(selectedSchedule.duration ? String(selectedSchedule.duration) : "");
    setIsValid(selectedSchedule.is_owner);
    if (selectedSchedule.datetime) {
      const date = selectedSchedule.datetime;
      let hour = date.getHours();
      const minute = date.getMinutes();
      const ampm = hour >= 12 ? "pm" : "am";
      hour = hour % 12;
      if (hour === 0) hour = 12; // 0시는 12시로 표시
      setHours(hour);
      setMinutes(minute);
      setSelectedAmPm(ampm);
    } else {
      setHours(10);
      setMinutes(10);
      setSelectedAmPm("am");
    }
  },[selectedSchedule])

  const scheduleMaker = () => {
    const newSchedule = {
      ...selectedSchedule,
      title: detailInput,
      tags: tagsArrayData,
      bid: selectedBias,
      duration: durationInput ? parseInt(durationInput, 10) : "",
      datetime: (() => {
        const targetDate = selectedSchedule.datetime || new Date();
        return new Date(
          targetDate.getFullYear(),
          targetDate.getMonth(),
          targetDate.getDate(),
          selectedAmPm === "pm" ? (hours % 12) + 12 : hours % 12,
          minutes,
          0
        );
      })(),
    };

    setSelectedSchedule(newSchedule);
    return newSchedule; 
  };

  // image upload 로직
  const [imageFile, setImageFile] = useState([]);
  const [previewImage, setPreviewImage] = useState(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setPreviewImage(URL.createObjectURL(file));
    }
  };

  const handleFileChange = (e) => {
    const files = e.target.files[0];
    setImageFile(files);
  };

  const postImage = async () => {
    const formData = new FormData();

    if (imageFile) {
      formData.append("image", imageFile); // 하나만 업로드 → key도 단수 "image"
    }
    else{
      alert("전송할 이미지가 없어요.")
    }

    console.log(imageFile)

    const send_data = {
      header: HEADER,
      body: {
        datetime: (() => {
          const targetDate = selectedSchedule.datetime || new Date();
          return new Date(
            targetDate.getFullYear(),
            targetDate.getMonth(),
            targetDate.getDate(),
            selectedAmPm === "pm" ? (hours % 12) + 12 : hours % 12,
            minutes,
            0
          );
        })(),
        bid : selectedBias
      },
    };

    formData.append("jsonData", JSON.stringify(send_data));

    await justPostApi.post("time_table_server/try_upload_schedule_image",
      formData,
       ).then((res) => {
      if (res.data.body.result) {
        alert("전송 완료");
      }
    });
  };

  const handleMakeSchedule = async () => {
    const newSchedule = scheduleMaker(); 
    if (!newSchedule.title){
      alert("콘텐츠 제목이 없으면 업로드할 수 없어요.")
      return
    }
    await tryFetchNewSchedule(newSchedule); // 새로 만든 값 바로 사용
    resetAll();
    setImageFile(null);
    setPreviewImage(null);
  };

  return(
    <div className={style["schedule-select-section-frame-gap"]}>
      <div className={style["schedule-select-section-frame"]}>
        <div className={style["schedule-select-section-frame-wrapper"]}>
          <span className={style["bias-select-section-title"]}>콘텐츠 일정 작성 </span>
          {
            !isValid &&
              <span className={style["bias-select-section-valid-info"]}>작성자와 스트리머만 수정할 수 있어요!</span>
          }
          <div className={style["schedule-detail-frame"]}>
            <div className={style["schedule-detail-input-wrapper"]}>
                <div className={style["searchFac"]}>
                  <span>*제목</span>
                  <div className={style["searchBoxMargin"]}>
                    <div className={style["searchBox"]}>
                      {
                        isValid ? 
                        <input
                          type="text"
                          value={detailInput}
                          onChange={onChangeDetailInput}
                          placeholder="콘텐츠 일정 제목"
                        />
                        :
                        <div  className={style["detail-readonly"]}
                        >{detailInput || "일정의 이름"}</div>
                      }
                    </div>
                  </div>
                </div>

                <div className={style["searchFac"]}>
                  <span>태그</span>
                  {
                    isValid &&
                      <div className={style["sampleTagsContainer"]}>
                        {sampleTags.map((tag, index) => (
                          <div
                            className={style["sampleTag"]}
                            key={index}
                            onClick={() => addSampleTag(tag)}
                          >
                            {tag}
                          </div>
                        ))}
                      </div>
                  }

                  <div className={style["searchBoxMargin"]}>
                    <div className={style["searchBox"]}>
                      {
                        isValid ? 
                        <input
                          type="text"
                          value={tagsInput}
                          onChange={onChangeTagsInput}
                          placeholder="각 태그의 뒤에 쉼표를 입력하세요"
                        />
                        :
                        <div  className={style["detail-readonly"]}
                        >{tagsInput || "작성된 태그가 없어요"}</div>
                      }
                    </div>
                  </div>

                  <div className={style["tagsContainer"]}>
                    {tagsArrayData.map((tag, index) => (
                        <div className={style["tag"]} key={index}>
                          {tag}
                          {
                            isValid &&
                              <button
                                className={style["removeButton"]}
                                onClick={() => removeTag(index)}
                              >
                                &times;
                              </button>
                          }
                        </div>
                      ))}
                  </div>
                </div>
            </div>
            <div className={style["schedule-detail-time-selector-wrapper"]}>
                <span className={style["schedule-detail-time-selector-title"]}>시작 시간</span>
              <div className={style["schedule-time-select-box"]}>
                {/* 시간 */}

                <div className={style["time-select-part-wrapper"]}
                  style={{
                    height: `${height}px`,
                    transition: "height 0.3s ease" // 부드럽게 변화
                  }}
                >
                  <div className={style["time-select-part"]}
                    onClick={() => {
                      return isValid ? setSelectedAmPm("am") : null}
                    }
                    style={{ color : selectedAmPm === "am" ? "#111" : "#6C6C6C" }}
                  >
                    am
                  </div>
                  <div className={style["time-select-part"]}
                    onClick={() => {
                      return isValid ? setSelectedAmPm("pm") : null}
                    }
                    style={{ color : selectedAmPm === "pm" ? "#111" : "#6C6C6C" }}
                  >
                    pm
                  </div>
                </div>

                <div className={style["time-select-button-wrapper"]}>
                  {
                    isValid ?
                    <>
                      <div
                        className={style["time-select-button"]}
                        onMouseDown={() => handleMouseDown("hours", 1)}
                        onMouseUp={handleMouseUp}
                        onMouseLeave={handleMouseUp}
                      >+</div>
                      <div className={style["time-select-intager"]}>{hours.toString().padStart(2, "0")}</div>
                      <div
                        className={style["time-select-button"]}
                        onMouseDown={() => handleMouseDown("hours", -1)}
                        onMouseUp={handleMouseUp}
                        onMouseLeave={handleMouseUp}
                      >-</div>
                    </>
                    :
                    <>
                      <div
                        className={style["time-select-button"]}
                      >+</div>
                      <div className={style["time-select-intager"]}>{hours.toString().padStart(2, "0")}</div>
                      <div
                        className={style["time-select-button"]}
                      >-</div>
                    </>

                  }
                </div>

                <div className={style["time-select-intager"]}>:</div>

                {/* 분 */}
                <div className={style["time-select-button-wrapper"]}>
                  {isValid ? 
                  <>
                    <div
                      className={style["time-select-button"]}
                      onMouseDown={() => handleMouseDown("minutes", 10)}
                      onMouseUp={handleMouseUp}
                      onMouseLeave={handleMouseUp}
                    >+</div>
                    <div className={style["time-select-intager"]}>{minutes.toString().padStart(2, "0")}</div>
                    <div
                      className={style["time-select-button"]}
                      onMouseDown={() => handleMouseDown("minutes", -10)}
                      onMouseUp={handleMouseUp}
                      onMouseLeave={handleMouseUp}
                    >-</div>
                  </>
                  : 
                  <>
                    <div
                      className={style["time-select-button"]}
                    >+</div>
                    <div className={style["time-select-intager"]}>{minutes.toString().padStart(2, "0")}</div>
                    <div
                      className={style["time-select-button"]}
                    >-</div>
                  </>
                  }
                </div>
              </div>

              <div className={style["searchFac"]}>
                <span>예상 방송 시간</span>
                <div className={style["searchBoxMargin"]}>
                  <div className={style["searchBox"]}>
                    {
                      isValid ?
                        <input
                          type="text"
                          value={durationInput ? durationInput + "시간" : ""}
                          onChange={onChangeDurationInput}
                          placeholder="2시간"
                        />
                        :
                        <div  className={style["detail-readonly"]}
                        >{durationInput ? durationInput + "시간" : "예상 방송 시간이 없어요"}</div>
                    }
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className={style["schedule-make-button-wrapper"]}>
            {
              isValid &&
              <div className={style["schedule-make-button-gap"]}>
                <div className={`${style["schedule-make-button"]} ${style["delete"]}`}
                  onClick={()=>{alert("잠만 지우려고?")}}
                >삭제</div>
                <div className={`${style["schedule-make-button"]} ${style["image-upload"]}`}
                  onClick={()=>{setIsImageUpload((prev)=>!prev)}}
                >이미지 업로드</div>
                <div className={`${style["schedule-make-button"]} ${style["upload"]}`}
                  onClick={handleMakeSchedule}
                >등록하기</div>
              </div>
            }
          </div>
        </div>
      </div>
      
      <div
        style={{height: isImageUpload ? "760px" : "0px"}}
      >
        <div className={style["schedule-select-section-frame"]}>
          <div className={style["schedule-select-section-frame-wrapper"]}>
            <span className={style["bias-select-section-title"]}>콘텐츠 일정 이미지 업로드</span>
            {
              !isValid &&
                <span className={style["bias-select-section-valid-info"]}>작성자와 스트리머만 수정할 수 있어요!</span>
            }
          </div>
          <div className={style["schedule-image"]}>
            {
              previewImage && <img src={previewImage}/>
            }
          </div>
          <div className={style["schedule-make-button-wrapper"]}>
            <div className={style["schedule-make-button-gap"]}>
              <div className={`${style["schedule-make-button"]} ${style["image-upload"]}`}
                onClick={() => document.getElementById("image").click()}
              >
                파일 선택
                <input
                  id="image"
                  type="file"
                  accept="image/*"
                  name="image"
                  style={{ display: "none" }}
                  onChange={(e) => {
                    handleImageChange(e);
                    handleFileChange(e);
                  }}
                />
              </div>
              <div
                className={style["schedule-make-button"]}
                onClick={()=>{
                  alert("진짜로 업로드 하게?");
                  postImage();
                }}
              >
                업로드
              </div>
          </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default DesktopScheduleSelectSection