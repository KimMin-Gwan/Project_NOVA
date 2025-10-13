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
    const testURL = "https://kr.object.ncloudstorage.com/nova-advertisement-image/%EB%8F%84%EB%A1%B1%ED%96%84%201.png";
    const targetURL = "https://supernova.io.kr";

    return (
        <div className={style["image-32-60-frame"]}>
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

export const ImageAd_50x32= () => {
    const testURL = "https://kr.object.ncloudstorage.com/nova-advertisement-image/Frame%201707482528%202.png";
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
    title : "액션 도트 로그라이크 게임 출시",
    detail : "LUNACY에서 만든 신작 액션 도트 로그라이크 출시 했는데 이름이 뭔지 몰라요...",
    _url : "https://supernova.io.kr"
}

const sampleAd2 = {
    title : "한결 단독 콘서트 결정",
    detail : "9월 27 - 9월 28일 서울랜드에서 아카이브 단독공연! [ OH! duck FESTIVAL ]",
    _url : "https://supernova.io.kr"
}

const sampleAd3 = {
    title : "별조각 게임 참여 광고주 모집",
    detail : "김루야가 운영하는 마크서버 별조각 게임의 인게임 내 광고를 해주실 광고주 모집",
    _url : "https://supernova.io.kr"
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

