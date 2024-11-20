import plus from "../../img/plus.png";
import empty_light from "../../img/empty_color.png";
import empty_dark from "../../img/empty_dark.png";
import more from "../../img/more.png";
import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import SelectBias from "../selectBias/SelectBias";
import { getModeClass } from "./../../App.js";
function MyGroupBias({ group_bias, bias_url, isError }) {
  let navigate = useNavigate();
  let [selectWindow, setSelectWindow] = useState(false);

  function showSelectModal() {
    setSelectWindow(!selectWindow);
  }

  let header = {
    "request-type": "default",
    "client-version": "v1.0.1",
    "client-ip": "127.0.0.1",
    uid: "1234-abcd-5678",
    endpoint: "/user_system/",
  };

  let send_data = {
    header: header,
    body: {
      // 'token': token,
      type: "group",
    },
  };

  let url = "https://nova-platform.kr/";
  let [bias_data, setBiasData] = useState();
  const [mode, setMode] = useState("bright");

  useEffect(() => {
    const storedMode = localStorage.getItem("brightMode");
    if (storedMode) {
      setMode(storedMode);
    }
  }, []);

  const empty = mode === "dark" ? empty_dark : empty_light;
  return (
    <div className="left-box">
      {isError && (
        <>
          <img
            src={empty}
            alt=""
            onClick={() => {
              alert("로그인해주세요");
            }}
          ></img>
          <div className="box">
            <div className={`my-bias-group ${getModeClass(mode)}`}>
              새로운 차애
              <br />
              지지하기
            </div>
          </div>
          {!selectWindow && (
            <div
              className="more"
              onClick={() => {
                alert("로그인해주세요");
              }}
            >
              <img src={plus} alt=""></img>
            </div>
          )}
          {selectWindow && <SelectBias selectWindow={selectWindow} setSelectWindow={setSelectWindow}></SelectBias>}
        </>
      )}
      {group_bias.bid === "" && (
        <>
          <img
            src={empty}
            alt=""
            onClick={() => {
              showSelectModal();
            }}
          ></img>
          <div className="box">
            <div className="my-bias-group">
              새로운 차애
              <br />
              지지하기
            </div>
          </div>
          {!selectWindow && (
            <div
              className="more"
              onClick={() => {
                showSelectModal();
              }}
            >
              <img src={plus} alt=""></img>
            </div>
          )}
          {selectWindow && <SelectBias selectWindow={selectWindow} setSelectWindow={setSelectWindow}></SelectBias>}
        </>
      )}
      {group_bias.bid && (
        <>
          <div className="image-container">
            <img src={bias_url + `${group_bias.bid}.PNG`} alt="bias" className="img2" />
          </div>
          <div className="box">
            <div className="my-bias-solo">나의 차애</div>
            <div className="bias-name">{group_bias.bname}</div>
          </div>
          {/* <div className='more'>
                        <img src={more}></img>
                    </div> */}
        </>
      )}
    </div>
  );
}

export default MyGroupBias;
