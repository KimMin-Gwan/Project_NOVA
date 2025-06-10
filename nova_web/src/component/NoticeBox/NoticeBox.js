import { useEffect, useState } from "react";
import "./index.css";
import NoticeItem from "./NoticeItem";

export default function NoticeBox() {
  let [isLoading, setIsLoading] = useState(true);
  let [noticeDatas, setNoticeDatas] = useState([]);

  async function fetchNoticeData() {
    await fetch("https://supernova.io.kr/nova_sub_system/sample_notice", {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        //console.log(data);
        setNoticeDatas(data.body.notice);
        setIsLoading(false);
      });
  }
  useEffect(() => {
    fetchNoticeData();
  }, []);

  return (
    <div className="NoticeBox">
      {noticeDatas.map((notice, i) => {
        return (
          <NoticeItem key={notice.nid} notice={notice} isLoading={isLoading} />
        );
      })}
    </div>
  );
}
