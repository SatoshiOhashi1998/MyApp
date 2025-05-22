import os
import subprocess
import shutil
import glob
import re
import logging
import argparse
from contextlib import contextmanager
from pathlib import Path

APP_BASE_PATH = os.getenv("APP_BASE_PATH", ".")
VIDEO_BASE_PATH = os.path.join(APP_BASE_PATH, "static", "video")

@contextmanager
def change_directory(destination: str):
    current_directory = os.getcwd()
    try:
        os.chdir(destination)
        yield
    finally:
        os.chdir(current_directory)

def download(video_id: str, save_dir: str, audio_only: bool = False) -> None:
    video_id = "https://www.youtube.com/watch?v=" + video_id
    video_id = video_id.split("&")[0] if "&" in video_id else video_id
    command = (
        [
            'dl', 
            '-f', 'bestaudio', 
            '--audio-format', 'mp3',
            '-o', f'{save_dir}/%(title)s.%(ext)s', 
            video_id
        ]
        if audio_only else
        [
            'dl', 
            '-f', 'bestvideo[ext=mp4]+bestaudio[ext=mp4]/mp4',
            '-o', f'{save_dir}/%(title)s.%(ext)s', 
            video_id
        ]
    )

    with change_directory(VIDEO_BASE_PATH):
        popen = subprocess.Popen(command)
        popen.wait()
        logging.info(f"Download completed: {video_id}")
        move_downloaded_files(save_dir)

def move_downloaded_files(save_dir: str):
    for path in glob.glob(os.path.join(VIDEO_BASE_PATH, "*.mp4")):
        new_filename = sanitize_filename(os.path.basename(path))
        target_path = os.path.join(save_dir, new_filename)
        
        if not os.path.exists(target_path):
            shutil.move(path, target_path)
            logging.info(f"Moved video to {target_path}")
        else:
            logging.warning(f"File {new_filename} already exists in {save_dir}, skipping...")

def sanitize_filename(filename: str) -> str:
    filename = re.sub(r'\[.*?\]', '', filename)
    filename = re.sub(r'[#＃\'’]', '', filename).strip()
    return filename

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download a video or audio from YouTube")
    parser.add_argument("video_id", type=str, help="The YouTube video ID or URL to download")
    parser.add_argument("save_dir", type=str, help="Directory to save the downloaded file")
    parser.add_argument("--audio_only", action="store_true", help="Download audio only if set")

    args = parser.parse_args()
    download(args.video_id, args.save_dir, args.audio_only)
