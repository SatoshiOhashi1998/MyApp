from getYouTubeLive import get_archived_live_streams_by_playlistid, send_to_gas

if __name__ == '__main__':
    playlist_id = 'PLGQ23FYBgLigUWT44e-3nm0jMpO7trgjG'  # あなたのプレイリストIDに置き換えてください
    archived_streams = get_archived_live_streams_by_playlistid(playlist_id)
    send_to_gas(archived_streams)
