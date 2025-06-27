import React, { useEffect, useState, useRef } from 'react';

const ContentTestPage = () => {
    const socketRef = useRef(null);
    const [inputData, setInputData] = useState("");
    const [connectionStatus, setConnectionStatus] = useState('Disconnected');

    const handleInput = (e) => {
        const newInput = e.target.value;
        setInputData(newInput)
    };

    const handleNewAnswer = (e) =>{
        if (e.key === 'Enter') {
            tryAddComment();
        }
    }



    useEffect(() => {
        const initialize = async () => {
        try {

            // 2. fetchFeedComment 완료 후 WebSocket 초기화
            const socket = new WebSocket('wss://supernova.io.kr/testing_websocket')
            socketRef.current = socket;

            socket.onopen = () => {
            setConnectionStatus('Connected');
            };

            socket.onmessage = (event) => {
            analyzeMessage();
            };

            socket.onclose = () => {
            setConnectionStatus('Disconnected');
            };

            socket.onerror = (error) => {
            console.error('WebSocket error:', error);
            };



        } catch (error) {
            console.error('Error during initialization:', error);
        }
        }
        initialize(); 

        return () => {
        if (socketRef.current) {
            socketRef.current.close();
        }
        };

    }, []); // 필요한 의존성 추가


  function analyzeMessage() {
    const socket = socketRef.current; // Access the WebSocket instance directly
    if (!socket) {
      console.error('Socket is not initialized');
      return;
    }


    socket.send("pong");
    return;
  }
 

  const tryAddComment = () => {
    if (socketRef && inputData!== "") {
    const socket = socketRef.current; // Access the WebSocket instance directly
    const sanitizedCommentValue = inputData.replace(/<br>/g, '[br]');
    const inputMessage = `${sanitizedCommentValue}<br>add`; // 실제 메시지로 변경
    socket.send(inputMessage);
    setInputData(''); // 메시지 전송 후 입력 필드 초기화
    }
  }

  return(
      <div
          style={{
              width: "100%", height: "100%", backgroundColor:"#767676",
              display:"flex", alignItems:"center", justifyContent:"center"
          }}
      >
          <input
            value={inputData}
            style={{
                border: "2px solid #5c5c5c",
                width: "60%",
                height: "20%"
            }}
            type="text"
            onChange={(e) => {
                handleInput(e);
            }}
            onKeyDown={handleNewAnswer}
          >
          </input>
      </div>
  );
};


export default ContentTestPage;