import os
import json
import time
import threading
import importlib.util
from flask import Flask, jsonify
from instagrapi import Client

# ------------------- CONFIG -------------------
USERNAME = "your_username"
PASSWORD = "your_password"
SESSION_FILE = "session.json"

# 🔑 Set your proxy directly here (leave as None for direct connection)
# Examples:
# PROXY = "socks5://127.0.0.1:9050"
# PROXY = "socks5://user:pass@host:port"
PROXY = "socks5://127.0.0.1:9050"   # <-- change here
# PROXY = None

bot_status = "🤖 Initializing bot..."
sent_count = 0
loaded_cmds_count = 0

# ------------------- Instagram Client Setup -------------------
cl = Client()

def setup_proxy():
    """Setup proxy if provided."""
    global bot_status
    if PROXY:
        try:
            cl.set_proxy(PROXY)
            bot_status = f"🌐 Using proxy {PROXY}"
            print(bot_status)
        except Exception as e:
            bot_status = f"⚠️ Proxy setup failed: {e}, using direct connection"
            print(bot_status)
    else:
        bot_status = "🌐 No proxy set, using direct connection"
        print(bot_status)

def login_instagram():
    """Login with saved session if possible, otherwise fresh login."""
    global bot_status
    setup_proxy()

    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r") as f:
                session = json.load(f)
            cl.set_settings(session)
            cl.get_timeline_feed()  # test session
            bot_status = f"✅ Restored session as {cl.username}"
            print(bot_status)
            return
        except Exception as e:
            print(f"⚠️ Session restore failed: {e}")

    # fallback login
    try:
        cl.login(USERNAME, PASSWORD)
        cl.dump_settings(SESSION_FILE)
        bot_status = f"✅ Fresh login successful as {cl.username}"
        print(bot_status)
    except Exception as e:
        bot_status = f"❌ Fresh login failed: {e}"
        print(bot_status)

login_instagram()

# ------------------- CMD Management -------------------
cmd_folder = "cmd"
cmd_threads = {}
cmd_flags = {}

def load_cmds():
    """Dynamically load all CMDs from the cmd/ folder."""
    global loaded_cmds_count
    loaded_cmds_count = 0

    if not os.path.exists(cmd_folder):
        print("⚠️ CMD folder not found.")
        return 0

    for file in os.listdir(cmd_folder):
        if file.endswith(".py"):
            path = os.path.join(cmd_folder, file)
            cmd_name = file[:-3]
            try:
                spec = importlib.util.spec_from_file_location(cmd_name, path)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                if hasattr(mod, "run"):
                    cmd_flags[cmd_name] = False  # Default OFF
                    cmd_threads[cmd_name] = {"module": mod, "thread": None}
                    loaded_cmds_count += 1
                    print(f"✅ Loaded CMD: {cmd_name}")
            except Exception as e:
                print(f"❌ Failed to load {file}: {e}")

    print(f"📦 Total commands loaded: {loaded_cmds_count}")
    return loaded_cmds_count

# ------------------- DM Command Listener -------------------
def monitor_cmd_dms():
    """Listen for /cmd on|off commands in Instagram DMs."""
    seen_msgs = set()
    while True:
        try:
            threads = cl.direct_threads(amount=10)
        except Exception as e:
            print(f"⚠️ Error fetching threads: {e}")
            time.sleep(10)
            continue

        for thread in threads:
            if not thread.messages:
                continue
            msg = thread.messages[0]
            sender_id = msg.user_id
            msg_text = (msg.text or "").strip().lower()

            if msg.id in seen_msgs or sender_id == cl.user_id:
                continue

            if msg_text.startswith("/"):
                parts = msg_text.split()
                if len(parts) == 2:
                    cmd_name = parts[0][1:]
                    action = parts[1]

                    if cmd_name in cmd_threads:
                        if action == "on" and not cmd_flags[cmd_name]:
                            cmd_flags[cmd_name] = True
                            t = threading.Thread(target=cmd_runner, args=(cmd_name,), daemon=True)
                            t.start()
                            cmd_threads[cmd_name]["thread"] = t
                            cl.direct_send(f"✅ CMD '{cmd_name}' turned ON", [sender_id])
                        elif action == "off" and cmd_flags[cmd_name]:
                            cmd_flags[cmd_name] = False
                            cl.direct_send(f"❌ CMD '{cmd_name}' turned OFF", [sender_id])

            seen_msgs.add(msg.id)
        time.sleep(5)

def cmd_runner(cmd_name):
    """Run a single command module in its own thread."""
    mod = cmd_threads[cmd_name]["module"]
    try:
        mod.run(cl, cmd_flags, cmd_name)
    except Exception as e:
        print(f"❌ Error in CMD '{cmd_name}': {e}")
        cmd_flags[cmd_name] = False  # reset state on crash

# ------------------- Flask API -------------------
app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "status": bot_status,
        "developer": "RIFAT",
        "sent_count": sent_count,
        "logged_in_as": cl.username if hasattr(cl, "username") else None,
        "proxy": PROXY if PROXY else "Direct connection",
        "loaded_commands": loaded_cmds_count,
        "cmds": {k: "ON" if v else "OFF" for k, v in cmd_flags.items()}
    })

# ------------------- Run Bot -------------------
if __name__ == "__main__":
    total_cmds = load_cmds()   # Auto load on startup
    print(f"🚀 Bot started with {total_cmds} command(s) loaded.")
    threading.Thread(target=monitor_cmd_dms, daemon=True).start()
    app.run(host="0.0.0.0", port=8080)
