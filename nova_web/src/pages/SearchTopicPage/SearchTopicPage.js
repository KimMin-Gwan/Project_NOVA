import ScheduleTopic from "../../component/ScheduleTopic/ScheduleTopic";
import style from "./SearchTopicPage.module.css";
import ScheduleSearch from "../../component/ScheduleSearch/ScheduleSearch";
import React, { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ScheduleFollow } from "../../component/ScheduleMore/ScheduleMore";
import ScheduleFollowBox from "../../component/ScheduleFollowBox/ScheduleFollowBox";
import { mockData } from "../../pages/SchedulePage/TestScheduleData";
import useToggleMore from "../../component/useToggleMore";
import mainApi from "../../services/apis/mainApi";
import HEADER from "../../constant/header";

export default function SearchTopicPage() {
  let [eventData, setEventData] = useState([]);

  const { moreClick, toggleMore } = useToggleMore();
  const [isModal, setIsModal] = useState(false);
  const navigate = useNavigate();

  const [biasData, setBiasData] = useState([]);
  const [nextKey, setNextKey] = useState(-1);

  async function fetchSearchData(keyword) {
    await mainApi
      .get(`time_table_server/try_search_bias?keyword=${keyword}&key=${nextKey}`)
      .then((res) => {
        setBiasData((prev) => [...prev, ...res.data.body.biases]);
        setNextKey(res.data.body.key);
      });
  }

  // 팔로우 모달창 나오게 하기
  function handleFollowModal() {
    setIsModal((isModal) => !isModal);
  }

  function clickPath(path) {
    navigate(`${path}`);
  }

  useEffect(() => {
    fetchSearchData("");
  }, []);

  function fetchTryFollowBias(target) {

    let send_data = {
      header: HEADER,
      body: {
        bid: target.bid,
      },
    };


    fetch("https://nova-platform.kr/nova_sub_system/try_select_my_bias", {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(send_data),
    })
      .then((res) => {
        if (res.status === 401) {
          alert("로그인이 필요한 서비스입니다.");
          navigate("/novalogin");
          return Promise.reject();
        }
        return res.json();
      })
      .then((data) => {
        if (biasData.some((item) => item.bid === target.bid)) {
          alert("팔로우 취소 완료");
        } else {
          alert("팔로우 완료!");
        }
        setIsModal(false);
        window.location.reload();
      });
  }

  return (
    <div className={`container ${style["SearchTopicPage"]}`}>
      <ScheduleSearch
        title={0}
        fetchMockData={fetchSearchData}
        clickButton={() => clickPath("/search/research")}
      />

      <ul className={style["scheduleList"]}>
        {biasData.map((item) => (
          <li key={item.id}>
            <ScheduleTopic key={item.id} {...item}toggleClick={() => toggleMore(item.id)} />
            {moreClick[item.id] && (
              <ScheduleFollow
                scheduleClick={() => clickPath("/search/schedule")}
                followClick={handleFollowModal}
              />
            )}
          </li>
        ))}
      </ul>

      {isModal && <ScheduleFollowBox closeModal={handleFollowModal} />}
    </div>
  );
}
