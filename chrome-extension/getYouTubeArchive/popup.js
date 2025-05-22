document.getElementById("sendQuery").addEventListener("click", async () => {
    const query = document.getElementById("query").value;
    if (query) {
        const url = `http://localhost:5000/getYouTubeLive?q=${encodeURIComponent(query)}`;
        try {
            const response = await fetch(url, { method: "POST" });
            const result = await response.json();
            console.log("Response:", result);
        } catch (error) {
            console.error("Error:", error);
        }
    } else {
        alert("検索クエリを入力してください。");
    }
});

// 動画IDを取得してボタンの表示/非表示を切り替える
chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const tab = tabs[0];
    const url = tab.url;
    const sendVideoIdButton = document.getElementById("sendVideoId");

    // URLがYouTubeのページかどうかを確認
    if (url.includes("youtube.com")) {
        const videoIdMatch = url.match(/(?:v=|\/)([0-9A-Za-z_-]{11})/);
        const videoId = videoIdMatch ? videoIdMatch[1] : null;

        if (videoId) {
            sendVideoIdButton.addEventListener("click", async () => {
                const endpointUrl = `http://localhost:5000/getYouTubeLive?video_id=${videoId}`;
                try {
                    const response = await fetch(endpointUrl, { method: "POST" });
                    const result = await response.json();
                    console.log("Response:", result);
                } catch (error) {
                    console.error("Error:", error);
                }
            });
        } else {
            // 動画IDが取得できなかった場合、ボタンを非表示にする
            sendVideoIdButton.style.display = "none";
        }
    } else {
        // YouTubeページ以外の場合、ボタンを非表示にする
        sendVideoIdButton.style.display = "none";
    }
});
