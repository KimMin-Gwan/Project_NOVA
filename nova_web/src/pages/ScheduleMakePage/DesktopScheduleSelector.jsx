import { useEffect, useState, useRef } from "react";
import style from "./ScheduleMakePage.module.css";

const DesktopScheduleSelectSection = ({
  selectedSchedule, setSelectedSchedule
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
  const [scheduleDetail, setScheduleDetail] = useState(defaultSchedule);
  const [durationInput, setDurationInput] = useState("");

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


  useEffect(()=>{
    initEditTag(scheduleDetail.tags);
  },[])

  useEffect(() => {
    setDetailInput(selectedSchedule.title);
    setTagsArrayData(selectedSchedule.tags || []);
    setTagsInput((selectedSchedule.tags || []).join(", "));
    setDurationInput(selectedSchedule.duration ? String(selectedSchedule.duration) : "");
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

  console.log(selectedAmPm);

  return(
    <div className={style["schedule-select-section-frame"]}>
      <span className={style["bias-select-section-title"]}>콘텐츠 일정 작성 </span>
      <div className={style["schedule-detail-frame"]}>
        <div className={style["schedule-detail-input-wrapper"]}>
            <div className={style["searchFac"]}>
              <span>*이름</span>
              <div className={style["searchBoxMargin"]}>
                <div className={style["searchBox"]}>
                  <input
                    type="text"
                    value={detailInput}
                    onChange={onChangeDetailInput}
                    placeholder="일정의 이름"
                  />
                </div>
              </div>
            </div>

            <div className={style["searchFac"]}>
              <span>태그</span>
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

              <div className={style["searchBoxMargin"]}>
                <div className={style["searchBox"]}>
                  <input
                    type="text"
                    value={tagsInput}
                    onChange={onChangeTagsInput}
                    placeholder="각 태그의 뒤에 쉼표를 입력하세요"
                  />
                </div>
              </div>

              <div className={style["tagsContainer"]}>
                {tagsArrayData.map((tag, index) => (
                    <div className={style["tag"]} key={index}>
                      {tag}
                      <button
                        className={style["removeButton"]}
                        onClick={() => removeTag(index)}
                      >
                        &times;
                      </button>
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
                onClick={() => setSelectedAmPm("am")}
                style={{ color : selectedAmPm === "am" ? "#111" : "#6C6C6C" }}
              >
                am
              </div>
              <div className={style["time-select-part"]}
                onClick={() => setSelectedAmPm("pm")}
                style={{ color : selectedAmPm === "pm" ? "#111" : "#6C6C6C" }}
              >
                pm
              </div>
            </div>

            <div className={style["time-select-button-wrapper"]}>
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
            </div>

            <div className={style["time-select-intager"]}>:</div>

            {/* 분 */}
            <div className={style["time-select-button-wrapper"]}>
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
            </div>
          </div>

          <div className={style["searchFac"]}>
            <span>예상 방송 시간</span>
            <div className={style["searchBoxMargin"]}>
              <div className={style["searchBox"]}>
                <input
                  type="text"
                  value={durationInput ? durationInput + "시간" : ""}
                  onChange={onChangeDurationInput}
                  placeholder="2시간"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default DesktopScheduleSelectSection