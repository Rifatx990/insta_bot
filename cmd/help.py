info = {
    "author": "RIFAT",
    "usage": "/help",
    "example": "/help",
    "description": "Sends the list of installed commands with status, usage, example, and author via DM."
}

def run(cl, cmd_flags, cmd_name):
    seen_msgs = set()
    while cmd_flags[cmd_name]:
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
                text = f"📦 Total Commands: {len(cmd_flags)}\n\n"
                for cmd, status in cmd_flags.items():
                    cmd_mod_info = None
                    try:
                        cmd_mod_info = __import__(f"cmd.{cmd}", fromlist=["info"]).info
                    except Exception:
                        cmd_mod_info = {"author": "RIFAT", "usage": "N/A", "example": "N/A"}

                    text += f"• {cmd} [{ 'ON' if status else 'OFF' }]\n"
                    text += f"  Author: {cmd_mod_info.get('author', 'RIFAT')}\n"
                    text += f"  Usage: {cmd_mod_info.get('usage', 'N/A')}\n"
                    text += f"  Example: {cmd_mod_info.get('example', 'N/A')}\n\n"

                try:
                    cl.direct_send(text, [sender_id])
                except Exception as e:
                    print(f"⚠️ Failed to send help DM: {e}")

            seen_msgs.add(msg.id)
        time.sleep(5)
