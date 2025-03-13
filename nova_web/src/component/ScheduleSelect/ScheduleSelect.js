import { useState } from "react";
import Input from "../Input/Input";
import "./index.css";
import Picker from "react-mobile-picker";

const date = new Date();
const year = date.getFullYear();
const month = date.getMonth() + 1;
const day = date.getDate();

const daysOfWeek = ["일요일", "월요일", "화요일", "수요일", "목요일", "금요일", "토요일"];

const selections = {
  year: Array.from({ length: 24 }, (_, i) => i + Number(year) - 12),
  month: Array.from({ length: 12 }, (_, i) => i + 1),
  day: Array.from({ length: 31 }, (_, i) => i + 1),
};

const timeSelections = {
  time: ["오전", "오후"],
  hour: Array.from({ length: 24 }, (_, i) => i),
  minute: Array.from({ length: 60 }, (_, i) => i),
};

export default function ScheduleSelect() {
  const [isStartPickerOpen, setIsStartPickerOpen] = useState(false);
  const [isEndPickerOpen, setIsEndPickerOpen] = useState(false);
  const [isStartTimePickerOpen, setIsStartTimePickerOpen] = useState(false);
  const [isEndTimePickerOpen, setIsEndTimePickerOpen] = useState(false);

  const [startPickerValue, setStartPickerValue] = useState({
    year,
    month,
    day,
  });
  const [endPickerValue, setEndPickerValue] = useState({
    year,
    month,
    day,
  });

  const [startTimePickerValue, setStartTimePickerValue] = useState({
    time: "오전",
    hour: 0,
    minute: 0,
  });
  const [endTimePickerValue, setEndTimePickerValue] = useState({
    time: "오전",
    hour: 0,
    minute: 0,
  });

  return (
    <div className="ScheduleSelect">
      <Input type={"text"} placeholder={"일정 상세"} />
      <Input placeholder={"장소"} />

      <div className="DateAndTimeInfo">
        <DatePicker
          pickerValue={startPickerValue}
          setIsOpen={setIsStartPickerOpen}
          id={"startDate"}
        />
        <TimePicker
          pickerValue={startTimePickerValue}
          setIsOpen={setIsStartTimePickerOpen}
          id={"startTime"}
        />
      </div>

      <div className="DateAndTimeInfo">
        <DatePicker pickerValue={endPickerValue} setIsOpen={setIsEndPickerOpen} id={"endDate"} />
        <TimePicker
          pickerValue={endTimePickerValue}
          setIsOpen={setIsEndTimePickerOpen}
          id={"endTime"}
        />
      </div>

      {/* 클릭 시 모달  */}
      {isStartPickerOpen && (
        <MyPicker
          pickerValue={startPickerValue}
          setPickerValue={setStartPickerValue}
          onClose={() => setIsStartPickerOpen(false)}
        />
      )}
      {isStartTimePickerOpen && (
        <TimePickers
          pickerValue={startTimePickerValue}
          setPickerValue={setStartTimePickerValue}
          onClose={() => setIsStartTimePickerOpen(false)}
        />
      )}
      {isEndPickerOpen && (
        <MyPicker
          pickerValue={endPickerValue}
          setPickerValue={setEndPickerValue}
          onClose={() => setIsEndPickerOpen(false)}
        />
      )}
      {isEndTimePickerOpen && (
        <TimePickers
          pickerValue={endTimePickerValue}
          setPickerValue={setEndTimePickerValue}
          onClose={() => setIsEndTimePickerOpen(false)}
        />
      )}
    </div>
  );
}

function DatePicker({ pickerValue, setIsOpen, id }) {
  return (
    <div className="DatePicker__container">
      <DateInfo {...pickerValue} id={id} onOpen={() => setIsOpen(true)} />
    </div>
  );
}

function TimePicker({ pickerValue, setIsOpen, id }) {
  return (
    <>
      <TimeInfo {...pickerValue} id={id} onOpen={() => setIsOpen(true)} />
    </>
  );
}

function DateInfo({ year, month, day, id, onOpen }) {
  const selectDate = new Date(year, month - 1, day);
  const selectDay = daysOfWeek[selectDate.getDay()];

  return (
    <>
      <label htmlFor={id} className="date">
        <div>{year}년</div>
        <div>{String(month).padStart(2, "0")}월</div>
        <div>{String(day).padStart(2, "0")}일</div>
        <div>{selectDay}</div>
      </label>
      <Input id={id} type={"date"} onClick={onOpen} />
    </>
  );
}

function TimeInfo({ time, hour, minute, id, onOpen }) {
  return (
    <>
      <label htmlFor={id} className="time">
        <div>{time}</div>
        <div>{`${String(hour).padStart(2, "0")}:${String(minute).padStart(2, "0")}`}</div>
      </label>
      <Input type={"time"} id={id} onClick={onOpen} />
    </>
  );
}

function MyPicker({ pickerValue, setPickerValue, onClose }) {
  return (
    <div className="DatePicker">
      <Picker value={pickerValue} onChange={setPickerValue} wheelMode="normal">
        {Object.keys(selections).map((name) => (
          <Picker.Column key={name} name={name}>
            {selections[name].map((option) => (
              <Picker.Item key={option} value={option}>
                {String(option).padStart(2, "0")}
              </Picker.Item>
            ))}
          </Picker.Column>
        ))}
      </Picker>
      <div onClick={onClose}>확인</div>
    </div>
  );
}

function TimePickers({ pickerValue, setPickerValue, onClose }) {
  return (
    <div className="TimePicker">
      <div className="TimePicker__wrapper">
        <Picker value={pickerValue} onChange={setPickerValue} wheelMode="normal">
          {Object.keys(timeSelections).map((name) => (
            <Picker.Column key={name} name={name}>
              {timeSelections[name].map((option) => (
                <Picker.Item key={option} value={option}>
                  {String(option).padStart(2, "0")}
                </Picker.Item>
              ))}
            </Picker.Column>
          ))}
        </Picker>
        <div onClick={onClose}>확인</div>
      </div>
    </div>
  );
}
