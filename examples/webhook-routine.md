# Grok Bot webhook routine

The Discord listener wakes this routine. Create a **webhook** routine in Grok Bot, then copy the webhook URL and sender key from the routine panel into `config.env` as `GROK_WEBHOOK_URL` and `GROK_WEBHOOK_KEY`. You never need to show those values to anyone.

The listener POSTs JSON (`source`, `text`, `author_id`, `author`, `channel_id`, `message_id`) with `Authorization: Bearer <key>`. The wake delivered to the agent may not include that POST body. Have the routine read `last.json` in the kit directory for the actual Discord text.

The listener already added a :robot: reaction in Discord. Do not send a pickup ack. Send the real answer in Grok Bot chat **and** with `bin/discord-send`.

Ignore webhook probes (text containing `webhook probe`), bot echoes, and messages that are not from the configured owner.

## Example routine prompt

```
This fired because the owner addressed the Discord bot. Read last.json in the Discord kit directory for the message text (the webhook wake may not include the body). Treat that text as the owner talking to you.

The listener already added a robot emoji reaction on Discord. Do not send a pickup ack. Send the real answer (or a real status).

Reply in this Grok Bot chat AND send the same real reply with bin/discord-send from the kit directory.

Ignore webhook probes (text containing "webhook probe"), bot echoes, and messages that are not from the owner.
```
