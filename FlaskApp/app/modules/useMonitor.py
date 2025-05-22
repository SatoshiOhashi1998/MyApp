import sys
import ctypes

# 定数の定義
HWND_BROADCAST = 0xFFFF
WM_SYSCOMMAND = 0x0112
SC_MONITORPOWER = 0xF170
MONITOR_OFF = 2
MONITOR_ON = -1

# SendMessageW 関数の定義
SendMessageW = ctypes.windll.user32.SendMessageW

def turn_off_monitor():
    SendMessageW(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, MONITOR_OFF)

def turn_on_monitor():
    SendMessageW(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, MONITOR_ON)

# メイン処理
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python useMonitor.py <function_name>")
        sys.exit(1)
    
    function_name = sys.argv[1]
    
    if function_name == "turn_off_monitor":
        turn_off_monitor()
    elif function_name == "turn_on_monitor":
        turn_on_monitor()
    else:
        print(f"Function '{function_name}' not found.")
        sys.exit(1)
