import time

# ---------------- CMD META ----------------
AUTHOR = "RIFAT"
USAGE = "/autoreact [on/off] [emoji]"
EXAMPLE = "/autoreact on 😍"

def run(cl, cmd_flags, cmd_name):
    """
    Auto react to posts with a chosen emoji when /autoreact on [emoji] is used.
    Turns off when /autoreact off is used.
    """
    print(f"🚀 CMD '{cmd_name}' started.")

    # Default emoji
    emoji = "❤️"

    while cmd_flags[cmd_name]:
        try:
            # Get last 5 posts from timeline
            posts = cl.timeline_feed(amount=5)

            for post in posts:
                if not cmd_flags[cmd_name]:
                    break

                media_id = post.dict().get("id")
                if not media_id:
                    continue

                # Get custom emoji from flags (if set)
                if isinstance(cmd_flags[cmd_name], str):
                    emoji = cmd_flags[cmd_name]

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
