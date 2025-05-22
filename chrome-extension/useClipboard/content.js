// content.js
function getPlaybackPosition() {
  const videoElement = document.querySelector('video');
  if (videoElement) {
    return videoElement.currentTime; // 再生位置（秒数）
  }
  return null;
}
