import React, { useState, useEffect, useRef } from "react";
import { Link, useNavigate } from "react-router-dom";
// import style from "./../FeedPage/FeedPage.module.css";
import style from "./WriteFeed.module.css";
// import stylePlanet from "./../PlanetPage/Planet.module.css";
import backword from "./../../img/back_icon.png";

import tags from "./../../img/tags.png";
import back from "./../../img/write_vector1.png";
import select from "./../../img/select-icon.png";
import img from "./../../img/img-icon.png";
import { getModeClass } from "./../../App.js";
import BiasBoxes from "../../component/BiasBoxes.js";
// import { Editor } from "@toast-ui/react-editor/index.js";
const WriteFeed = ({ brightmode }) => {
  const navigate = useNavigate();

  let [showModal, setShowModal] = useState(false);
  let [showVoteModal, setShowVoteModal] = useState(false);
  let [showLinkModal, setShowLinkModal] = useState(false);
  let [linkTitle, setLinkTitle] = useState("");
  let [linkUrl, setLinkUrl] = useState("");
  let [linkList, setLinkList] = useState([]);
  let [biasId, setBiasId] = useState();
  // useEffect(() => {
  //   setLinkList([{ name: linkTitle, url: linkUrl }]);
  //   console.log("linklist");
  // }, [linkTitle, linkUrl]);
  let [numImg, setNumImg] = useState(0);

  function onClickModal() {
    setShowModal(!showModal);
  }
  function onClickVoteModal() {
    setShowVoteModal(!showVoteModal);
  }
  function onClickLinkModal() {
    setShowLinkModal(!showLinkModal);
  }

  // let [isLogined, setIsLogined] = useState(false);
  let header = {
    "request-type": "default",
    "client-version": "v1.0.1",
    "client-ip": "127.0.0.1",
    uid: "1234-abcd-5678",
    endpoint: "/user_system/",
  };

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

  const [imagePreview, setImagePreview] = useState([]);
  const [imageFiles, setImageFiles] = useState([]);

  const [imageFile, setImageFile] = useState(null);
  const [bodyText, setBodyText] = useState(""); // 글 입력 내용 상태로 저장
  const [choice, setChoice] = useState([]); // 선택지 4개 상태로 저장
  let [inputTagCount, setInputTagCount] = useState(0); //글자수
  let [inputBodyCount, setInputBodyCount] = useState(0); //글자수

  let [urlLink, setUrlLink] = useState([{ name: "", url: "" }]);
  let [numLink, setNumLink] = useState(0);
  let [createOptions, setCreateOptions] = useState(0);

  function onClickAddLink() {
    setNumLink(numLink + 1);
    // setLinkList((items) => [...items, linkTitle]);
    let newLink = { title: linkTitle, url: linkUrl };
    setLinkList([...linkList, newLink]);
    setLinkTitle("");
    setLinkUrl("");
  }

  function onClickAdd() {
    setCreateOptions(createOptions + 1);
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

  const handleSubmit = (event) => {
    event.preventDefault(); // 기본 동작을 막음 (중요)

    const send_data = {
      header: header,
      body: {
        body: bodyText, // 입력된 글 본문 반영
        fid: "",
        fclass: "short",
        choice: choice, // 4지선다 선택지 반영
        hashtag: tagList,
        link: { lname: linkTitle, url: linkUrl },
        bid: biasId,
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
        console.log("111", data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  const handleChoiceChange = (index, value) => {
    const newChoices = [...choice];
    newChoices[index] = value;
    setChoice(newChoices); // 4지선다 선택지 업데이트
  };

  function handleLinkChange() {}

  let title = ["줄 글", "사지선다", "이지선다", "외부 좌표"];
  let fclassName = ["card", "multiple", "balance", "station"];
  let [currentTitle, setCurrentTitle] = useState(0);
  let [currentFclass, setCurrentFclass] = useState(0);

  function handlePrev() {
    setCurrentTitle((prevIndex) => {
      return prevIndex === 0 ? title.length - 1 : prevIndex - 1;
    });
    setCurrentFclass((prevIndex) => {
      return prevIndex === 0 ? fclassName.length - 1 : prevIndex - 1;
    });
  }
  function handleNext() {
    setCurrentTitle((prevIndex) => {
      return prevIndex === title.length - 1 ? 0 : prevIndex + 1;
    });
    setCurrentFclass((prevIndex) => {
      return prevIndex === fclassName.length - 1 ? 0 : prevIndex + 1;
    });
  }

  let [inputTag, setInputTag] = useState("");
  let [plusTag, setPlusTag] = useState("");
  let [tagList, setTagList] = useState([]);
  let [link, setLink] = useState([]);

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

  function onClickUpload() {
    if (isUserState) {
      alert("업로드가 완료되었습니다.");
      navigate(-1);
    } else {
      alert("로그인이 필요합니다.");
      navigate("/");
    }
  }

  const [showImageModal, setShowImageModal] = useState(false);
  const [showChoiceModal, setShowChoiceModal] = useState(false);

  const handleImageModalOpen = () => setShowImageModal(true);
  const handleChoiceModalOpen = () => setShowChoiceModal(true);
  const closeModal = () => {
    setShowImageModal(false);
    setShowChoiceModal(false);
  };
  const [mode, setMode] = useState(() => {
    // 로컬 스토리지에서 가져온 값이 있으면 그것을, 없으면 'bright'로 초기화
    return localStorage.getItem("brightMode") || "bright";
  });
  return (
    // <form onSubmit={handleSubmit}>
    <div className={style["WriteFeed"]}>
      <div className={style["top_container"]}>
        <p
          onClick={() => {
            navigate(-1);
          }}
        >
          취소
        </p>
        <p>숏 피드 작성</p>
        <p
          type="submit"
          onClick={(e) => {
            e.preventDefault();
            e.stopPropagation();
            handleSubmit(e);
            onClickUpload();
          }}
        >
          게시
        </p>
      </div>

      <section className={style["bias-section"]}>
        <div className={style["title"]}>커뮤니티 선택</div>
        <BiasBoxes setBiasId={setBiasId} writeCommunity />
      </section>

      <div className={style["hashtag_container"]}>
        <div>제목(해시태그)</div>
        <div className={style["input-container"]}>
          <input
            placeholder="#해시태그"
            type="text"
            value={`#${inputTag}`}
            onChange={onChangeTag}
            onKeyDown={onKeyDown}
            className={style["input-hashtag"]}
          />
          <button
            className={style["check-button"]}
            onClick={(e) => {
              onClickCheck(e);
            }}
          >
            확인
          </button>
        </div>
        <span className={style["count-text"]}>{inputTagCount}/12</span>
        <div className={style["tag-container"]}>
          <div className={style["tag-icon-box"]}>
            <img src={tags} alt="tag" />
          </div>
          {tagList.length !== 0 &&
            tagList.map((tag, i) => (
              <div className={style["tag-box"]} key={i}>
                #{tag}
                <button onClick={() => onDeleteTag(i)} className={style["delete-tag"]}>
                  &times; {/* 삭제 아이콘 */}
                </button>
              </div>
            ))}
        </div>
        {/* <div>#샘플</div> */}
      </div>

      <div className={style["content_container"]}>
        <div className={style["content-title"]}>본문</div>
        <textarea
          className={style["write_body"]}
          name="body"
          placeholder="내용을 입력해주세요"
          value={bodyText}
          onChange={onChangeBody}
        />
        <span className={style["count-text"]}>{inputBodyCount}/300</span>
      </div>

      <p className={style["alert_message"]}>
        숏 피드 게시글은 작성 후 24시간 동안 노출됩니다.
      </p>

      <div className={style["content_button"]}>
        <button
          onClick={(e) => {
            e.stopPropagation();
            onClickModal();
          }}
        >
          이미지
        </button>
        <button
          onClick={(e) => {
            e.stopPropagation();
            onClickVoteModal();
          }}
        >
          투표
        </button>
        <button
          onClick={(e) => {
            e.stopPropagation();
            onClickLinkModal();
          }}
        >
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
    </div>
    // {/* </form> */}
  );
};

export default WriteFeed;

export const Modal = ({
  show,
  closeModal,
  title,
  children,
  onClickModal,
  handleFileChange,
  imagePreview,
  currentFileName,
  imageFiles,
}) => {
  const [mode, setMode] = useState(() => {
    return localStorage.getItem("brightMode") || "bright";
  });

  let fileRef = useRef();

  // if (!show) return null;
  // return (
  //   <div className={`${style["modal-overlay"]} ${style[getModeClass(mode)]}`} onClick={closeModal}>
  //     <div className={style["modal-content"]} onClick={(e) => e.stopPropagation()}>
  //       <p className={style["modal-title"]}>{title}</p>
  //       {children}
  //       <button onClick={closeModal}>닫기</button>
  //     </div>
  //   </div>
  // );
  return (
    <div className={style["wrapper-container"]}>
      <div className={style["modal-container"]}>
        <div className={style["modal-title"]}>이미지 삽입</div>
        <div className={style["image-container"]}>
          <label htmlFor={style["image-file"]} className={style["input-image"]}>
            이미지를 추가하려면 여기를 클릭하세요
          </label>
          <input
            ref={fileRef}
            id={style["image-file"]}
            name="image"
            type="file"
            accept="image/*"
            multiple
            onChange={(e) => {
              handleFileChange(e);
            }}
          />
          {imagePreview.length !== 0 &&
            imagePreview.map((preview, index) => {
              return (
                <div key={index} className={style["preview-container"]}>
                  <div>닫기</div>
                  <div>{imageFiles[index].name}</div>
                  <div className={style["preview-image"]}>
                    <img key={index} src={preview} />
                  </div>
                </div>
              );
            })}
        </div>
        <div className={style["modal-buttons"]}>
          <button className={style["close_button"]} onClick={onClickModal}>
            닫기
          </button>
          <button
            className={`${style["apply_button"]} ${
              imagePreview.length > 0 ? style["apply_button_on"] : ""
            }`}
            onClick={() => {
              onClickModal();
            }}
            disabled={imagePreview.length === 0}
          >
            적용
          </button>
        </div>
      </div>
    </div>
  );
};

export function VoteModal({
  onClickModal,
  createOptions,
  onClickAdd,
  handleChoiceChange,
  optionValue,
  choice,
  setChoice,
}) {
  let optionRef = useRef(0);

  return (
    <div className={style["wrapper-container"]}>
      <div className={style["modal-container"]}>
        <div className={style["modal-title"]}>투표 추가</div>
        <div className={style["image-container"]}>
          {Array.from({ length: createOptions }).map((option, i) => {
            return (
              <input
                key={i}
                ref={optionRef}
                id={style["vote-option"]}
                name="option"
                type="text"
                value={choice[i]}
                placeholder="이곳을 눌러 수정"
                onChange={(e) => {
                  handleChoiceChange(i, e.target.value);
                }}
              />
            );
          })}
          {createOptions < 4 && (
            <div className={style["option-box"]} onClick={onClickAdd}>
              선택지를 추가하려면 여기를 클릭하세요
            </div>
          )}
        </div>
        <div className={style["modal-buttons"]}>
          <button className={style["close_button"]} onClick={onClickModal}>
            닫기
          </button>
          <button
            className={`${style["apply_button"]} ${
              choice.length > 0 ? style["apply_button_on"] : ""
            }`}
            disabled={choice.length === 0}
            onClick={onClickModal}
          >
            적용
          </button>
        </div>
      </div>
    </div>
  );
}

export function LinkModal({
  onClickModal,
  setLinkTitle,
  setLinkUrl,
  linkTitle,
  linkUrl,
  numLink,
  onClickAdd,
  linkList,
}) {
  return (
    <div className={style["wrapper-container"]}>
      <div className={style["modal-container"]}>
        <div className={style["modal-title"]}>좌표 추가</div>
        <div className={style["link-box-container"]}>
          {linkList.length > 0 &&
            linkList.map((link, i) => {
              return (
                <div key={i} className={style["link-box"]}>
                  <div>닫기</div>
                  <div>{link.title}</div>
                  <div>{link.url}</div>
                </div>
              );
            })}
        </div>

        <div className={style["link-input-container"]}>
          <div className={style["link-input"]}>
            <input
              type="text"
              value={linkTitle}
              onChange={(e) => setLinkTitle(e.target.value)}
              placeholder="좌표 이름"
            />
            <input
              type="url"
              value={linkUrl}
              onChange={(e) => setLinkUrl(e.target.value)}
              placeholder="이곳을 클릭해서 URL을 추가하세요"
            />
          </div>
          <button onClick={onClickAdd}>추가</button>
        </div>

        <div className={style["modal-buttons"]}>
          <button
            className={style["close_button"]}
            onClick={() => {
              onClickModal();
            }}
          >
            닫기
          </button>
          <button
            className={`${style["apply_button"]} ${
              linkList.length > 0 ? style["apply_button_on"] : ""
            }`}
            disabled={linkList.length === 0}
            onClick={onClickModal}
          >
            적용
          </button>
        </div>
      </div>
    </div>
  );
}
