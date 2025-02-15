import React, { useState, useEffect, useRef } from "react";
import { Link, useNavigate, useNavigation, useParams } from "react-router-dom";
import style from "./WriteFeed.module.css";
import style2 from "./WriteMoment.module.css";
import useBiasStore from "../../stores/BiasStore/useBiasStore.js";
import tag from "./../../img/tag.svg";
import img_icon from "./../../img/image.png";
import vote_icon from "./../../img/vote.png";
import link_icon from "./../../img/link.png";
import { Modal } from "./Write.js";
import { VoteModal } from "./Write.js";
import { LinkModal } from "./Write.js";
const categoryData = [
  { key: 0, category: "자유게시판" },
  { key: 1, category: "팬아트" },
  { key: 2, category: "유머게시판" },
];

const WriteMoment = ({ onClickMoment }) => {
  let { biasList, loading, fetchBiasList } = useBiasStore();
  const navigate = useNavigate();
  let [biasId, setBiasId] = useState();
  let [inputTagCount, setInputTagCount] = useState(0);
  let [inputTag, setInputTag] = useState("");
  let [tagList, setTagList] = useState([]);
  const [bodyText, setBodyText] = useState("");
  let [inputBodyCount, setInputBodyCount] = useState(0); //글자수
  let [longData, setLongData] = useState();
  const [choice, setChoice] = useState([]); // 선택지 4개 상태로 저장
  const [imageFiles, setImageFiles] = useState([]);
  const [imagePreview, setImagePreview] = useState([]);
  const params = useParams();
  const type = params.type;
  let [linkList, setLinkList] = useState([]);
  let [createOptions, setCreateOptions] = useState(0);
  let [showModal, setShowModal] = useState(false);
  let [showVoteModal, setShowVoteModal] = useState(false);
  let [showLinkModal, setShowLinkModal] = useState(false);

  let [urlLink, setUrlLink] = useState([{ name: "", url: "" }]);
  let [numLink, setNumLink] = useState(0);
  let [linkTitle, setLinkTitle] = useState("");
  let [linkUrl, setLinkUrl] = useState("");
  function onClickCheck(e) {
    e.stopPropagation();
    if (inputTag && inputTagCount <= 12) {
      // 해시태그가 최대 글자 수 이내일 때만 추가
      setTagList([...tagList, `${inputTag}`]); // 태그 목록에 추가
      setInputTag(""); // 입력 필드 초기화
      setInputTagCount(0); // 글자 수 초기화
    }
    e.preventDefault();
  }
  let [isUserState, setIsUserState] = useState(false);
  function handleValidCheck() {
    fetch("https://nova-platform.kr/home/is_valid", {
      credentials: "include",
    })
      .then((response) => {
        if (response.status === 200) {
          setIsUserState(true);
        } else {
          setIsUserState(false);
        }
        return response.json();
      })
      .then((data) => {
        console.log(data);
      })
      .catch((error) => {
        console.error("Error:", error);
        setIsUserState(false);
      });
  }

  useEffect(() => {
    handleValidCheck();
  }, []);

  function onChangeTag(e) {
    const inputText = e.target.value;

    // 첫 글자가 #이면 제외하고 저장
    const processedText = inputText.startsWith("#") ? inputText.slice(1) : inputText;
    if (processedText.length <= 12) {
      setInputTag(processedText);
      setInputTagCount(processedText.length); // 글자 수 업데이트
    }
  }

  function onKeyDown(e) {
    if (e.key === "Enter") {
      // Enter 키로 태그 추가
      if (inputTag && inputTagCount <= 12) {
        // 해시태그가 최대 글자 수 이내일 때만 추가
        setTagList([...tagList, `${inputTag}`]); // 태그 목록에 추가
        setInputTag(""); // 입력 필드 초기화
        setInputTagCount(0); // 글자 수 초기화
      }
      e.preventDefault(); // 기본 Enter 동작 방지 (예: 줄바꿈)
    }
  }

  const onDeleteTag = (index) => {
    // 현재 해시태그 리스트에서 삭제할 인덱스를 기준으로 필터링
    const updatedTags = tagList.filter((_, i) => i !== index);
    setTagList(updatedTags); // 업데이트된 해시태그 리스트를 상태에 설정
  };

  function onChangeBody(e) {
    const inputText = e.target.value;

    if (inputText.length <= 300) {
      setBodyText(e.target.value);
      setInputBodyCount(e.target.value.length);
    }
  }
  let header = {
    "request-type": "default",
    "client-version": "v1.0.1",
    "client-ip": "127.0.0.1",
    uid: "1234-abcd-5678",
    endpoint: "/user_system/",
  };
  const [category, setCategory] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault(); // 기본 동작을 막음 (중요)

    const send_data = {
      header: header,
      body: {
        body: bodyText || longData, // 입력된 글 본문 반영
        fid: "",
        fclass: type,
        choice: choice, // 4지선다 선택지 반영
        hashtag: tagList,
        link: linkList,
        bid: biasId,
        category: category,
        image_names: "",
      },
    };

    const formData = new FormData();
    if (imageFiles) {
      for (let file of imageFiles) {
        formData.append("images", file); // "images" 키로 여러 파일 추가
      }
    }
    formData.append("jsonData", JSON.stringify(send_data)); // JSON 데이터 추가

    fetch("https://nova-platform.kr/feed_explore/try_edit_feed", {
      method: "POST",
      credentials: "include",
      body: formData,
    })
      .then((response) => {
        response.json();
      })
      .then((data) => {
        alert("업로드가 완료되었습니다.");
        navigate("/");
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("업로드 실패!");
      });
  };

  function onClickUpload() {
    if (!isUserState) {
      alert("로그인이 필요합니다.");
      navigate("/nova_login");
    }
  }

  function onClickModal() {
    setShowModal(!showModal);
  }
  function onClickVoteModal() {
    setShowVoteModal(!showVoteModal);
  }
  function onClickLinkModal() {
    setShowLinkModal(!showLinkModal);
  }

  let [currentFileName, setCurrentFileName] = useState([]);

  const handleFileChange = (event) => {
    const files = Array.from(event.target.files);
    const names = files.map((file) => file.name);
    if (names) {
      setCurrentFileName(names);
    } else {
      setCurrentFileName([""]);
    }
    const selectedFile = Array.from(event.target.files);
    const validFiles = selectedFile.filter((file) => file.type.startsWith("image/"));

    if (validFiles.length < selectedFile.length) {
      alert("이미지 파일만 가능");
    }

    setImageFiles((prevFiles) => [...prevFiles, ...validFiles]);

    const previewUrls = validFiles.map((file) => {
      return URL.createObjectURL(file);
    });

    setImagePreview((prevUrls) => [...prevUrls, ...previewUrls]);
    validFiles.forEach((file) => URL.revokeObjectURL(file));
  };

  function onClickAdd() {
    setChoice([...choice, ""]);
    setCreateOptions((prev) => prev + 1);
  }

  function onDeleteOption(i) {
    setChoice((prevChoices) => prevChoices.filter((_, index) => index !== i));
    setCreateOptions((prev) => Math.max(0, prev - 1));
  }

  function handleLinkChange() {}

  const handleChoiceChange = (index, value) => {
    const newChoices = [...choice];
    newChoices[index] = value;
    setChoice(newChoices); // 4지선다 선택지 업데이트
  };

  function onClickAddLink() {
    setNumLink(numLink + 1);
    // setLinkList((items) => [...items, linkTitle]);
    let newLink = { explain: linkTitle, url: linkUrl };
    setLinkList([...linkList, newLink]);
    setLinkTitle("");
    setLinkUrl("");
  }
  return (
    <div className={style2["nav_moment"]}>
      <h4>모멘트 작성</h4>
      <form className={style2["nav_form"]}>
        <div className={style2["input-container"]}>
          <div className={style2["input-wrapper"]}>
            <input
              placeholder="해시태그 입력"
              type="text"
              value={`${inputTag}`}
              onChange={onChangeTag}
              onKeyDown={onKeyDown}
              className={style2["input-hashtag"]}
            />
            <span className={style2["count-text"]}>{inputTagCount}/12</span>
          </div>
          <div className={style2["button-wrapper"]}>
            <button
              className={style2["check-button"]}
              onClick={(e) => {
                onClickCheck(e);
              }}
            >
              확인
            </button>
          </div>
        </div>
        <div className={style2["tag-container"]}>
          <div className={style2["tag-icon-box"]}>
            <img src={tag} alt="tag" />
          </div>
          {tagList.length !== 0 &&
            tagList.map((tag, i) => (
              <div className={style2["tag-box"]} key={i}>
                #{tag}
                <button onClick={() => onDeleteTag(i)} className={style2["delete-tag"]}>
                  &times; {/* 삭제 아이콘 */}
                </button>
              </div>
            ))}
        </div>

        <div className={` ${style2["content-container"]}`}>
          <div className={`${style2["content-title"]}`}>경험을 모두와 함께 이야기 해봐요!</div>

          <textarea
            className={style2["write_body"]}
            name="body"
            placeholder="내용을 입력해주세요"
            value={bodyText}
            onChange={onChangeBody}
          />
        </div>

        <section className={` ${style2["select-container"]}`}>
          <div className={style2["section_title"]}>주제</div>

          <section>
            <DropDownSection options={biasList} setBiasId={setBiasId} />
          </section>
        </section>

        <section className={` ${style2["select-container"]}`}>
          <div className={style2["section_title"]}>카테고리</div>
          <section>
            <DropDownSection options={categoryData} setCategory={setCategory} />
          </section>
        </section>

        <span className={style2["moment_footer"]}>
          <div className={style2["content_button"]}>
            {type !== "long" && (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  e.preventDefault();
                  onClickModal();
                }}
              >
                <img src={img_icon} alt="img" />
                이미지
              </button>
            )}
            <button
              onClick={(e) => {
                e.stopPropagation();
                e.preventDefault();
                onClickVoteModal();
              }}
            >
              <img src={vote_icon} alt="img" />
              투표
            </button>
            <button
              onClick={(e) => {
                e.stopPropagation();
                e.preventDefault();
                onClickLinkModal();
              }}
            >
              <img src={link_icon} alt="img" />
              링크
            </button>
          </div>
          {showModal && (
            <Modal
              onClickModal={onClickModal}
              handleFileChange={handleFileChange}
              imagePreview={imagePreview}
              currentFileName={currentFileName}
              imageFiles={imageFiles}
            />
          )}
          {showVoteModal && (
            <VoteModal
              onClickModal={onClickVoteModal}
              createOptions={createOptions}
              onClickAdd={onClickAdd}
              onClickDelete={onDeleteOption}
              handleChoiceChange={handleChoiceChange}
              choice={choice}
              setChoice={setChoice}
            />
          )}
          {showLinkModal && (
            <LinkModal
              onClickModal={onClickLinkModal}
              link={urlLink}
              setLink={setUrlLink}
              numLink={numLink}
              linkTitle={linkTitle}
              linkUrl={linkUrl}
              setLinkTitle={setLinkTitle}
              setLinkUrl={setLinkUrl}
              onClickAdd={onClickAddLink}
              handleLinkChange={handleLinkChange}
              linkList={linkList}
            />
          )}
          <p onClick={onClickMoment}>취소</p>

          <p
            type="submit"
            onClick={(e) => {
              e.preventDefault();
              e.stopPropagation();
              handleSubmit(e);
              onClickUpload();
            }}
          >
            게시하기
          </p>
        </span>
      </form>
    </div>
  );
};

export default WriteMoment;

function DropDownSection({ options, setBiasId, setCategory }) {
  const [showTopic, setShowTopic] = useState(false);
  const [currentTopic, setCurrentTopic] = useState("선택 없음");
  function onClickTopic() {
    setShowTopic(!showTopic);
  }

  function onClickSelectTopic(e, bid, category) {
    // console.log(e.target.innerText);
    setCurrentTopic(e.target.innerText);
    setShowTopic(!showTopic);
    if (setBiasId) {
      setBiasId(bid);
    } else if (setCategory) {
      setCategory(category);
    }
  }
  return (
    <>
      <label className={style["Select_box"]} onClick={onClickTopic}>
        {currentTopic}
      </label>
      <ul className={`${showTopic ? style["Select_options_on"] : style["Select_options"]}`}>
        <li onClick={onClickSelectTopic}>선택 없음</li>
        {options &&
          options.map((option, i) => {
            return (
              <li
                key={option.bid || option.key}
                value={option.bname || option.category}
                onClick={(e) => {
                  onClickSelectTopic(e, option.bid, option.category);
                }}
              >
                {option.bname || option.category}
              </li>
            );
          })}
      </ul>
    </>
  );
}
