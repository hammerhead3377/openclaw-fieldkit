# Troubleshooting — Symptom First

| Symptom                              | Station   | Quick Action                              |
|--------------------------------------|-----------|-------------------------------------------|
| Bot is silent in Telegram            | S3, S7    | Check token, restart gateway              |
| "401 Unauthorized"                   | S4        | Re-issue API key                          |
| Gateway won't start                  | S5        | `journalctl -u openclaw`                  |
| Responses wrong / no personality     | S6        | Check identity file                       |
| Local model fails to load            | S0, S5    | RAM too low — switch tier                 |
| Stuck in loop                        | S7        | Restore from S8 snapshot                  |

See **Five-Zone Diagnostic** in full manual.
