# ------------------- CMD INFO -------------------
info = {
    "name": "broadcast",
    "author": "RIFAT",
    "usage": "/broadcast [message]",
    "example": "/broadcast Hello everyone! This is an important update.",
    "admin_only": True  # Only admin can use this
}

def run(cl, cmd_flags, cmd_name):
    """
    DM command to broadcast a message to all users known to the bot.
    Usage: /broadcast [your message]
    Admin only.
    """
    import time
    from main import user_roles, ROLE_ADMIN

    # Fetch last DM
    threads = cl.direct_threads(amount=5)
    if not threads:
        return
    msg = threads[0].messages[0]
    sender_id = msg.user_id
    msg_text = (msg.text or "").strip()

    # Ensure the command is /broadcast
    if not msg_text.lower().startswith("/broadcast"):
        return

    # Check if sender is admin
    if user_roles.get(sender_id, 1) != ROLE_ADMIN:
        cl.direct_send("❌ You are not authorized to use /broadcast. Admin only.", [sender_id])
        return

    # Get message to broadcast
    parts = msg_text.split(maxsplit=1)
    if len(parts) < 2:
        cl.direct_send("⚠️ Please provide a message to broadcast.", [sender_id])
        return
    broadcast_message = parts[1]

    # Get all users known to the bot
    user_ids = list(user_roles.keys())
    if not user_ids:
        cl.direct_send("⚠️ No users found to broadcast.", [sender_id])
        return

    # Send broadcast
    cl.direct_send("📢 Broadcast started... ✨", [sender_id])
    success_count = 0
    for uid in user_ids:
        try:
            cl.direct_send(f"📣 Message from Admin:\n\n{broadcast_message}", [uid])
            success_count += 1
            time.sleep(0.5)  # prevent spamming too fast
        except Exception as e:
            print(f"❌ Failed to send to {uid}: {e}")

    cl.direct_send(f"✅ Broadcast completed! Sent to {success_count} users.", [sender_id])
