chrome.runtime.onInstalled.addListener(() => {
  console.log('YouTube Timestamp Link Extension is installed!');
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'copyTimestamp') {
    navigator.clipboard.writeText(message.timestampUrl).then(
      () => {
        sendResponse({ success: true });
      },
      (err) => {
        console.error('コピーに失敗しました:', err);
        sendResponse({ success: false, error: err });
      }
    );
    return true;  // 非同期応答を待機
  }
});
