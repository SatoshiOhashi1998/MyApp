document.getElementById('extract-data-button').addEventListener('click', async () => {
  console.log("000000000");
    try {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        console.log("1111111111111")
        chrome.scripting.executeScript({
            target: { tabId: tab.id },
            func: () => {
                // Twitchからアカウント名とチャンネルポイントを取得するロジックを実装する
                const accountName = document.querySelector('[XPath for account name]').innerText.trim();
                const channelPoints = document.querySelector('[XPath for channel points]').innerText.trim();
                return {
                    accountName,
                    channelPoints
                };
            }
        }, async (results) => {
            if (results && results[0].result) {
                const { accountName, channelPoints } = results[0].result;
                const data = {
                    accountName,
                    channelPoints
                };

                // Flaskサーバにデータを送信
                const url = 'http://127.0.0.1:5000/saveTwitchPoint';
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });

                if (response.ok) {
                    document.getElementById('result').innerText = 'データが正常に送信されました。';
                    document.getElementById('result').style.color = '#28a745'; // Success color
                } else {
                    document.getElementById('result').innerText = 'エラー: データの送信中に問題が発生しました。';
                    document.getElementById('result').style.color = '#d9534f'; // Error color
                }
            }
        });
    } catch (err) {
        console.error('Error:', err);
        document.getElementById('result').innerText = 'エラーが発生しました。コンソールを確認してください。';
        document.getElementById('result').style.color = '#d9534f'; // Error color
    }
});
