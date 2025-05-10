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

  const [showMoreOption, setShowMoreOption] = useState(false);
  const [links, setLinks] = useState([]);

  const [messages, setMessages] = useState([]);
  const [connectionStatus, setConnectionStatus] = useState('Disconnected');

  const [socket, setSocket] = useState(null);
  const [user, setUser] = useState("");

  useEffect(() => {
    const initialize = async () => {
      try {
        // 1. fetchFeedComment가 완료될 때까지 대기
        const uid = await fetchFeedComment();
        setUser(uid);

        // 2. fetchFeedComment 완료 후 WebSocket 초기화
        const socket = new WebSocket(`wss://nova-platform.kr/feed_detail_realtime/chatting_socket?fid=${fid}&uid=${uid}`);
        setSocket(socket);

        socket.onopen = () => {
          setConnectionStatus('Connected');
          console.log('WebSocket Connection established');
        };

        socket.onmessage = (event) => {
          //setMessages((prevMessages) => [...prevMessages, event.data]);
          analyzeMessage(event.data);
          console.log('Message received:', event.data);
        };

        socket.onclose = () => {
          setConnectionStatus('Disconnected');
          console.log('WebSocket connection closed');
        };

        socket.onerror = (error) => {
          console.error('WebSocket error:', error);
        };



      } catch (error) {
        console.error('Error during initialization:', error);
      }
    }
    initialize();

  }, []); // 필요한 의존성 추가


  function parseDataToObject(data) {
    // 데이터를 줄바꿈 단위로 분리
    const [type, uid, uname, cid, body, date] = data.split('<br>');

    // 객체 생성 및 반환
    return {
      type: type,
      cid: cid, 
      uid: uid, // 유아이디
      owner: uname,
      uname: uname, // 유저 이름
      is_reply: true, // 항상 true
      reply: {}, // 항상 빈 객체
      body: body, // 본문
      date: date, // 날짜
    };
  }

  function analyzeMessage(message) {
    // 메시지 분석 로직을 여기에 추가합니다.
    // 예를 들어, JSON 형식의 메시지를 파싱하거나 특정 키워드를 찾는 등의 작업을 수행할 수 있습니다.
    if (message === "ping") {
      return;
    }else{
      const parsedMessage = parseDataToObject(message);
      if (parsedMessage.type === "add") {
        console.log('Parsed message:', parsedMessage);
        setComments((prevComments) => [...prevComments, parsedMessage]);
      }else if (parsedMessage.type === "delete") {
        console.log('Delete message:', parsedMessage);
        setComments((prevComments) => prevComments.filter(comment => comment.cid !== parsedMessage.body));
      }
    }

    try {
      const parsedMessage = JSON.parse(message);
      console.log('Parsed message:', parsedMessage);
    } catch (error) {
      console.error('Error parsing message:', error);
    }
  }

  const tryDeleteComment = (cid) => {
    if (socket) {
      const inputMessage = `${cid}<br>delete`; // 실제 메시지로 변경
      setComments((prevComments) => prevComments.filter(comment => comment.cid !== cid));
      socket.send(inputMessage);
    }
  };

  const tryAddComment = () => {
    if (user === "") {
      alert("로그인 후 댓글을 남길 수 있습니다.");
      return;
    }else{
      if (socket && socket.readyState === WebSocket.OPEN) {
        const sanitizedCommentValue = commentValue.replace(/<br>/g, '[br]');
        const inputMessage = `${sanitizedCommentValue}<br>add`; // 실제 메시지로 변경
        socket.send(inputMessage);
        setCommentValue(''); // 메시지 전송 후 입력 필드 초기화
      } else {
        console.error('WebSocket is not open. Unable to send message.');
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
      await mainApi.get(`feed_explore/feed_detail/comment_data?fid=${fid}&target_cid=${targetCid}`).then((res) => {
        putCommentProcess({ fetchedComments: res.data.body.comments });
        uid = res.data.body.uid;
        setIsLoading(false);
      });
    } else{
      await mainApi.get(`feed_explore/feed_detail/comment_data?fid=${fid}`).then((res) => {
        putCommentProcess({ fetchedComments: res.data.body.comments });
        uid = res.data.body.uid;
        setIsLoading(false);
      });
    };
    console.log("uid", uid)
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
    } else {
      console.log("No new comments to add.");
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
      //fetchMakeComment();
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
          {comments.map((comment, index) => {
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


function CommentComponent({cid, uid, owner, uname, isReply, reply, body}){

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
