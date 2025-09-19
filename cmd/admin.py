# ------------------- CMD INFO -------------------
info = {
    "name": "admin",
    "author": "RIFAT",
    "usage": "/admin",
    "example": "/admin",
    "admin_only": False  # Accessible to all users
}

def run(cl, cmd_flags, cmd_name):
    """
    Public command to show admin bot profile info in a stylish DM.
    Usage: /admin
    """
    import time
    from main import ADMIN_BOT, bot_status, PROXY, loaded_cmds_count

    # Get the last DM
    threads = cl.direct_threads(amount=5)
    if not threads:
        return
    msg = threads[0].messages[0]
    sender_id = msg.user_id
    msg_text = (msg.text or "").strip()

    if not msg_text.lower().startswith("/admin"):
        return

    # Build a stylish response with admin bot info
    response = (
        "╔════════════════════╗\n"
        "║ 👑 ADMIN BOT INFO ║\n"
        "╠════════════════════╣\n"
        f"║ Username      : {ADMIN_BOT}\n"
        f"║ Status        : {bot_status}\n"
        f"║ Loaded CMDs   : {loaded_cmds_count}\n"
        f"║ Proxy         : {PROXY if PROXY else 'Direct connection'}\n"
        "╚════════════════════╝\n"
        "✨ Developed by RIFAT"
    )

    # Send DM to the user
    cl.direct_send(response, [sender_id])
