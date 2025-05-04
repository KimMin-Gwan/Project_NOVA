import { useLocation, useNavigate, useParams } from "react-router-dom";
import { useState, useEffect, useRef } from "react";

import mainApi from "../../services/apis/mainApi";
import postApi from "../../services/apis/postApi";

import HEADER from "../../constant/header";

import more_icon from "./../../img/more_icon.svg";
import back from "./../../img/detail_back.png";
import input from "./../../img/input.svg";
import reArrow1 from "./../../img/reArrow1.svg";
import reArrow2 from "./../../img/reArrow2.svg";
import reArrow3 from "./../../img/reArrow3.svg";
import reArrow4 from "./../../img/reArrow4.svg";

import { ContentFeed } from "../../component/feed";

import style from "./NewFeedDetail.module.css";


const temp_comment = [
  {cid: "1", uid:"1", owner:false, uname:"익명", isReply:false, reply:"", body:"원글 그림 왜 잘그림? 님 혹시 제것도 슬쩍 그려주실 수 있음?"},
  {cid: "2", uid:"2", owner:false, uname:"니말이다맞음", isReply:false, reply:"", body:"윗댓 정신좀 차려라. 그냥 날로 처먹으려고 하네;; 님들 같은 사람들 때문에 멀정한 치수들 다 욕먹는거임"},
  {cid: "3", uid:"3", owner:true, uname:"관리자", isReply:false, reply:"", body:"님들 싸우지 말죠 ㅋㅋㅋ"},
  {cid: "4", uid:"1", owner:false, uname:"익명", isReply:false, reply:"", body:"뭐래;; 그냥 하는말인데 왜 급발진함;;"},
  {cid: "5", uid:"3", owner:true, uname:"관리자", isReply:true, reply:{cid:"2", uname:"익명", body:"뭐래;; 그냥 하는말인데 왜 급발진함;;"}, body:"그려드릴테니 진정하십쇼 ㅋㅋㅋㅋㅋ"},
]





export default function NewFeedDetail() {
  let navigate = useNavigate();
  //let { fid } = useParams();
  let fid = '6adf-fb09-4907-ULIx2R'

  let location = useLocation();
  //let { state } = location;

  let commentRef = useRef(null);

  const [isLoading, setIsLoading] = useState(true); // 로딩 상태 관리
  const [isComment, setIsComment] = useState(false);
  let [feedData, setFeedData] = useState([]);
  let [comments, setComments] = useState([]);
  let [commentValue, setCommentValue] = useState("");
  let [commentId, setCommentId] = useState("");
  const [showMoreOption, setShowMoreOption] = useState(false);
  const [links, setLinks] = useState([]);

  const [messages, setMessages] = useState([]);
  const [connectionStatus, setConnectionStatus] = useState('Disconnected');

  useEffect(() => {
    const socket = new WebSocket('');

    socket.onopen = () => {
      setConnectionStatus('Connected');
      console.log('WebSocket Connection established')
    }

    socket.onmessage = (event) => {
      setMessages((prevMessages) => [...prevMessages, event.data]);
      console.log('Meesage received:', event.data);
    }

    socket.onclose= () => {
      setConnectionStatus('Disconnected')
      console.log('WebSocket connection closed')
    }

    socket.onerror= (error) => {
      console.error('WebSocket error :', error)
    }

  }, []);



  //useEffect(() => {
    //if (!isLoading && commentRef.current && state.commentClick) {
      //commentRef.current.focus();
    //}
  //}, [isLoading]);

  async function fetchFeed() {
    await mainApi.get(`feed_explore/feed_detail/feed_data?fid=${fid}`).then((res) => {
      setFeedData(res.data.body.feed[0]);
      setLinks(res.data.body.links);
      setIsLoading(false);
      setIsComment(false);
    });
  }

  useEffect(() => {
    fetchFeed();
  }, [comments, fid]);

  async function fetchFeedComment() {
    await mainApi.get(`feed_explore/feed_detail/comment_data?fid=${fid}`).then((res) => {
      setComments(res.data.body.comments);
      setIsLoading(false);
    });
  }

  useEffect(() => {
    fetchFeedComment();
  }, []);

  async function handleCheckStar(fid, e) {
    await mainApi
      .get(`feed_explore/check_star?fid=${fid}`)
      .then((res) => {
        setFeedData((prevData) => {
          return prevData.fid === fid
            ? {
                ...prevData,
                star: res.data.body.feed[0].star,
                star_flag: res.data.body.feed[0].star_flag,
              }
            : prevData;
        });
      })
      .catch((err) => {
        if (err.response.status === 401) {
          navigate("/novalogin");
        } else {
          console.error("Error checking star:", err);
        }
      });
  }

  function onChangeComment(e) {
    setCommentValue(e.target.value);
  }

  function onKeyDownEnter(e) {
    if (e.key === "Enter") {
      setIsComment(true);
      fetchMakeComment();
      setCommentValue("");
    }
  }

  function onClickInput() {
    fetchMakeComment();
    setCommentValue("");
  }

  const header = HEADER;

  async function fetchMakeComment() {
    await postApi
      .post("feed_explore/make_comment", {
        header: header,
        body: {
          fid: `${fid}`,
          body: `${commentValue}`,
          target_cid: commentId,
        },
      })
      .then((res) => {
        setComments(res.data.body.comments);
        setCommentId("");
      });
  }

  const onClickComment = (cid, targetCid, uname) => {
    setCommentId(targetCid || cid);
    setCommentValue(`@${uname} `);
    commentRef.current.focus();
  };

  function fetchRemoveFeed() {
    mainApi.get(`feed_explore/try_remove_feed?fid=${fid}`).then((res) => {
      if (res.data.body.result) {
        alert("삭제되었습니다.");
        navigate(-1);
      }
    });
  }

  function fetchRemoveComment(cid) {
    mainApi.get(`feed_explore/remove_comment?fid=${fid}&cid=${cid}`).then(() => {
      setComments((prev) => {
        return prev
          .map((comment) => {
            if (comment.cid === cid) {
              return null;
            }

            if (comment.reply && comment.reply.length > 0) {
              comment.reply = comment.reply.filter((reply) => reply.cid !== cid);
            }

            return comment;
          })
          .filter((comment) => comment !== null);
      });
    });
  }

  function onClickOption(e) {
    e.preventDefault();
    e.stopPropagation();
    setShowMoreOption(!showMoreOption);
  }

  if (isLoading) {
    return <div>Loading</div>;
  }

  return (
    <div className="container">
      <div className={style["top-container"]}>
        <button
          className={style["back-button"]}
          onClick={() => {
            navigate(-1);
          }}
        >
          <img src={back} alt="back" />
          <span>뒤로</span>
        </button>
        {feedData.is_owner && (
          <button
            className={style["delete-button"]}
            onClick={(e) => {
              onClickOption(e);
            }}
          >
            <img src={more_icon} />
          </button>
        )}
        {showMoreOption && (
          <OptionModal onClickOption={onClickOption} onClickDelete={fetchRemoveFeed} />
        )}
      </div>

      <div className={style["content-box"]}>
        <ContentFeed detailPage feed={feedData} handleCheckStar={handleCheckStar} links={links} />
      </div>
      
      <div className="section-separator"></div>

      <div className={style["comment-wrapper"]}>
        <div className={style["comment-wrapper-title"]}>
          코멘트
        </div>

        <div className={style["new-comment-box"]}>
          {temp_comment.map((comment, index) => {
            return <CommentComponent key={index} {...comment}/>
          })}
        </div>

        <div className={style["input-container"]}>
          <div className={style["input-wrapper"]}>
            <input
              ref={commentRef}
              type="text"
              id={style["comment"]}
              value={commentValue}
              onChange={onChangeComment}
              onKeyDown={onKeyDownEnter}
              placeholder="당신의 생각을 남겨보세요."
            />
            <button className={style["input-button"]} onClick={onClickInput}>
              <img src={input} alt="input" />
            </button>
          </div>
        </div>
      </div>

    </div>

  );
}


function CommentComponent({cid, uid, owner, uname, isReply, reply, body}){
  const sampleWriter = "익명"
  const sampleText = "이건 댓글 샘플임 긴걸 적으면 어떻게 될까? \n줄바꿈이 되는지도 한번 보자";



  if(owner){
    return(
      <div className={style["comment-component-my"]}>
        <div className={style["comment-box"]}>
          <div className={style["comment-body-my"]}>
            {body}
          </div>
        </div>
      </div>
    );
  }else{
    if(isReply){
      return (
        <div className={style["comment-component"]}>
          <div className={style["profile-box"]}>
            <div style={{width:"36px", height:"36px", borderRadius:"50%", backgroundColor:"white"}}>

            </div>

          </div>
            <div style={{width:"14px"}}>
            </div>

          <div className={style["comment-box"]}>
            <div className={style["comment-writer"]}>
              {uname}
            </div>

            <div className={style["comment-body"]}>
              {body}
            </div>
          </div>

        </div>
      );
    }else{
      return (
        <div className={style["comment-component"]}>
          <div className={style["profile-box"]}>
            <div style={{width:"36px", height:"36px", borderRadius:"50%", backgroundColor:"white"}}>

            </div>

          </div>
            <div style={{width:"14px"}}>
            </div>

          <div className={style["comment-box"]}>
            <div className={style["comment-writer"]}>
              {uname}
            </div>

            <div className={style["comment-body"]}>
              {body}
            </div>
          </div>

        </div>
      );
    }
  }
}







// 대댓글
function ReplyComment({ index, length, reply, fetchOriginalComment, handleRemove }) {
  const [firstWord, ...restWords] = reply.body.split(" ");

  let src;

  if (length === 1) {
    src = reArrow1;
  } else {
    if (index === 0) {
      src = reArrow2;
    } else if (index + 1 === length) {
      src = reArrow4;
    } else {
      src = reArrow3;
    }
  }

  return (
    <div className={style["img-container"]}>
      <img src={src} alt="대댓글" />
      <div key={reply.cid} className={`${style["reply-box"]}`} onClick={(e) => e.stopPropagation()}>
        <div className={style["comment-user"]}>
          <p>{reply.uname}</p>
          <div className={style["function_button_container"]}>
            {reply.is_reworked && (
              <button
                className={style["AI_text"]}
                onClick={(e) => {
                  e.preventDefault();
                  e.stopPropagation();
                  fetchOriginalComment(reply.cid);
                }}
              >
                원문 보기
              </button>
            )}
            {reply.owner ? (
              <div
                className={style["comment-delete-report"]}
                onClick={(e) => {
                  e.stopPropagation();
                  handleRemove(reply.cid);
                }}
              >
                삭제
              </div>
            ) : (
              <div className={style["comment-delete-report"]}>신고</div>
            )}
          </div>
        </div>

        <div className={style["comment-content"]}>
          <span style={{ color: reply.mention ? "#2C59CD" : "black" }}>{firstWord} </span>
          {restWords.join("")}
        </div>

        <span className={style["date-st"]}> {reply.date}</span>
      </div>
    </div>
  );
}

// 모달
function OptionModal({ onClickOption, onClickDelete }) {
  return (
    <div className={style["OptionModal"]} onClick={onClickOption}>
      <div className={style["modal_container"]}>
        <div className={style["modal_title"]}>설정</div>
        {/* <div className={style["modal_content"]}>수정</div> */}
        <div
          className={`${style["modal_content"]} ${style["modal_content_accent"]}`}
          onClick={onClickDelete}
        >
          삭제
        </div>
      </div>
    </div>
  );
}
