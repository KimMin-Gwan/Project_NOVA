import React, { useState, useRef, useEffect } from "react";
import Input from "../Input/Input";
import style from "./style.module.css";
import "./scheduleSelcetStyle.css";
import Picker from "react-mobile-picker";
import down_arrow from "./Expand_down_light.svg";

const date = new Date();
const year = date.getFullYear();
const month = date.getMonth() + 1;
const day = date.getDate();

const daysOfWeek = [
  "일요일",
  "월요일",
  "화요일",
  "수요일",
  "목요일",
  "금요일",
  "토요일",
];

const getDaysInMonth = (year, month) => {
  return new Date(year, month, 0).getDate();
};

export default function ScheduleSelect({
  index,
  setSendScheduleData,
  sendScheduleData,  // fetch에 보낼 스케줄 데이터
  isEditMode,
  targetSchedule, // fetch로 받아온 수정용 데이터
}) {
  //파라미터로 넘어온 데이터 에서 location이랑 sname 바꾸는 함수
  const handleScheduleChange = (field, value) => {  
    setSendScheduleData((prevState) => {
      const updatedSchedules = [...prevState.schedules];
      updatedSchedules[index] = { ...updatedSchedules[index], [field]: value };
      return { ...prevState, schedules: updatedSchedules };
    });
  }

  // Picker 에서 선택 가능한 시간 범위
  // 근데 이 친구는 왜 함수 밖에 있냐? 뭐지?
  const timeSelections = {
    hour: Array.from({ length: 24 }, (_, i) => i),
    minute: Array.from({ length: 60 }, (_, i) => i),
  };

  // 파라미터로 넘어온 데이터에서 schedule 데이터 바꾸는 함수
  const handleScheduleDateTimeChange = (
    startDate,
    endDate,
    startTime,
    endTime
  ) => {
    const updatedSchedules = [...sendScheduleData.schedules];
    updatedSchedules[index] = {
      ...updatedSchedules[index],
      start_date: startDate,
      end_date: endDate,
      start_time: startTime,
      end_time: endTime,
    };
    setSendScheduleData({ ...sendScheduleData, schedules: updatedSchedules });
  };

  // 시작 시간 선택 플래그 같은거임
  const [isStartYearPickerOpen, setIsStartYearPickerOpen] = useState(false);
  const [isStartMonthPickerOpen, setIsStartMonthPickerOpen] = useState(false);
  const [isStartDayPickerOpen, setIsStartDayPickerOpen] = useState(false);
  const [isStartTimePickerOpen, setIsStartTimePickerOpen] = useState(false);

  // 종료 시간 선택 플래그 같은거임
  const [isEndYearPickerOpen, setIsEndYearPickerOpen] = useState(false);
  const [isEndMonthPickerOpen, setIsEndMonthPickerOpen] = useState(false);
  const [isEndDayPickerOpen, setIsEndDayPickerOpen] = useState(false);
  const [isEndTimePickerOpen, setIsEndTimePickerOpen] = useState(false);

  const [tagsInput, setTagsInput] = useState("");
  const [tagsArrayData, setTagsArrayData] = useState([]);
  const [sid, setSid] = useState("");
  const [bid, setBid] = useState("");

  // 실제로 선택한 시작 날짜
  const [startPickerValue, setStartPickerValue] = useState({
    year,
    month,
    day,
  });

  // 실제로 선택된 종료 시간
  const [endPickerValue, setEndPickerValue] = useState({
    year,
    month,
    day,
  });

  // 실제로 선택한 시작 시간
  const [startTimePickerValue, setStartTimePickerValue] = useState({
    hour: 0,
    minute: 0,
  });

  // 실제로 선택한 종료 시간
  const [endTimePickerValue, setEndTimePickerValue] = useState({
    hour: 0,
    minute: 0,
  });

  // 요일 선택해주는 useState
  const [startWeek, setStartWeek] = useState(() => {
    const selectDate = new Date(year, month - 1, day);
    return daysOfWeek[selectDate.getDay()];
  });
  const [endWeek, setEndWeek] = useState(() => {
    const selectDate = new Date(year, month - 1, day);
    return daysOfWeek[selectDate.getDay()];
  });

  // 일 수를 31, 30 이런식으로 잡으려고 만든거
  const daysInMonth =
    startPickerValue.year && startPickerValue.month
      ? getDaysInMonth(startPickerValue.year, startPickerValue.month)
      : 31;

  // Picker 에서  선택가능한 날짜의 범위
  const selections = {
    year: Array.from({ length: 4 }, (_, i) => i + Number(year)),
    month: Array.from({ length: 12 }, (_, i) => i + 1),
    day: Array.from({ length: daysInMonth }, (_, i) => i + 1),
  };

  // 특정 연도, 월에 해당하는 마지막 유효 날짜를 반환
  const getValidDay = (year, month, day) => {
    const daysInMonth = new Date(year, month, 0).getDate(); // 해당 월의 마지막 날짜
    return Math.min(day, daysInMonth); // 유효한 날짜 범위 내에서만 설정
  };

  // Picker 값을 설정할 때 날짜가 유효한 범위 내로 조정
  const validateAndSetPickerValue = (year, month, day, setPickerValue) => {
    const validDay = getValidDay(year, month, day); // 유효한 날짜로 수정
    setPickerValue({ year, month, day: validDay });
  };

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

  // 수정하기 전용 초기 데이터 세팅 하는 곳
  // 초기화임 중요한 부분임
  useEffect(() => {
    if (isEditMode) {
      if (targetSchedule) {
        setTagsArrayData([]);
        setTagsInput("");
        setStartPickerValue({
          year: targetSchedule.startYear,
          month: targetSchedule.startMonth,
          day: targetSchedule.startDay,
        });
        setEndPickerValue({
          year: targetSchedule.endYear,
          month: targetSchedule.endMonth,
          day: targetSchedule.endDay,
        });
        setStartTimePickerValue({
          hour: targetSchedule.startHour,
          minute: targetSchedule.startMinute,
        });
        setEndTimePickerValue({
          hour: targetSchedule.endHour,
          minute: targetSchedule.endMinute,
        });
        setDetailInput(targetSchedule.sname);
        setPlaceInput(targetSchedule.location);
        setSid(targetSchedule.sid);
        setBid(targetSchedule.bid);
        initEditTag(targetSchedule.tags)

        const targetStartDate = `${targetSchedule.startYear}/${targetSchedule.startMonth}/${targetSchedule.startDay}`;
        const targetEndDate = `${targetSchedule.endYear}/${targetSchedule.endMonth}/${targetSchedule.endDay}`;
        const targetStartTime = `${targetSchedule.startHour}:${targetSchedule.startMinute}`;
        const targetEndTime = `${targetSchedule.endHour}:${targetSchedule.endMinute}`;

        handleScheduleDateTimeChange(
          targetStartDate,
          targetEndDate,
          targetStartTime,
          targetEndTime
        );
      }
    }
  }, [targetSchedule]);

  // 무슨 요일인지 맞춰주는 마법같은 함수
  useEffect(() => {
    updateDaysOfWeek(
      startPickerValue.year,
      startPickerValue.month,
      startPickerValue.day,
      setStartWeek
    );
  }, [startPickerValue]);

  // 무슨 요일인지 맞춰주는 마법같은 함수
  useEffect(() => {
    updateDaysOfWeek(
      endPickerValue.year,
      endPickerValue.month,
      endPickerValue.day,
      setEndWeek
    );
  }, [endPickerValue]);

  // 예시: startPickerValue가 변경될 때 날짜를 검증하여 유효한 날짜로 수정
  useEffect(() => {
    validateAndSetPickerValue(
      startPickerValue.year,
      startPickerValue.month,
      startPickerValue.day,
      setStartPickerValue
    );
  }, [startPickerValue.year, startPickerValue.month]);

  useEffect(() => {
    validateAndSetPickerValue(
      endPickerValue.year,
      endPickerValue.month,
      endPickerValue.day,
      setEndPickerValue
    );
  }, [endPickerValue.year, endPickerValue.month]);

  // 시작시간보다 종료시간이 더 빠른 말이 안되는 상황을 해결해주는 마법
  useEffect(() => {
    // 날짜와 시간 설정
    const startDate = new Date(
      startPickerValue.year,
      startPickerValue.month - 1,
      startPickerValue.day,
      startTimePickerValue.hour,
      startTimePickerValue.minute,
      0,
      0
    );

    const endDate = new Date(
      endPickerValue.year,
      endPickerValue.month - 1,
      endPickerValue.day,
      endTimePickerValue.hour,
      endTimePickerValue.minute,
      0,
      0
    );

    if (startDate > endDate) {
      // start가 end보다 크면 end를 start와 같게 조정
      setEndPickerValue({
        year: startPickerValue.year,
        month: startPickerValue.month,
        day: startPickerValue.day,
      });

      setEndTimePickerValue({
        hour: startTimePickerValue.hour,
        minute: startTimePickerValue.minute,
      });
    }
  }, [
    startPickerValue,
    endPickerValue,
    startTimePickerValue,
    endTimePickerValue,
  ]);

  // Picker 에서 선택하면 실제로 바꿔주는 함수
  const updatePickerField = (field, value, setValue) => {
    setValue((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  // Picker 에서 선택하면 실제로 바꿔주는 함수
  const updateTimePickerField = (field, value, setValue) => {
    setValue((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  // 무슨요일인지 바꿔주는 인터페이스
  const updateDaysOfWeek = (year, month, day, setWeek) => {
    const selectDate = new Date(year, month - 1, day);
    setWeek(daysOfWeek[selectDate.getDay()]);
  };

 
  const sampleTags= ["게임", "저챗", "음악", "그림", "스포츠", "시참"];
  // 장소 및 일정 디테일 입력
  const [detailInput, setDetailInput] = useState("");

  const [placeInput, setPlaceInput] = useState("");

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

  const removeTag = (index) => {
    // 특정 태그 제거
    setTagsArrayData((prevTags) => {
      const updatedTags = prevTags.filter((_, i) => i !== index);

      // `tagsInput` 업데이트: 삭제된 태그를 제외한 나머지 태그를 쉼표로 결합
      setTagsInput(updatedTags.join(", "));
      return updatedTags;
    });
  };

  // 스케줄 상세 바꾸기
  const onChangeDetailInput = (e) => {
    setDetailInput(e.target.value);
  };

  // 스케줄 장소 바꾸기
  const onChangePlaceInput = (e) => {
    setPlaceInput(e.target.value);
  };

  const addSampleTag = (tag) => {
    if (!tagsArrayData.includes(tag)) {
      // 중복 방지
      setTagsArrayData((prev) => [...prev, tag]);
      setTagsInput((prevInput) => (prevInput ? `${prevInput}, ${tag}` : tag));
    }
  };




  // 변경이 있고 나서 전송용 데이터를 수정하게 하는 useEffect
  useEffect(() => {
    const targetStartDate = `${startPickerValue.year}/${startPickerValue.month}/${startPickerValue.day}`;
    const targetEndDate = `${endPickerValue.year}/${endPickerValue.month}/${endPickerValue.day}`;
    const targetStartTime = `${startTimePickerValue.hour}:${startTimePickerValue.minute}`;
    const targetEndTime = `${endTimePickerValue.hour}:${endTimePickerValue.minute}`;

    handleScheduleDateTimeChange(
      targetStartDate,
      targetEndDate,
      targetStartTime,
      targetEndTime
    );
  }, [
    startPickerValue,
    endPickerValue,
    startTimePickerValue,
    endTimePickerValue,
  ]);

  // 위와 같은 목적 => bid
  useEffect(() => {
    handleScheduleChange("bid", bid);
  }, [sid]);

  // 위와 같은 목적 => sid
  useEffect(() => {
    handleScheduleChange("sid", sid);
  }, [sid]);

  // 위와 같은 목적 => sname
  useEffect(() => {
    handleScheduleChange("sname", detailInput);
  }, [detailInput]);

  // 위와 같은 목적 => sname
  useEffect(() => {
    handleScheduleChange("tags", tagsArrayData);
  }, [tagsArrayData]);

  // 위와 같은 목적 => location
  useEffect(() => {
    handleScheduleChange("location", placeInput);
  }, [placeInput]);

  return (
    <div className="ScheduleSelect">
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
        <span>*장소</span>
        <div className={style["searchBoxMargin"]}>
          <div className={style["searchBox"]}>
            <input
              type="text"
              value={placeInput}
              onChange={onChangePlaceInput}
              placeholder="쉼표(,)를 사용하여 여러개의 장소를 입력"
            />
          </div>
        </div>
      </div>

      <div className={style["searchFac"]}>
        <span>*시간</span>
      </div>

      <div className="DateAndTimeInfo">
        <DatePicker
          index={index}
          {...startPickerValue}
          setIsYearPickerOpen={setIsStartYearPickerOpen}
          setIsMonthPickerOpen={setIsStartMonthPickerOpen}
          setIsDayPickerOpen={setIsStartDayPickerOpen}
          isYearPickerOpen={isStartYearPickerOpen}
          isMonthPickerOpen={isStartMonthPickerOpen}
          isDayPickerOpen={isStartDayPickerOpen}
          type={"시작"}
          weekDay={startWeek}
        />
        <div></div>
        <TimePicker
          pickerValue={startTimePickerValue}
          setIsOpen={setIsStartTimePickerOpen}
          id={"startTime"}
          isOpen={isStartTimePickerOpen}
        />
      </div>

      <div className="DateAndTimeInfo">
        <DatePicker
          {...endPickerValue}
          setIsYearPickerOpen={setIsEndYearPickerOpen}
          setIsMonthPickerOpen={setIsEndMonthPickerOpen}
          setIsDayPickerOpen={setIsEndDayPickerOpen}
          isYearPickerOpen={isEndYearPickerOpen}
          isMonthPickerOpen={isEndMonthPickerOpen}
          isDayPickerOpen={isEndDayPickerOpen}
          type={"종료"}
          weekDay={endWeek}
        />
        <TimePicker
          index={index}
          pickerValue={endTimePickerValue}
          setIsOpen={setIsEndTimePickerOpen}
          id={"endTime"}
          isOpen={isEndTimePickerOpen}
        />
      </div>

      <div style={{height : "20px"}}></div>

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

      {/** 시작시간 선택 모달 */}
      {isStartYearPickerOpen && (
        <MyPicker
          pickerValue={{ year: startPickerValue.year }}
          displayData={selections.year}
          setPickerValue={updatePickerField}
          onClose={() => setIsStartYearPickerOpen(false)}
          type={"year"}
          setValue={setStartPickerValue}
        />
      )}
      {isStartMonthPickerOpen && (
        <MyPicker
          pickerValue={{ month: startPickerValue.month }}
          displayData={selections.month}
          setPickerValue={updatePickerField}
          onClose={() => setIsStartMonthPickerOpen(false)}
          type={"month"}
          setValue={setStartPickerValue}
        />
      )}
      {isStartDayPickerOpen && (
        <MyPicker
          pickerValue={{ day: startPickerValue.day }}
          displayData={selections.day}
          setPickerValue={updatePickerField}
          onClose={() => setIsStartDayPickerOpen(false)}
          type={"day"}
          setValue={setStartPickerValue}
        />
      )}
      {isStartTimePickerOpen && (
        <TimePickers
          pickerValue={startTimePickerValue}
          setPickerValue={setStartTimePickerValue}
          displayData={timeSelections}
          onClose={() => setIsStartTimePickerOpen(false)}
        />
      )}

      {/* 종료 시간 선택 모달 */}
      {isEndYearPickerOpen && (
        <MyPicker
          pickerValue={{ year: endPickerValue.year }}
          displayData={selections.year}
          setPickerValue={updatePickerField}
          onClose={() => setIsEndYearPickerOpen(false)}
          type={"year"}
          setValue={setEndPickerValue}
        />
      )}
      {isEndMonthPickerOpen && (
        <MyPicker
          pickerValue={{ month: endPickerValue.month }}
          displayData={selections.month}
          setPickerValue={updatePickerField}
          onClose={() => setIsEndMonthPickerOpen(false)}
          type={"month"}
          setValue={setEndPickerValue}
        />
      )}
      {isEndDayPickerOpen && (
        <MyPicker
          pickerValue={{ day: endPickerValue.day }}
          displayData={selections.day}
          setPickerValue={updatePickerField}
          onClose={() => setIsEndDayPickerOpen(false)}
          type={"day"}
          setValue={setEndPickerValue}
        />
      )}
      {isEndTimePickerOpen && (
        <TimePickers
          pickerValue={endTimePickerValue}
          setPickerValue={setEndTimePickerValue}
          displayData={timeSelections}
          onClose={() => setIsEndTimePickerOpen(false)}
        />
      )}
    </div>
  );
}

function DatePicker({
  year,
  month,
  day,
  setIsYearPickerOpen,
  setIsMonthPickerOpen,
  setIsDayPickerOpen,
  isYearPickerOpen,
  isMonthPickerOpen,
  isDayPickerOpen,
  type,
  weekDay,
  index,
}) {
  const selectDate = new Date(year, month - 1, day);
  return (
    <div className="DatePicker__container">
      <div className="date">{type}</div>
      <YearInfo
        year={year}
        setIsOpen={setIsYearPickerOpen}
        isOpen={isYearPickerOpen}
      />
      <MonthInfo
        month={month}
        setIsOpen={setIsMonthPickerOpen}
        isOpen={isMonthPickerOpen}
      />
      <DayInfo
        day={day}
        setIsOpen={setIsDayPickerOpen}
        isOpen={isDayPickerOpen}
      />
      <div>{weekDay}</div>
    </div>
  );
}

function TimePicker({ pickerValue, setIsOpen, id, isOpen }) {
  return (
    <div className="TimePicker__container">
      <TimeInfo {...pickerValue} id={id} onOpen={setIsOpen} isOpen={isOpen} />
    </div>
  );
}

function UpDownArrow({ isOpen }) {
  return (
    <img
      src={down_arrow} // 항상 같은 이미지 사용
      alt="arrow"
      className={`arrow ${isOpen ? "open" : "closed"}`}
    />
  );
}

function DayInfo({ day, setIsOpen, isOpen }) {
  return (
    <div className="date" onClick={() => setIsOpen(true)}>
      <div>{String(day).padStart(2, "0")}일</div>
      <UpDownArrow isOpen={isOpen} />
    </div>
  );
}

function MonthInfo({ month, setIsOpen, isOpen }) {
  return (
    <div className="date" onClick={() => setIsOpen(true)}>
      <div>{String(month).padStart(2, "0")}월</div>
      <UpDownArrow isOpen={isOpen} />
    </div>
  );
}

function YearInfo({ year, setIsOpen, isOpen }) {
  return (
    <div className="date" onClick={() => setIsOpen(true)}>
      <div>{year}년</div>
      <UpDownArrow isOpen={isOpen} />
    </div>
  );
}

function TimeInfo({ index, hour, minute, id, onOpen, isOpen }) {
  return (
    <>
      <label htmlFor={id} className="time" onClick={() => onOpen(true)}>
        <div>{`${String(hour).padStart(2, "0")}:${String(minute).padStart(
          2,
          "0"
        )}`}</div>
        <UpDownArrow isOpen={isOpen} index={index} />
      </label>
    </>
  );
}

function MyPicker({
  pickerValue,
  displayData,
  setPickerValue,
  onClose,
  type,
  setValue,
}) {
  return (
    <div className="PickerMoreContainer">
      <div className="DatePicker">
        <Picker
          value={pickerValue}
          onChange={(name, _) => {
            setPickerValue(type, name[type], setValue);
          }}
          wheelMode="normal"
        >
          <Picker.Column name={type}>
            {displayData.map((option) => (
              <Picker.Item key={option} value={option}>
                {String(option).padStart(2, "0")}
              </Picker.Item>
            ))}
          </Picker.Column>
        </Picker>
        <div className="ok-button" onClick={onClose}>
          확인
        </div>
      </div>
    </div>
  );
}

function TimePickers({ pickerValue, setPickerValue, displayData, onClose }) {
  return (
    <div className="TimeMoreContainer">
      <div className="TimePicker">
        <div className="TimePicker__wrapper">
          <Picker
            value={pickerValue}
            onChange={setPickerValue}
            wheelMode="normal"
          >
            {Object.keys(displayData).map((name) => (
              <Picker.Column key={name} name={name}>
                {displayData[name].map((option) => (
                  <Picker.Item key={option} value={option}>
                    {String(option).padStart(2, "0")}
                  </Picker.Item>
                ))}
              </Picker.Column>
            ))}
          </Picker>
          <div className="ok-button" onClick={onClose}>
            확인
          </div>
        </div>
      </div>
    </div>
  );
}
