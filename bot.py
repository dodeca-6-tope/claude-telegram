"""Telegram bot that bridges messages to a Claude Code agent."""

import argparse
import json
import os
import subprocess
import sys
import threading
from pathlib import Path

import telebot

_env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
_lock = threading.Lock()


def _ask_agent(text: str, cmd: list[str], cwd: Path) -> str:
    with _lock:
        result = subprocess.run(
            cmd + ["--", text], capture_output=True, text=True, env=_env, cwd=cwd
        )
        if result.returncode != 0:
            return f"Error: {result.stderr.strip() or 'unknown failure'}"
        try:
            data = json.loads(result.stdout)
            return data.get("result", result.stdout.strip())
        except json.JSONDecodeError:
            return result.stdout.strip() or "(no response)"


def main():
    parser = argparse.ArgumentParser(description="Telegram bot → Claude Code agent")
    parser.add_argument("--name", default="claude-telegram", help="session name (default: claude-telegram)")
    parser.add_argument("--system-prompt", help="system prompt for the agent")
    parser.add_argument("--allowed-tools", help='tools the agent can use (e.g. "Bash(jora *)")')
    args = parser.parse_args()

    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Set TELEGRAM_BOT_TOKEN environment variable", file=sys.stderr)
        sys.exit(1)

    allowed_user = os.environ.get("TELEGRAM_USER_ID")

    cwd = Path("/tmp") / args.name
    cwd.mkdir(exist_ok=True)

    cmd = ["claude", "-p", "--output-format", "json", "--continue"]
    if args.system_prompt:
        cmd += ["--append-system-prompt", args.system_prompt]
    if args.allowed_tools:
        cmd += ["--allowedTools", args.allowed_tools]

    bot = telebot.TeleBot(token)

    @bot.message_handler(content_types=["text"])
    def handle(message):
        if allowed_user and str(message.from_user.id) != allowed_user:
            return
        stop = threading.Event()

        def typing_loop():
            while not stop.is_set():
                bot.send_chat_action(message.chat.id, "typing")
                stop.wait(3)

        t = threading.Thread(target=typing_loop, daemon=True)
        t.start()
        try:
            reply = _ask_agent(message.text, cmd, cwd)
        except Exception as e:
            reply = f"Error: {e}"
        finally:
            stop.set()
            t.join()
        bot.reply_to(message, reply)

    print(f"Bot started (session: {cwd})")
    bot.infinity_polling()


if __name__ == "__main__":
    main()
