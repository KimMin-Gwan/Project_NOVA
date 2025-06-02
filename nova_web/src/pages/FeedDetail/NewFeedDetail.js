import { useLocation, useNavigate, useParams } from "react-router-dom";
import { useState, useEffect, useRef } from "react";
import mainApi from "../../services/apis/mainApi";
import postApi from "../../services/apis/postApi";

import HEADER from "../../constant/header";

import more_icon from "./../../img/more_icon.svg";
import user_icon from "./../../img/user_profile.svg";
import back from "./../../img/detail_back.png";
import input from "./../../img/input.svg";
import reArrow1 from "./../../img/reArrow1.svg";
import reArrow2 from "./../../img/reArrow2.svg";
import reArrow3 from "./../../img/reArrow3.svg";
import reArrow4 from "./../../img/reArrow4.svg";

import { ContentFeed } from "../../component/feed";

import style from "./NewFeedDetail.module.css";


//const temp_comment = [
  //{cid: "1", uid:"1", owner:false, uname:"익명", is_reply:false, reply:"", body:"원글 그림 왜 잘그림? 님 혹시 제것도 슬쩍 그려주실 수 있음?"},
  //{cid: "2", uid:"2", owner:false, uname:"니말이다맞음", is_reply:false, reply:"", body:"윗댓 정신좀 차려라. 그냥 날로 처먹으려고 하네;; 님들 같은 사람들 때문에 멀정한 치수들 다 욕먹는거임"},
  //{cid: "3", uid:"3", owner:true, uname:"관리자", is_reply:false, reply:"", body:"님들 싸우지 말죠 ㅋㅋㅋ"},
  //{cid: "4", uid:"1", owner:false, uname:"익명", is_reply:false, reply:"", body:"뭐래;; 그냥 하는말인데 왜 급발진함;;"},
  //{cid: "5", uid:"3", owner:true, uname:"관리자", is_reply:true, reply:{cid:"2", uname:"익명", body:"뭐래;; 그냥 하는말인데 왜 급발진함;;"}, body:"그려드릴테니 진정하십쇼 ㅋㅋㅋㅋㅋ"},
//]


export default function NewFeedDetail() {
  let navigate = useNavigate();
  let { fid } = useParams();
  //let fid = '6adf-fb09-4907-ULIx2R'

  let location = useLocation();
  //let { state } = location;
  let commentRef = useRef(null);

  const [isLoading, setIsLoading] = useState(true); // 로딩 상태 관리
  const [isComment, setIsComment] = useState(false);
  let [feedData, setFeedData] = useState([]);
  let [comments, setComments] = useState([]);
  let [commentValue, setCommentValue] = useState("");

  let [commentId, setCommentId] = useState("");
  let [targetCid, setTargetCid] = useState("");
  let [isMoreComment, setIsMoreComment] = useState(false);

  const [showMoreOption, setShowMoreOption] = useState(false);
  const [links, setLinks] = useState([]);

  const [messages, setMessages] = useState([]);
  const [connectionStatus, setConnectionStatus] = useState('Disconnected');

  const [socket, setSocket] = useState(null);
  const [user, setUser] = useState("");
  const [newComment, setNewComment] = useState(false);

  const socketRef = useRef(null);
  const commentBoxRef = useRef(null);

  const [showCommentMoreOption, setShowCommentMoreOption] = useState(false);
  const [optionTargetComment, setOptionTargetComment] = useState("");

  const togglePushingComment = (cid) => {
    setOptionTargetComment(cid);
    setShowCommentMoreOption(!showCommentMoreOption);
  }

  useEffect(() => {
    if (newComment){
      if (commentBoxRef.current) {
        commentBoxRef.current.scrollTo({top: commentBoxRef.current.scrollHeight, behavior:"smooth"})
        setNewComment(false);
      }
    }
  }, [newComment]);

  useEffect(() => {
    const initialize = async () => {
      try {
        // 1. fetchFeedComment가 완료될 때까지 대기
        const uid = await fetchFeedComment();
        setUser(uid);

        // 2. fetchFeedComment 완료 후 WebSocket 초기화
        const socket = new WebSocket(`wss://nova-platform.kr/feed_detail_realtime/chatting_socket?fid=${fid}&uid=${uid}`);
        socketRef.current = socket;

        socket.onopen = () => {
          setConnectionStatus('Connected');
        };

        socket.onmessage = (event) => {
          analyzeMessage(event.data);
        };

        socket.onclose = () => {
          setConnectionStatus('Disconnected');
        };

        socket.onerror = (error) => {
          console.error('WebSocket error:', error);
        };



      } catch (error) {
        console.error('Error during initialization:', error);
      }
    }
    initialize(); 

    return () => {
      if (socketRef.current) {
        socketRef.current.close();
      }
    };

  }, []); // 필요한 의존성 추가

  useEffect(() => {
    // 현재 경로에 fid가 포함되어 있는지 확인
    if (!location.pathname.includes(fid)) {
      if (socketRef.current) {
        socketRef.current.close();
      }
    }
  }, [location]);

  function analyzeMessage(message) {
    const socket = socketRef.current; // Access the WebSocket instance directly
    if (!socket) {
      console.error('Socket is not initialized');
      return;
    }


    if (message === "ping") {
      socket.send("pong");
      return;
    }

    try {
      // Parse the message
      const messageParts = message.split('<br>');
      // Extract `type` and remove it from parsedMessage
      const messageType = messageParts[0];


      const transformedMessage = parseDataToObject(message);
      
      // Handle different message types
      if (messageType === "add") {
        setComments((prevComments) => [...prevComments, transformedMessage]);
        setNewComment(true);
      } else if (messageType === "delete") {
        setComments((prevComments) =>
          prevComments.map((comment) =>
            comment.cid === transformedMessage.body
              ? { ...comment, body: "삭제된 메시지입니다" }
              : comment
          )
        );
      }
    } catch (error) {
      console.error('Error parsing message:', error);
    }
  }

  function parseDataToObject(data) {
    // 데이터를 줄바꿈 단위로 분리
    const [type, owner, uid, uname, cid, body, date] = data.split('<br>');


    let booleanValue = owner.toLowerCase() === "true";

    // 객체 생성 및 반환
    return {
      cid: cid, 
      uid: uid, // 유아이디
      owner: booleanValue,
      uname: uname, // 유저 이름
      is_reply: true, // 항상 true
      reply: {}, // 항상 빈 객체
      body: body, // 본문
      date: date, // 날짜
    };
  }


  const tryDeleteComment = (cid) => {
    if (socketRef.current) {
      const socket = socketRef.current; // Access the WebSocket instance directly
      const inputMessage = `${cid}<br>delete`; // 실제 메시지로 변경
      //setComments((prevComments) => prevComments.filter(comment => comment.cid !== cid));
      socket.send(inputMessage);
      togglePushingComment("");
    }
  };

  const tryAddComment = () => {
    if (user === "") {
      alert("로그인 후 댓글을 남길 수 있습니다.");
      return;
    }else{
      if (socketRef && commentValue !== "") {
        const socket = socketRef.current; // Access the WebSocket instance directly
        const sanitizedCommentValue = commentValue.replace(/<br>/g, '[br]');
        const inputMessage = `${sanitizedCommentValue}<br>add`; // 실제 메시지로 변경
        socket.send(inputMessage);
        setCommentValue(''); // 메시지 전송 후 입력 필드 초기화
      }
    }
  }


  //useEffect(() => {
    //if (!isLoading && commentRef.current && state.commentClick) {
      //commentRef.current.focus();
    //}
  //}, [isLoading]);

  async function fetchFeed() {
    await mainApi.get(`feed_explore/feed_detail/feed_data?fid=${fid}`).then((res) => {
      console.log(res.data.body)
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
    let uid = "-1";
    if (targetCid !== "") {
      await mainApi.get(`feed_explore/feed_detail/comment_data?fid=${fid}&cid=${targetCid}`).then((res) => {
        putCommentProcess({ fetchedComments: res.data.body.comments });
        setIsMoreComment(res.data.body.is_more);
        uid = res.data.body.uid;
        setIsLoading(false);
      });
    } else{
      await mainApi.get(`feed_explore/feed_detail/comment_data?fid=${fid}`).then((res) => {
        putCommentProcess({ fetchedComments: res.data.body.comments });
        setIsMoreComment(res.data.body.is_more);
        uid = res.data.body.uid;
        setIsLoading(false);
      });
    };
    return uid;
  }

  function putCommentProcess({ fetchedComments }) {
    // 중복 확인: 기존 comments에 없는 cid만 필터링
    const uniqueComments = fetchedComments.filter(
      (newComment) => !comments.some((existingComment) => existingComment.cid === newComment.cid)
    );

    // 중복이 없는 댓글만 추가
    if (uniqueComments.length > 0) {
      const newComments = [...uniqueComments, ...comments];
      setComments(newComments);

      // 첫 번째 댓글의 cid를 타겟으로 설정
      setTargetCid(newComments[0].cid);
    } 
  }


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
      tryAddComment();
      setCommentValue("");
    }
  }

  function onClickInput() {

    tryAddComment();
    //fetchMakeComment();
    setCommentValue("");

  }

  const header = HEADER;

  //async function fetchMakeComment() {
    //await postApi
      //.post("feed_explore/make_comment", {
        //header: header,
        //body: {
          //fid: `${fid}`,
          //body: `${commentValue}`,
          //target_cid: commentId,
        //},
      //})
      //.then((res) => {
        //setComments(res.data.body.comments);
        //setCommentId("");
      //});
  //}

  const setPlaceholder = () => {
    if (user !== "") { 
      return "당신의 생각을 남겨보세요.";
    }else{
      return "로그인 후 댓글을 남길 수 있습니다.";
    }
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
        navigate("/");
      }
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
          <OptionModal onClickOption={onClickOption} onClickDelete={fetchRemoveFeed} fid={fid} />
        )}
      </div>

      <div className={style["content-box"]}>
        <ContentFeed detailPage feed={feedData} handleCheckStar={handleCheckStar} links={links} disableClick={true} />
      </div>
      
      <div className="section-separator"></div>

      {showCommentMoreOption && (
        <CommentOptionModal onClose={togglePushingComment} onClickDelete={tryDeleteComment} deleteTargetCid={optionTargetComment} />
      )}


      <div className={style["comment-wrapper"]}>
        <div className={style["comment-wrapper-title"]}>
          실시간 코멘트
        </div>
        
        {
         isMoreComment && (
          <button className={style["comment-more-button"]}
              onClick={() => {
                fetchFeedComment();
              }}
          >
              지난 댓글 불러오기
          </button>
        )}


        <div className={style["new-comment-box"]}
          ref={commentBoxRef} // ref 연결
        >
          {comments.map((comment, index) => {
            return <CommentComponent key={index} {...comment} commentAction={togglePushingComment}/>
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
              placeholder={setPlaceholder()}
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


function CommentComponent({cid, uid, owner, uname, isReply, reply, body, date, commentAction}){
  const profile = `https://kr.object.ncloudstorage.com/nova-profile-bucket/${uid}.png`;
  const pressTimer = useRef(null);

  const handlePressStart = () => {
    pressTimer.current = setTimeout(() => {
      // 꾹 누르기 감지 시 실행할 작업
      commentAction(cid);
    }, 500); // 500ms 이상 눌렀을 때 실행
  };

  const handlePressEnd = () => {
    clearTimeout(pressTimer.current); // 타이머 초기화
  };

  if(owner){
    return(
      <div id={cid} className={style["comment-component-my"]}>
        <div className={style["comment-box"]}>
          <div className={style["comment-flex-vertical-container"]}>
            <div className={style["comment-date"]}>
              {date}
            </div>
            <div className={style["comment-body-my"]}
              onMouseDown={handlePressStart}
              onMouseUp={handlePressEnd}
              onMouseLeave={handlePressEnd} // 마우스가 벗어날 경우 초기화
              onTouchStart={handlePressStart}
              onTouchEnd={handlePressEnd} // 모바일 터치 지원
            >
              {body}
            </div>
          </div>
        </div>
      </div>
    );
  }else{
    if(isReply){
      return (
        <div id={cid} className={style["comment-component"]}>
          <div className={style["profile-box"]}>
              <img className={style=["profile-img"]} src={profile} alt="img" onError={(e) => (e.target.src = user_icon)} />
          </div>
            <div style={{width:"14px"}}>
            </div>

          <div className={style["comment-box"]}>
            <div className={style["comment-writer"]}>
              {uname}
            </div>
            <div className={style["comment-flex-vertical-container"]}>
              <div className={style["comment-body"]}>
                {body}
              </div>
              <div className={style["comment-date"]}>
                {date}
              </div>
            </div>
          </div>
        </div>
      );
    }else{
      return (
        <div id={cid} className={style["comment-component"]}>
          <div className={style["profile-box"]}>
              <img src={profile} alt="img" onError={(e) => (e.target.src = user_icon)} />
          </div>
            <div style={{width:"14px"}}>
            </div>
          <div className={style["comment-box"]}>
            <div className={style["comment-writer"]}>
              {uname}
            </div>

            <div className={style["comment-flex-vertical-container"]}>
              <div className={style["comment-body"]}>
                {body}
              </div>
              <div className={style["comment-date"]}>
                {date}
              </div>
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
function OptionModal({ onClickOption, onClickDelete, fid }) {
  const navigate = useNavigate();

  const handleNavigate = () => {
    navigate(`/write_feed/${fid}`);
  };

  return (
    <div className={style["OptionModal"]} onClick={onClickOption}>
      <div className={style["modal_container"]}>
        <div className={style["modal_title"]}>설정</div>
        {/* <div className={style["modal_content"]}>수정</div> */}
        <div
          className={`${style["modal_content"]} ${style["modal_content_accent"]}`}
          onClick={handleNavigate}
        >
          수정
        </div>
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

// 댓글 옵션 모달
function CommentOptionModal({ onClose, onClickDelete, deleteTargetCid }) {
  return (
    <div className={style["OptionModal"]} onClick={()=>onClose("")}>
      <div
        className={style["modal_container"]}
        onClick={(e) => e.stopPropagation()} // 이벤트 버블링 방지
      >
        <div className={style["modal_title"]}>댓글</div>
        {/* <div className={style["modal_content"]}>수정</div> */}
        <div
          className={`${style["modal_content"]} ${style["modal_content_accent"]}`}
          onClick={() => onClickDelete(deleteTargetCid)}
        >
          삭제
        </div>
      </div>
    </div>
  );
}