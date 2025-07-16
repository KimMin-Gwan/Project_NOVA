// src/hooks/useChzzkSocket.ts
import { useEffect, useRef } from "react";
import { io, Socket } from "socket.io-client";

interface UseChzzkSocketProps {
  sessionUrl: string; // 백엔드에서 받은 WebSocket URL
  channelId: string;  // 시청 중인 방송의 채널 ID
}

export default function useChzzkSocket({ sessionUrl, channelId }: UseChzzkSocketProps) {
  const socketRef = useRef<Socket | null>(null);

  useEffect(() => {
    if (!sessionUrl || !channelId) return;

    const socket = io(sessionUrl, {
      transports: ["websocket"],
      reconnection: false,
      timeout: 3000,
      forceNew: true,
    });

    socketRef.current = socket;

    socket.on("connect", () => {
      console.log("✅ 소켓 연결 성공");

      // 채널 구독 (chzzk 문서에 정의된 이벤트 명 따라야 함)
      socket.emit("subscribe", {
        channelId,
        sessionType: "user", // or "client" depending on session type
      });
    });

    socket.on("chat", (chatData) => {
      console.log("💬 채팅 수신:", chatData);
      // 여기에 채팅 state 업데이트 로직 연결 가능
    });

    socket.on("disconnect", () => {
      console.log("❌ 소켓 연결 종료됨");
    });

    return () => {
      socket.disconnect();
    };
  }, [sessionUrl, channelId]);
}
