import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import style from "./../FeedPage/FeedPage.module.css";
import stylePlanet from "./../PlanetPage/Planet.module.css";
import backword from "./../../img/back_icon.png";

import back from "./../../img/write_vector1.png";
import select from "./../../img/select-icon.png";
import img from "./../../img/img-icon.png";
import { getModeClass } from "./../../App.js";
const WriteFeed = ({ brightmode }) => {
  const navigate = useNavigate();

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
  const [choice, setChoice] = useState(["", "", "", ""]); // 선택지 4개 상태로 저장
  // const [isClickedBtn, setIsClickedBtn] = useState('card'); // 버튼 클릭 상태
  let [inputTagCount, setInputTagCount] = useState(0); //글자수
  let [inputBodyCount, setInputBodyCount] = useState(0); //글자수
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
        body: bodyText, // 입력된 글 본문 반영
        fid: "",
        fclass: fclassName[currentFclass],
        choice: choice, // 4지선다 선택지 반영
        hashtag: tagList,
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
        console.log(data);
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
    <div className={`${style["test_container"]} ${style["container"]}`}>
      <div
        className={`${style["short_form"]} ${style["short_form_write"]} ${
          style[getModeClass(mode)]
        }`}
      >
        <div className={`${stylePlanet["top_area"]} ${style["top_bar_area"]}`}>
          <img
            src={backword}
            alt="Arrow"
            className={style.backword}
            onClick={() => {
              navigate(-1);
            }}
          />
          <p>새로운 이야기를 시작해요!</p>
        </div>

        <div className={`${style["write_container"]} ${style[getModeClass(mode)]}`}>
          <div className={`${style["input-area"]} ${style[getModeClass(mode)]}`}>
            <div className={style["boxbox"]}>
              <div className={style["hash-tag-area"]}>
                <div id={style["hashtag"]}>제목(해시태그)</div>

                <input
                  type="text"
                  value={`#${inputTag}`} // #이 붙은 상태로 보여줌
                  onChange={onChangeTag}
                  onKeyDown={onKeyDown}
                  className={style["write-tag"]}
                />
                <span className={style["count-text"]}>{inputTagCount}/12</span>
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
              </div>
            </div>
            <div className={style["text_body"]}>
              <div id={style["content"]}>본문</div>
              <textarea
                name="body"
                placeholder="내용을 입력해주세요"
                className={style["write_body"]}
                value={bodyText}
                onChange={onChangeBody} // 본문 내용 상태 업데이트
              ></textarea>
              <span className={style["count-text"]}>{inputBodyCount}/300</span>
            </div>
          </div>

          <form onSubmit={handleSubmit}>
            {/* <div className={`${style['write-image-box']}`}> */}
            {/* <div className={style['image-show']}> */}
            {/* <img src={back} alt="이미지" /> */}

            {/*모달 열기*/}
            <div className={`${style["click-icon"]} ${style[getModeClass(mode)]}`}>
              <div className={style["icon-box"]} onClick={handleImageModalOpen}>
                <img src={img} alt="이미지 편집" />
                <span>이미지 편집</span>
              </div>

              <div className={style["icon-box"]} onClick={handleChoiceModalOpen}>
                <img src={select} alt="선택지 편집" />
                <span>선택지 편집</span>
              </div>
            </div>

            {/* 이미지 편집 모달 */}
            <Modal show={showImageModal} closeModal={closeModal} title="이미지 편집">
              {/* 이미지 관련 편집 내용 */}
              <div className={`${style["write-image-box"]} ${style[getModeClass(mode)]}`}>
                <label className={style["upload_area"]} htmlFor={style["upload-file"]}>
                  {/* 업로드 */}
                  {imagePreview.length === 0 ? (
                    <div className={style["upload-text"]}>
                      <span>이미지 삽입</span>
                      <div>PNG, SVG, JPG, WEPG, GIF 등</div>
                    </div>
                  ) : (
                    imagePreview.map((preview, index) => {
                      return <img key={index} src={preview} alt={`preview ${index}`} />;
                    })
                  )}
                </label>
                <input
                  id={style["upload-file"]}
                  type="file"
                  accept="image/*"
                  multiple
                  onChange={handleFileChange}
                ></input>
              </div>
            </Modal>

            {/* 선택지 편집 모달 */}
            <Modal show={showChoiceModal} closeModal={closeModal} title="선택지 편집">
              {/* 선택지 편집 관련 내용 */}
              <div className={style["fclass_btn"]}>
                <img
                  className={style["order_btn"]}
                  src={back}
                  alt="prev"
                  onClick={handlePrev}
                ></img>
                <div className={style["fclass-box"]}>
                  {/* 4지선다 */}
                  {currentTitle === 1 && (
                    <MultipleWrite choice={choice} handleChoiceChange={handleChoiceChange} />
                  )}
                  {/* 둘 중 하나 */}
                  {currentTitle === 2 && <BalanceWrite handleChoiceChange={handleChoiceChange} />}
                  {/* 정거장 */}
                  {currentTitle === 3 && <StationWrite handleChoiceChange={handleChoiceChange} />}
                  {currentTitle === 0 && <CardWrite />}
                </div>
                <img
                  className={style["order_btn"]}
                  src={back}
                  alt="next"
                  onClick={handleNext}
                ></img>
              </div>
            </Modal>
            <hr className={`${style["line_write"]} ${style[getModeClass(mode)]}`}></hr>
            <div className={style["func_part"]}>
              <div className={style["btn_func_area"]}>
                <div className={style["btn_func"]}>
                  <label className={style["custom-checkbox"]}>
                    <input name="comment" type="checkbox"></input>댓글 허용
                  </label>
                  <label className={style["custom-checkbox"]}>
                    <input name="share" type="checkbox"></input>공유 허용
                  </label>
                </div>
                <button type="submit" className={style["upload-btn"]} onClick={onClickUpload}>
                  업로드
                </button>
              </div>
              <div className={style["warning_text"]}>
                타인에게 불편을 줄 수 있는 내용의 게시글은 경고 없이 삭제될 수 있습니다.
              </div>
            </div>
          </form>
        </div>
        <div className={style["empty-box"]}></div>
      </div>
    </div>
  );
};

export default WriteFeed;

function CardWrite() {
  const [mode, setMode] = useState(() => {
    return localStorage.getItem("brightMode") || "bright";
  });

  return (
    <div className={`${style["fclass-container"]} ${style[getModeClass(mode)]}`}>
      <div className={style["empathy-box"]} name="content">
        선택지 없음
      </div>
    </div>
  );
}
function MultipleWrite({ choice, handleChoiceChange }) {
  const [mode, setMode] = useState(() => {
    return localStorage.getItem("brightMode") || "bright";
  });
  return (
    <div className={`${style["one_of_four_area"]} ${style[getModeClass(mode)]}`}>
      <ol className={style["one_of_four_list"]}>
        {choice.map((ch, index) => (
          <li key={index}>
            <input
              name="select"
              value={ch}
              onChange={(e) => handleChoiceChange(index, e.target.value)}
              placeholder={`${index + 1}. 선택지${index + 1}`}
            ></input>
          </li>
        ))}
      </ol>
    </div>
  );
}
function BalanceWrite({ handleChoiceChange }) {
  const [mode, setMode] = useState(() => {
    return localStorage.getItem("brightMode") || "bright";
  });
  return (
    <div className={`${style["button_container"]} ${style[getModeClass(mode)]}`}>
      <input
        name="balance"
        maxLength={10}
        placeholder="버튼 내용"
        className={`${style["select_button"]} ${style["balance_btn"]}`}
        onChange={(e) => handleChoiceChange(0, e.target.value)}
      ></input>
      <input
        name="balance"
        maxLength={10}
        placeholder="버튼 내용"
        className={`${style["select_button"]} ${style["balance_btn"]}`}
        onChange={(e) => handleChoiceChange(1, e.target.value)}
      ></input>
    </div>
  );
}
function StationWrite({ handleChoiceChange }) {
  const [mode, setMode] = useState(() => {
    return localStorage.getItem("brightMode") || "bright";
  });
  return (
    <div className={`${style["station_container"]} ${style[getModeClass(mode)]}`}>
      <div className={style["station_box"]}>
        <input
          name="site_name"
          type="text"
          className={style["site_name"]}
          placeholder="사이트 이름"
          onChange={(e) => handleChoiceChange(0, e.target.value)}
        ></input>
        <input
          name="script"
          type="text"
          className={style["site_script"]}
          placeholder="설명"
          onChange={(e) => handleChoiceChange(1, e.target.value)}
        ></input>
        <input
          name="url"
          type="url"
          className={style["site_url"]}
          placeholder="url"
          onChange={(e) => handleChoiceChange(2, e.target.value)}
        ></input>
      </div>
    </div>
  );
}

const Modal = ({ show, closeModal, title, children }) => {
  const [mode, setMode] = useState(() => {
    return localStorage.getItem("brightMode") || "bright";
  });
  if (!show) return null;
  return (
    <div className={`${style["modal-overlay"]} ${style[getModeClass(mode)]}`} onClick={closeModal}>
      <div className={style["modal-content"]} onClick={(e) => e.stopPropagation()}>
        <p className={style["modal-title"]}>{title}</p>
        {children}
        <button onClick={closeModal}>닫기</button>
      </div>
    </div>
  );
};
