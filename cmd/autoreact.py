import time

info = {
    "author": "RIFAT",
    "usage": "/autoreact [on/off] [emoji]",
    "example": "/autoreact on ❤️",
    "description": "Auto reacts to last 5 posts on timeline with chosen emoji."
}

def run(cl, cmd_flags, cmd_name):
    print(f"🚀 CMD '{cmd_name}' started.")
    emoji = "❤️"  # default

    while cmd_flags[cmd_name]:
        # If a custom emoji is given via DM, update it
        if isinstance(cmd_flags[cmd_name], str):
            emoji = cmd_flags[cmd_name]

        try:
            posts = cl.timeline_feed(amount=5)
            for post in posts:
                if not cmd_flags[cmd_name]:
                    break

                media_id = post.dict().get("id")
                if not media_id:
                    continue

                try:
                    cl.media_like(media_id, module_name="timeline", reaction_type=emoji)
                    print(f"✅ Reacted to post {media_id} with {emoji}")
                except Exception as e:
                    print(f"⚠️ Failed to react: {e}")
                time.sleep(5)
        except Exception as e:
            print(f"⚠️ Error in autoreact: {e}")
            time.sleep(15)

    print(f"🛑 CMD '{cmd_name}' stopped.")
