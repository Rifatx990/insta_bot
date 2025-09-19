import threading
import time

# ------------------- CMD INFO -------------------
info = {
    "name": "reminder",
    "author": "RIFAT",
    "usage": "/reminder [seconds] [message]",
    "example": "/reminder 60 Drink water",
    "admin_only": False  # Accessible to all users
}

def run(cl, cmd_flags, cmd_name):
    """
    Sets a reminder for the user.
    Usage: /reminder [seconds] [message]
    """
    threads = cl.direct_threads(amount=5)
    if not threads:
        return
    msg = threads[0].messages[0]
    sender_id = msg.user_id
    msg_text = (msg.text or "").strip()

    if not msg_text.lower().startswith("/reminder"):
        return

    parts = msg_text.split(maxsplit=2)
    if len(parts) < 3:
        cl.direct_send("⚠️ Invalid usage. Example: /reminder 60 Drink water", [sender_id])
        return

    try:
        seconds = int(parts[1])
        reminder_msg = parts[2]
    except ValueError:
        cl.direct_send("⚠️ Time must be a number in seconds.", [sender_id])
        return

    cl.direct_send(f"⏰ Reminder set! I will remind you in {seconds} seconds.", [sender_id])

    def send_reminder():
        time.sleep(seconds)
        response = (
            "╔════════════════════╗\n"
            "║ ⏰ REMINDER ALERT ║\n"
            "╠════════════════════╣\n"
            f"║ {reminder_msg}\n"
            "╚════════════════════╝\n"
            "✨ Stay focused! - RIFAT"
        )
        cl.direct_send(response, [sender_id])

    threading.Thread(target=send_reminder, daemon=True).start()
