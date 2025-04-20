import style from "./Tabs.module.css";

export default function Tabs({ activeIndex, handleClick, onClickType }) {
  return (
    <section className={`${style["info-list"]} ${style["search-nav-bar"]}`}>
      <ul className={style["post-list"]} data-active-index={activeIndex}>
        {["게시글", "댓글", "일정", "일정 번들"].map((post, index) => (
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
