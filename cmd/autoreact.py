info = {
    "author": "RIFAT",
    "usage": "/autoreact [on/off] [emoji]",
    "example": "/autoreact on 🎀",
    "description": "Automatically reacts to latest timeline posts with a chosen emoji."
}

import time

def run(cl, cmd_flags, cmd_name):
    """
    Auto react to latest posts in timeline with the emoji sent in DM.
    /autoreact on [emoji] to start
    /autoreact off to stop
    """
    print(f"🚀 CMD '{cmd_name}' started.")

    while cmd_flags[cmd_name]:
        try:
            # Determine emoji
            emoji = cmd_flags[cmd_name] if isinstance(cmd_flags[cmd_name], str) else "❤️"

            # Get last 5 posts from timeline
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

                time.sleep(5)  # wait a bit before next

        except Exception as e:
            print(f"⚠️ Error in autoreact: {e}")
            time.sleep(15)

    print(f"🛑 CMD '{cmd_name}' stopped.")
