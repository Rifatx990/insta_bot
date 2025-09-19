import random

# ------------------- CMD INFO -------------------
info = {
    "name": "rps",
    "author": "RIFAT",
    "usage": "/rps [rock/paper/scissors]",
    "example": "/rps rock",
    "admin_only": False  # Accessible to all users
}

def run(cl, cmd_flags, cmd_name):
    """
    Play Rock-Paper-Scissors with the bot.
    Usage: /rps [rock/paper/scissors]
    """
    threads = cl.direct_threads(amount=5)
    if not threads:
        return
    msg = threads[0].messages[0]
    sender_id = msg.user_id
    msg_text = (msg.text or "").strip().lower()

    if not msg_text.startswith("/rps"):
        return

    parts = msg_text.split()
    if len(parts) < 2:
        cl.direct_send("⚠️ Usage: /rps [rock/paper/scissors]", [sender_id])
        return

    user_choice = parts[1]
    choices = ["rock", "paper", "scissors"]
    if user_choice not in choices:
        cl.direct_send("❌ Invalid choice! Use rock, paper, or scissors.", [sender_id])
        return

    bot_choice = random.choice(choices)

    # Determine result
    if user_choice == bot_choice:
        result = "🤝 It's a tie!"
    elif (
        (user_choice == "rock" and bot_choice == "scissors") or
        (user_choice == "paper" and bot_choice == "rock") or
        (user_choice == "scissors" and bot_choice == "paper")
    ):
        result = "🎉 You win!"
    else:
        result = "💀 You lose!"

    # Stylish DM output
    response = (
        "╔════════════════════╗\n"
        "║ 🎮 ROCK-PAPER-SCISSORS ║\n"
        "╠════════════════════╣\n"
        f"║ Your choice : {user_choice.capitalize()}\n"
        f"║ Bot choice  : {bot_choice.capitalize()}\n"
        f"║ Result      : {result}\n"
        "╚════════════════════╝\n"
        "✨ Fun game by RIFAT"
    )

    cl.direct_send(response, [sender_id])
