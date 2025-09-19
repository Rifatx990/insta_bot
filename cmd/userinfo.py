# ------------------- CMD INFO -------------------
info = {
    "name": "userinfo",
    "author": "RIFAT",
    "usage": "/userinfo [username]",
    "example": "/userinfo instagram",
    "admin_only": False  # Accessible to all users
}

def run(cl, cmd_flags, cmd_name):
    """
    Fetch and display Instagram user info in a stylish DM.
    Usage: /userinfo [username]
    Accessible to all users.
    """
    # Fetch last DM
    threads = cl.direct_threads(amount=5)
    if not threads:
        return
    msg = threads[0].messages[0]
    sender_id = msg.user_id
    msg_text = (msg.text or "").strip()

    if not msg_text.lower().startswith("/userinfo"):
        return

    parts = msg_text.split()
    if len(parts) < 2:
        cl.direct_send("⚠️ Usage: /userinfo [username]", [sender_id])
        return

    username = parts[1]

    try:
        user_info = cl.user_info_by_username(username)
    except Exception as e:
        cl.direct_send(f"❌ Failed to fetch info for '{username}': {e}", [sender_id])
        return

    # Build a stylish response
    response = (
        "╔════════════════════╗\n"
        f"║ 👤 USER INFO: {username} ║\n"
        "╠════════════════════╣\n"
        f"║ Full Name     : {user_info.full_name}\n"
        f"║ User ID       : {user_info.pk}\n"
        f"║ Followers     : {user_info.follower_count}\n"
        f"║ Following     : {user_info.following_count}\n"
        f"║ Bio           : {user_info.biography or 'N/A'}\n"
        f"║ Private       : {'Yes' if user_info.is_private else 'No'}\n"
        f"║ Verified      : {'Yes' if user_info.is_verified else 'No'}\n"
        f"║ Profile Pic   : {user_info.profile_pic_url}\n"
        "╚════════════════════╝\n"
        "✨ Developed by RIFAT"
    )

    cl.direct_send(response, [sender_id])
