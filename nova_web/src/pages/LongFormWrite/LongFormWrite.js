import { useEffect, useState } from "react";
import style from "./LongFormWrite.module.css";
import { useNavigate } from "react-router-dom";
import BiasBoxes from "../../component/BiasBoxes";
import { Editor } from "@toast-ui/react-editor";

import "@toast-ui/editor/dist/toastui-editor.css";
import EditorBox from "../../component/EditorBox";
import { LinkModal, Modal, VoteModal } from "../WriteFeed/WriteFeed";

export default function LongFormWrite() {
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
    setLinkTitle("");
    setLinkUrl("");
  }

  function onClickAdd() {
    setCreateOptions(createOptions + 1);
  }
  const handleFileChange = (event) => {
    // const selectedFile = event.target.files[0];
    const selectedFile = Array.from(event.target.files);
    const validFiles = selectedFile.filter((file) => file.type.startsWith("image/"));

    if (validFiles.length < selectedFile.length) {
      alert("이미지 파일만 가능");
    }

    setImageFiles(validFiles);

    const previewUrls = validFiles.map((file) => {
      return URL.createObjectURL(file);
    });

    setImagePreview(previewUrls);
    validFiles.forEach((file) => URL.revokeObjectURL(file));
  };

  const handleSubmit = (event) => {
    event.preventDefault(); // 기본 동작을 막음 (중요)

    const send_data = {
      header: header,
      body: {
        body: longData, // 입력된 글 본문 반영
        fid: "",
        fclass: "long",
        choice: choice, // 4지선다 선택지 반영
        hashtag: tagList,
        link: { lname: linkTitle, url: linkUrl },
        bid: biasId || "",
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
      // navigate(-1);
    } else {
      alert("로그인이 필요합니다.");
      navigate("/");
    }
  }
  return (
    <div className={style["WriteFeed"]}>
      <div className={style["top_container"]}>
        <p
          onClick={() => {
            navigate(-1);
          }}
        >
          취소
        </p>
        <p>롱 피드 작성</p>
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
      <div>
        <div>커뮤니티 선택</div>
        <BiasBoxes setBiasId={setBiasId} />
      </div>
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
            onClick={(e) => {
              e.stopPropagation();
            }}
          >
            확인
          </button>
        </div>
        <div className={style["tag-container"]}>
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
        <div>본문</div>
        <EditorBox setLongData={setLongData} />
        {/* <textarea
          className={style["write_body"]}
          name="body"
          placeholder="내용을 입력해주세요"
          value={bodyText}
          onChange={onChangeBody}
        /> */}
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
  );
}
