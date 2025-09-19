import time
from datetime import datetime

# ------------------- CMD INFO -------------------
info = {
    "name": "ping",
    "author": "RIFAT",
    "usage": "/ping",
    "example": "/ping",
    "admin_only": False  # accessible to all users
}

# Track bot start time globally
try:
    from main import bot_start_time
except ImportError:
    bot_start_time = datetime.now()

def run(cl, cmd_flags, cmd_name):
    """
    Respond to /ping command with bot status, uptime, and loaded commands.
    Accessible to all users.
    """
    from main import bot_status, loaded_cmds_count, PROXY, cl as main_cl

    # Get the last DM
    threads = cl.direct_threads(amount=5)
    if not threads:
        return

    msg = threads[0].messages[0]
    sender_id = msg.user_id
    msg_text = (msg.text or "").strip()

    if not msg_text.lower().startswith("/ping"):
        return

    # Calculate uptime
    uptime = datetime.now() - bot_start_time
    uptime_str = str(uptime).split(".")[0]  # remove microseconds

    response = (
        f"📡 **Bot Status**\n"
        f"🤖 Status: {bot_status}\n"
        f"⏱ Uptime: {uptime_str}\n"
        f"📦 Loaded Commands: {loaded_cmds_count}\n"
        f"🌐 Proxy: {PROXY if PROXY else 'Direct connection'}\n"
        f"💻 Logged in as: {main_cl.username if hasattr(main_cl, 'username') else 'N/A'}"
    )

    # Send response via DM
    cl.direct_send(response, [sender_id])
