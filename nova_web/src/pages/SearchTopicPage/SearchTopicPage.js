import ScheduleTopic from "../../component/ScheduleTopic/ScheduleTopic";
import style from "./SearchTopicPage.module.css";
import ScheduleSearch from "../../component/ScheduleSearch/ScheduleSearch";
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ScheduleFollow } from "../../component/ScheduleMore/ScheduleMore";
import useToggleMore from "../../hooks/useToggleMore";
import mainApi from "../../services/apis/mainApi";
import HEADER from "../../constant/header";
import FollowBiasModal from "../../component/FollowBiasModal/FollowBiasModal";
import { TITLE_TYPES } from "../../constant/type_data";

export default function SearchTopicPage() {
  const navigate = useNavigate();
  const { moreClick, handleToggleMore } = useToggleMore();
  // const [clickedBid, setClickedBid] = useState();

  const [isOpenModal, setIsOpenModal] = useState(false);

  const [biasData, setBiasData] = useState([]);
  const [nextKey, setNextKey] = useState(-1);
  const [searchKeyword, setSearchKeyword] = useState("");

  async function fetchSearchData() {
    await mainApi
      .get(`time_table_server/try_search_bias?keyword=${searchKeyword}&key=${nextKey}`)
      .then((res) => {
        // setBiasData((prev) => [...prev, ...res.data.body.biases]);
        setBiasData(res.data.body.biases);
        setNextKey(res.data.body.key);
      });
  }

  // 팔로우 모달창 나오게 하기
  function handleFollowModal() {
    setIsOpenModal((prev) => !prev);
  }

  function handleNavigate(path) {
    navigate(`${path}`);
  }

  useEffect(() => {
    setNextKey(-1);
    fetchSearchData();
  }, [searchKeyword]);

  async function fetchTryFollowBias(target) {
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
        setIsOpenModal(false);
        window.location.reload();
      });

    // await postApi.post(
    //   "nova_sub_system/try_select_my_bias",
    //   {
    //     header: HEADER,
    //     body: {
    //       bid: target.bid,
    //     },
    //   }.then((res) => {
    //     console.log(res.data);
    //   })
    // );
  }

  return (
    <div className={`container ${style["SearchTopicPage"]}`}>
      <ScheduleSearch
        title={TITLE_TYPES.BIAS}
        fetchSearchData={fetchSearchData}
        searchKeyword={searchKeyword}
        setSearchKeyword={setSearchKeyword}
      />

      <ul className={style["scheduleList"]}>
        {biasData.map((bias) => (
          <li key={bias.bid}>
            <ScheduleTopic
              key={bias.bid}
              {...bias}
              toggleClick={() => handleToggleMore(bias.bid)}
            />
            {moreClick[bias.bid] && (
              <ScheduleFollow
                scheduleClick={() => handleNavigate(`/search/schedule?keyword=${bias.bname}`)}
                followClick={handleFollowModal}
              />
            )}
            {isOpenModal && (
              <FollowBiasModal
                biasData={bias}
                closeModal={handleFollowModal}
                fetchFollowBias={fetchTryFollowBias}
              />
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
