import React, { useState, useEffect } from 'react';
// import style from "../css/loundspeaker.module.css"
import '../css/speaker.css';
//import resetPageAndRunItemPage from 'ResetPageAndRunItemPage'
import speakerStar from '../img/speaker-star.png';

function Loundspeaker({ chattingData }) {
    //function App( itit_txt ) {
    const itit_txt = { text: "계약 만료일인 1월 31일 이후  파기하시면됩니다.계약 일 이후 3개월 이내에 파기하시면됩니다.", type: 'server-message' }
    const [messages, setMessages] = useState([itit_txt]);
    const [newMessage, setNewMessage] = useState('');
    const [socket, setSocket] = useState(null);
    // const state = { messages: [], newMessage : '' };
    const [showTitleAndButton, setShowTitleAndButton] = useState(true);

    // const [chattingData, setChattingData] = useState([]);
    // let chattingList = [];

    // useEffect(()=>{
    //     fetch('http://nova-platform.kr/chatting_list')
    //     .then(res=>res.json())
    //     .then(data=>{
    //         chattingList = [...data.body.chatting_list];
    //         setChattingData(chattingList);
    //         console.log(chattingData);
    //     })
    // },[])

    useEffect(() => {
        const newSocket = new WebSocket('ws://175.106.99.34/chatting'); // 서버 주소를 적절히 변경하세요

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
                        <div className='title-box'>
                            <div className='speaker-star'>
                                <img src={speakerStar} />
                            </div>
                            확성기
                            <div className='speaker-star'>
                                <img src={speakerStar} />
                            </div>
                        </div>
                        <div className='button-container'>
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
                            <button className='non-clicked-button'>사수자리</button>
                            <button className='non-clicked-button'>사수자리</button>
                        </div>

                        <div className="message-container">
                            <ul>
                                <li className={'message server-message'}>{messages[0].text}</li>
                                {chattingData.map((chat, index) => (
                                    <li key={chat.cid} className={'message server-message'}>
                                        {/* {message.text} */}
                                        {chat.content}
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