import os
import shutil
import importlib.util

# ------------------- CMD INFO -------------------
info = {
    "name": "cmd",
    "author": "RIFAT",
    "usage": "/cmd [install/load/unload] [cmd_name]",
    "example": "/cmd install autoreact.py",
    "admin_only": True
}

# Folder where this cmd.py exists
cmd_folder = os.path.dirname(os.path.abspath(__file__))

def run(cl, cmd_flags, cmd_name):
    """
    DM command to install/load/unload other command modules.
    Only accessible by bot admin.
    Usage: /cmd install/load/unload [cmd_name]
    """
    import time
    print(f"🚀 CMD '{cmd_name}' started")

    # Get the last DM
    threads = cl.direct_threads(amount=5)
    if not threads:
        return
    msg = threads[0].messages[0]
    sender_id = msg.user_id
    msg_text = (msg.text or "").strip()

    parts = msg_text.split()
    if len(parts) < 2:
        cl.direct_send("⚠️ Invalid usage. Example: /cmd install autoreact.py", [sender_id])
        return

    action = parts[1].lower()
    target_cmd = parts[2] if len(parts) > 2 else None

    if not target_cmd:
        cl.direct_send("⚠️ Please specify a command name.", [sender_id])
        return

    # ------------------- INSTALL -------------------
    if action == "install":
        # Assume the uploaded cmd file is in the same folder as cmd.py
        source_path = os.path.join(cmd_folder, target_cmd)
        dest_path = os.path.join(cmd_folder, target_cmd)
        if not os.path.exists(source_path):
            cl.direct_send(f"❌ File not found in the cmd folder: {source_path}", [sender_id])
            return

        try:
            shutil.copy(source_path, dest_path)
            cl.direct_send(f"✅ Command '{target_cmd}' installed successfully in cmd folder!", [sender_id])
        except Exception as e:
            cl.direct_send(f"❌ Failed to install '{target_cmd}': {e}", [sender_id])

    # ------------------- LOAD -------------------
    elif action == "load":
        path = os.path.join(cmd_folder, target_cmd)
        cmd_name_only = target_cmd[:-3] if target_cmd.endswith(".py") else target_cmd
        try:
            if not os.path.exists(path):
                cl.direct_send(f"❌ Command file '{target_cmd}' not found.", [sender_id])
                return
            spec = importlib.util.spec_from_file_location(cmd_name_only, path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, "run") and hasattr(mod, "info"):
                from main import cmd_flags, cmd_threads, cmd_info
                cmd_flags[cmd_name_only] = False
                cmd_threads[cmd_name_only] = {"module": mod, "thread": None}
                cmd_info[cmd_name_only] = mod.info
                cl.direct_send(f"✅ Command '{cmd_name_only}' loaded successfully!", [sender_id])
            else:
                cl.direct_send(f"❌ '{target_cmd}' is not a valid command module.", [sender_id])
        except Exception as e:
            cl.direct_send(f"❌ Failed to load '{target_cmd}': {e}", [sender_id])

    # ------------------- UNLOAD -------------------
    elif action == "unload":
        cmd_name_only = target_cmd[:-3] if target_cmd.endswith(".py") else target_cmd
        from main import cmd_flags, cmd_threads, cmd_info
        if cmd_name_only in cmd_threads:
            # Stop the thread if running
            if cmd_threads[cmd_name_only]["thread"] and cmd_threads[cmd_name_only]["thread"].is_alive():
                cmd_flags[cmd_name_only] = False
                time.sleep(1)
            del cmd_flags[cmd_name_only]
            del cmd_threads[cmd_name_only]
            del cmd_info[cmd_name_only]
            cl.direct_send(f"✅ Command '{cmd_name_only}' unloaded successfully!", [sender_id])
        else:
            cl.direct_send(f"❌ Command '{cmd_name_only}' is not loaded.", [sender_id])

    else:
        cl.direct_send("⚠️ Invalid action. Use: install / load / unload", [sender_id])
