import os
import time
import json
import threading

# ------------------- CMD INFO -------------------
info = {
    "name": "restart2",
    "version": "1.1",
    "author": "rifat",
    "role": 2,  # Admin only
    "description": {
        "vi": "Khởi động lại bot",
        "en": "Restart bot"
    },
    "category": "Owner",
    "guide": {
        "vi": "{pn}: Khởi động lại bot",
        "en": "{pn}: Restart bot"
    }
}

admin_only = True  # only admins can run

# Path to store restart info
RESTART_FILE = os.path.join(os.path.dirname(__file__), "tmp_restart.json")

# Ensure tmp folder exists
os.makedirs(os.path.dirname(RESTART_FILE), exist_ok=True)

# ------------------- ON LOAD -------------------
def on_load(bot_client):
    if os.path.exists(RESTART_FILE):
        try:
            with open(RESTART_FILE, "r") as f:
                data = json.load(f)
            thread_id = data.get("thread_id")
            timestamp = data.get("time")
            if thread_id and timestamp:
                elapsed = round(time.time() - timestamp, 2)
                bot_client.direct_send(f"✅ | Bot restarted\n⏰ | Time: {elapsed}s", [thread_id])
            os.remove(RESTART_FILE)
        except Exception as e:
            print(f"⚠️ Restart on_load failed: {e}")

# ------------------- CMD RUN -------------------
def run(bot_client, cmd_flags, cmd_name, event=None, message=None, getLang=None):
    try:
        # Save thread info
        if event:
            os.makedirs(os.path.dirname(RESTART_FILE), exist_ok=True)
            with open(RESTART_FILE, "w") as f:
                json.dump({"thread_id": event.thread_id, "time": time.time()}, f)
        
        # Reply to user
        if message and getLang:
            message.reply(getLang("restartting") if getLang else "🔄 | Restarting bot...")

        # Exit process to allow restart
        threading.Thread(target=lambda: os._exit(2), daemon=True).start()
    except Exception as e:
        print(f"❌ Restart command failed: {e}")
