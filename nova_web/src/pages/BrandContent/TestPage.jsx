import React, { useEffect, useRef } from 'react';

const YouTubePlayerWithControls = () => {
  const playerRef = useRef(null);

  useEffect(() => {
    // Load the IFrame Player API code asynchronously
    const tag = document.createElement('script');
    tag.src = 'https://www.youtube.com/iframe_api';
    const firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

    // Function to create a YouTube player after the API loads
    window.onYouTubeIframeAPIReady = () => {
      playerRef.current = new window.YT.Player('player', {
        height: '620',
        width: '980',
        videoId: '7y6XuryGHww', // Replace with your desired video ID
        playerVars: {
          autoplay: 0, // Prevent auto-play
          controls: 1,
          playsinline: 1,
        },
      });
    };

    return () => {
      if (playerRef.current) {
        playerRef.current.destroy();
      }
    };
  }, []);

  const playVideo = () => {
    if (playerRef.current) {
      playerRef.current.playVideo();
    }
  };

  const pauseVideo = () => {
    if (playerRef.current) {
      playerRef.current.pauseVideo();
    }
  };

  const stopVideo = () => {
    if (playerRef.current) {
      playerRef.current.stopVideo();
    }
  };

  const restartVideo = () => {
    if (playerRef.current) {
      playerRef.current.seekTo(0); // Seek to the start of the video
      playerRef.current.playVideo(); // Play the video
    }
  };

  return (
    <div>
      <div id="player"></div>
      <div style={{ marginTop: '20px' }}>
        <button onClick={playVideo} style={{ marginRight: '10px' }}>Play</button>
        <button onClick={pauseVideo} style={{ marginRight: '10px' }}>Pause</button>
        <button onClick={stopVideo} style={{ marginRight: '10px' }}>Stop</button>
        <button onClick={restartVideo}>Restart</button>
      </div>
    </div>
  );
};

export default YouTubePlayerWithControls;
