import os
import zipfile
import shutil
from datetime import datetime
from pathlib import Path

# 設定したディレクトリのパス
DOWNLOADS_DIR = Path(os.getenv("DOWNLOADS_DIR"))
EXCEL_DIR = Path(os.getenv("EXCEL_DIR"))
CSV_DIR = Path(os.getenv("CSV_DIR"))
JSON_DIR = Path(os.getenv("JSON_DIR"))
CURSOR_DIR = Path(os.getenv("CURSOR_DIR"))

# ファイルを移動する関数
def move_file(file_path, target_dir):
    print("move_file")
    try:
        target_dir.mkdir(parents=True, exist_ok=True)  # 必要に応じてディレクトリ作成
        target_file_path = target_dir / file_path.name

        if target_file_path.exists():
            target_file_path.unlink()  # 同名ファイルが存在する場合は削除して上書き

        shutil.move(str(file_path), str(target_file_path))
        print(f"Moved file: {file_path} to {target_file_path}")
    except Exception as e:
        print(f"Error moving file {file_path}: {e}")

# zipファイルを解凍してファイルを分類・移動する関数
def process_files_in_directory(start_date, end_date):
    print("process_files_in_directory")
    for file_path in DOWNLOADS_DIR.iterdir():
        try:
            file_mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)

            # 指定された期間内にダウンロードされたファイルのみ処理
            if start_date <= file_mod_time <= end_date:
                # zipファイルの場合、解凍して中身を処理
                if file_path.suffix == '.zip':
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        extract_path = file_path.with_suffix('')  # zipファイル名でディレクトリ作成
                        zip_ref.extractall(extract_path)
                        print(f"Extracted zip file: {file_path}")

                        # 解凍したディレクトリ内のファイルを再帰的に処理
                        for root, _, files in os.walk(extract_path):
                            for file in files:
                                extracted_file_path = Path(root) / file
                                classify_and_move_file(extracted_file_path)

                        # 解凍したフォルダを削除
                        shutil.rmtree(extract_path)
                        print(f"Deleted extracted folder: {extract_path}")

                    # 元のzipファイルを削除
                    file_path.unlink()
                    print(f"Deleted original zip file: {file_path}")

                # zip以外のjson, csv, excelファイルを直接処理
                elif file_path.suffix in {'.json', '.csv', '.xlsx'}:
                    classify_and_move_file(file_path)
        
        except zipfile.BadZipFile:
            print(f"Error: {file_path} is not a valid zip file.")
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

# ファイルを拡張子に基づいて分類し、移動する関数
def classify_and_move_file(file_path):
    print("classify_and_move_file")
    try:
        if file_path.suffix == '.xlsx':
            move_file(file_path, EXCEL_DIR)
        elif file_path.suffix == '.csv':
            move_file(file_path, CSV_DIR)
        elif file_path.suffix == '.json':
            move_file(file_path, JSON_DIR)
    except Exception as e:
        print(f"Error classifying file {file_path}: {e}")

# 指定されたzipファイルを解凍し、フォルダごと移動する関数
def extract_and_move_cursor_folders(start_date=None, end_date=None):
    print("extract_and_move_cursor_folders")
    # デフォルトは全期間
    if start_date is None:
        start_date = datetime.min
    if end_date is None:
        end_date = datetime.max

    for file_path in DOWNLOADS_DIR.glob("*.zip"):
        # ファイル名に「マウスカーソル」を含み、指定期間内のファイルを対象にする
        if "マウスカーソル" in file_path.stem and start_date <= datetime.fromtimestamp(file_path.stat().st_mtime) <= end_date:
            try:
                # zipファイルの解凍
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    extract_folder = DOWNLOADS_DIR / file_path.stem  # zipファイル名のフォルダを作成
                    zip_ref.extractall(extract_folder)
                    print(f"Extracted zip file to folder: {extract_folder}")

                    # フォルダを移動
                    target_folder = CURSOR_DIR / extract_folder.name
                    CURSOR_DIR.mkdir(parents=True, exist_ok=True)  # 必要に応じてディレクトリを作成

                    if target_folder.exists():
                        shutil.rmtree(target_folder)  # 同名フォルダがある場合は削除して上書き

                    shutil.move(str(extract_folder), str(target_folder))
                    print(f"Moved folder: {extract_folder} to {target_folder}")

                # 元のzipファイルを削除
                file_path.unlink()
                print(f"Deleted original zip file: {file_path}")

            except zipfile.BadZipFile:
                print(f"Error: {file_path} is not a valid zip file.")
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")


# 使用例
if __name__ == "__main__":
    # 指定期間 (例: 2024年10月1日から2024年10月30日)
    start_date = datetime(2024, 10, 1)
    end_date = datetime(2024, 12, 31)
    extract_and_move_cursor_folders(start_date, end_date)
    process_files_in_directory(start_date, end_date)
