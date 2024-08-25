import style from './nameCard.module.css';

function NameCard() {
    return (
        <div className="frame">
            <div className='title'>최애 인증하기</div>
            <div className='text-area'>
                <div>타이틀</div>
            </div>
            <div className='namecard-area'>
                <div className='namecard'>
                    <div className='img-area'>
                        <div className='bias-img'></div>
                    </div>
                    <div className='data-area'>
                        <div className='data'>이름</div>
                    </div>
                </div>
            </div>
            <div className='share-area'>공유 영역</div>
            <div className='ad-area'>광고</div>
        </div>
    )
}

export default NameCard;