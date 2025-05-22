"""
[エッチなイラストまとめ - Dynalist](https://dynalist.io/d/lwOPbvn4fs4LlFtFFD__Oy90)
上記ページにまとめておいた好きなイラストが、Twitterの規約改定により見られなく可能性が高かったので今のうちにダウンロードしておく。
parse_text_file: Dynalistのメモをテキストファイルにコピペし、そのファイルをもとにExcelファイルにまとめなおす。
download_images_from_excel: Excelファイルをもとに画像をダウンロードする。
"""


import os
import re
import requests
import pandas as pd
from urllib.parse import urlparse

def download_images_from_excel(excel_path, output_folder):
    # 出力フォルダが存在しない場合は作成
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Excelファイルの読み込み
    df = pd.read_excel(excel_path, engine='openpyxl')
    
    # 各行の画像URLから画像をダウンロード
    for index, row in df.iterrows():
        image_url = row['Image URL']
        title = row['Title']
        
        try:
            # 画像のダウンロード
            response = requests.get(image_url)
            response.raise_for_status()  # ステータスコードが200でなければエラー
            
            # ファイル名を生成
            parsed_url = urlparse(image_url)
            image_extension = os.path.splitext(parsed_url.path)[-1]
            if not image_extension:  # 拡張子がない場合の対処
                image_extension = ".jpg"
            
            # ファイル名に使用できない文字を除去
            sanitized_title = re.sub(r'[\\/*?:"<>|]', "", title)
            image_filename = f"{sanitized_title}_{index}{image_extension}"
            image_path = os.path.join(output_folder, image_filename)
            
            # 画像の保存
            with open(image_path, 'wb') as img_file:
                img_file.write(response.content)
            
            print(f"Downloaded {image_filename}")
        
        except requests.exceptions.RequestException as e:
            print(f"Failed to download image from {image_url}: {e}")

def parse_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 初期化
    data = []

    # テキストファイルからデータを抽出
    for i in range(0, len(lines), 2):
        line1 = lines[i].strip()
        line2 = lines[i + 1].strip()

        # 1行目のタイトルと画像URLを抽出
        title_match = re.search(r'!\[(.*?)\]\((.*?)\)', line1)
        if title_match:
            title = title_match.group(1)
            image_url = title_match.group(2)
        else:
            continue  # タイトルと画像URLが見つからない場合、次のデータへ

        # 2行目の著者名、プロフィールURL、タグを抽出
        author_match = re.search(r'\[(.*?)\]\((.*?)\)', line2)
        if author_match:
            author_name = author_match.group(1)
            profile_url = author_match.group(2)
        else:
            continue  # 著者情報が見つからない場合、次のデータへ

        # タグを抽出（複数タグがある場合に対応）
        tags = ' '.join(re.findall(r'(#\S+)', line2))

        # 抽出したデータをリストに追加
        data.append({
            'Title': title,
            'Image URL': image_url,
            'Author Name': author_name,
            'Profile URL': profile_url,
            'Tags': tags
        })

    # DataFrameに変換してExcelファイルに出力
    df = pd.DataFrame(data)
    output_path = 'output.xlsx'
    df.to_excel(output_path, index=False, engine='openpyxl')
    print(f"Data has been written to {output_path}")

# # 使用例
# parse_text_file('target.txt')

# 使用例
# download_images_from_excel('output.xlsx', 'downloaded_images')
