document.getElementById("copyButton").addEventListener("click", () => {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const tab = tabs[0];
    const videoId = getVideoIdFromUrl(tab.url);

    if (videoId) {
      chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: getCurrentTime
      }, (result) => {
        if (result && result[0] && result[0].result !== undefined) {
          const timestamp = result[0].result;
          updateTimestampUrl(videoId, timestamp);
        }
      });
    } else {
      alert("Not a valid YouTube video page.");
    }
  });
});

// タイムスタンプを増減するボタンのクリックイベント
document.querySelectorAll(".adjust-buttons button").forEach(button => {
  button.addEventListener("click", () => {
    const adjustValue = parseInt(button.getAttribute("data-adjust"));
    const currentUrl = document.getElementById("timestampUrl").value;
    const currentTimestamp = getTimestampFromUrl(currentUrl);
    if (currentTimestamp !== null) {
      const newTimestamp = Math.max(0, currentTimestamp + adjustValue);
      const videoId = getVideoIdFromUrl(currentUrl);
      updateTimestampUrl(videoId, newTimestamp);
    }
  });
});

// URLのタイムスタンプを更新し、フォーマットに基づいてテキストを生成して表示・コピー
function updateTimestampUrl(videoId, timestamp) {
  const timestampUrl = `https://www.youtube.com/watch?v=${videoId}&t=${timestamp}s`;
  const formatOption = document.querySelector('input[name="format"]:checked').value;

  let copyText = timestampUrl;
  if (formatOption === "titleWithUrl") {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const videoTitle = tabs[0].title.replace(" - YouTube", "");
      copyText = `[${videoTitle}](${timestampUrl})`;
      setAndCopyText(copyText);
    });
  } else {
    setAndCopyText(copyText);
  }
}

// テキストを入力欄にセットし、クリップボードにコピー
function setAndCopyText(text) {
  document.getElementById("timestampUrl").value = text;
  navigator.clipboard.writeText(text);
}

// 現在のYouTube動画の再生位置を取得
function getCurrentTime() {
  const video = document.querySelector('video');
  return video ? Math.floor(video.currentTime) : null;
}

// YouTubeのURLから動画IDを取得
function getVideoIdFromUrl(url) {
  const match = url.match(/[?&]v=([^&]+)/);
  return match ? match[1] : null;
}

// URLからタイムスタンプを取得
function getTimestampFromUrl(url) {
  const match = url.match(/[?&]t=(\d+)s/);
  return match ? parseInt(match[1], 10) : null;
}
