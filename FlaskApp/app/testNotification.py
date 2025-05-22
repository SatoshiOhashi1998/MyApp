from plyer import notification

# 通知のタイトルとメッセージ
title = 'こんにちは!'
message = 'これはデスクトップ通知のサンプルです。'

# 通知の送信
notification.notify(
    title=title,
    message=message,
    app_name='My App',  # アプリ名
    timeout=10  # 通知が表示される時間（秒）
)
