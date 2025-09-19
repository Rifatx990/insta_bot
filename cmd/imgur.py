# ------------------- CMD INFO -------------------
info = {
    "name": "imgur",
    "author": "rifat",
    "usage": "/imgur (reply to an image)",
    "example": "/imgur",
    "admin_only": False,  # accessible to all users
    "description": {
        "en": "Upload a replied image to Imgur and get the link"
    }
}

import requests
import os

# ------------------- IMGUR CONFIG -------------------
IMGUR_CLIENT_ID = "806aba6e4de9142"  # Put your Imgur client ID here

def run(cl, cmd_flags, cmd_name):
    """
    Upload an image to Imgur from a replied message.
    Usage: Reply to an image with /imgur
    """
    # Get the last DM
    threads = cl.direct_threads(amount=5)
    if not threads:
        return
    msg = threads[0].messages[0]
    sender_id = msg.user_id
    msg_text = (msg.text or "").strip()

    if not msg_text.lower().startswith("/imgur"):
        return

    # Check if the message is a reply with an image
    reply_attachments = getattr(msg, "attachments", None)
    if not reply_attachments or len(reply_attachments) == 0:
        cl.direct_send("⚠️ Please reply to an image to upload it to Imgur.", [sender_id])
        return

    image_url = reply_attachments[0].url
    if not image_url:
        cl.direct_send("⚠️ Could not find image URL.", [sender_id])
        return

    # Notify user that upload is in progress
    cl.direct_send("⏳ Uploading image to Imgur...", [sender_id])

    try:
        # Download the image
        resp = requests.get(image_url)
        if resp.status_code != 200:
            cl.direct_send("❌ Failed to download the image.", [sender_id])
            return

        # Save temporarily
        temp_path = os.path.join(os.path.dirname(__file__), "temp_image.jpg")
        with open(temp_path, "wb") as f:
            f.write(resp.content)

        # Upload to Imgur
        with open(temp_path, "rb") as f:
            headers = {"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"}
            response = requests.post("https://api.imgur.com/3/upload", headers=headers, files={"image": f})
            data = response.json()

        # Remove temp file
        os.remove(temp_path)

        # Check response
        if data.get("success"):
            imgur_link = data["data"]["link"]
            cl.direct_send(f"✅ Successfully Uploaded:\n{imgur_link}", [sender_id])
        else:
            cl.direct_send("❌ Failed to upload image to Imgur.", [sender_id])

    except Exception as e:
        cl.direct_send(f"❌ An error occurred: {e}", [sender_id])
