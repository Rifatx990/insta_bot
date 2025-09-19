# ------------------- CMD INFO -------------------
info = {
    "name": "role",
    "author": "RIFAT",
    "usage": "/role add [username] [1-or-2]",
    "example": "/role add john_doe 2",
    "admin_only": True  # Only adminbot can access
}

def run(cl, cmd_flags, cmd_name):
    """
    DM command to update user role.
    Usage: /role add [username] [1-or-2]
    Only accessible by adminbot.
    """
    import time
    from main import ADMIN_BOT, user_roles, ROLE_ADMIN, ROLE_USER, cl as main_cl

    # Fetch last DM
    threads = cl.direct_threads(amount=5)
    if not threads:
        return
    msg = threads[0].messages[0]
    sender_id = msg.user_id
    msg_text = (msg.text or "").strip()

    # Only respond to /role commands
    if not msg_text.lower().startswith("/role"):
        return

    # Verify sender is admin bot
    sender_info = main_cl.user_info(sender_id)
    if sender_info.username != ADMIN_BOT:
        cl.direct_send("❌ You are not authorized to use this command. Admin only.", [sender_id])
        return

    parts = msg_text.split()
    if len(parts) != 4 or parts[1].lower() != "add":
        cl.direct_send("⚠️ Invalid usage! Example: /role add username 2", [sender_id])
        return

    target_username = parts[2]
    try:
        new_role = int(parts[3])
        if new_role not in [1, 2]:
            raise ValueError
    except ValueError:
        cl.direct_send("⚠️ Role must be 1 (User) or 2 (Admin).", [sender_id])
        return

    # Find user ID from username
    try:
        target_user = main_cl.user_info_by_username(target_username)
        target_id = target_user.pk
    except Exception as e:
        cl.direct_send(f"❌ User '{target_username}' not found: {e}", [sender_id])
        return

    # Update role
    user_roles[target_id] = new_role
    role_name = "Admin" if new_role == ROLE_ADMIN else "User"

    # Stylish confirmation
    response = (
        "╔════════════════════╗\n"
        "║ ✅ ROLE UPDATED ║\n"
        "╠════════════════════╣\n"
        f"║ Username : {target_username}\n"
        f"║ New Role : {role_name}\n"
        "╚════════════════════╝\n"
        "✨ Developed by RIFAT"
    )
    cl.direct_send(response, [sender_id])
