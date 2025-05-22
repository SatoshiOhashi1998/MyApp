"""
YouTubeのプレイリストからデータを取得してExcelに保存する。
"""
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from openpyxl import Workbook, load_workbook
from openpyxl.utils.exceptions import InvalidFileException
from datetime import datetime
import os
import json
import time
import pytz
import xlwings as xw

# APIキーを設定する
API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build('youtube', 'v3', developerKey=API_KEY)

# プレイリストのタイトルを取得する関数
def get_playlist_title(playlist_id):
    try:
        playlist_response = youtube.playlists().list(
            part='snippet',
            id=playlist_id
        ).execute()
        title = playlist_response['items'][0]['snippet']['title']
        return title
    except HttpError as e:
        print(f'An error occurred: {e}')
        return None

# プレイリスト内のビデオIDを取得する関数
def fetch_playlist_video_ids(playlist_id):
    video_ids = []
    next_page_token = None

    try:
        while True:
            playlist_response = youtube.playlistItems().list(
                part='snippet',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token if next_page_token else ''
            ).execute()

            for item in playlist_response['items']:
                video_id = item['snippet']['resourceId']['videoId']
                video_ids.append(video_id)

            next_page_token = playlist_response.get('nextPageToken')
            if not next_page_token:
                break

        return video_ids

    except HttpError as e:
        print(f'An HTTP error {e.resp.status} occurred:\n{json.loads(e.content)["error"]["message"]}')
        return video_ids

# 各種動画の詳細情報を取得する関数
def fetch_video_details(video_id, title, include_duration=False, include_playlist=False):
    try:
        video_response = youtube.videos().list(
            part='snippet,contentDetails',
            id=video_id
        ).execute()

        if video_response['items']:
            snippet = video_response['items'][0]['snippet']
            video_title = snippet['title']
            channel_title = snippet['channelTitle']
            published_at = datetime.strptime(snippet['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
            published_at = published_at.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Tokyo'))

            # 動画の長さを取得
            video_duration = None
            if include_duration:
                content_details = video_response['items'][0]['contentDetails']
                video_duration = content_details['duration']

            # 動画IDをURL化
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            # タプルで返すためのデータ準備
            video_data = (
                video_title,       # title
                channel_title,     # channel
                published_at,      # published_at
                video_url          # url
            )

            # 'playlist'を含める場合、データに追加
            if include_playlist:
                video_data = (0,) + video_data
                video_data += (title,)  # playlistをタプルに追加

            # 動画の長さを含める場合
            if include_duration:
                video_data += (video_duration,)  # durationをタプルに追加

            return video_data
        else:
            print(f"Video with ID {video_id} is unavailable or private.")
            return None

    except HttpError as e:
        print(f'An HTTP error {e.resp.status} occurred:\n{json.loads(e.content)["error"]["message"]}')
        return None


def update_excel_multiple(file_path, sheet_name, new_data_list):
    """
    Excelファイルを開き、指定されたシートに複数のデータを追加する関数

    :param file_path: Excelファイルのパス
    :param sheet_name: 対象のシート名
    :param new_data_list: 追加する新しいデータのリスト（タプルのリスト）
    """
    app = xw.App(visible=False)
    wb = None
    try:
        wb = app.books.open(file_path)
        sheet = wb.sheets[sheet_name]

        # B列のデータが空でない最終行を取得（空なら1行目から）
        if sheet.range('B2').value is None:
            last_row = 1
        else:
            last_row = sheet.range('B2').end('down').row

        # 複数データを順番に追加
        for new_data in new_data_list:
            sheet.range(f'B{last_row + 1}:D{last_row + 1}').value = new_data
            last_row += 1  # 行を更新

        # 保存
        wb.save()

        # 追加したデータの確認
        start_row = 2 if sheet.range('B2').value else last_row - len(new_data_list) + 1
        for row in sheet.range(f'B{start_row}:D{last_row}').value:
            print(row)

    finally:
        if wb:
            wb.close()
        app.quit()


def get_music_data(playlist_id=os.getenv("YOUTUBE_MUSIC_LIST")):
    video_ids = fetch_playlist_video_ids(playlist_id)
    title = get_playlist_title(playlist_id)

    video_data = []

    for video_id in video_ids:
        video_details = fetch_video_details(video_id, title, include_playlist=True)
        if video_details:
            video_data.append(video_details)
            time.sleep(1)  # APIへの負荷を減らすために一定時間待機
        else:
            print(f"Skipping video with ID: {video_id}")

    if video_data:
        save_path = os.path.join(os.getenv('SAVE_EXCEL_DIR'), os.getenv('SAVE_EXCEL_MUSIC_FILE'))
        update_excel_multiple(save_path, '動画一覧', video_data)
    else:
        print('Error occurred while fetching video details. Data not saved.')


def get_live_data(playlist_id=os.getenv("YOUTUBE_LIVE_LIST")):
    video_ids = fetch_playlist_video_ids(playlist_id)
    title = get_playlist_title(playlist_id)

    video_data = []

    for video_id in video_ids:
        video_details = fetch_video_details(video_id, title, include_playlist=False)
        if video_details:
            video_data.append(video_details)
            time.sleep(1)  # APIへの負荷を減らすために一定時間待機
        else:
            print(f"Skipping video with ID: {video_id}")

    if video_data:
        save_path = os.path.join(os.getenv('SAVE_EXCEL_DIR'), os.getenv('SAVE_EXCEL_LIVE_FILE'))
        update_excel_multiple(save_path, '2025年上半期', video_data)
    else:
        print('Error occurred while fetching video details. Data not saved.')


if __name__ == '__main__':
    get_live_data()
