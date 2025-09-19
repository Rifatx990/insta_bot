# Instagram CMD Bot 🤖

This project is an **Instagram automation bot** that:
- Logs into Instagram (restores session if possible).
- Dynamically loads commands from the `cmd/` folder.
- Allows turning commands `on` / `off` via Instagram DMs (`/cmdname on` or `/cmdname off`).
- Exposes a **Flask API** showing bot status, loaded commands, and developer info.
- Supports optional **SOCKS5 proxy** connection (configurable directly in the code).

---

## ⚙️ Features
- Auto login with session persistence (`session.json`).
- Dynamic CMD loading from `cmd/` folder.
- Proxy support (`socks5://host:port` or with user/pass).
- Flask status API at `http://localhost:8080/`.
- Developer info shown in API (`RIFAT`).

---

## 📦 Installation

1. Clone this repo:
   ```bash
   git clone https://github.com/Rifatx990/insta_bot.git
   cd insta_bot

2. Install requirements:

pip install -r requirements.txt


3. Configure your Instagram credentials in the script:

USERNAME = "your_username"
PASSWORD = "your_password"


4. (Optional) Configure proxy inside the code:

PROXY = "socks5://127.0.0.1:9050"




---

▶️ Running the Bot

python main.py

When the bot starts:

It loads all commands from cmd/.

Prints how many commands were loaded.

Starts monitoring Instagram DMs.

Exposes Flask API at http://localhost:8080.



---

🌐 Flask API Output Example

{
  "status": "✅ Restored session as your_username",
  "developer": "RIFAT",
  "sent_count": 0,
  "logged_in_as": "your_username",
  "proxy": "Direct connection",
  "loaded_commands": 3,
  "cmds": {
    "example": "ON",
    "auto_reply": "OFF"
  }
}


---

📝 CMD Development

Place .py files in cmd/.

Each file must define a run(cl, cmd_flags, cmd_name) function.

Example cmd/echo.py:

def run(cl, cmd_flags, cmd_name):
    while cmd_flags[cmd_name]:
        print("Echo running...")



---

👨‍💻 Developer

RIFAT


---


