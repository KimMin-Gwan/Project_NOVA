import { useEffect, useState } from "react";
import MySoloBias from "../component/subscribeBias/mySoloBias";
import MyGroupBias from "../component/subscribeBias/myGroupBias";

function MyBias({ url, showBox, blackBox }) {
  let [solo_bias, setSoloBias] = useState([]);
  let [group_bias, setGroupBias] = useState([]);

  let solo_bias_copy = [];
  let group_bias_copy = [];

  let [supportBias, setSupportBias] = useState();
  let supportBiasCopy = [];

  // let header = {
  //     "request-type": "default",
  //     "client-version": 'v1.0.1',
  //     "client-ip": '127.0.0.1',
  //     "uid": '1234-abcd-5678',
  //     "endpoint": "/core_system/",
  // }

  // let send_data = {
  //     "header": header,
  //     "body": {
  //         'token': token
  //     }
  // }
  let [isError, setIsError] = useState();

  let my_bias_url = "https://kr.object.ncloudstorage.com/nova-images/";

  useEffect(() => {
    fetch(url + "my_bias", {
      credentials: "include",
    })
      .then((response) => {
        if (!response.ok) {
          if (response.status === 401) {
            setIsError(response.status);
          } else {
            throw new Error(`status: ${response.status}`);
          }
        }
        return response.json();
      })
      .then((data) => {
        console.log("11", data);
        solo_bias_copy = data.body.bias_list;
        group_bias_copy = data.body.bias_list;

        setSoloBias(solo_bias_copy);
        setGroupBias(group_bias_copy);
        // console.log('솔로 그룹 바이어스 부분', data.body);
        // console.log('fasfa', data)
      })
      .catch((error) => {
        console.error("Fetch error:", error);
        // alert('데이터를 가져오는 중 오류가 발생했습니다. 다시 시도해 주세요.'); // 일반적인 에러 처리
      });
  }, []);

  return (
    <>
      <MySoloBias
        solo_bias={solo_bias}
        bias_url={my_bias_url}
        showBox={showBox}
        blackBox={blackBox}
        isError={isError}
      ></MySoloBias>
      <MyGroupBias
        group_bias={group_bias}
        bias_url={my_bias_url}
        showBox={showBox}
        blackBox={blackBox}
        isError={isError}
      ></MyGroupBias>
    </>
  );
}

export default MyBias;
