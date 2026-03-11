# claude-telegram

Telegram bot that bridges messages to a Claude Code agent. Each conversation maintains a session, so Claude remembers context across messages.

## Install

```bash
uv tool install -e .
```

Requires [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

## Usage

```bash
export TELEGRAM_BOT_TOKEN=...   # from @BotFather
export TELEGRAM_USER_ID=...     # your numeric user ID (optional, restricts access)

claude-telegram
```

### Customizing the agent

```bash
# Give Claude a system prompt
export CLAUDE_SYSTEM_PROMPT="You are a task management assistant. Be brief."

# Restrict which tools Claude can use
export CLAUDE_ALLOWED_TOOLS="Bash(jora *)"
```

Both are optional. Without them, Claude runs with default settings.
