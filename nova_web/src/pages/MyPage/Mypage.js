import { useNavigate } from "react-router-dom";
import style from "./Mypage.module.css";
import backword from "./../../img/back_icon.png";

function MyPage() {
  let navigate = useNavigate();

  function handleMovePage(e, page) {
    e.preventDefault();
    navigate(page);
  }

  const handleLogout = (e) => {
    e.preventDefault();
    fetch("https://nova-platform.kr/user_home/try_logout", {
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
        console.log(data);
        navigate("/");
      })
      .catch((error) => {
        console.error("Logout error:", error);
      });
  };

  return (
    <div className={style.container}>
      <div className={style.top_area}>
        <p
          className={style.backword}
          onClick={() => {
            navigate(-1);
          }}
        >
          뒤로
        </p>
      </div>
      <div>이미지</div>
      <div>
        <section>
          <h3>사용자 이름</h3> <img src={backword} alt="" />
        </section>
        <section>
          <ul>
            <li>
              <p>23</p>
              <p>포스트</p>
            </li>
          </ul>
        </section>
        <section>
          <ul>
            <li>
              <p>23</p>
              <p>포스트</p>
            </li>
          </ul>
        </section>
      </div>
      <div className={`${style["logout_box"]}`} onClick={handleLogout} style={{ cursor: "pointer" }}>
        로그아웃
      </div>
    </div>
  );
}

export default MyPage;
