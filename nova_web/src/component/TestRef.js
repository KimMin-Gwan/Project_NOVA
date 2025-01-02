import { useEffect, useState } from "react";
import { useRef } from "react";

export default function TestRef() {
  let [tagList, setTagList] = useState([]);

  function fetchTagData() {
    fetch("https://nova-platform.kr/home/realtime_best_hashtag", {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        setTagList(data.body.hashtags);
      });
  }

  useEffect(() => {
    fetchTagData();
  }, []);

  // const [position, setPosition] = useState(0);
  // let [items, setItems] = useState([]);

  // useEffect(() => {
  //   const interval = setInterval(() => {
  //     setPosition((prevPosition) => prevPosition - 50); // 50px씩 위로 이동
  //   }, 2000); // 2초마다 실행

  //   return () => clearInterval(interval);
  // }, [position]);

  const ulRef = useRef(null);

  useEffect(() => {
    const interval = setInterval(() => {
      if (ulRef.current) {
        ulRef.current.style.transitionDuration = "400ms";
        ulRef.current.style.marginTop = "-50px";

        setTimeout(() => {
          if (ulRef.current) {
            ulRef.current.style.transitionDuration = "";
            ulRef.current.style.marginTop = "";
            // 첫 번째 요소를 400ms 후에 뒤로 보냅니다.
            ulRef.current.appendChild(ulRef.current.querySelector("li:first-child"));
          }
        }, 400);
      }
    }, 2000);

    return () => {
      clearInterval(interval);
    };
  }, []);

  return (
    <section>
      <ul ref={ulRef} className="test-box">
        {tagList.map((tag, i) => {
          return (
            <li
              className="test-container"
              key={i}
              // style={{ transform: `translateY(${position}px)` }}
            >
              {tag}
            </li>
          );
        })}
      </ul>
    </section>
  );
}
