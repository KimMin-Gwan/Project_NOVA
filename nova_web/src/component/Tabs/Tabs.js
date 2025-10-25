import style from "./Tabs.module.css";

export default function Tabs({ activeIndex, handleClick, onClickType }) {
  const tabElement = [
    "후기글",
    //"댓글",
    "콘텐츠"
  ]

  return (
    <section className={`${style["info-list"]} ${style["search-nav-bar"]}`}>
      <ul className={style["post-list"]} data-active-index={activeIndex}>
        {tabElement.map((post, index) => (
          <li
            key={index}
            className={`${style.post} ${activeIndex === index ? style.active : ""}`}
            onClick={() => {
              handleClick(index);
              onClickType(post);
            }}
          >
            <p>{post}</p>
          </li>
        ))}
      </ul>
    </section>
  );
}
