import React, { useEffect } from 'react';

const YouTubePlayer = () => {
  let player;

  useEffect(() => {
    // 1. This code loads the IFrame Player API code asynchronously.
    const tag = document.createElement('script');
    tag.src = 'https://youtu.be/Gz2Q1-Q7B8s?si=r3s9Eby19kY4c_JI';
    const firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

    // 2. This function creates an <iframe> (and YouTube player)
    //    after the API code downloads.
    window.onYouTubeIframeAPIReady = () => {
      player = new window.YT.Player('player', {
        height: '0', // Hidden height
        width: '0',  // Hidden width
        videoId: 'M7lc1UVf-VE', // Replace with your desired video ID
        playerVars: {
          playsinline: 1,
        },
        events: {
          onReady: onPlayerReady,
        },
      });
    };

    // Clean up function
    return () => {
      if (player) {
        player.destroy();
      }
    };
  }, []);

  // 3. The API will call this function when the video player is ready.
  const onPlayerReady = (event) => {
    event.target.playVideo();
  };

  return (
    <div>
      {/* 1. The <iframe> (and video player) will replace this <div> tag. */}
      <div id="player" style={{ display: 'none' }}></div>
    </div>
  );
};

export default YouTubePlayer;
