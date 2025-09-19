import random

# ------------------- CMD INFO -------------------
info = {
    "name": "quote",
    "author": "RIFAT",
    "usage": "/quote",
    "example": "/quote",
    "admin_only": False  # Accessible to all users
}

QUOTES = [
    "🌟 The only way to do great work is to love what you do. – Steve Jobs",
    "💡 Success is not final, failure is not fatal: It is the courage to continue that counts. – Winston Churchill",
    "🚀 Don't watch the clock; do what it does. Keep going. – Sam Levenson",
    "✨ Believe you can and you're halfway there. – Theodore Roosevelt",
    "🌈 Your limitation—it’s only your imagination. Keep pushing!"
]

def run(cl, cmd_flags, cmd_name):
    """
    Sends a random motivational quote.
    Usage: /quote
    Accessible to all users.
    """
    threads = cl.direct_threads(amount=5)
    if not threads:
        return
    msg = threads[0].messages[0]
    sender_id = msg.user_id
    msg_text = (msg.text or "").strip()

    if not msg_text.lower().startswith("/quote"):
        return

    quote = random.choice(QUOTES)

    response = (
        "╔════════════════════╗\n"
        "║ 🌟 MOTIVATIONAL QUOTE ║\n"
        "╠════════════════════╣\n"
        f"║ {quote}\n"
        "╚════════════════════╝\n"
        "✨ Developed by RIFAT"
    )

    cl.direct_send(response, [sender_id])
