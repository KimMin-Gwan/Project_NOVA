import { useLocation, useNavigate } from "react-router-dom";
import  { useEffect, useState, useRef } from "react";
import style from "./Mypage.module.css";
import useLoginStore from "../../stores/LoginStore/useLoginStore";
import useBiasStore from "../../stores/BiasStore/useBiasStore";
import mainApi from "../../services/apis/mainApi";
import postApi from "../../services/apis/postApi";
import useMediaQuery from "@mui/material/useMediaQuery";
import DesktopLayout from "../../component/DesktopLayout/DeskTopLayout";
const user_icon= 'https://sgsryiav12510.edge.naverncp.com/user_profile.svg';

function MyPage() {
  const isMobile = useMediaQuery('(max-width:1100px)');
  const { tryLogin, tryLogout } = useLoginStore();
  const { fetchBiasList } = useBiasStore();
  let navigate = useNavigate();
  const location = useLocation();
  const [isUserState, setIsUserState] = useState(false);
  let [isLoading, setIsLoading] = useState(true);
  let [nickname, setNickname] = useState("");
  let [newNickname, setNewNickname] = useState("");
  let [password, setPassword] = useState("");
  let [newPassword, setNewPassword] = useState("");
  let [checkPassword, setCheckPassword] = useState("");
  let [myProfile, setMyProfile] = useState();

  const [isUploading, setIsUploading] = useState(false);
  const [image, setImage] = useState(null);
  const fileInputRef = useRef(null);
  const [imagePre, setImagePre] = useState(null);
  const [isVali, setIsVali] = useState(false);
  const [isValiPw, setIsValiPw] = useState(false);
  const [warningMessage, setWarningMessage] = useState(
    "영소문자, 숫자, 특수문자를 포함해 10자리 이상이어야 합니다."
  );
  const regexArray = [
    /^[a-zA-Z0-9가-힣]{2,6}$/, // 알파벳, 숫자, 한글만 허용, 2~6글자
    /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$/
  ];

  let header = {
    "request-type": "default",
    "client-version": "v1.0.1",
    "client-ip": "127.0.0.1",
    uid: "1234-abcd-5678",
    endpoint: "/core_system/",
  };

  async function fetchChangeNickname() {
    await postApi
      .post(`user_home/try_change_nickname`, {
        header: header,
        body: {
          uname: nickname,
        },
      })
      .then((res) => {
        if (res.data.body.result) {
          // setNewNickname(res.data.body.uname);
          alert(res.data.body.detail);
          setNewNickname(res.data.body.uname);
          setNickname("");
        } else {
          alert(res.data.body.detail);
        }
      });
  }

  async function fetchPasswordChange() {
    await postApi
      .post("user_home/try_change_password", {
        header: header,
        body: {
          password: password,
          new_password: newPassword,
        },
      })
      .then((res) => {
        if (!res.data.body.result) {
          alert(res.data.body.detail);
        } else {
          alert(res.data.body.detail);
          setPassword("");
          setNewPassword("");
          setCheckPassword("");
        }
      });
  }

  function onChangeInput(e, index) {
    handleVali(e, index);
    if (index === 0) {
      onChangeNickname(e);
    } else if (index === 1) {
      onChangeNewPassword(e);
    }
  }

  function onChangeNickname(e) {
    setNickname(e.target.value);
  }

  function onChangePassword(e) {
    setPassword(e.target.value);
  }
  function onChangeNewPassword(e) {
    setNewPassword(e.target.value);
  }
  function onChangecheckPassword(e) {
    setCheckPassword(e.target.value);
  }

  const handleVali = (e, index) => {
    var Regex = regexArray[index];

    if (!Regex.test(e.target.value)) {
      setWarningMessage("영소문자, 숫자, 특수문자를 포함해 8자리 이상이어야 합니다.");
      index === 0 ? setIsVali(true) : setIsValiPw(true);
    } else {
      index === 0 ? setIsVali(false) : setIsValiPw(false);
    }
  };

  const handleCheckPassWord = () => {
    if (newPassword === checkPassword) {
      setIsValiPw(false);
    } else {
      setWarningMessage("비밀번호가 같지 않습니다");
      setIsValiPw(true);
    }
  };

  useEffect(() => {


    handleCheckPassWord();
  }, [checkPassword]);

  const handleLogout = (e) => {
    tryLogin("");

    e.preventDefault();
    fetch("https://supernova.io.kr/user_home/try_logout", {
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
        navigate("/");
        fetchBiasList();
        localStorage.removeItem("history");
      })
      .catch((error) => {
        console.error("Logout error:", error);
      });
  };

  async function fetchEditProfile() {
    await fetch("https://supernova.io.kr/user_home/get_my_profile_data", {
      credentials: "include",
    })
      .then((res) => res.json())
      .then((data) => {
        setMyProfile(data.body);
        setIsLoading(false);
        setNewNickname(data.body.uname);
      });
  }

  const handleValidCheck = async () => {
    mainApi.get("https://supernova.io.kr/home/is_valid?only_token=n").then((res) => {
        if (res.status === 200) {
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

  useEffect(() => {
    if (!isUserState) {
      handleValidCheck();
    }else{
      fetchEditProfile();
    }
  }, [isUserState]);

  if (isLoading) {
    return <div>loading...</div>;
  }

  const profile = `https://sgsryiav12510.edge.naverncp.com/${myProfile.uid}.png`;


  const handleFileChange = async (event) => {
    const formData = new FormData();
    const file = event.target.files[0];
    formData.append("image", file);

    if (file) {
      const imageUrl = URL.createObjectURL(file);
      setImage(imageUrl);
    }

    await fetch("https://supernova.io.kr/user_home/try_change_profile_photo", {
      method: "POST",
      credentials: "include",
      body: formData,
    })
      .then((res) => {
        res.json();
      })
      .then((data) => {
        alert("완료");
      })
      .catch((error) => {
        alert("실패");
      });
  };

  const handleWithdrawal = () => {
    alert("회원 탈퇴를 하더라도 게시글과 콘텐츠는 삭제되지 않습니다.");
    if (window.confirm("화원 탈퇴를 진행하시겠습니까?")) {
      if (window.confirm("회원 탈퇴를 진행하면 이미 작성한 게시글과 콘텐츠를 더 이상 수정하거나 삭제할 수 없습니다. 탈퇴를 계속 진행하시겠습니까?")){
        mainApi.get("user_home/try_resign").then((res) => {
          if (res.data.result) {
            alert("슈퍼노바를 이용해 주셔서 진심으로 감사드립니다. 다시 만날 수 있기를 바랍니다.")
            navigate("/");
          }
        });
      }
    } else {
      return null;
    }
  };

  const handlePreview = (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.readAsDataURL(file);

    return new Promise((resolve) => {
      reader.onload = () => {
        setImagePre(reader.result || null);
        resolve();
      };
    });
  };

  const handleButtonClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };



  if (isMobile){
    return (
      <div className={`${style["container"]} ${style["edit-container"]}`}>

        {
          isUploading && (
            <div className={style["upload-feedback-background"]}>
              <div className={style["upload-feedback"]}>
                업로드 중입니다.
              </div>
            </div>
          )
        }

        <div className={style.top_area}>
          <p
            className={style.backword}
            onClick={() => {
              navigate("/");
            }}
          >
            뒤로
          </p>
        </div>
        <section className={style["profile-section"]}>
          <div className={style["user-img-edit"]}>
            <img
              src={image ? image : profile}
              alt="profile"
              onError={(e) => (e.target.src = user_icon)}
            />
          </div>
          <button onClick={handleButtonClick}>
            <label htmlFor="profileImg">프로필 이미지 변경</label>
            <input
              type="file"
              accept="image/*"
              ref={fileInputRef}
              onChange={async(e) => {
                setIsUploading(true);
                await handleFileChange(e);
                await handlePreview(e);
                setIsUploading(false);
              }}
            />
          </button>
        </section>

        <section className={style["profile-info"]}>
          <h3>프로필 정보</h3>
          <p className={style["input-name"]}>닉네임</p>
          <div className={style["user-name-input"]}>
            <input
              className={style["input-st"]}
              type="text"
              value={nickname}
              onChange={(e) => {
                onChangeInput(e, 0);
              }}
              placeholder={`${newNickname} (7글자 이내로 변경 가능합니다)`}
              minLength={2}
              maxLength={7}
            />
            <button
              className={style["change-button"]}
              onClick={(e) => {
                isVali ? alert("올바르게 입력하세요") : fetchChangeNickname();
              }}
            >
              변경
            </button>
          </div>

          {isVali && (
            <span className={style["warning-message"]}>
              2글자 이상 7글자 미만으로 하고, 특수문자 사용 금지
            </span>
          )}
          <p className={style["input-name"]}> 비밀번호 변경</p>
          <div className={style["pw-change"]}>
            <input
              className={style["input-st"]}
              type="text"
              value={password}
              onChange={(e) => {
                onChangePassword(e);
              }}
              placeholder="기존 비밀번호"
            />
            <input
              className={style["input-st"]}
              value={newPassword}
              onChange={(e) => {
                onChangeInput(e, 1);
              }}
              type="text"
              placeholder="새로운 비밀번호"
            />
            <input
              className={style["input-st"]}
              value={checkPassword}
              onChange={(e) => {
                onChangecheckPassword(e);
              }}
              type="text"
              placeholder="비밀번호 확인"
            />

            {isValiPw && (
              <span className={`${style["warning-message"]} ${style["pw-st"]}`}>
                {warningMessage}
              </span>
            )}
            <button
              className={style["change-button"]}
              onClick={() => {
                isValiPw ? alert("비밀번호를 올바르게 입력하세요") : fetchPasswordChange();
              }}
            >
              변경
            </button>
          </div>
        </section>

        <section className={style["user-info"]}>
          <h3>개인정보</h3>
          <p className={style["input-name"]}>uid</p>
          <input
            className={style["input-st"]}
            type="text"
            placeholder={myProfile.uid}
            readOnly
            tabIndex="-1"
          />
          <p className={style["input-name"]}>email</p>
          <input
            className={style["input-st"]}
            type="text"
            placeholder={myProfile.email}
            readOnly
            tabIndex="-1"
          />
          <p className={style["input-name"]}>태어난 해</p>
          <input
            className={style["input-st"]}
            type="text"
            placeholder={`${myProfile.birth_year}년`}
            readOnly
            tabIndex="-1"
          />
          <p className={style["input-name"]}>성별</p>
          <input
            className={style["input-st"]}
            type="text"
            placeholder={`${myProfile.gender}`}
            readOnly
            tabIndex="-1"
          />
        </section>
        <button className={`${style["logout_box"]}`} onClick={handleLogout}>
          로그아웃
        </button>
        <div style={{height: "130px"}}>
        </div>
        <button className={style["withdrawal_button"]} onClick={handleWithdrawal}>
          회원 탈퇴
        </button>
      </div>
    );
  }else{
    return(
    <DesktopLayout>
      <div className={`${style["container"]} ${style["edit-container"]}`}>
          {
            isUploading && (
              <div className={style["upload-feedback-background"]}>
                <div className={style["upload-feedback2"]}>
                  업로드 중입니다.
                </div>
              </div>
            )
          }

        <div className={style.top_area}>
          <p
            className={style.backword}
            onClick={() => {
              navigate("/");
            }}
          >
            뒤로
          </p>
        </div>
        <section className={style["profile-section"]}>
          <div className={style["user-img-edit"]}>
            <img
              src={image ? image : profile}
              alt="profile"
              onError={(e) => (e.target.src = user_icon)}
            />
          </div>
          <button onClick={handleButtonClick}>
            <label htmlFor="profileImg">프로필 이미지 변경</label>
            <input
              type="file"
              accept="image/*"
              ref={fileInputRef}
              onChange={async(e) => {
                setIsUploading(true);
                await handleFileChange(e);
                await handlePreview(e);
                setIsUploading(false);
              }}
            />
          </button>
        </section>

        <section className={style["profile-info"]}>
          <h3>프로필 정보</h3>
          <p className={style["input-name"]}>닉네임</p>
          <div className={style["user-name-input"]}>
            <input
              className={style["input-st"]}
              type="text"
              value={nickname}
              onChange={(e) => {
                onChangeInput(e, 0);
              }}
              placeholder={`${newNickname} (7글자 이내로 변경 가능합니다)`}
              minLength={2}
              maxLength={7}
            />
            <button
              className={style["change-button"]}
              onClick={(e) => {
                isVali ? alert("올바르게 입력하세요") : fetchChangeNickname();
              }}
            >
              변경
            </button>
          </div>

          {isVali && (
            <span className={style["warning-message"]}>
              2글자 이상 7글자 미만으로 하고, 특수문자 사용 금지
            </span>
          )}
          <p className={style["input-name"]}> 비밀번호 변경</p>
          <div className={style["pw-change"]}>
            <input
              className={style["input-st"]}
              type="text"
              value={password}
              onChange={(e) => {
                onChangePassword(e);
              }}
              placeholder="기존 비밀번호"
            />
            <input
              className={style["input-st"]}
              value={newPassword}
              onChange={(e) => {
                onChangeInput(e, 1);
              }}
              type="text"
              placeholder="새로운 비밀번호"
            />
            <input
              className={style["input-st"]}
              value={checkPassword}
              onChange={(e) => {
                onChangecheckPassword(e);
              }}
              type="text"
              placeholder="비밀번호 확인"
            />

            {isValiPw && (
              <span className={`${style["warning-message"]} ${style["pw-st"]}`}>
                {warningMessage}
              </span>
            )}
            <button
              className={style["change-button"]}
              onClick={() => {
                isValiPw ? alert("비밀번호를 올바르게 입력하세요") : fetchPasswordChange();
              }}
            >
              변경
            </button>
          </div>
        </section>

        <section className={style["user-info"]}>
          <h3>개인정보</h3>
          <p className={style["input-name"]}>uid</p>
          <input
            className={style["input-st"]}
            type="text"
            placeholder={myProfile.uid}
            readOnly
            tabIndex="-1"
          />
          <p className={style["input-name"]}>email</p>
          <input
            className={style["input-st"]}
            type="text"
            placeholder={myProfile.email}
            readOnly
            tabIndex="-1"
          />
          <p className={style["input-name"]}>태어난 해</p>
          <input
            className={style["input-st"]}
            type="text"
            placeholder={`${myProfile.birth_year}년`}
            readOnly
            tabIndex="-1"
          />
          <p className={style["input-name"]}>성별</p>
          <input
            className={style["input-st"]}
            type="text"
            placeholder={`${myProfile.gender}`}
            readOnly
            tabIndex="-1"
          />
        </section>
        <button className={`${style["logout_box"]}`} onClick={handleLogout}>
          로그아웃
        </button>
        <div style={{height: "130px"}}>

        </div>
        <button className={style["withdrawal_button"]} onClick={handleWithdrawal}>
          회원 탈퇴
        </button>
      </div>
    </DesktopLayout>
    );
  }


}

export default MyPage;
