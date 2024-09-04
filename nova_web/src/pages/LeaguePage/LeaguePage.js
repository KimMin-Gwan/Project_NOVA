import style from './LeaguePage.module.css';

export default function LeaguePage() {

    const array = [1, 2, 3, 4, 5];

    return (
        <div className={style.container}>
            <div className={style.title}>리그 페이지</div>
            {
                array.map((box, i) => {
                    return (
                        <div className={style['league-box']} key={i}>
                            <h2>리그 이름</h2>
                            <div>최애 이름</div>
                            <div>포인트</div>
                            <div>이미지?</div>
                            <div>기타 등등</div>
                        </div>
                    )
                })
            }
        </div>
    )
}