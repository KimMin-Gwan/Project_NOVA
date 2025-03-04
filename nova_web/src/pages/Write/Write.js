import React, { useState, useEffect, useRef } from "react";
import { useNavigate, useParams } from "react-router-dom";
import style from "./WriteFeed.module.css";
import tag from "./../../img/tag.svg";
import add_icon from "./../../img/add.svg";
import close_icon from "./../../img/close.svg";
import img_icon from "./../../img/image.png";
import vote_icon from "./../../img/vote.png";
import link_icon from "./../../img/link.png";
import EditorBox from "../../component/EditorBox.js";
import postApi from "../../services/apis/postApi.js";
import useBiasStore from "../../stores/BiasStore/useBiasStore.js";
import HEADER from "../../constant/header.js";
import toast, { Toaster } from "react-hot-toast";
import DropDown from "../../component/DropDown/DropDown.js";
import Input from "../../component/Input/Input.js";

const categoryData = [
  { key: 0, category: "자유게시판" },
  { key: 1, category: "팬아트" },
  { key: 2, category: "유머게시판" },
  { key: 3, category: "스토리게시판" },
];

const Write = ({ brightmode }) => {
  const params = useParams();
  const type = params.type;
  const navigate = useNavigate();

  let [showModal, setShowModal] = useState(false);
  let [showVoteModal, setShowVoteModal] = useState(false);
  let [showLinkModal, setShowLinkModal] = useState(false);
  let [linkTitle, setLinkTitle] = useState("");
  let [linkUrl, setLinkUrl] = useState("");
  let [linkList, setLinkList] = useState([]);
  let [longData, setLongData] = useState();

  let [biasId, setBiasId] = useState();

  function onClickModal() {
    setShowModal(!showModal);
  }
  function onClickVoteModal() {
    setShowVoteModal(!showVoteModal);
  }
  function onClickLinkModal() {
    setShowLinkModal(!showLinkModal);
  }

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
    let newLink = { explain: linkTitle, url: linkUrl };
    setLinkList([...linkList, newLink]);
    setLinkTitle("");
    setLinkUrl("");
  }

  function onClickAdd() {
    setChoice([...choice, ""]);
    setCreateOptions((prev) => prev + 1);
  }

  function onDeleteOption(i) {
    setChoice((prevChoices) => prevChoices.filter((_, index) => index !== i));
    setCreateOptions((prev) => Math.max(0, prev - 1));
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
  const [category, setCategory] = useState("");
  const handleSubmit = (event) => {
    event.preventDefault(); // 기본 동작을 막음 (중요)

    const loadingText = toast.loading("업로드 중입니다..");
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
        toast.success("업로드가 완료되었습니다.");
        // alert("업로드가 완료되었습니다.");
        navigate("/");
      })
      .catch((error) => {
        toast.error("업로드 실패!");
        // console.error("Error:", error);
        // alert("업로드 실패!");
      });
  };

  const handleChoiceChange = (index, value) => {
    const newChoices = [...choice];
    newChoices[index] = value;
    setChoice(newChoices); // 4지선다 선택지 업데이트
  };

  function onDeleteLink(i) {
    setLinkList((prev) => prev.filter((_, index) => index !== i));
    setCreateOptions((prev) => Math.max(0, prev - 1));
  }

  let [inputTag, setInputTag] = useState("");
  let [tagList, setTagList] = useState([]);

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
    if (!isUserState) {
      alert("로그인이 필요합니다.");
      navigate("/nova_login");
    }
  }
  let { biasList } = useBiasStore();

  const [showTopic, setShowTopic] = useState(false);
  const [currentTopic, setCurrentTopic] = useState("선택 없음");
  function onClickTopic() {
    setShowTopic(!showTopic);
  }

  function onClickSelectTopic(e) {
    // console.log(e.target.innerText);
    setCurrentTopic(e.target.innerText);
    setShowTopic(!showTopic);
  }

  return (
    // <form onSubmit={handleSubmit}>
    <div className={style["WriteFeed"]}>
      <Toaster />
      <div className={style["top_container"]}>
        <p
          className={style["buttons"]}
          onClick={() => {
            navigate(-1);
          }}
        >
          취소
        </p>
        {type === "long" && <p>롱 피드 작성</p>}
        {type === "short" && <p>모멘트 작성</p>}

        <p
          className={style["buttons"]}
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

      <section className={style["Select_container"]}>
        <div className={style["section_title"]}>주제 선택</div>
        <DropDown options={biasList} setBiasId={setBiasId} />

        <div style={{ textAlign: "right" }}>
          <div
            className={style["more-find"]}
            onClick={() => {
              navigate("/follow_page");
            }}
          >
            더 많은 주제 찾아보기
          </div>
        </div>
      </section>

      <section className={style["Select_container"]}>
        <div className={style["section_title"]}>카테고리 선택</div>
        <DropDown options={categoryData} setCategory={setCategory} />
      </section>

      <div className={style["hashtag_container"]}>
        <div>해시태그</div>
        <div className={style["input-container"]}>
          <div className={style["input-wrapper"]}>
            <input
              placeholder="#해시태그"
              type="text"
              value={`${inputTag}`}
              onChange={onChangeTag}
              onKeyDown={onKeyDown}
              className={style["input-hashtag"]}
            />
            <span className={style["count-text"]}>{inputTagCount}/12</span>
          </div>
          <div className={style["button-wrapper"]}>
            <button
              className={style["check-button"]}
              onClick={(e) => {
                onClickCheck(e);
              }}
            >
              확인
            </button>
          </div>
        </div>
        <div className={style["tag-container"]}>
          <div className={style["tag-icon-box"]}>
            <img src={tag} alt="tag" />
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
        <div
          className={`${style["content-title"]} ${type === "long" && style["content-title-long"]}`}
        >
          본문
        </div>
        {type === "short" && (
          <>
            <textarea
              className={style["write_body"]}
              name="body"
              placeholder="내용을 입력해주세요"
              value={bodyText}
              onChange={onChangeBody}
            />
            <span className={style["count-text"]}>{inputBodyCount}/300</span>
          </>
        )}

        {type === "long" && <EditorBox setLongData={setLongData} />}
      </div>

      {type === "short" && (
        <p className={style["alert_message"]}>숏 피드 게시글은 작성 후 24시간 동안 노출됩니다.</p>
      )}
      {type === "long" && (
        <p className={style["alert_message"]}>
          타인에게 불편을 줄 수 있는 내용의 게시글은 경고 없이 삭제 될 수 있습니다.
        </p>
      )}

      <div className={style["content_button"]}>
        {type !== "long" && (
          <button
            onClick={(e) => {
              e.stopPropagation();
              onClickModal();
            }}
          >
            <img src={img_icon} alt="img" />
            이미지
          </button>
        )}
        {/* <button
          onClick={(e) => {
            e.stopPropagation();
            onClickVoteModal();
          }}
        >
          <img src={vote_icon} alt="img" />
          투표
        </button> */}
        <button
          onClick={(e) => {
            e.stopPropagation();
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
      {/* {showVoteModal && (
        <VoteModal
          onClickModal={onClickVoteModal}
          createOptions={createOptions}
          onClickAdd={onClickAdd}
          onClickDelete={onDeleteOption}
          handleChoiceChange={handleChoiceChange}
          choice={choice}
          setChoice={setChoice}
        />
      )} */}
      {showLinkModal && (
        <LinkModal
          onClickModal={onClickLinkModal}
          linkTitle={linkTitle}
          linkUrl={linkUrl}
          setLinkTitle={setLinkTitle}
          setLinkUrl={setLinkUrl}
          onClickAdd={onClickAddLink}
          linkList={linkList}
          onDeleteLink={onDeleteLink}
        />
      )}
    </div>
    // {/* </form> */}
  );
};

export default Write;

export const Modal = ({
  onClickModal,
  handleFileChange,
  imagePreview,
  currentFileName,
  imageFiles,
}) => {
  return (
    <div className={style["wrapper-container"]}>
      <div className={style["modal-container"]}>
        <div className={style["modal-title"]}>이미지 삽입</div>
        <div className={style["image-container"]}>
          <label htmlFor={style["image-file"]} className={style["input-image"]}>
            <span className={style["add-icon"]}>
              <img src={add_icon} alt="add" />
            </span>
            이미지를 추가하려면 여기를 클릭하세요
          </label>
          <input
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
                  <div className={style["remove-icon"]}>
                    <img src={close_icon} alt="remove" />
                  </div>
                  <div className={style["img-name"]}>{imageFiles[index].name}</div>
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
  onClickDelete,
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
          {choice.map((option, i) => {
            return (
              <div key={i} className={style["vote-option-wrapper"]}>
                <button
                  className={`${style["delete-option"]} ${style["remove-icon"]}`}
                  onClick={() => {
                    onClickDelete(i);
                  }}
                >
                  <img src={close_icon} alt="remove" />
                </button>
                <input
                  ref={optionRef}
                  id={style["vote-option"]}
                  name="option"
                  type="text"
                  value={option}
                  placeholder="이곳을 눌러 수정"
                  onChange={(e) => {
                    handleChoiceChange(i, e.target.value);
                  }}
                />
              </div>
            );
          })}
          {createOptions < 4 && (
            <div className={style["option-box"]} onClick={onClickAdd}>
              <span className={style["add-icon"]}>
                <img src={add_icon} alt="add" />
              </span>
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
  onClickAdd,
  linkList,
  onDeleteLink,
}) {
  const [urlImage, setUrlImage] = useState([]);

  const header = HEADER;

  const [isLoading, setIsLoading] = useState(true);
  async function fetchkUrlImage() {
    await postApi
      .post("nova_sub_system/image_tag", {
        header: header,
        body: {
          url: linkUrl,
        },
      })
      .then((res) => {
        setUrlImage((prev) => [...prev, res.data.body.image]);
        console.log("image", res.data);
        setIsLoading(false);
      });
  }

  return (
    <div className={style["wrapper-container"]}>
      <div className={style["modal-container"]}>
        <div className={style["modal-title"]}>좌표 추가</div>
        <div className={style["link-box-container"]}>
          {linkList.length > 0 &&
            linkList.map((link, i) => {
              return (
                <div key={i} className={`${style["preview-container"]} ${style["link-box"]}`}>
                  <div
                    className={style["remove-icon"]}
                    onClick={() => {
                      onDeleteLink(i);
                    }}
                  >
                    <img src={close_icon} alt="remove" />
                  </div>
                  <div className={style["link_explain"]}>{link.explain}</div>
                  {/* <div>{link.url}</div> */}
                  <div className={style["preview-image"]}>
                    <img src={urlImage[i]} alt="img" />
                  </div>
                </div>
              );
            })}
        </div>

        <div className={style["link-input-container"]}>
          <div className={style["link-input"]}>
            <Input
              type="text"
              value={linkTitle}
              onChange={(e) => setLinkTitle(e.target.value)}
              placeholder="좌표 설명"
            />
            <Input
              type="url"
              value={linkUrl}
              onChange={(e) => setLinkUrl(e.target.value)}
              placeholder="이곳을 클릭해서 URL을 추가하세요"
            />
          </div>
          <button
            disabled={!(linkTitle && linkUrl)}
            className={style["add_link_button"]}
            onClick={() => {
              onClickAdd();
              fetchkUrlImage();
            }}
          >
            추가
          </button>
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
