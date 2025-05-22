document.getElementById('clean-url-button').addEventListener('click', async () => {
    try {
        const text = await navigator.clipboard.readText();
        const cleanUrl = cleanYouTubeUrl(text);
        if (cleanUrl) {
            await navigator.clipboard.writeText(cleanUrl);
            document.getElementById('result').innerText = `クリーンなURL: ${cleanUrl}`;
        } else {
            document.getElementById('result').innerText = 'エラー: クリップボードの内容は有効なYouTubeリンクではありません。';
        }
    } catch (err) {
        console.error('Error:', err);
        document.getElementById('result').innerText = 'エラーが発生しました。コンソールを確認してください。';
    }
});

document.querySelectorAll('button[data-increment]').forEach(button => {
    button.addEventListener('click', async (event) => {
        const increment = parseInt(event.target.getAttribute('data-increment'), 10);
        try {
            const text = await navigator.clipboard.readText();
            const updatedUrl = updateTimeParam(text, increment);
            if (updatedUrl) {
                await navigator.clipboard.writeText(updatedUrl);
                document.getElementById('result').innerText = `更新されたURL: ${updatedUrl}`;
            } else {
                document.getElementById('result').innerText = 'エラー: クリップボードの内容は有効なYouTubeリンクではありません。';
            }
        } catch (err) {
            console.error('Error:', err);
            document.getElementById('result').innerText = 'エラーが発生しました。コンソールを確認してください。';
        }
    });
});

function cleanYouTubeUrl(url) {
    try {
        const urlObj = new URL(url);
        if (urlObj.hostname.includes('youtube.com') || urlObj.hostname.includes('youtu.be')) {
            const cleanUrlObj = new URL(urlObj.origin + urlObj.pathname);
            if (urlObj.searchParams.has('v')) {
                cleanUrlObj.searchParams.set('v', urlObj.searchParams.get('v'));
            }
            return cleanUrlObj.toString();
        }
        return null;
    } catch (e) {
        console.error('Invalid URL:', url);
        return null;
    }
}

function updateTimeParam(url, increment) {
    try {
        const urlObj = new URL(url);
        if (urlObj.hostname.includes('youtube.com') || urlObj.hostname.includes('youtu.be')) {
            let seconds = 0;
            if (urlObj.searchParams.has('t')) {
                seconds = parseInt(urlObj.searchParams.get('t').replace('s', ''), 10);
            }
            seconds += increment;
            if (seconds < 0) seconds = 0;
            urlObj.searchParams.set('t', `${seconds}s`);
            return urlObj.toString();
        }
        return null;
    } catch (e) {
        console.error('Invalid URL:', url);
        return null;
    }
}
