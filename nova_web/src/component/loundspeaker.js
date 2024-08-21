import React, { useState, useEffect } from 'react';
// import style from "../css/loundspeaker.module.css"
import '../css/speaker.css';
//import resetPageAndRunItemPage from 'ResetPageAndRunItemPage'

function Loundspeaker() {
    //function App( itit_txt ) {
    const itit_txt = { text: "어떤 물건을 찾으러 오셨나요?", type: 'server-message' }
    const [messages, setMessages] = useState([itit_txt]);
    const [newMessage, setNewMessage] = useState('');
    const [socket, setSocket] = useState(null);
    // const state = { messages: [], newMessage : '' };
    const [showTitleAndButton, setShowTitleAndButton] = useState(true);

    useEffect(() => {
        const newSocket = new WebSocket('ws://127.0.0.1:4000/chatting'); // 서버 주소를 적절히 변경하세요

        newSocket.onopen = () => {
            console.log('WebSocket 연결 성공');
        };

        // 메시지 받는부분
        newSocket.onmessage = (event) => {
            setMessages((prevMessages) => {
                const newMessages = [...prevMessages, { text: event.data, type: 'server-message' }];
                return newMessages;
            });
        };

        setSocket(newSocket);
        return () => {
            //newSocket.close();
        };
    }, []);

    const handleSendMessage = () => {
        if (newMessage.trim() !== '' && socket) {
            // 메시지를 보낼 때 메시지를 WebSocket을 통해 전송
            socket.send(newMessage);
            // setMessages([...messages, { text: newMessage, type: 'user-message' }]);
            setNewMessage('');
        }
    };

    return (
        <div className='main-container'>
            <div className="container-speaker" onClick={(e) => { e.stopPropagation() }}>
                {showTitleAndButton && (
                    <div className="chat-messages">
                        <div className='title-box'>확성기</div>
                        <span className='button-container'>
                            <button className='clicked-button'>오리온자리</button>
                            <button className='non-clicked-button'>사수자리</button>
                            <button className='non-clicked-button'>사수자리</button>
                            <button className='non-clicked-button'>사수자리</button>
                            <button className='non-clicked-button'>사수자리</button>
                            <button className='non-clicked-button'>사수자리</button>
                            <button className='non-clicked-button'>사수자리</button>
                            <button className='non-clicked-button'>사수자리</button>
                            <button className='non-clicked-button'>사수자리</button>
                            <button className='non-clicked-button'>사수자리</button>
                        </span>

                        <div className="message-container">
                            <ul>
                                {messages.map((message, index) => (
                                    <li key={index} className={'message server-message'}>
                                        {message.text}
                                    </li>
                                ))}
                            </ul>
                        </div>
                        <div className="input-container">
                            <p>Text</p>
                            <input type="text" placeholder="텍스트를 입력해주세요" value={newMessage}
                                onChange={(e) => setNewMessage(e.target.value)}
                            />
                            <button className='clicked-button send-button' onClick={handleSendMessage}>알리기</button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );

}

export default Loundspeaker;