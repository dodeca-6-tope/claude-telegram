# claude-telegram

Telegram bot that bridges messages to a Claude Code agent. Each conversation maintains a session, so Claude remembers context across messages.

## Install

```bash
curl -fsSL https://raw.githubusercontent.com/dodeca-6-tope/claude-telegram/main/setup.sh | bash
```

Requires [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

## Usage

```bash
export TELEGRAM_BOT_TOKEN=...   # from @BotFather
export TELEGRAM_USER_ID=...     # your numeric user ID (optional, restricts access)

claude-telegram
```

### Options

```
--name              session name, persisted at /tmp/claude-telegram/<name> (default: default)
--system-prompt     system prompt for the agent
--allowed-tools     tools the agent can use (e.g. "Bash(jora *)")
```

Example:

```bash
claude-telegram --name jora --system-prompt "Be brief." --allowed-tools "Bash(jora *)"
```
