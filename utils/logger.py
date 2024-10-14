from datetime import datetime

def print_(message):
    now = datetime.now().isoformat(" ").split(".")[0]
    print(f"[{now}] {message}")