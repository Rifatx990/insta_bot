import os
import time

# ------------------- CMD INFO -------------------
info = {
    "name": "share",
    "author": "RIFAT",
    "usage": "/share [on/off/cmd_name]",
    "example": "/share autoreact.py",
    "admin_only": True  # only bot admin can use
}

# Folder where all commands are stored
cmd_folder = os.path.dirname(os.path.abspath(__file__))

# Global flag to enable/disable share mode
share_mode = False

def run(cl, cmd_flags, cmd_name):
    """
    Share command code from server. Admin-only.
    Usage: /share [on/off/cmd_name]
    """
    global share_mode

    # Get the last DM
    threads = cl.direct_threads(amount=5)
    if not threads:
        return
    msg = threads[0].messages[0]
    sender_id = msg.user_id
    msg_text = (msg.text or "").strip()
    from main import adminbot, role  # import global admin info

    # Only allow bot admin
    if sender_id != adminbot:
        cl.direct_send("❌ You are not authorized to use this command.", [sender_id])
        return

    parts = msg_text.split()
    if len(parts) < 2:
        cl.direct_send("⚠️ Usage: /share [on/off/cmd_name]", [sender_id])
        return

    action = parts[1].lower()

    # ------------------- ENABLE SHARE MODE -------------------
    if action == "on":
        share_mode = True
        cl.direct_send("✅ Share mode ENABLED.", [sender_id])
        return

    # ------------------- DISABLE SHARE MODE -------------------
    elif action == "off":
        share_mode = False
        cl.direct_send("❌ Share mode DISABLED.", [sender_id])
        return

    # ------------------- SHARE COMMAND -------------------
    elif share_mode:
        target_cmd = parts[1]
        path = os.path.join(cmd_folder, target_cmd)
        if not os.path.exists(path):
            cl.direct_send(f"❌ Command '{target_cmd}' not found.", [sender_id])
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                code = f.read()

            # Split long code into DM-friendly chunks
            MAX_LEN = 1000
            for i in range(0, len(code), MAX_LEN):
                part = code[i:i+MAX_LEN]
                cl.direct_send(f"```python\n{part}\n```", [sender_id])
                time.sleep(1)

            cl.direct_send(f"✅ Command '{target_cmd}' shared successfully!", [sender_id])
        except Exception as e:
            cl.direct_send(f"❌ Failed to share '{target_cmd}': {e}", [sender_id])
        return

    else:
        cl.direct_send("⚠️ Share mode is OFF. Enable it with /share on", [sender_id])
