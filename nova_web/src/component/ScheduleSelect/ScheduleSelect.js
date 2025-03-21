import { useState } from "react";
import Input from "../Input/Input";
import style from "./style.module.css";
import "./index.css";
import Picker from "react-mobile-picker";
import down_arrow from "./Expand_down_light.svg"
import up_arrow from "./Expand_up_light.svg"

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


export function MakeScheduleDetail() {
  const [isStartPickerOpen, setIsStartPickerOpen] = useState(false);
  const [isStartTimePickerOpen, setIsStartTimePickerOpen] = useState(false);

  const [searchKeyword, setKeyword] = useState("");

  const onChangeSearchKeyWord = (e) => {
    setKeyword(e.target.value);
  };

  const [startPickerValue, setStartPickerValue] = useState({
    year,
    month,
    day,
  });
  const [startTimePickerValue, setStartTimePickerValue] = useState({
    time: "오전",
    hour: 0,
    minute: 0,
  });

  return(
    <div>
      <div className={style["searchFac"]}>
        <div className={style["searchBox"]}>
          <input
            type="text"
            value={searchKeyword}
            onChange={onChangeSearchKeyWord}
            placeholder="일정 상세"
          />
        </div>
        <div className={style["searchBox"]}>
          <input
            type="text"
            value={searchKeyword}
            onChange={onChangeSearchKeyWord}
            placeholder="장소"
          />
        </div>
      </div>
      <div className="ScheduleSelect">
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
      </div>
    </div>
  );
}

export default function ScheduleSelect() {
  //const [isStartPickerOpen, setIsStartPickerOpen] = useState(false);
  const [isStartYearPickerOpen, setIsStartYearPickerOpen] = useState(false);
  const [isStartMonthPickerOpen , setIsStartMonthPickerOpen] = useState(false);
  const [isStartDayPickerOpen, setIsStartDayPickerOpen] = useState(false);
  const [isStartTimePickerOpen, setIsStartTimePickerOpen] = useState(false);

  const [isEndYearPickerOpen, setIsEndYearPickerOpen] = useState(false);
  const [isEndMonthPickerOpen , setIsEndMonthPickerOpen] = useState(false);
  const [isEndDayPickerOpen, setIsEndDayPickerOpen] = useState(false);
  const [isEndTimePickerOpen, setIsEndTimePickerOpen] = useState(false);


  const [detailInput, setDetailPlaceInput] = useState("");
  const [placeInput, setPlaceInput] = useState("");

  const onChangeDetailInput = (e) => {
    setDetailPlaceInput(e.target.value);
  };

  const onChangePlaceInput= (e) => {
    setPlaceInput(e.target.value);
  };

  const [startPickerValue, setStartPickerValue] = useState({
    year,
    month,
    day,
  });

  const [startTimePickerValue, setStartTimePickerValue] = useState({
    time: "오전",
    hour: 0,
    minute: 0,
  });

  const [endPickerValue, setEndPickerValue] = useState({
    year,
    month,
    day,
  });

  const [endTimePickerValue, setEndTimePickerValue] = useState({
    time: "오전",
    hour: 0,
    minute: 0,
  });

  return (
    <div className="ScheduleSelect">
      <div className={style["searchFac"]}>
        <div className={style["searchBox"]}>
          <input
            type="text"
            value={detailInput}
            onChange={onChangeDetailInput}
            placeholder="일정 상세"
          />
        </div>
        <div className={style["searchBox"]}>
          <input
            type="text"
            value={placeInput}
            onChange={onChangePlaceInput}
            placeholder="장소"
          />
        </div>
      </div>

      <div className="DateAndTimeInfo">
        <DatePicker
          {...startPickerValue}
          setIsYearPickerOpen={setIsStartYearPickerOpen}
          setIsMonthPickerOpen={setIsStartMonthPickerOpen}
          setIsDayPickerOpen={setIsStartDayPickerOpen}
          isYearPickerOpen={isStartYearPickerOpen}
          isMonthPickerOpen={isStartMonthPickerOpen}
          isDayPickerOpen={isStartDayPickerOpen}
        />
        <TimePicker
          pickerValue={startTimePickerValue}
          setIsOpen={setIsStartTimePickerOpen}
          id={"startTime"}
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
        />
        <TimePicker
          pickerValue={startTimePickerValue}
          setIsOpen={setIsStartTimePickerOpen}
          id={"startTime"}
        />
      </div>

      {/* 
      <div className="DateAndTimeInfo">
        <DatePicker pickerValue={endPickerValue} setIsOpen={setIsEndPickerOpen} id={"endDate"} />
        <TimePicker
          pickerValue={endTimePickerValue}
          setIsOpen={setIsEndTimePickerOpen}
          id={"endTime"}
        />
      </div>
      
      */}

      {/* 클릭 시 모달  */}
      {isStartYearPickerOpen && (
        <MyPicker
          pickerValue={{ year : startPickerValue.year}}
          setPickerValue={(newValue) =>
            setStartPickerValue((prev) => ({ ...prev, ...newValue}))
          }
          onClose={() => setIsStartYearPickerOpen(false)}
        />
      )}
      {isStartMonthPickerOpen && (
        <MyPicker
          pickerValue={{ month : startPickerValue.month}}
          setPickerValue={(newValue) =>
            setStartPickerValue((prev) => ({ ...prev, ...newValue}))
          }
          onClose={() => setIsStartMonthPickerOpen(false)}
        />
      )}
      {isStartDayPickerOpen && (
        <MyPicker
          pickerValue={{ month : startPickerValue.day}}
          setPickerValue={(newValue) =>
            setStartPickerValue((prev) => ({ ...prev, ...newValue}))
          }
          onClose={() => setIsStartDayPickerOpen(false)}
        />
      )}
      {isStartTimePickerOpen && (
        <TimePickers
          pickerValue={startTimePickerValue}
          setPickerValue={setStartTimePickerValue}
          onClose={() => setIsStartTimePickerOpen(false)}
        />
      )}

      {/*
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

       */}
    </div>
  );
}

function DatePicker({ year, month, day,
   setIsYearPickerOpen, setIsMonthPickerOpen, setIsDayPickerOpen,
   isYearPickerOpen, isMonthPickerOpen, isDayPickerOpen
  }) {
  const selectDate = new Date(year, month - 1, day);

  return (
    <div className="DatePicker__container">
      <div className="date">시작</div>
      <YearInfo year={year} setIsOpen={setIsYearPickerOpen} isOpen={isYearPickerOpen}/>
      <MonthInfo month={month} setIsOpen={setIsMonthPickerOpen} isOpen={isMonthPickerOpen}/>
      <DayInfo day={day} setIsOpen={setIsDayPickerOpen} isOpen={isDayPickerOpen}/>
    </div>
  );
}

function TimePicker({ pickerValue, setIsOpen, id }) {
  return (
    <div className="DatePicker__container">
      <TimeInfo {...pickerValue} id={id} onOpen={() => setIsOpen(true)} />
    </div>
  );
}


function UpDownArrow({onOpen}){
  return (
    <>
      {
        onOpen ?  <img src={up_arrow} alt="up_arrow" />:
        <img src={down_arrow} alt="down_arrow" /> 
      }
    </>
  )
}

function DayInfo({day, setIsOpen, onOpen}){
  return (
    <div className="date" onClick={() => setIsOpen(true)}>
      <div>{String(day).padStart(2, "0")}일</div>
      <UpDownArrow onOpen={onOpen}/>
    </div>
  )
}

function MonthInfo({month, setIsOpen, onOpen}){
  return (
    <div className="date" onClick={() => setIsOpen(true)}>
      <div>{String(month).padStart(2, "0")}월</div>
      <UpDownArrow onOpen={onOpen}/>
    </div>
  )
}

function YearInfo({ year, setIsOpen, onOpen }) {
  //const selectDate = new Date(year, month - 1, day);
  //const selectDay = daysOfWeek[selectDate.getDay()];
  return (
    <div className="date" onClick={() => setIsOpen(true)}>
      <div>{year}년</div>
      <UpDownArrow onOpen={onOpen}/>
    </div>
  )


  //return (
    //<>
      //<label htmlFor={id} className="date">
        //<div>{year}년</div>
        //<div>{String(month).padStart(2, "0")}월</div>
        //<div>{String(day).padStart(2, "0")}일</div>
        //<div>{selectDay}</div>
      //</label>
      //<Input id={id} type={"date"} onClick={onOpen} />
    //</>
  //);
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

function MyPicker({ pickerValue, setPickerValue, onClose}) {
  return (
        <div className="DatePicker">
      <Picker
        value={pickerValue}
        onChange={(name, value) =>
          setPickerValue((prev) => ({ ...prev, [name]: value }))
        }
        wheelMode="normal"
      >
        <Picker.Column name="year">
          {selections.year.map((option) => (
            <Picker.Item key={option} value={option}>
              {String(option).padStart(2, "0")}
            </Picker.Item>
          ))}
        </Picker.Column>
      </Picker>
      <div onClick={onClose}>확인</div>
    </div>
  );
}

//function MyPicker({ pickerValue, setPickerValue, onClose }) {
  //return (
    //<div className="DatePicker">
      //<Picker value={pickerValue} onChange={setPickerValue} wheelMode="normal">
        //{Object.keys(selections).map((name) => (
          //<Picker.Column key={name} name={name}>
            //{selections[name].map((option) => (
              //<Picker.Item key={option} value={option}>
                //{String(option).padStart(2, "0")}
              //</Picker.Item>
            //))}
          //</Picker.Column>
        //))}
      //</Picker>
      //<div onClick={onClose}>확인</div>
    //</div>
  //);
//}

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


//export default function ScheduleSelect() {
  //const [isStartPickerOpen, setIsStartPickerOpen] = useState(false);
  //const [isStartTimePickerOpen, setIsStartTimePickerOpen] = useState(false);
  //const [isEndPickerOpen, setIsEndPickerOpen] = useState(false);
  //const [isEndTimePickerOpen, setIsEndTimePickerOpen] = useState(false);

  //const [startPickerValue, setStartPickerValue] = useState({
    //year,
    //month,
    //day,
  //});
  //const [startTimePickerValue, setStartTimePickerValue] = useState({
    //time: "오전",
    //hour: 0,
    //minute: 0,
  //});
  //const [endPickerValue, setEndPickerValue] = useState({
    //year,
    //month,
    //day,
  //});

  //const [endTimePickerValue, setEndTimePickerValue] = useState({
    //time: "오전",
    //hour: 0,
    //minute: 0,
  //});

  //return (
    //<div className={style["ScheduleSelect"]}>
      //<Input type={"text"} placeholder={"일정 상세"} />
      //<Input placeholder={"장소"} />

      //<div className={style["DateAndTimeInfo"]}>
        //<DatePicker
          //pickerValue={startPickerValue}
          //setIsOpen={setIsStartPickerOpen}
          //id={"startDate"}
        ///>
        //<TimePicker
          //pickerValue={startTimePickerValue}
          //setIsOpen={setIsStartTimePickerOpen}
          //id={"startTime"}
        ///>
      //</div>

      //<div className={style["DateAndTimeInfo"]}>
        //<DatePicker pickerValue={endPickerValue} setIsOpen={setIsEndPickerOpen} id={"endDate"} />
        //<TimePicker
          //pickerValue={endTimePickerValue}
          //setIsOpen={setIsEndTimePickerOpen}
          //id={"endTime"}
        ///>
      //</div>

      //{/* 클릭 시 모달  */}
      //{isStartPickerOpen && (
        //<MyPicker
          //pickerValue={startPickerValue}
          //setPickerValue={setStartPickerValue}
          //onClose={() => setIsStartPickerOpen(false)}
        ///>
      //)}
      //{isStartTimePickerOpen && (
        //<TimePickers
          //pickerValue={startTimePickerValue}
          //setPickerValue={setStartTimePickerValue}
          //onClose={() => setIsStartTimePickerOpen(false)}
        ///>
      //)}
      //{isEndPickerOpen && (
        //<MyPicker
          //pickerValue={endPickerValue}
          //setPickerValue={setEndPickerValue}
          //onClose={() => setIsEndPickerOpen(false)}
        ///>
      //)}
      //{isEndTimePickerOpen && (
        //<TimePickers
          //pickerValue={endTimePickerValue}
          //setPickerValue={setEndTimePickerValue}
          //onClose={() => setIsEndTimePickerOpen(false)}
        ///>
      //)}
    //</div>
  //);
//}

//function DatePicker({ pickerValue, setIsOpen, id }) {
  //return (
    //<div className={style["DatePicker__container"]}>
      //<DateInfo {...pickerValue} id={id} onOpen={() => setIsOpen(true)} />
    //</div>
  //);
//}

//function TimePicker({ pickerValue, setIsOpen, id }) {
  //return (
    //<>
      //<TimeInfo {...pickerValue} id={id} onOpen={() => setIsOpen(true)} />
    //</>
  //);
//}

//function DateInfo({ year, month, day, id, onOpen }) {
  //const selectDate = new Date(year, month - 1, day);
  //const selectDay = daysOfWeek[selectDate.getDay()];

  //return (
    //<>
      //<label htmlFor={id} className={style["date"]}>
        //<div>{year}년</div>
        //<div>{String(month).padStart(2, "0")}월</div>
        //<div>{String(day).padStart(2, "0")}일</div>
        //<div>{selectDay}</div>
      //</label>
      //<Input id={id} type={"date"} onClick={onOpen} />
    //</>
  //);
//}

//function TimeInfo({ time, hour, minute, id, onOpen }) {
  //return (
    //<>
      //<label htmlFor={id} className={style["time"]}>
        //<div>{time}</div>
        //<div>{`${String(hour).padStart(2, "0")}:${String(minute).padStart(2, "0")}`}</div>
      //</label>
      //<Input type={"time"} id={id} onClick={onOpen} />
    //</>
  //);
//}

//function MyPicker({ pickerValue, setPickerValue, onClose }) {
  //return (
    //<div className={style["DatePicker"]}>
      //<Picker value={pickerValue} onChange={setPickerValue} wheelMode="normal">
        //{Object.keys(selections).map((name) => (
          //<Picker.Column key={name} name={name}>
            //{selections[name].map((option) => (
              //<Picker.Item key={option} value={option}>
                //{String(option).padStart(2, "0")}
              //</Picker.Item>
            //))}
          //</Picker.Column>
        //))}
      //</Picker>
      //<div onClick={onClose}>확인</div>
    //</div>
  //);
//}

//function TimePickers({ pickerValue, setPickerValue, onClose }) {
  //return (
    //<div className={style["TimePicker"]}>
      //<div className={style["TimePicker__wrapper"]}>
        //<Picker value={pickerValue} onChange={setPickerValue} wheelMode="normal">
          //{Object.keys(timeSelections).map((name) => (
            //<Picker.Column key={name} name={name}>
              //{timeSelections[name].map((option) => (
                //<Picker.Item key={option} value={option}>
                  //{String(option).padStart(2, "0")}
                //</Picker.Item>
              //))}
            //</Picker.Column>
          //))}
        //</Picker>
        //<div onClick={onClose}>확인</div>
      //</div>
    //</div>
  //);
//}
