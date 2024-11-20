import plus from "../../img/plus.png";
import empty_light from "../../img/empty_color.png";
import empty_dark from "../../img/empty_dark.png";
import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import SelectBias from "../selectBias/SelectBias";
import { getModeClass } from "./../../App.js";
function MySoloBias({ solo_bias, bias_url, showBox, blackBox, isError }) {
  let [selectWindow, setSelectWindow] = useState(false);
  let navigate = useNavigate();

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
      type: "solo",
    },
  };

  let url = "https://nova-platform.kr/";
  let [bias_data, setBiasData] = useState();

  // async function fetchCheckPoint() {
  //     const response = await fetch(url + `nova_check/server_info/check_page`, {
  //         method: 'post',
  //         headers: {
  //             "Content-Type": 'application/json',
  //         },
  //         credentials: 'include',
  //         body: JSON.stringify(send_data),
  //     });
  //     const data = await response.json();
  //     console.log('1414141',data.body);
  //     setBiasData(data.body);
  //     // .then(response => response.json())
  //     // .then(data => {
  //     //     // JSON.stringify(data)
  //     //     console.log(data.body)
  //     //     setBiasData(data.body)
  //     // });
  // };
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
              새로운 최애
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
      {solo_bias.bid === "" && (
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
              새로운 최애
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
      {solo_bias.bid && (
        <>
          <div className="image-container">
            <img src={bias_url + `${solo_bias.bid}.PNG`} alt="bias" className="img2" />
          </div>

          <div className="box">
            <div className="my-bias-solo">나의 최애</div>
            <div className="bias-name">{solo_bias.bname}</div>
          </div>
          {/* <div className='more' onClick={() => {
                        navigate(`/bias_info/user_contribution?bias_id=${solo_bias.bid}`)
                    }}>
                        <img src={more} alt=''></img>
                    </div> */}
        </>
      )}
    </div>
  );
}

export default MySoloBias;

// , {
//     // state: {
//     //     bias: bias_data.bias, result: bias_data.result, point: bias_data.point,
//     //     specialTime: bias_data.special_time
//     // }
// }
