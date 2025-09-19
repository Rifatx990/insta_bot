info = {
    "author": "RIFAT",
    "usage": "/help",
    "example": "/help",
    "description": "Sends a stylish DM listing all installed commands with status, usage, example, and author."
}

import time
from main import cmd_flags, cmd_info

def run(cl, flags, cmd_name):
    """
    Sends a stylish DM with all installed commands, their status,
    usage, example, and author.
    """
    seen_msgs = set()

    while flags[cmd_name]:
        try:
            threads = cl.direct_threads(amount=10)
        except Exception:
            time.sleep(5)
            continue

        for thread in threads:
            if not thread.messages:
                continue
            msg = thread.messages[0]
            sender_id = msg.user_id
            msg_text = (msg.text or "").strip().lower()

            if msg.id in seen_msgs or sender_id == cl.user_id:
                continue

            if msg_text == "/help":
                text = "🎀📦 *RIFAT BOT HELP* 📦🎀\n\n"
                text += f"🟢 Total Commands Installed: {len(cmd_flags)}\n\n"

                for cmd, status in cmd_flags.items():
                    cmd_data = cmd_info.get(cmd, {})
                    author = cmd_data.get("author", "RIFAT")
                    usage = cmd_data.get("usage", "N/A")
                    example = cmd_data.get("example", "N/A")

                    text += f"┌─💠 {cmd} [{ 'ON' if status else 'OFF' }]\n"
                    text += f"│ Author : {author}\n"
                    text += f"│ Usage  : {usage}\n"
                    text += f"│ Example: {example}\n"
                    text += "└───────────────\n\n"

                text += "🌟 Developer: RIFAT 🌟"

                try:
                    cl.direct_send(text, [sender_id])
                except Exception as e:
                    print(f"⚠️ Failed to send help DM: {e}")

            seen_msgs.add(msg.id)
        time.sleep(5)
