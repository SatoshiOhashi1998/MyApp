import os
import shutil
from datetime import datetime

def backup_directories(src_dir):
    # 現在の日付を取得
    date_str = datetime.now().strftime("%Y%m%d")
    # バックアップ先ディレクトリの名前を作成
    backup_dir = os.path.join(src_dir, f"バックアップ{date_str}")
    
    # バックアップ先ディレクトリを作成
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # 除外するディレクトリのパスをリスト化
    exclude_dirs = {
        os.path.abspath(os.path.join(src_dir, "FlaskApp", "app", "static", "video")),
        os.path.abspath(os.path.join(src_dir, "FlaskApp", "app", "static", "image")),
        os.path.abspath(backup_dir)
    }
    
    # 既存のバックアップディレクトリを除外リストに追加
    for item in os.listdir(src_dir):
        if item.startswith("バックアップ") and os.path.isdir(os.path.join(src_dir, item)):
            exclude_dirs.add(os.path.abspath(os.path.join(src_dir, item)))
    
    # コピー処理
    for root, dirs, files in os.walk(src_dir):
        abs_root = os.path.abspath(root)
        
        # 除外するディレクトリかそのサブディレクトリの場合、コピー処理をスキップ
        if any(abs_root.startswith(exclude) for exclude in exclude_dirs):
            # 除外対象のディレクトリ内のサブディレクトリもスキップ
            dirs[:] = []
            continue
        
        # 現在のディレクトリの相対パスを取得
        relative_path = os.path.relpath(root, src_dir)
        if relative_path == ".":
            relative_path = ""
        
        # バックアップ先のパスを作成
        backup_root = os.path.join(backup_dir, relative_path)
        
        # 現在のディレクトリとバックアップ先のディレクトリが異なる場合のみ、バックアップディレクトリを作成
        if backup_root != backup_dir and not os.path.exists(backup_root):
            os.makedirs(backup_root)
        
        for file in files:
            file_path = os.path.join(root, file)
            backup_file_path = os.path.join(backup_root, file)
            try:
                shutil.copy2(file_path, backup_file_path)
            except Exception as e:
                print(f"エラーが発生しました: {e}")
    
    print(f"バックアップが完了しました。バックアップ先: {backup_dir}")

def main():
    # 使用例
    src_dir = os.getcwd()  # 現在の作業ディレクトリ
    src_dir = r"C:\Users\user\PycharmProjects\MyUtilProject\MyApp"
    backup_directories(src_dir)


if __name__ == '__main__':
    print("make backup")
    main()
