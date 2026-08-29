#!/usr/bin/env python3
"""Forward the owner's Discord mentions of this bot to a Grok Bot webhook."""
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

try:
    import discord
except ImportError:
    sys.stderr.write("discord.py missing — install from requirements.txt into a venv\n")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent
CFG = ROOT / "config.env"
LOG = ROOT / "relay.log"
LAST = ROOT / "last.json"


def log(msg: str) -> None:
    line = time.strftime("%Y-%m-%d %H:%M:%S ") + msg
    with LOG.open("a") as f:
        f.write(line + "\n")


def load_env(path: Path) -> dict:
    out = {}
    if not path.exists():
        return out
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def cfg(env: dict, key: str, default: str = "") -> str:
    return env.get(key) or os.environ.get(key) or default


env = load_env(CFG)
TOKEN = cfg(env, "DISCORD_BOT_TOKEN")
CHANNEL_ID = int(cfg(env, "DISCORD_CHANNEL_ID") or "0")
USER_ID = int(cfg(env, "DISCORD_USER_ID") or "0")
WEBHOOK_URL = cfg(env, "GROK_WEBHOOK_URL")
WEBHOOK_KEY = cfg(env, "GROK_WEBHOOK_KEY")
BOT_NAME = cfg(env, "BOT_NAME", "bot").strip().lstrip("@").lower()
if not TOKEN or not CHANNEL_ID or not USER_ID or not WEBHOOK_URL or not WEBHOOK_KEY:
    log("config incomplete")
    sys.exit(1)

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
client = discord.Client(intents=intents)


def post_webhook(payload: dict) -> int:
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        WEBHOOK_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + WEBHOOK_KEY,
            "User-Agent": "GrokBotDiscordRelay/1.0",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        resp.read()
        return resp.status


def is_addressed(message: discord.Message) -> bool:
    text = (message.content or "").strip()
    low = text.lower()
    mentioned = client.user is not None and client.user in message.mentions
    named = low.startswith(BOT_NAME) or low.startswith("@" + BOT_NAME)
    role_named = any(r.name.lower() == BOT_NAME for r in message.role_mentions)
    return mentioned or named or role_named


@client.event
async def on_ready():
    log(f"ready {client.user} channel={CHANNEL_ID}")


@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if message.channel.id != CHANNEL_ID:
        return
    if message.author.id != USER_ID:
        return
    if not is_addressed(message):
        log(f"skip no-mention id={message.id}")
        return
    try:
        await message.add_reaction("\N{ROBOT FACE}")
        log(f"acked {message.id} react=robot")
    except Exception as e:
        log(f"ack failed {type(e).__name__}")
    payload = {
        "source": "discord",
        "text": (message.content or "").strip(),
        "author_id": str(message.author.id),
        "author": str(message.author),
        "channel_id": str(message.channel.id),
        "message_id": str(message.id),
    }
    LAST.write_text(json.dumps(payload, indent=2))
    try:
        status = post_webhook(payload)
        log(f"forwarded {message.id} http={status}")
    except Exception as e:
        log(f"forward failed {type(e).__name__}")


client.run(TOKEN)
