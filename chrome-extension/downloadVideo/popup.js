document.addEventListener('DOMContentLoaded', function() {
    const downloadSound = document.getElementById('downloadSound');
    
    fetch('http://localhost:5000/downloadVideo', {  // JSONエンドポイントに変更
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        let select = document.getElementById('directories');
        if (select) {
            data.forEach(dir => {
                let option = document.createElement('option');
                option.value = dir;
                option.text = dir;
                select.appendChild(option);
            });
        } else {
            console.error('The select element with id "directories" was not found.');
        }
    })
    .catch(error => console.error('Error fetching directories:', error));

    document.getElementById('downloadButton').addEventListener('click', function() {
        let selectedDir = document.getElementById('directories').value;
        let selectedQuality = document.getElementById('qualities').value;
        let startTime = document.getElementById('start_time').value.trim();
        let endTime = document.getElementById('end_time').value.trim();

        chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
            let videoId = tabs[0].url;
            
        // ダウンロード開始音を再生
            document.getElementById('downloadSound').play();
            
            fetch('http://localhost:5000/downloadVideo', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    video_id: videoId,
                    save_dir: selectedDir,
                    save_quality: selectedQuality,
                start_time: startTime || null,  // 空白の場合は null に
                end_time: endTime || null       // 空白の場合は null に
            })
            })
            .then(response => response.json())
            .then(data => {
                alert(data.response);
            })
            .catch(error => console.error('Error downloading video:', error));
        });
    });

});
