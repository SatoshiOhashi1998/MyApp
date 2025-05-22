import csv
import os
import subprocess
import logging
from googleapiclient.discovery import build

# ログ設定（エラーメッセージをファイルに出力）
logging.basicConfig(
    filename='error_log.txt',  # エラーログを保存するファイル名
    level=logging.ERROR,  # エラーレベルを設定（ERRORレベルのログを記録）
    format='%(asctime)s - %(levelname)s - %(message)s',  # ログメッセージのフォーマット
    encoding="utf-8"  # ログファイルのエンコーディングをUTF-8に設定
)

API_KEY = "AIzaSyCfnk8M5KndLVlsoEWJt3nOEVf0okdTozw"
# TARGET_CHANNEL = "UCiMG6VdScBabPhJ1ZtaVmbw" # なずちゃん
TARGET_CHANNEL = "UCIcAj6WkJ8vZ7DeJVgmeqKw" # 胡桃のあ
# TARGET_CHANNEL = "UC5LyYg6cCA4yHEYvtUsir3g" # うるは
# TARGET_CHANNEL = "UCyLGcqYs7RsBb3L0SJfzGYA" # すみー
# TARGET_CHANNEL = "UCF_U2GCKHvDz52jWdizppIA" # 空澄セナ
# PUBLISHED_AFTER_DATE = "2022-07-29T19:19:49Z" # なずちゃん ここから先を取得する
# PUBLISHED_BEFORE_DATE = None
# PUBLISHED_BEFORE_DATE = "2022-10-08T19:40:47Z" # 空澄 ここから前
PUBLISHED_BEFORE_DATE = "2025-01-15T10:12:50Z" # 胡桃のあ
PUBLISHED_AFTER_DATE = None
# PUBLISHED_AFTER_DATE = "2025-03-02T01:40:28Z" # すみー ここから後を取得する
CSV_FILENAME = "youtube_videos.csv"
OUTPUT_DIR = "live_chat"


def save_to_csv(videos, filename=CSV_FILENAME):
    """取得した動画データをCSVに保存"""
    file_exists = os.path.isfile(filename)
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Title", "URL", "NextPageToken"])
        for video in videos:
            writer.writerow([video["title"], video["url"], video["published_at"]])


def get_videos_from_channel(channel_id, max_results=50):
    """チャンネルIDから動画の一覧を取得"""
    youtube = build("youtube", "v3", developerKey=API_KEY)
    next_page_token = None
    videos = []

    try:
        while True:
            request = youtube.search().list(
                part="id,snippet",
                channelId=channel_id,
                maxResults=max_results,
                order="date",
                publishedBefore=PUBLISHED_BEFORE_DATE,
                publishedAfter=PUBLISHED_AFTER_DATE,
                pageToken=next_page_token
            )
            response = request.execute()

            for item in response.get("items", []):
                if item["id"]["kind"] == "youtube#video":
                    video_id = item["id"]["videoId"]
                    title = item["snippet"]["title"]
                    published_at = item["snippet"]["publishedAt"]
                    url = f"https://www.youtube.com/watch?v={video_id}"
                    videos.append({
                        "title": title,
                        "url": url,
                        "published_at": published_at
                    })

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

        save_to_csv(videos)  # ループ外で一度だけ呼び出す

    except Exception as e:
        logging.error(f"エラー発生: {e}")
        logging.error("これまでに取得したデータを保存しました。")
        save_to_csv(videos)


def download_live_chat(video_url):
    """yt-dlp を使用してライブチャットデータを取得"""
    try:
        command = [
            "dl",
            "--skip-download",
            "--write-subs",
            "--sub-lang", "live_chat",
            "-o", f"{OUTPUT_DIR}/%(title)s [%(id)s].%(ext)s",
            "--cookies", "cookies.txt",
            video_url
        ]
        subprocess.run(command, check=True)
        print(f"✅ {video_url} のライブチャットを取得しました。")
    except subprocess.CalledProcessError as e:
        logging.error(f"⚠️ エラー発生: {video_url} - コマンド: {' '.join(command)} - {e}")


def get_chat_from_csv(filename=CSV_FILENAME):
    """CSVからURLリストを取得してライブチャットをダウンロード"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if not os.path.isfile(filename):
        logging.error(f"ファイル {filename} が見つかりません。処理をスキップします。")
        return  # ファイルがない場合は処理を終了

    try:
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)  # ヘッダーをスキップ
            for row in reader:
                title, url, _ = row
                print(f"▶ {title} のライブチャットを取得中...")
                download_live_chat(url)

        print("🎉 すべてのライブチャット取得が完了しました！")

    except Exception as e:
        logging.error(f"ライブチャット取得中にエラーが発生しました: {e}")


if __name__ == '__main__':
    # 動画の基本情報を取得
    get_videos_from_channel(channel_id=TARGET_CHANNEL)

    # ライブチャットを取得
    get_chat_from_csv()
