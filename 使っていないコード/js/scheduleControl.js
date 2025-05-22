$(document).ready(function() {
    $('#schedule_url_form').submit(function(event) {
        event.preventDefault(); // フォームのデフォルトの送信動作を停止

        // フォームから値を取得
        var url = $('#url').val();
        var hour = $('#hour').val();
        var minute = $('#minute').val();

        // Ajax通信を行う
        $.ajax({
            type: 'POST',
            url: '/schedule_url',
            contentType: 'application/json',
            data: JSON.stringify({
                url: url,
                hour: hour,
                minute: minute
            }),
            success: function(response) {
                // 成功時の処理を記述
                console.log('ダウンロードリクエストが成功しました。');
                console.log('レスポンス:', response);
                
            },
            error: function(xhr, status, error) {
                // エラー時の処理を記述
                console.error('ダウンロードリクエストが失敗しました。');
                console.error('エラー:', error);
            }
        });
    });

    $('#shutdown_pc_form').submit(function(event) {
        event.preventDefault(); // フォームのデフォルトの送信動作を停止

        // フォームから値を取得
        var shutdown_hour = $('#shutdown_hour').val();
        var shutdown_minute = $('#shutdown_minute').val();

        // Ajax通信を行う
        $.ajax({
            type: 'POST',
            url: '/shutdown_pc',
            contentType: 'application/json',
            data: JSON.stringify({
                shutdown_hour: shutdown_hour,
                shutdown_minute: shutdown_minute
            }),
            success: function(response) {
                // 成功時の処理を記述
                console.log('シャットダウンリクエストが成功しました。');
                console.log('レスポンス:', response);
            },
            error: function(xhr, status, error) {
                // エラー時の処理を記述
                console.error('シャットダウンリクエストが失敗しました。');
                console.error('エラー:', error);
            }
        });
    });
});
