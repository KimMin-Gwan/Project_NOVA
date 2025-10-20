import { useState, useEffect, useRef } from "react";
import useMediaQuery from '@mui/material/useMediaQuery';
import { useLocation, useNavigate, useParams, useSearchParams} from "react-router-dom";
import style from "./WriteFeed.module.css";
import style2 from "./WriteDesktop.module.css";

import tag from "./../../img/tag.svg";
import add_icon from "./../../img/add.svg";
import close_icon from "./../../img/close.svg";
import img_icon from "./../../img/image.png";
import link_icon from "./../../img/link.png";
import EditorBox from "../../component/EditorBox.js";
import postApi from "../../services/apis/postApi.js";
import useBiasStore from "../../stores/BiasStore/useBiasStore.js";
import HEADER from "../../constant/header.js";
import toast, { Toaster } from "react-hot-toast";
import DropDown from "../../component/DropDown/DropDown.js";
import Input from "../../component/Input/Input.js";
import Button from "../../component/Button/Button.js";
import mainApi from "../../services/apis/mainApi.js";
import DesktopLayout from "../../component/DesktopLayout/DeskTopLayout.jsx";
import { DesktopBiasSelectSectionPlus } from "../ScheduleMakePage/DesktopBiasSelector.jsx";
import SelectCategoryComponent from "./SelectCategoryComponent.jsx";
import feedApi from "../../services/apis/feedApi.js";

const categoryData = [
  { key: 2, category: "후기" },
  { key: 0, category: "자유게시판" },
  { key: 1, category: "아트" },
];

const Write = () => {
  const isMobile = useMediaQuery('(max-width:1100px)');
  const param = useParams();
  const [searchParams] = useSearchParams();

  const targetFid =  searchParams.get("fid");
  const targetTitle = searchParams.get("title");
  const targetBias  = searchParams.get("bias");
  const targetName = searchParams.get("biasName")
  const [isUploading, setIsUploading] = useState(false);

  const navigate = useNavigate();
  const editorRef = useRef();
  const location = useLocation();

  let [showModal, setShowModal] = useState(false);
  let [showLinkModal, setShowLinkModal] = useState(false);
  let [linkTitle, setLinkTitle] = useState("");
  let [linkUrl, setLinkUrl] = useState("");
  let [linkList, setLinkList] = useState([]);
  let [longData, setLongData] = useState();
  let [initialValue, setInitialValue] = useState("");
  let [user, setUser] = useState("");
  let [category, setCategory] = useState("선택 없음");

  let [biasId, setBiasId] = useState();
  let [tagList, setTagList] = useState([]);
  let { biasList, loading, fetchBiasList } = useBiasStore();


  function onClickModal() {
    setShowModal(!showModal);
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
    mainApi.get("https://supernova.io.kr/home/is_valid?only_token=n").then((res) => {
        if (res.status === 200) {
          setUser(res.data.body.user);
          setIsUserState(true);
        } else {
          if (window.confirm("로그인이 필요합니다.")){
            navigate("/novalogin", { state: { from: location.pathname } });
          }else{
            navigate("/");
          }
          setIsUserState(false);
        }
        return 
      })
      .catch((error) => {
        if (error.response.status == 401){
          if (window.confirm("로그인이 필요합니다.")){
            navigate("/novalogin", { state: { from: location.pathname } });
          }else{
            navigate("/");
          }
          setIsUserState(false);
        }
        setIsUserState(false);
      });
  }

  async function fetchFeed() {
    await mainApi.get(`feed_explore/feed_detail/feed_data?fid=${targetFid}`).then((res) => {
      if (res.data.body.feed[0].uid !== user) {
        alert("잘못된 접근입니다.");
        navigate("/");
      }
      setTagList(res.data.body.feed[0].hashtag);
      setLinkList(res.data.body.links);
      setCategory(res.data.body.feed[0].board_type);
      setBiasId(res.data.body.feed[0].bid);
      setLinkList(res.data.body.links)
    });
    await fetchBodyData(targetFid)
  }

  const fetchBodyData = async (fid) => {
    try {
      const res = await feedApi.get(fid);
      if (res.status === 200) {
        setInitialValue(res.data);
      }

    } catch (err) {
      //console.error("요청 에러:", err);

      // CORS 에러인 경우
      if (err.message === "Network Error") {
        alert("본문 내용을 불러오는데 실패했습니다.")
      }
    }
  };

  useEffect(() => {
    handleValidCheck();
  }, []);

  useEffect(() => {
    if (user){
      fetchBiasList();
    }

    if (user && targetFid){
      fetchFeed();
    }

    if (user && targetTitle && targetBias && targetName){
      setTagList((prev)=>
        [
          ...prev,
          "후기",
          targetTitle,
          targetName
        ]
      )
    }
  }, [user]);

  useEffect(()=>{
    if (biasList.length > 0){
      if (biasList.some(bias => bias.bid === targetBias)) {
        setBiasId(targetBias);
      }
    }
  }, [biasList])


  // 에디터 내용 관찰
  useEffect(() => {
    const editorElement = editorRef.current?.editorInst?.rootEl;

    if (!editorElement) return;

    const observer = new MutationObserver(() => {
      // 현재 에디터의 이미지 목록 가져오기
      const currentImages = Array.from(editorElement.querySelectorAll("img")).map(
        (img) => img.getAttribute("src")
      );

      // imagePreview에서 없는 이미지 제거
      setImagePreview((prevUrls) =>
        prevUrls.filter((url) => currentImages.includes(url))
      );
    });

    // 에디터 DOM의 변화를 관찰
    observer.observe(editorElement, { childList: true, subtree: true });

    return () => observer.disconnect();
  }, []);

  const [imagePreview, setImagePreview] = useState([]);
  const [imageFiles, setImageFiles] = useState([]);
  let [inputTagCount, setInputTagCount] = useState(0); //글자수
  let [numLink, setNumLink] = useState(0);

  function onClickAddLink() {
    setNumLink(numLink + 1);
    let newLink = { explain: linkTitle, url: linkUrl };
    setLinkList([...linkList, newLink]);
    setLinkTitle("");
    setLinkUrl("");
  }


  const handleFileChange = (event) => {
    const files = Array.from(event.target.files);
    // 유효한 이미지 파일 필터링
    const validFiles = files.filter((file) => file.type.startsWith("image/"));

    if (validFiles.length < files.length) {
      alert("이미지 파일만 가능합니다.");
    }

    const editorInstance = editorRef.current?.getInstance();

    validFiles.forEach((file) => {
      const reader = new FileReader();
      reader.onload = () => {
        const base64Image = reader.result;
        const imgTag = `<img src="${base64Image}" alt="Uploaded Image" style="max-width: 100%;">`;

        // 현재 HTML 가져오기
        const currentHtml = editorInstance?.getHTML() || "";
        // 새로운 HTML 삽입
        editorInstance?.setHTML(currentHtml + imgTag);
      };
      reader.readAsDataURL(file);
    });

  };

  const handleSubmit = async (event) => {
    event.preventDefault(); // 기본 동작을 막음 (중요)

    const editorInstance = editorRef.current?.getInstance();
    const currentHtml = editorInstance?.getHTML() || "";
    if (currentHtml == "<p><br></p>"){
      alert("본문이 비었습니다.")
      return;
    }

    const send_data = {
      header: header,
      body: {
        body: longData, // 입력된 글 본문 반영
        fid: targetFid || "",
        hashtag: tagList,
        link: linkList,
        bid: biasId,
        category: category
      },
    };

    const formData = new FormData();
    if (imageFiles) {
      for (let file of imageFiles) {
        formData.append("images", file); // "images" 키로 여러 파일 추가
      }
    }
    formData.append("jsonData", JSON.stringify(send_data)); // JSON 데이터 추가

    await fetch("https://supernova.io.kr/feed_explore/try_edit_feed", {
      method: "POST",
      credentials: "include",
      body: formData,
    })
      .then((response) => {
        response.json();
      })
      .then(() => {
        toast.success("업로드가 완료되었습니다.");
        navigate("/");
      })
      .catch((error) => {
        toast.error("업로드 실패!");
      });

  };


  function onDeleteLink(i) {
    setLinkList((prev) => prev.filter((_, index) => index !== i));
  }

  let [inputTag, setInputTag] = useState("");

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
      if (inputTag && inputTagCount <= 30) {
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
    if (inputTag && inputTagCount <= 30) {
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


  function onClickUpload() {
    if (!isUserState) {
      alert("로그인이 필요합니다.");
      navigate("/nova_login");
    }
  }

  const handleSelectBias = (bias) =>{
    setBiasId(bias.bid);
  }

  if (isMobile){
    return (
      // <form onSubmit={handleSubmit}>
      <div className={style["WriteFeed"]}>
        <Toaster />
        <div className={style["top_container"]}>
          <p
            className={style["buttons"]}
            onClick={() => {
              navigate('/');
            }}
          >
            취소
          </p>
          <span className={style["page-title"]}>게시글 작성</span>

          <p
            className={style["fake-buttons"]}
          >
          </p>
        </div>

        <section className={style["Select_container"]}>
          <div className={style["section_title"]}>주제 선택</div>
          <DropDown biasId={biasId} options={biasList} setBiasId={setBiasId} />

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
          <DropDown category={category} options={categoryData} setCategory={setCategory} />
        </section>

        <div className={style["hashtag_container"]}>
          <div className={style["section_title"]}>해시태그</div>
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
        </div>

        <div className={style["content_container"]}>
          <EditorBox setLongData={setLongData} editorRef={editorRef} initialValue={initialValue}/>
        </div>

        <p className={style["alert_message"]}>
          작성 규정을 위반한 게시글은 경고 없이 삭제 될 수 있습니다.
        </p>
        
        
        <div className={style["submit-button-wrapper"]}>
          <div className={style["submit-button"]}
            type="submit"
            onClick={async (e) => {
              e.preventDefault();
              e.stopPropagation();
              setIsUploading(true);
              onClickUpload();
              await handleSubmit(e);
              setIsUploading(false);
            }}
          >
            게시하기
          </div>
        </div>

        {
          isUploading && (
            <div className={style["upload-feedback-background"]}>
              <div className={style["upload-feedback"]}>
                업로드 중입니다.
              </div>
            </div>
          )
        }

        <div className={style["content_button"]}>
          <button
            onClick={(e) => {
              e.stopPropagation();
              onClickModal();
            }}
          >
            <img src={img_icon} alt="img" />
            이미지
          </button>
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
          />
        )}
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
    );

  }else{
    return (
      <DesktopLayout>
        <div className={style2["write-frame-desktop"]}>
          <div className={style2["write-frame-wrapper-desktop"]}>
            <div className={style["top_container"]}>
              <span className={style["page-title"]}>게시글 작성</span>
            </div>

            <div className={style2["write-option-wrapper"]}>
              <DesktopBiasSelectSectionPlus
                biasList={biasList}
                selectedBias={biasId}
                handleSelectBias={handleSelectBias}
              />
              <SelectCategoryComponent
                category={category}
                options={categoryData}
                setCategory={setCategory}
              />
            </div>

            <div className={style2["hashtag_container"]}>
              <div className={style2["section-title-wrapper"]}
                style={{marginBottom: "10px"}}
              >
                <div className={style2["section-title"]}>해시태그</div>
              </div>
              <div className={style["input-container"]}>
                <div className={style["input-wrapper"]}>
                  <input
                    placeholder="#해시태그"
                    type="text"
                    value={`${inputTag}`}
                    onChange={onChangeTag}
                    onKeyDown={onKeyDown}
                    className={style2["input-hashtag"]}
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
                    <div className={style2["tag-box"]} key={i}>
                      #{tag}
                      <button onClick={() => onDeleteTag(i)} className={style["delete-tag"]}>
                        &times; {/* 삭제 아이콘 */}
                      </button>
                    </div>
                  ))}
              </div>
            </div>

            <div className={style2["content_container"]}
            >
              <div className={style2["section-title-wrapper"]}
                style={{marginBottom: "10px"}}
              >
                <div className={style2["section-title"]}>본문</div>
              </div>
              <EditorBox setLongData={setLongData} editorRef={editorRef} initialValue={initialValue}/>
            </div>

            <p className={style2["alert-message"]}>
              작성 규정을 위반한 게시글은 경고 없이 삭제 될 수 있습니다.
            </p>

            <div className={style2["submit-button"]}
              type="submit"
              onClick={async (e) => {
                e.preventDefault();
                e.stopPropagation();
                setIsUploading(true);
                onClickUpload();
                await handleSubmit(e);
                setIsUploading(false);
              }}
            >
              게시하기
            </div>

            {
              isUploading && (
                <div className={style2["upload-feedback-background"]}>
                  <div className={style2["upload-feedback"]}>
                    업로드 중입니다.
                  </div>
                </div>
              )
            }


            <div className={style["content_button"]}>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onClickModal();
                }}
              >
                <img src={img_icon} alt="img" />
                이미지
              </button>
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
              />
            )}
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
          </div>
      </DesktopLayout>
    );
  }
};

export default Write;

export const Modal = ({
  onClickModal,
  handleFileChange,
}) => {
  return (
    <ModalWrapper title={"이미지 추가"}>
      <div className={style["image-container"]}>
        <ImageUploader handleFileChange={handleFileChange} />
      </div>

      <div className={style["modal-buttons"]}>
        <Button
          type={"apply"}
          onClick={() => {
            onClickModal();
          }}
        >
          닫기
        </Button>
      </div>
    </ModalWrapper>
  );
};


export function ImageUploader({ handleFileChange }) {
  return (
    <>
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
    </>
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
  const [isLoading, setIsLoading] = useState(true);

  async function fetchkUrlImage() {
    await postApi
      .post("nova_sub_system/image_tag", {
        header: HEADER,
        body: {
          url: linkUrl,
        },
      })
      .then((res) => {
        setUrlImage((prev) => [...prev, res.data.body.image]);
        setIsLoading(false);
      });
  }

  return (
    <ModalWrapper title={"좌표 추가"}>
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
        <Button type={"close"} onClick={onClickModal}>
          닫기
        </Button>
        <Button type={"apply"} onClick={onClickModal} disabled={linkList.length === 0}>
          적용
        </Button>
      </div>
    </ModalWrapper>
  );
}

export function ModalWrapper({ title, children }) {
  return (
    <div className={style["wrapper-container"]}>
      <div className={style["modal-container"]}>
        <div className={style["modal-title"]}>{title}</div>
        {children}
      </div>
    </div>
  );
}


