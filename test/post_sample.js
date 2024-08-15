import React, { useState } from 'react';

function PostRequestExample() {
    const [responseData, setResponseData] = useState(null);

    const handlePostRequest = async () => {
        const url = 'http://127.0.0.1:6000/login'; // 요청할 URL
        const data = { token: '토큰 정보' }; // 전송할 데이터

        try {
            const response = await fetch(url, {
                method: 'POST', // 요청 방식을 POST로 지정
                headers: {
                    'Content-Type': 'application/json', // JSON 데이터를 전송할 때 헤더 설정
                },
                body: JSON.stringify(data), // 데이터를 JSON 문자열로 변환하여 전송
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const result = await response.json(); // 서버의 응답을 JSON으로 변환
            setResponseData(result); // 응답 데이터를 상태로 저장
        } catch (error) {
            console.error('There was an error!', error);
        }
    };

    return (
        <div>
            <button onClick={handlePostRequest}>Send POST Request</button>
            {responseData && <div>Response: {JSON.stringify(responseData)}</div>}
        </div>
    );
}

export default PostRequestExample;
