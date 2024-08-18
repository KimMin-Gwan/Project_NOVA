

function EmptyBias() {
    return (
        <div className='left-box'>
            <img src={empty}></img>
            {/* <div className='support'>지지하기</div> */}
            <div className='box'>
                <div className='my-bias-group'>새로운 최애 그룹<br />지지하기</div>
                {/* <div className='bias-name'>{bias.bname}</div> */}
            </div>
            <div className='more'>
                <img src={plus}></img>
            </div>
        </div>
    )
}

export default EmptyBias;