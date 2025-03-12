// 실시간 랭킹 받아오기
//   useEffect(() => {
//     fetchTagList();
//   }, []);
// const [currentIndex, setCurrentIndex] = useState(0); // 현재 표시 중인 태그 인덱스
// const intervalTime = 3000; // 2초마다 태그 변경
// let [biasId, setBiasId] = useState();

// 실시간 랭킹 동작(꺼놓음)
// useEffect(() => {
//   const timer = setInterval(() => {
//     setCurrentIndex((prevIndex) => {
//       const nextIndex = (prevIndex + 1) % tagList.length;
//       return nextIndex;
//     }, intervalTime);

//     return clearInterval(timer);
//   }, 3000);
//   return () => clearInterval(timer); // 컴포넌트 언마운트 시 타이머 정리
// });

{
  /* <section className="up-container">
                  <div>
                    <img src={upIcon} alt="급상승 해시태그" />
                    <h3>급상승 해시태그</h3>
                  </div>
                  <ul className="rt-ranking ">
                    {tagList.map((tag, i) => {
                      return (
                        <li
                          key={i}
                          style={{
                            display: i === currentIndex ? "flex" : "none",
                          }}
                        >
                          <p>{i + 1}</p>
                          {tag}
                        </li>
                      );
                    })}
                  </ul>
                </section> */
}

{
  /* <section className="search-category">
        <h3>실시간 트렌드</h3>

        <ul className="tag-list">
          {tagList.map((tag, i) => {
            return (
              <li
                key={i}
                onClick={() => {
                  onClickList(tag);
                }}
              >
                {tag}
              </li>
            );
          })}
        </ul>
      </section> */
}
