# ------------------- CMD INFO -------------------
info = {
    "name": "hashtag",
    "author": "RIFAT",
    "usage": "/hashtag [tag]",
    "example": "/hashtag nature",
    "admin_only": False  # Accessible to all users
}

def run(cl, cmd_flags, cmd_name):
    """
    Fetch recent posts from a given hashtag.
    Usage: /hashtag [tag]
    Accessible to all users.
    """
    # Fetch last DM
    threads = cl.direct_threads(amount=5)
    if not threads:
        return
    msg = threads[0].messages[0]
    sender_id = msg.user_id
    msg_text = (msg.text or "").strip()

    if not msg_text.lower().startswith("/hashtag"):
        return

    parts = msg_text.split()
    if len(parts) < 2:
        cl.direct_send("⚠️ Usage: /hashtag [tag]", [sender_id])
        return

    tag = parts[1]

    try:
        medias = cl.hashtag_medias_recent(tag, amount=5)
    except Exception as e:
        cl.direct_send(f"❌ Failed to fetch posts for '#{tag}': {e}", [sender_id])
        return

    if not medias:
        cl.direct_send(f"⚠️ No recent posts found for '#{tag}'", [sender_id])
        return

    response = f"╔════════════════════╗\n"
    response += f"║ 📌 Recent posts for #{tag} ║\n"
    response += "╠════════════════════╣\n"

    for idx, media in enumerate(medias, start=1):
        response += f"║ {idx}. Likes: {media.like_count}, Comments: {media.comment_count}\n"
        response += f"║ URL: {media.code}\n"

    response += "╚════════════════════╝\n"
    response += "✨ Developed by RIFAT"

    cl.direct_send(response, [sender_id])
