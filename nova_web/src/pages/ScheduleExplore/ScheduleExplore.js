import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { TITLE_TYPES } from "../../constant/type_data";
import HEADER from "../../constant/header";

import { ScheduleBundle } from "../../component/ScheduleEvent/ScheduleBundle";
import ScheduleCard from "../../component/EventCard/EventCard";
import ScheduleSearch from "../../component/ScheduleSearch/ScheduleSearch";
import {
  ScheduleMore,
  ScheduleAdd,
  ScheduleEdit,
  ScheduleRemove,
} from "../../component/ScheduleMore/ScheduleMore";
import {
  BundleScheduleDetail,
  ScheduleDetail,
  MakeSingleSchedule,
  EditSingleSchedule,
} from "../../component/EventMore/EventMore";
import back from "./../../img/detail_back.png";

import useToggleMore from "../../hooks/useToggleMore";

import mainApi from "../../services/apis/mainApi";
import postApi from "../../services/apis/mainApi";
import "./index.css";

export default function ScheduleExplore() {
  const { moreClick, handleToggleMore } = useToggleMore();
  const navigate = useNavigate();

  let [searchKeyword, setSearchKeyword] = useState("");

  const typeSelectData = ["schedule_bundle", "schedule"];
  const scheduleKind = ["일정 번들", "일정"];

  const [activeIndex, setActiveIndex] = useState(0);

  // 모달
  const [addScheduleModal, setAddScheduleModal] = useState(false);
  const [addScheduleBundleModal, setAddScheduleBundleModal] = useState(false);
  const [makeScheduleModal, setMakeScheduleModal] = useState(false);
  const [editScheduleModal, setEditScheduleModal] = useState(false);

  // 데이터
  const [scheduleBundleData, setScheduleBundleData] = useState([]);
  const [scheduleData, setScheduleData] = useState([]);

  // 키 값
  const [scheduleBundleKey, setScheduleBundleKey] = useState(-1);
  const [scheduleKey, setScheduleKey] = useState(-1);

  const [targetSchedule, setTargetSchedule] = useState({});
  const [targetScheduleBundle, setTargetScheduleBundle] = useState({});

  // const [hasMore, setHasMore] = useState(false);

  async function fetchSearchData() {
    let key = activeIndex === 0 ? scheduleBundleKey : scheduleKey;
    let type = typeSelectData[activeIndex];

    await mainApi
      .get(
        `time_table_server/try_search_schedule_with_keyword?keyword=${searchKeyword}&key=${key}&type=${type}`
      )
      .then((res) => {
        if (activeIndex === 0) {
          setScheduleBundleData(res.data.body.schedule_bundles);
          setScheduleBundleKey(res.data.body.key);
        } else if (activeIndex === 1) {
          setScheduleData(res.data.body.schedules);
          setScheduleKey(res.data.body.key);
        }
      });
  }

  async function fecthSearchDataDefault() {
    let type = typeSelectData[activeIndex];

    await mainApi
      .get(
        `time_table_server/try_search_schedule_with_keyword?keyword=${searchKeyword}&key=-1&type=${type}`
      )
      .then((res) => {
        if (activeIndex === 0) {
          setScheduleBundleData(res.data.body.schedule_bundles);
          setScheduleBundleKey(res.data.body.key);
        } else if (activeIndex === 1) {
          setScheduleData(res.data.body.schedules);
          setScheduleKey(res.data.body.key);
        }
      });
  }

  useEffect(() => {
    setScheduleKey(-1);
    setScheduleBundleKey(-1);
    setScheduleData([]);
    setScheduleBundleData([]);

    fecthSearchDataDefault();
  }, [searchKeyword, activeIndex]);

  // 탭 변경시 검색 초기화
  useEffect(() => {
    setSearchKeyword("");
    setScheduleBundleKey(-1);
  }, [activeIndex]);

  // 일정 탐색 페이지에 일정번들, 일정, 이벤트 상태 변경
  // 누르면 키가 자꾸 올라가는 문제가 있음 !!!!
  const handleClick = (index) => {
    setActiveIndex(index);
  };

  // 일정 추가하기 버튼 누르면 동작하는애
  const toggleMakeScheduleModal = (target) => {
    setMakeScheduleModal((makeScheduleModal) => !makeScheduleModal);
  };

  const toggleEditScheduleModal = (target) => {
    setEditScheduleModal((editScheduleModal) => !editScheduleModal);
    setTargetSchedule(target);
  };

  // 일정 추가하기 버튼 누르면 동작하는애
  const toggleAddScheduleModal = (target) => {
    setAddScheduleModal((addScheduleModal) => !addScheduleModal);
    setTargetSchedule(target);
  };

  // 일정 번들 추가하기 버튼 누르면 동작하는 애
  const toggleAddScheduleBundleModal = (target) => {
    setAddScheduleBundleModal(
      (addScheduleBundleModal) => !addScheduleBundleModal
    );
    setTargetScheduleBundle(target);
  };

  // 게시판으로 이동
  const navBoard = () => {
    navigate("/");
  };

  // 내 스케줄에 등록하는 함수 (추가하기 버튼 누르면 동작해야됨)
  // 완료하면 성공했다고 알려주면 좋을듯
  async function fetchTryAddSchedule(target) {
    // 무조건 리스트로 만들어야됨
    const sids = [target.sid];

    await postApi
      .post("time_table_server/try_add_schedule", {
        header: HEADER,
        body: {
          sids: sids,
        },
      })
      .then((res) => {
        setScheduleData((prev) => {
          if (!prev.some((item) => item.sid === target.sid)) {
            // 목표 item이 없으면 기존 상태 반환
            return prev;
          }
          // 목표 item이 있으면 업데이트
          return prev.map((item) =>
            item.sid === target.sid ? { ...item, is_already_have: true } : item
          );
        });
      });
  }

  // 내 스케줄에 등록하는 함수 (추가하기 버튼 누르면 동작해야됨)
  // 완료하면 성공했다고 알려주면 좋을듯
  async function fetchTryRejectSchedule(target) {
    // 무조건 리스트로 만들어야됨

    await mainApi
      .get(`time_table_server/try_reject_from_my_schedule?sid=${target.sid}`)
      .then((res) => {
        setScheduleData((prev) => {
          if (!prev.some((item) => item.sid === target.sid)) {
            // 목표 item이 없으면 기존 상태 반환
            return prev;
          }
          // 목표 item이 있으면 업데이트
          return prev.map((item) =>
            item.sid === target.sid ? { ...item, is_already_have: false } : item
          );
        });
      });
  }

  // 내 스케줄에 등록하는 함수 (추가하기 버튼 누르면 동작해야됨)
  // 완료하면 성공했다고 알려주면 좋을듯
  async function fetchTryDeleteSchedule(target) {
    // 무조건 리스트로 만들어야됨

    await mainApi
      .get(`time_table_server/try_delete_schedule?sid=${target.sid}`)
      .then((res) => {
        setScheduleData((prev) => {
          if (!prev.some((item) => item.sid === target.sid)) {
            // 목표 item이 없으면 기존 상태 반환
            return prev;
          }
          // 목표 item이 있으면 업데이트
          return prev.map((item) =>
            item.sid === target.sid
              ? { ...item, is_already_have: false, is_owner: false }
              : item
          );
        });
      });
  }

  // 내 스케줄에 등록하는 함수 (추가하기 버튼 누르면 동작해야됨)
  // 완료하면 성공했다고 알려주면 좋을듯
  async function fetchTryEditSchedule(target) {
    // 무조건 리스트로 만들어야됨

    await postApi
      .post("time_table_server/try_reject_from_my_schedule", {
        header: HEADER,
        body: {
          sid: target.sid,
        },
      })
      .then((res) => {});
  }

  return (
    <div className="container SearchSchedulePage">
      {/* 탭 영역 */}
      <section className={"info-list"}>
        <ul className={"post-list"} data-active-index={activeIndex}>
          <TabItem
            tabs={scheduleKind}
            activeIndex={activeIndex}
            handleClick={handleClick}
          />
        </ul>
      </section>
      <section>
        <button>시간 설정</button>
        <button>시간 설정</button>
        <button>시간 설정</button>
      </section>
      <ul className="scheduleList">
        {activeIndex === 0
          ? scheduleBundleData.map((item) => (
              <li key={item.sbid}>
                <ScheduleBundle
                  item={item}
                  toggleClick={() => handleToggleMore(item.sbid)} // id 전달
                />
                {moreClick[item.sbid] && ( // 해당 id의 상태만 확인
                  <ScheduleMore
                    target={item}
                    navBoardClick={navBoard}
                    scheduleClick={toggleAddScheduleBundleModal}
                  />
                )}
              </li>
            ))
          : scheduleData.map((item) => (
              <li key={item.sid}>
                <ScheduleCard
                  {...item}
                  toggleClick={() => handleToggleMore(item.sid)} // id 전달
                />

                {moreClick[item.sid] &&
                  (item.is_already_have === false ? (
                    <ScheduleAdd
                      target={item}
                      detailClick={toggleAddScheduleModal}
                      navBoardClick={navBoard}
                      addClick={fetchTryAddSchedule}
                    />
                  ) : item.is_owner === false ? (
                    <ScheduleRemove
                      target={item}
                      navBoardClick={navBoard}
                      removeClick={fetchTryRejectSchedule}
                    />
                  ) : (
                    <ScheduleEdit
                      target={item}
                      navBoardClick={navBoard}
                      editClick={toggleEditScheduleModal}
                    />
                  ))}
              </li>
            ))}
      </ul>
    </div>
  );
}

// Tabs 컴포넌트가 존재, 그거랑 합치기 필요
function TabItem({ tabs, activeIndex, handleClick }) {
  return (
    <>
      {tabs.map((tab, index) => (
        <li
          key={index}
          className={`post ${activeIndex === index ? "active" : ""}`}
          onClick={() => handleClick(index, tab)}
        >
          <button>{tab}</button>
        </li>
      ))}
    </>
  );
}
