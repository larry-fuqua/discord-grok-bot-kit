# Discord ↔ Grok Bot drop-in kit

A small Unix kit: a Discord bot listener, an instant :robot: reaction on the owner's message, a webhook wake into a Grok Bot routine, outbound replies as the bot, and a keep-alive so the listener comes back after crashes or computer restarts.

It wakes only when the **owner** addresses the bot: an @mention of the bot user, a role whose name equals `BOT_NAME`, or a line starting with `BOT_NAME` / `@BOT_NAME`. Not every message.

## What you get

- `relay.py` — discord.py listener (owner + channel + address filters)
- `watch.sh` — restart loop if the listener process dies
- `ensure-up.sh` — start `watch.sh` if it is not running
- `bin/discord-send` — POST a reply as the bot (stdlib only)
- `examples/webhook-routine.md` — Grok Bot webhook routine to create
- `examples/keep-alive-routine.md` — scheduled check after restarts

## Prerequisites

Python 3, a Discord account, and Grok Bot.

## Setup

1. Create a Discord app and bot at [discord.com/developers/applications](https://discord.com/developers/applications). Copy the bot token. Under Bot, enable the **Message Content Intent** (privileged).

2. Invite the bot. Use the OAuth2 URL generator, scope `bot`, permissions **View Channel**, **Send Messages**, **Read Message History**, and **Add Reactions** (bitmask `68672`):

   `https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=68672&integration_type=0&scope=bot`

3. Optional: create a Discord role named exactly `BOT_NAME` so an @role mention also wakes the bot.

4. Create a Grok Bot **webhook** routine (see [examples/webhook-routine.md](examples/webhook-routine.md)). Copy the webhook URL and sender key from the routine panel into `config.env`.

5. Copy `config.env.example` to `config.env` and fill in `BOT_NAME`, the bot token, the channel id, the owner's Discord user id, and the webhook URL/key. Enable Discord Developer Mode to copy channel and user ids (right-click → Copy ID). Never commit `config.env`.

6. Install:

   ```
   python3 -m venv venv
   ./venv/bin/pip install -r requirements.txt
   chmod +x watch.sh ensure-up.sh bin/discord-send relay.py
   ```

7. Start:

   ```
   ./ensure-up.sh
   ```

   Confirm `relay.log` contains `ready`.

8. Test: the owner @mentions the bot in the configured channel. Discord should get an instant :robot: reaction and the Grok Bot routine should fire.

9. Outbound reply from the kit directory:

   ```
   bin/discord-send "hello"
   ```

   Or set `DISCORD_RELAY_DIR` to the kit path and call `bin/discord-send` from anywhere.

10. Keep-alive after computer restarts: [examples/keep-alive-routine.md](examples/keep-alive-routine.md).

## Wake rules

The listener ignores bots, other channels, and anyone except `DISCORD_USER_ID`. It then requires one of:

- @mention of the bot user
- a role mention whose role name equals `BOT_NAME` (case-insensitive)
- message text starting with `BOT_NAME` or `@BOT_NAME` (case-insensitive)

## Security

Do not commit `config.env`, `last.json`, or `relay.log`. The bot token and webhook key are secrets; rotate them if they leak. The webhook key is sent as a bearer token.
