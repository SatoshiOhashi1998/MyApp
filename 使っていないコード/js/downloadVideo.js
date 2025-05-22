$(document).ready(function() {
    // ページ読み込み時に音声ファイルを追加
    var decidedAudioElement = createAudioElement('/static/sound/decided.mp3');
    var endedAudioElement = createAudioElement('/static/sound/ended.mp3');

    $('#downloadForm').submit(function(event) {
        event.preventDefault(); // フォームのデフォルトの送信動作を停止

        // 音声を再生する
        playAudio(decidedAudioElement);

        // フォームから値を取得
        var videoId = $('#video_id').val();
        var saveDir = $('#saveDir').val();

        // 正規表現を使用して動画IDを抽出→新しいURLを生成
        var videoId = videoId.match(/[?&]v=([^&]+)/)[1];
        var newURL = "https://www.youtube.com/watch?v=" + videoId;

        // Ajax通信を行う
        $.ajax({
            type: 'POST',
            url: '/downloadVideo',
            contentType: 'application/json',
            data: JSON.stringify({
                video_id: newURL,
                save_dir: saveDir
            }),
            success: function(response) {
                // 成功時の処理を記述
                console.log('ダウンロードリクエストが成功しました。');
                console.log('レスポンス:', response);
                
                // 音声を再生する
                playAudio(endedAudioElement);
            },
            error: function(xhr, status, error) {
                // エラー時の処理を記述
                console.error('ダウンロードリクエストが失敗しました。');
                console.error('エラー:', error);
            }
        });
    });

    // 音声ファイルの再生を行う関数
    function playAudio(audioElement) {
        audioElement.play();
    }

    // 音声ファイルのDOM要素を生成する関数
    function createAudioElement(src) {
        var audioElement = document.createElement('audio');
        audioElement.src = src;
        audioElement.style.display = 'none'; // 音声ファイルを隠す
        document.body.appendChild(audioElement);
        return audioElement;
    }
});
