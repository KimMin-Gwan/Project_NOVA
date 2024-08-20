import "./Login.css";
import back from "../img/back.png";
import naverBtn from "./../img/naver.png";

function generateStateString() {
  return [...Array(30)].map(() => Math.random().toString(36)[2]).join("");
}

function Login() {
  const CLIENT_ID = "U613plVglLseinfMi35E";
  const REDIRECT_URI = encodeURIComponent("nova-platform.kr");
  const STATE_STRING = generateStateString();

  localStorage.setItem("oauth_state", STATE_STRING);

  const naverLoginUrl = `https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&state=${STATE_STRING}`;

  return (
    <div className="Login">
      <div className="Header">
        <div className="BackBtn">
          <button>
            <img src={back} alt="Back"></img>
          </button>
        </div>
        <div className="Top">
          <h3>로그인/회원가입</h3>
        </div>
      </div>
      <h2>
        로그인하고 최애를 응원하는
        <br />
        지지자가 되어주세요!
      </h2>

      <div className="naverBtn">
        <a href={naverLoginUrl}>
          <img src={naverBtn} alt="네이버 로그인 버튼"></img>
        </a>
      </div>
    </div>
  );
}

export default Login;
