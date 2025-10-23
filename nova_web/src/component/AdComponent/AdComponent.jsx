import { useRef, useState, useEffect } from "react";
import style from "./AdComponents.module.css";
import arrow from "./arrow.svg";

const AdComponent = ({ type }) => {
  const [nowWidth, setNowWidth] = useState(0);
  const frameRef = useRef(null);

  const sizeRules = {
    "image_32x60": { min: 200, max: 260 },
    "image_50x32": { min: 340, max: 460 },
    "link": { min: 340, max: 1020 },
  };

  useEffect(() => {
    if (!frameRef.current) return;

    const observer = new ResizeObserver((entries) => {
      for (let entry of entries) {
        setNowWidth(entry.contentRect.width);
      }
    });

    observer.observe(frameRef.current);

    return () => {
      observer.disconnect();
    };
  }, []);

  const rule = sizeRules[type] || { min: 0, max: "100%" };

  return (
    <div
      ref={frameRef}
      className={style["frame"]}
      style={{ maxWidth: rule.max }}
    >
      <div className={style["test-background"]}>
        {nowWidth >= rule.min ? (
          type === "image_32x60" ? (
            <ImageAd_32x60 />
          ) : type === "image_50x32" ? (
            <ImageAd_50x32 />
          ) : type === "link" ? (
            <LinkAd />
          ) : null
        ) : (
          <div style={{ width: "100%", height: "100%" }}></div>
        )}
      </div>
    </div>
  );
};


export default AdComponent;



export const ImageAd_32x60 = () => {
    const testURL1 = "https://hxb87ac312512.edge.naverncp.com/ad-default-2.png";
    const testURL2 = "https://hxb87ac312512.edge.naverncp.com/ad-default-3.png";
    const targetURL = "https://supernova.io.kr/submit_new";

    // 최초 렌더링 시 한 번만 랜덤 선택
    const [selectedURL] = useState(() =>
        Math.random() < 0.5 ? testURL1 : testURL2
    );

    return (
        <div className={style["image-32-60-frame"]}>
            <img
                className={style["image-iframe"]}
                src={selectedURL}
                frameBorder="0"
            />
            <div className={style["ad-desktop-top-tag-wrapper"]}>
                <div className={style["ad-desktop-left-tag"]}
                    onClick={() => window.open("https://naver.com", "_blank")}
                >AD</div>
                <div className={style["ad-desktop-right-tag"]}
                    onClick={() => window.open("https://naver.com", "_blank")}
                >광고 등록</div>
            </div>
            <div 
                className={style["ad-click-overlay"]}
                onClick={() => window.open(targetURL, "_blank")}
            />
        </div>
    );
}

export const ImageAd_50x32= () => {
    const testURL = "https://hxb87ac312512.edge.naverncp.com/ad-default-4.png";
    const targetURL = "https://supernova.io.kr";

    return (
        <div className={style["image-50-32-frame"]}>
            <img
                className={style["image-iframe"]}
                src={testURL}
                frameBorder="0"
            />
            <div className={style["ad-desktop-top-tag-wrapper"]}>
                <div className={style["ad-desktop-left-tag"]}
                    onClick={() => window.open("https://naver.com", "_blank")}
                >AD</div>
                <div className={style["ad-desktop-right-tag"]}
                    onClick={() => window.open("https://naver.com", "_blank")}
                >광고 등록</div>
            </div>
            <div 
                className={style["ad-click-overlay"]}
                onClick={() => window.open(targetURL, "_blank")}
            />
        </div>
    );
}

const sampleAd1 = {
    title : "SUPERNOVA 드디어 출시",
    detail : "생방송 일정 작성과 생방송 일정 탐색을 위한 유일무이한 공간! SUPERNOVA",
    _url : "https://supernova.io.kr/welcome"
}

const sampleAd2 = {
    title : "TEAM SUPERNOVA",
    detail : "스트리머와 팬들을 위한 특별한 공간을 만들어낸 대학생들. TEAM SUPERNOVA",
    _url : "https://projectsupernova.notion.site/"
}

const sampleAd3 = {
    title : "게임 및 방송 콘텐츠 홍보",
    detail : "이 위치에 게임 또는 방송 콘텐츠, 스트리머 등등 홍보를 할 수 있게 됩니다!!",
    _url : "https://supernova.io.kr/welcome"
}


export const LinkAd = () => {
  const sampleList = [sampleAd1, sampleAd2, sampleAd3];
  const [maxItems, setMaxItems] = useState(sampleList.length);

  useEffect(() => {
    const el = document.getElementById("link-container");
    if (el) {
      if (el.clientWidth > 600) {
        setMaxItems(sampleList.length); // 전체 다 보여줌
      } else {
        setMaxItems(2); // 2개만 보여줌
      }
    }
  }, []);

  return (
    <div id="link-container" className={style["link-60-14-frame"]}>
      <div className={style["ad-link-top-tag-wrapper"]}>
        <div
          className={style["ad-desktop-left-tag"]}
          onClick={() => window.open("https://naver.com", "_blank")}
        >
          파워링크
        </div>
        <div
          className={style["ad-desktop-right-tag"]}
          onClick={() => window.open("https://naver.com", "_blank")}
        >
          광고 등록
        </div>
      </div>

      <div className={style["link-ad-outer-frame"]}>
        <div className={style["link-ad-wrapper"]}>
          {sampleList.slice(0, maxItems).map((sample, index) => (
            <LinkComponent key={index} {...sample} />
          ))}
        </div>
      </div>
    </div>
  );
};



const LinkComponent = ({title, detail, _url}) => {
    return (
        <div className={style["link-component-wrapper"]}>
            <div className={style["link-component-detail-wrapper"]}>
                <div className={style["link-component-title"]}
                    onClick={() => window.open(_url, "_blank")}
                >
                    {title}
                </div>
                <div className={style["link-component-detail"]}
                    onClick={() => window.open(_url, "_blank")}
                >
                    {detail}
                </div>
            </div>
            <div className={style["link-component-direct-button-wrapper"]}
                onClick={() => window.open(_url, "_blank")}
            >
                <div className={style["link-component-direct-button"]}>
                    바로가기
                </div>
                <img src={arrow}/>
            </div>
        </div>
    );
}

