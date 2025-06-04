import { useNavigate } from "react-router-dom";
import logo2 from "../../img/logo2.png";
import logo3 from "../../img/logo3.svg";

export default function Header() {
  const navigate = useNavigate();

  return (
    <header className="header">
      <div
        className="logo"
        onClick={() => {
          navigate("/");
        }}
      >
        <img src={logo3} alt="logo" className={`logo-st `}></img>
      </div>
    </header>
  );
}
