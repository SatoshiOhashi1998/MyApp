import pandas as pd
from sklearn.cluster import DBSCAN
import numpy as np
import requests
import json
import os
from datetime import datetime, timedelta
import pprint


def cluster_tenhou_data(file_prefix="Primmie", start_date=None, end_date=None):
    # CSVファイルのパスを作成
    file_path = os.path.join("csv", f"{file_prefix} -- 天鳳IDログ検索 - nodocchi.moe.csv")
    print(f"Loading file from: {file_path}")

    # CSVファイルを読み込む
    if not os.path.exists(file_path):
        print("File not found.")
        return []

    df = pd.read_csv(file_path, usecols=["順位", "期間", "始まる時間", "ルール"])

    # 始まる時間列をdatetime型に変換
    try:
        df["始まる時間"] = pd.to_datetime(df["始まる時間"])
    except Exception as e:
        print("Error in converting '始まる時間' to datetime:", e)
        return []

    # 日付の範囲でフィルタリング
    if start_date:
        start_date = pd.to_datetime(start_date)
        df = df[df["始まる時間"] >= start_date]
    if end_date:
        end_date = pd.to_datetime(end_date)
        df = df[df["始まる時間"] <= end_date]

    # Unixタイムスタンプに変換して新しい列に保存
    df["Timestamp"] = df["始まる時間"].astype(np.int64) // 10**9  # 秒単位のタイムスタンプ

    # DBSCANクラスタリングを実行
    dbscan = DBSCAN(eps=3600, min_samples=2)
    df["Cluster"] = dbscan.fit_predict(df[["Timestamp"]])

    # クラスタごとのデータを出力用のリストにまとめる
    clusters_info = []
    for cluster in np.unique(df["Cluster"]):
        if cluster != -1:  # -1はノイズとして除外
            cluster_data = df[df["Cluster"] == cluster]
            start_time = cluster_data["始まる時間"].min()
            end_time = cluster_data["始まる時間"].max()

            # エンドタイムを「期間」を考慮して計算
            last_duration = cluster_data["期間"].iloc[-1]
            last_duration_minutes = int(last_duration.replace("分", ""))
            end_time += timedelta(minutes=last_duration_minutes)

            combined_rules = [entry[:3] + str(rank) for entry, rank in zip(cluster_data["ルール"], cluster_data["順位"])]
            combined_rules_string = ' '.join(combined_rules)

            cluster_dict = {
                "Start Time": start_time.strftime('%Y-%m-%d %H:%M:%S'),
                "End Time": end_time.strftime('%Y-%m-%d %H:%M:%S'),
                "Match Result": combined_rules_string
            }
            clusters_info.append(cluster_dict)

    return clusters_info


def send_to_gas_tenhou_history(start_date=None, end_date=None):
    url = os.getenv('GAS_TENHOU_URL')
    pprint.pprint(url)

    result = cluster_tenhou_data(start_date=start_date, end_date=end_date)

    pprint.pprint(result)

    # データをJSON形式に変換
    json_data = json.dumps(result)

    # リクエストヘッダーを設定
    headers = {
        'Content-Type': 'application/json',
    }

    # POSTリクエストを送信
    response = requests.post(url, data=json_data, headers=headers)
    print('Response content:', response.text)

    if response.status_code == 200:
        print('データが正常に送信されました:', response.json())
    else:
        print('エラーが発生しました:', response.status_code, response.text)


if __name__ == '__main__':
    # 例として期間を指定して実行
    start_date = "2024-12-5"
    send_to_gas_tenhou_history(start_date=start_date)
