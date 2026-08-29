# Keep-alive so the listener survives restarts

`watch.sh` restarts `relay.py` if the process dies. After a computer reboot, nothing starts `watch.sh` unless you add a keep-alive.

## Grok Bot scheduled routine

Create a **scheduled** routine that runs `./ensure-up.sh` in the kit directory.

Stay quiet if the listener is already up. Only message the owner if it could not be started.

Discord pings can arrive any day, including weekends. A several-times-daily cadence works: 08:15, 12:15, 16:15, and 20:15 local, all seven days.

### Example routine prompt

```
Check that the Discord relay listener is running on this computer.

If watch.sh or relay.py is not running in the kit directory, run ./ensure-up.sh from that directory (venv python, not system python). Confirm relay.log recently shows "ready".

Stay quiet if the listener is already up. Only message the owner if the listener could not be started.
```

## Optional cron

```
@reboot /path/to/discord-grok-bot-kit/ensure-up.sh
15 8,12,16,20 * * * /path/to/discord-grok-bot-kit/ensure-up.sh
```
