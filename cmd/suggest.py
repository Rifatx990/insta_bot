# ------------------- CMD INFO -------------------
info = {
    "name": "suggest",
    "author": "RIFAT",
    "usage": "/suggest [your message]",
    "example": "/suggest Please add a new feature to the bot!",
    "admin_only": False  # Accessible to all users
}

def run(cl, cmd_flags, cmd_name):
    """
    Public command to send suggestions/messages to the bot admin.
    Includes sender's profile picture in the admin DM.
    Usage: /suggest [your message]
    Accessible to all users.
    """
    import time
    from main import ADMIN_BOT, cl as main_cl

    # Fetch last DM
    threads = cl.direct_threads(amount=5)
    if not threads:
        return
    msg = threads[0].messages[0]
    sender_id = msg.user_id
    msg_text = (msg.text or "").strip()

    # Ensure command is /suggest
    if not msg_text.lower().startswith("/suggest"):
        return

    # Extract the suggestion text
    parts = msg_text.split(maxsplit=1)
    if len(parts) < 2:
        cl.direct_send("⚠️ Please provide a message to send to the admin.", [sender_id])
        return
    suggestion = parts[1]

    # Fetch sender info
    try:
        sender_info = main_cl.user_info(sender_id)
        sender_username = sender_info.username
        sender_pic = sender_info.profile_pic_url
    except Exception:
        sender_username = f"ID {sender_id}"
        sender_pic = None

    # Build stylish message for admin
    admin_message = (
        "╔════════════════════╗\n"
        "║ ✉️ NEW SUGGESTION ║\n"
        "╠════════════════════╣\n"
        f"║ From      : {sender_username}\n"
        f"║ User ID   : {sender_id}\n"
        "╠════════════════════╣\n"
        f"║ Message   : {suggestion}\n"
        "╚════════════════════╝\n"
        "✨ Sent via your bot"
    )

    # Find admin user id
    try:
        admin_id = None
        threads_admin = main_cl.direct_threads(amount=50)
        for t in threads_admin:
            if t.users:
                for u in t.users:
                    if u.username == ADMIN_BOT:
                        admin_id = u.pk
                        break
            if admin_id:
                break

        if admin_id:
            # Send admin DM with profile picture if available
            if sender_pic:
                cl.direct_send_photo(sender_pic, admin_message, [admin_id])
            else:
                cl.direct_send(admin_message, [admin_id])

            # Confirm to sender
            cl.direct_send("✅ Your message has been sent to the admin!", [sender_id])
        else:
            cl.direct_send("❌ Could not find admin to send your message.", [sender_id])
    except Exception as e:
        cl.direct_send(f"❌ Failed to send message: {e}", [sender_id])
