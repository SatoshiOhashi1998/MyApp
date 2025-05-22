import json
import csv
import os
import sqlite3
import pandas as pd
import re
import logging
import unicodedata
import ctypes

# ログ設定（エラーメッセージをファイルに出力）
logging.basicConfig(
    filename='error_log.txt',  # エラーログを保存するファイル名
    level=logging.ERROR,  # エラーレベルを設定（ERRORレベルのログを記録）
    format='%(asctime)s - %(levelname)s - %(message)s',  # ログメッセージのフォーマット
    encoding="utf-8"  # ログファイルのエンコーディングをUTF-8に設定
)


JSON_DIRECTORY = "live_chat"
# SAVE_CHANNEL = "花芽すみれ / Nazuna Sumire"
# SAVE_CHANNEL = "花芽なずな / Nazuna Kaga"
# SAVE_CHANNEL = "一ノ瀬うるは"
SAVE_CHANNEL = "胡桃のあ"
# SAVE_CHANNEL = "空澄セナ -Asumi Sena-"

DB_FILE = "live_chat_comments.db"
FILTERED_DATA = "comments.csv"
GETED_DATA = 'uruha_chat.csv'

# FILTERED_DATA = "sumires.csv"
# DB_FILE = "sumire_member_comments.db"
# GETED_DATA = 'getedSumireData.csv'

# FILTERED_DATA = "yoru.csv"
# DB_FILE = "yoru_comments.db"
# GETED_DATA = 'yoruData.csv'
# SQLiteデータベースの接続とテーブルの作成

def create_db():
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        # コメント用のテーブルを作成（url列とdate列を追加）
        c.execute('''      
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER NOT NULL,
            comment TEXT NOT NULL,
            title TEXT NOT NULL,
            channel TEXT NOT NULL DEFAULT "一ノ瀬うるは",
            url TEXT,            
            date TEXT            
        )  
        ''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        logging.error(f"データベースの作成または接続に失敗しました: {e}")

# JSONからコメントのテキストと時間を抽出
def extract_comments_from_json(json_file):
    comments = []
    df = getVideoData()
    print(f"処理中: {json_file}")  # デバッグ用にファイル名を表示

    try:
        with open(json_file, "r", encoding="utf-8") as f:
            content = f.read()

            try:
                # 複数のJSONオブジェクトが含まれている場合、1行ずつ処理
                data_list = content.splitlines()  # 改行で区切って複数のJSONオブジェクトに分割

                for line in data_list:
                    try:
                        data = json.loads(line)  # 1行ずつJSONを読み込み

                        actions = data.get("replayChatItemAction", {}).get("actions", [])
                        if not actions:
                            continue  # コメントがなければ次に進む

                        # コメント部分を抽出
                        for action in actions:
                            item = action.get("addChatItemAction", {}).get("item", {})
                            renderer = item.get("liveChatTextMessageRenderer", {})
                            message_data = renderer.get("message", {})

                            # "emoji" キーがある場合はスルー
                            if 'emoji' in message_data:
                                continue

                            # コメントテキストを取得
                            comment_text = ""
                            for run in message_data.get("runs", []):
                                # "text" キーが存在する場合のみ処理
                                if "text" in run:
                                    comment_text += run["text"]

                            # タイムスタンプを取得
                            timestamp_text = renderer.get("timestampText", {}).get("simpleText", "")

                            # タイムスタンプの形式が "hh:mm:ss" または "mm:ss" の場合に対応
                            if timestamp_text:
                                # マイナスの時間を考慮
                                negative = timestamp_text.startswith("-")
                                timestamp_text = timestamp_text.lstrip("-")

                                timestamp_parts = timestamp_text.split(":")
                                if len(timestamp_parts) == 3:  # 時:分:秒形式の場合
                                    hours = int(timestamp_parts[0])
                                    minutes = int(timestamp_parts[1])
                                    seconds = int(timestamp_parts[2])
                                    timestamp = hours * 3600 + minutes * 60 + seconds
                                    if negative:
                                        timestamp = -timestamp
                                elif len(timestamp_parts) == 2:  # 分:秒形式の場合
                                    minutes = int(timestamp_parts[0])
                                    seconds = int(timestamp_parts[1])
                                    timestamp = minutes * 60 + seconds
                                    if negative:
                                        timestamp = -timestamp
                                else:
                                    timestamp = 0  # タイムスタンプの形式が異なる場合の対応
                            else:
                                timestamp = 0  # タイムスタンプが取得できなかった場合

                            insert_title = os.path.splitext(os.path.basename(json_file))[0].strip().replace('⧸', '/')

                            # Unicode正規化 (NFKC または NFKD を試す)
                            df['Title'] = df['Title'].apply(lambda x: unicodedata.normalize('NFKC', x))
                            insert_title = unicodedata.normalize('NFKC', insert_title)

                            filtered_df = df[df['Title'] == insert_title]

                            # コメント情報にファイル名（title）を追加
                            comments.append({
                                "timestamp": timestamp,
                                "comment": comment_text,
                                "title": insert_title,  # ファイル名をtitleとして保存
                                "channel": SAVE_CHANNEL,  # channelの初期値
                                "url": filtered_df['URL'].values[0],
                                "date": filtered_df['date'].values[0]
                            })
                    except json.JSONDecodeError as e:
                        logging.error(f"JSONデコードエラー (行処理中): {e}")
                        print(f"JSONデコードエラー (行処理中): {e}")
            except json.JSONDecodeError as e:
                logging.error(f"JSONデコードエラー: {e}")
                print(f"JSONデコードエラー: {e}")
    except FileNotFoundError as e:
        logging.error(f"ファイルが見つかりません: {e}")
        print(f"ファイルが見つかりません: {e}")
    except Exception as e:
        logging.error(f"予期しないエラーが発生しました: {e}")
        print(f"予期しないエラーが発生しました: {e}")

    return comments

# コメントをSQLiteデータベースに保存
def save_comments_to_db(comments):
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()

        # コメントデータを挿入（urlとdateはNULLで保存）
        for comment in comments:
            try:
                c.execute('''      
                INSERT INTO comments (timestamp, comment, title, channel, url, date)
                VALUES (?, ?, ?, ?, ?, ?)  
                ''', (comment["timestamp"], comment["comment"], comment["title"], comment["channel"], comment["url"], comment["date"]))
            except sqlite3.Error as e:
                logging.error(f"コメントの保存に失敗しました: {e}")

        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        logging.error(f"データベース接続に失敗しました: {e}")

# ディレクトリ内のJSONファイルを処理
def process_json_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            json_file = os.path.join(directory, filename)
            
            # 明示的に UTF-8 に変換
            json_file = json_file.encode("utf-8", "ignore").decode("utf-8")

            print(f"▶ {filename} を処理中...")

            # JSONからコメントを抽出
            comments = extract_comments_from_json(json_file)

            # コメントをデータベースに保存
            if comments:
                save_comments_to_db(comments)
            else:
                logging.error(f"コメントが抽出できませんでした: {filename}")

    print("🎉 すべてのコメントをデータベースに保存しました！")

def getVideoData():
    # CSVファイルの読み込み
    try:
        df = pd.read_csv(GETED_DATA)
        return df
    except FileNotFoundError as e:
        logging.error(f"CSVファイルが見つかりません: {e}")
        return pd.DataFrame()  # 空のデータフレームを返す

def main():
    # データベースの作成
    create_db()

    # JSONファイルを処理するディレクトリを指定
    json_directory = JSON_DIRECTORY  # ここにJSONファイルが格納されているディレクトリのパスを指定

    # ディレクトリ内のJSONファイルを処理
    process_json_files(json_directory)


def rename_json():
    import os
    import re

    # 対象ディレクトリのパスを指定
    target_directory = "live_chat"

    # ファイル名のパターン
    pattern = re.compile(r" \[[a-zA-Z0-9_-]+\]\.live_chat\.json$")

    # ディレクトリ内のファイルを取得してリネーム
    for filename in os.listdir(target_directory):
        old_path = os.path.join(target_directory, filename)
        
        # JSONファイルのみ対象にする
        if filename.endswith(".json"):
            new_filename = pattern.sub(".json", filename)  # 該当部分を削除
            new_path = os.path.join(target_directory, new_filename)

            # 既に存在する場合はスキップ
            if old_path != new_path and not os.path.exists(new_path):
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} -> {new_filename}")
            elif old_path != new_path:
                print(f"Skipped (file exists): {new_filename}")

def remove_duplicates():
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        
        # 重複する行を削除（id以外のすべての列が重複している行）
        c.execute('''
            DELETE FROM comments
            WHERE id NOT IN (
                SELECT MIN(id)
                FROM comments
                GROUP BY timestamp, comment, title, channel, url, date
            );
        ''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        logging.error(f"データベースから重複を削除する際にエラーが発生しました: {e}")


def count_rows():
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        # 行数をカウント
        c.execute('SELECT COUNT(*) FROM comments')
        row_count = c.fetchone()[0]
        conn.close()
        print(f"コメントテーブルの行数: {row_count}")
        return row_count
    except sqlite3.Error as e:
        print(f"データベースエラー: {e}")
        return None

def search_comments(channel=None, title=None, date=None, comment=None):
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()

        # 基本的な検索クエリ
        query = "SELECT * FROM comments WHERE 1=1"
        params = []

        # チャンネルで絞り込み（条件が指定されていれば）
        if channel:
            query += " AND channel = ?"
            params.append(channel)

        # タイトルで絞り込み（条件が指定されていれば）
        if title:
            query += " AND title LIKE ?"
            params.append(f"%{title}%")  # 部分一致検索

        # 日付で絞り込み（条件が指定されていれば）
        if date:
            query += " AND date = ?"
            params.append(date)

        # コメントで絞り込み（条件が指定されていれば）
        if comment:
            query += " AND comment LIKE ?"
            params.append(f"%{comment}%")  # 部分一致検索

        # クエリ実行
        c.execute(query, params)
        results = c.fetchall()

        # 結果があればリストで返す
        conn.close()

        if results:
            return results  # 結果を返す
        else:
            return []  # 該当するデータがない場合は空のリストを返す

    except sqlite3.Error as e:
        logging.error(f"検索中にエラーが発生しました: {e}")
        return []  # エラーが発生した場合も空のリストを返す

def save_to_csv(data, filename=FILTERED_DATA):
    if not data:
        logging.warning("保存するデータがありません。")
        return

    try:
        # CSVファイルを開く（追記モード）
        with open(filename, mode="w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)

            # ヘッダー行を書き込む
            writer.writerow(["ID", "Timestamp", "Comment", "Title", "Channel", "URL", "Date"])

            # データ行を書き込む
            for row in data:
                writer.writerow(row)

        logging.info(f"データが {filename} に保存されました。")
    
    except Exception as e:
        logging.error(f"CSVファイルの保存中にエラーが発生しました: {e}")

def get_oldest_and_latest_comment(channel_name):
    """
    使い方
    oldest_comment, latest_comment = get_oldest_and_latest_comment("一ノ瀬うるは")
    print("最も古いコメント:", oldest_comment)
    print("最も新しいコメント:", latest_comment)
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # 最も早い `date`
    c.execute('''
        SELECT * FROM comments 
        WHERE channel = ? 
        ORDER BY date ASC 
        LIMIT 1
    ''', (channel_name,))
    oldest = c.fetchone()

    # 最も遅い `date`
    c.execute('''
        SELECT * FROM comments 
        WHERE channel = ? 
        ORDER BY date DESC 
        LIMIT 1
    ''', (channel_name,))
    latest = c.fetchone()

    conn.close()
    return oldest, latest

def update_channel_by_url(url, new_channel):
    """
    使い方
    update_channel_by_url("https://example.com/video123", "新しいチャンネル名")
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute('''
        UPDATE comments 
        SET channel = ? 
        WHERE url = ?
    ''', (new_channel, url))

    conn.commit()
    conn.close()

def delete_json_files(directory):
    """
    指定されたディレクトリ内のすべてのJSONファイルを削除し、
    ゴミ箱も空にする関数。
    
    Parameters:
    directory (str): JSONファイルを削除する対象ディレクトリのパス
    """
    # 1. 指定ディレクトリ内のすべてのJSONファイルを削除
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            json_file = os.path.join(directory, filename)
            try:
                os.remove(json_file)
                print(f"削除しました: {json_file}")
            except Exception as e:
                print(f"{json_file} の削除に失敗しました: {e}")

    # 2. ゴミ箱を空にする
    ctypes.windll.shell32.SHEmptyRecycleBinW(0, None, 1)
    print("ゴミ箱を空にしました。")

if __name__ == "__main__":
    # # delete_json_files(JSON_DIRECTORY)
    # rename_json()
    # main()
    # # # remove_duplicates()
    # # count_rows()
    # response = search_comments(channel=SAVE_CHANNEL, comment="腹筋")
    # save_to_csv(response)
    # # oldest, latest = get_oldest_and_latest_comment("花芽すみれ / Kaga Sumire")
    oldest, latest = get_oldest_and_latest_comment("胡桃のあ")
    print(oldest)
