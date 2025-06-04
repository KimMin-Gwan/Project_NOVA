import style from "./Footer.module.css";
import logo from "./../../img/footer-logo.svg";
export default function Footer() {
  return (
    <footer className={style.footer}>
      <div style={{marginBottom:"10px"}}>
        <img src={logo} alt="logo_Icon" className={style.logo_img} />
      </div>
      {/*<h4>팀 세상을 바꾸는 청년들</h4>*/}
      {/*<p className={style.nova_info}>경북 경산시 압량읍 압독2로1길 21, 1층 184</p>*/}
      {/*<p className={style.nova_info}>대표: 김민관 | 사업자등록번호: 000-00-00000</p>*/}
      <p className={style.nova_info}>대표: 김민관</p>
      { /*<p className={style.nova_info}>통신판매업신고번호: 0000-0000-000000</p> 
      <p className={style.nova_info}>
        전화번호: 010-9875-2508 | 이메일:youths0828@nova-platform.kr
      </p>
      */}
      <p className={style.nova_info}>
        이메일: youths0828@naver.com
      </p>
    </footer>
  );
}
