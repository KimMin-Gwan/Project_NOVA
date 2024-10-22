import { Routes, Route, Link, useNavigate } from "react-router-dom";
import style from "./Mypage.module.css";
import backword from "./../../img/back_icon.png";
import ticket_icon from "./../../img/ticket_icon.png";
import funding_icon from "./../../img/funding_icon.png";
import novaAL_icon from "./../../img/novaAL_icon.png";
import judge_icon from "./../../img/judge_icon.png";
import galaxyleague from "./../../img/galaxyleague.png";
import star_powder from "./../../img/starpowder.png";
import empty from './../../img/empty.png';

import { TfiCommentAlt } from "react-icons/tfi";

import { CiStar, CiEdit } from "react-icons/ci";
// import { SlSpeech } from "react-icons/sl";
import { HiOutlineBellAlert } from "react-icons/hi2";
import { IoIosArrowForward, IoIosArrowBack, IoMdCheckmarkCircleOutline } from "react-icons/io";
import { useEffect, useState } from "react";
// import MySoloBias from '../../component/subscribeBias/mySoloBias';
function MyPage() {
  let bias_url = "https://kr.object.ncloudstorage.com/nova-images/";

  let navigate = useNavigate();

  let [isClicked, setIsClicked] = useState(false);

  let [mySoloBias, setMySoloBias] = useState([]);
  let [myGroupBias, setMyGroupBias] = useState([]);
  let [myData, setMyData] = useState([]);

  useEffect(() => {
    fetch("https://nova-platform.kr/user_home/my_data", {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data.body);
        setMySoloBias(data.body.solo_bias);
        setMyGroupBias(data.body.group_bias);
        setMyData(data.body.user);
      });
  }, []);

  function handleClick() {
    setIsClicked(!isClicked);
  }

  useEffect(() => {
    return setIsClicked(false);
  }, []);

  function handleMovePage(e, page) {
    e.preventDefault();
    navigate(page);
  }

  const handleLogout = (e) => {
    e.preventDefault();
    fetch("https://nova-platform.kr/user_home/try_logout", {
      credentials: "include",
    })
      .then((response) => {
        if (!response.ok) {
          return response.text().then((text) => {
            throw new Error(`Error: ${response.status}, ${text}`);
          });
        }
        return response.json();
      })
      .then((data) => {
        console.log(data);
        navigate("/");
      })
      .catch((error) => {
        console.error("Logout error:", error);
      });
  };

  return (
    <div className={style.container}>
      <div className={style.top_area}>
        <img
          src={backword}
          alt="Arrow"
          className={style.backword}
          onClick={() => {
            navigate(-1);
          }}
        />
      </div>

      <div className={style["base_box"]}>
        <div className={style["wrap_box"]}>
          <div className={style["sup_part"]}>
            <div className={style["wrap_sup"]}>
              <div className={style.support}>지지자</div>
              <div className={style.space_pass}>우주인 패스 +</div>
              <div onClick={handleClick}>{isClicked ? <IoIosArrowBack size={40} style={{ cursor: 'pointer' }} /> : <IoIosArrowForward size={40} style={{ cursor: 'pointer' }} />}</div>
            </div>
          </div>
          <div className={style["ticket_part"]}>
            <div className={style["ticket_info"]}>
              <div className={style["ticket_wrapper"]}>
                <img src={ticket_icon} alt="Ticket Icon" className={style["ticket_box"]} />
                <div style={{ color: "#FF6966" }}>별별 티켓</div>
              </div>
              <div>{myData.credit} 개</div>
            </div>

            <div className={style["btn_container"]}>
              <button>충전</button>
              <button>패스</button>
            </div>
          </div>
        </div>
      </div>

      {!isClicked && (
        <>
          <div className={style["base_box"]}>
            <h4>최애-개인</h4>
            <div className={style["wrap_box"]} style={{ flexDirection: "row", height: "auto" }}>
              <div className={style["half_box"]}>
                <div className={`left-box ${style["img_box"]}`}>
                  <div className="image-container">
                    {
                      mySoloBias.bid === '' ? <img src={empty} /> :
                        <img src={bias_url + `${mySoloBias.bid}.PNG`} alt="bias" />
                    }
                  </div>
                </div>
              </div>
              <div className={style["half_box"]}>
                <div className={style["text_box"]}>
                  <p>나의최애</p>
                  {mySoloBias.bname === "" ? <div className={style["not_name"]}>아직 최애가 없어요</div> : <div className={style["bias_name"]}>{mySoloBias.bname}</div>}
                  {
                    myData.solo_bid === '' ? (
                      <div className={style["support_text"]}>최애를 정하고 지지해보는건 어떨까요?</div>
                    ) : (
                      <>
                        <div className={style["powder_wrapper"]}>
                          <img src={star_powder} alt="star_powder" className={style["poweder_box"]} />
                          <div className={style["season_star_dust"]}>이번 시즌에 기여한 별가루</div>
                        </div>
                        <h2>{myData.solo_point} pt</h2>
                        <button className={style["funding_btn"]} disabled>펀딩</button>
                      </>
                    )
                  }
                </div>
              </div>
            </div>
          </div>

          <div className={style["base_box"]}>
            <div className={style["title_box"]}>
              <h4>최애-단체</h4>
              <h6>최애 - 단체는 리그와 펀딩을 하지 않아요.</h6>
            </div>
            <div className={style["wrap_box"]} style={{ flexDirection: "row", height: "auto" }}>
              <div className={style["half_box"]}>
                <div className={`left-box ${style["img_box"]}`}>
                  <div className="image-container">
                    {
                      myGroupBias.bid === '' ? <img src={empty} /> :
                        <img src={bias_url + `${myGroupBias.bid}.PNG`} alt="bias" />
                    }
                  </div>
                </div>
              </div>
              <div className={style["half_box"]}>
                <div className={style["text_box"]}>
                  {myGroupBias.bname === "" ? <div className={style["not_name"]}>아직 최애가 없어요</div> : <div className={style["bias_name"]}>{myGroupBias.bname}</div>}
                  {
                    myData.group_bid === '' ? (
                      <div className={style["support_text"]}>최애를 정하고 지지해보는건 어떨까요?</div>
                    ) : (
                      <>
                        <div className={style["powder_wrapper"]}>
                          <img src={star_powder} alt="star_powder" className={style["poweder_box"]} />
                          <div className={style["season_star_dust"]}>이번 시즌에 기여한 별가루</div>
                        </div>
                        <h2>{myData.group_point} pt</h2>
                        <button className={style["funding_btn"]} disabled>펀딩</button>
                      </>
                    )
                  }
                </div>
              </div>
            </div>
          </div>

          <div className={`${style["base_box"]} ${style["height_auto"]}`}>
            <h4>서비스</h4>
            <div className={style["grid_container_right"]}>
              <div className={style["item"]} onClick={(e) => handleMovePage(e, "/galaxy")}>
                <div className={style["icon_text_wrapper"]}>
                  <img src={galaxyleague} alt="galaxyleague" className={style["icon_box"]} />
                  <span>은하 리그</span>
                </div>
              </div>

              <div className={style["item"]}>
                <div className={style["icon_text_wrapper"]}>
                  <img src={funding_icon} alt="funding_Icon" className={style["icon_box"]} />
                  <span>노바 펀딩</span>
                </div>
              </div>

              <div className={style["item"]}>
                <div className={style["icon_text_wrapper"]}>
                  <img src={judge_icon} alt="judge_icon" className={style["icon_box"]} />
                  <span>노바 재판</span>
                </div>
              </div>

              <div className={style["item"]}>
                <div className={style["icon_text_wrapper"]}>
                  <img src={novaAL_icon} alt="novaAL_icon" className={style["icon_box"]} />
                  <span>노바 알고리즘</span>
                </div>
              </div>
            </div>
          </div>

          <div className={`${style["base_box"]} ${style["height_auto"]}`}>
            <h4>나의 활동</h4>
            <div className={style["my_activity"]}>
              <div className={style.activity}>

                <CiEdit className={style["activity_icon"]} />
                <div>내가 작성한 피드</div>
                <IoIosArrowForward
                  className={`${style["activity_icon"]} ${style.cursor}`}
                  onClick={(e) => {
                    handleMovePage(e, "/my_write_feed");
                  }}
                />

                <CiStar className={style["activity_icon"]} />
                <div>관심 표시한 피드</div>
                <IoIosArrowForward
                  className={`${style["activity_icon"]} ${style.cursor}`}
                  onClick={(e) => {
                    handleMovePage(e, "/my_interest_feed");
                  }}
                />

                <IoMdCheckmarkCircleOutline className={style["activity_icon"]} />
                <div>내가 참여한 피드</div>
                <IoIosArrowForward
                  className={`${style["activity_icon"]} ${style.cursor}`}
                  onClick={(e) => {
                    handleMovePage(e, "/my_active_feed");
                  }}
                />

                {/* <TfiCommentAlt className={style["activity_icon"]}/>
                <div>내가 작성한 댓글</div>
                <IoIosArrowForward
                  className={style["activity_icon"]}
                  onClick={(e) => {
                    handleMovePage(e, "/my_comment_feed");
                  }}
                />

                <HiOutlineBellAlert className={style["activity_icon"]} />
                <div>알림</div>
                <IoIosArrowForward
                  className={style["activity_icon"]}
                  onClick={(e) => {
                    handleMovePage(e, "/my_alerts");
                  }}
                /> */}
              </div>
            </div>
          </div>
          <div
            className={`${style["logout_box"]}`}
            onClick={handleLogout}
            style={{ cursor: "pointer" }} // 클릭 가능한 요소처럼 보이게 하기
          >
            로그아웃
          </div>
        </>
      )}

      {isClicked && (
        <>
          <div className={`${style["base_box"]} ${style["height_auto"]}`}>
            <h4>개인 정보</h4>
            <div className={style["personal_info"]}>
              <div className={style["info_list"]}>
                <div className={style["info_items"]}>UID</div>
                <div className={style["info_items"]}>{myData.uid}</div>

                <div className={style["info_items"]}>Email</div>
                <div className={style["info_items"]}>{myData.email}</div>

                <div className={style["info_items"]}>나이</div>
                <div className={style["info_items"]}>{myData.age}세</div>

                <div className={style["info_items"]}>성별</div>
                <div className={style["info_items"]}>{myData.gender === "f" ? "여성" : myData.gender === "m" ? "남성" : ""}</div>

                <div className={style["info_items"]}>별별 티켓 보유량</div>
                <div className={style["info_items"]}>{myData.credit}개</div>

                <div className={style["info_items"]}>우주인 패스</div>
                <div className={style["info_items"]}>미등록</div>
              </div>
            </div>
          </div>

          <div className={`${style["base_box"]} ${style["height_auto"]}`}>
            <h4>비밀번호 관리</h4>
            <div className={style["pwd_manage_box"]}>
              <form>
                <div className={style["pwd_box"]}>
                  <div>현재 비밀번호</div>
                  <input type="password"></input>

                  <div>새로운 비밀번호</div>
                  <input type="password"></input>

                  <div>비밀번호 확인</div>
                  <input type="password"></input>
                </div>
                <div className={style["pwd_submit_btn"]}>
                  <button type="submit">변경하기</button>
                </div>
              </form>
            </div>
          </div>

          <div className={`${style["base_box"]} ${style["height_auto"]}`}>
            <h4>닉네임</h4>
            <div className={style["nickname_container"]}>
              <div className={style["nickname_box"]}>
                <div>기본 사용자명</div>
                <div>지지자</div>
                <button className={style.cursor}>선택</button>

                <div>개인 팬덤명</div>
                <div>지지자</div>
                <button className={style.cursor}>선택</button>

                <div>그룹 팬덤명</div>
                <div>지지자</div>
                <button className={style.cursor}>선택</button>

                <div>커스텀 닉네임</div>
                <input placeholder="우주인 패스 결제 상품"></input>
                <button className={style.cursor}>선택</button>
              </div>
            </div>
          </div>
          <div className={`${style["base_box"]} ${style["height_auto"]}`}>
            <h4>활동 배지</h4>
          </div>
        </>
      )}
    </div>
  );
}

export default MyPage;
