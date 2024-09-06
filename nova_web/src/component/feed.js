import style from './../pages/FeedPage/FeedPage.module.css';

export default function Feed() {

    const array = [1, 2, 3, 4, 5, 6];

    return (
        <>
            {
                array.map((a, i) => {
                    return (
                        <div className={style.feed} key={i}>피드</div>
                    )
                })
            }
        </>
    )
} 