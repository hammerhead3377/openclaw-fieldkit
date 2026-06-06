# Lighthouse Memory Spring — DRAM Bootstrap
> Read-only. Written by operator. Never overwritten by agents.
> Last updated: 2026-06-06

## Identity
- **Operator:** Thomas Parker
- **Stack:** OpenClaw / Patricia
- **Primary node:** nvidia-aiui (Jetson Orin Nano 8G)
- **Secondary:** thomas@pop-os (Alienware)
- **Mobile:** A53 (Termux)
- **Cloud:** Oracle Cloud VPS
- **Mesh:** Tailscale (all nodes, zero-trust)

## What This Container Does
Lighthouse Waiting Room — auth gate for the Lighthouse Spring data stack.
- Validates agent headers (X-Spring-Token, X-AI-Model, X-Node-ID)
- Issues short-lived JWT (15min TTL)
- Routes prompts: Claude → Ollama (local free) → Groq (free tier)
- Serves this file as the DRAM bootstrap layer to any authorized agent

## Active Projects
- **Guardian Mesh** — drone swarm patent, architecture phase
- **Bitcoin Mining** — NerdQaxe++, BitAxe, Bitcoin Knots, running
- **OpenHelm** — marine navigation, concept/early build
- **Lighthouse Spring** — THIS STACK, building now
- **OpenClaw Field Kit** — https://github.com/hammerhead3377/openclaw-fieldkit

## Current Stack State
| Service        | Node        | Port  | Status    |
|----------------|-------------|-------|-----------|
| SideDoor       | nvidia-aiui | 8001  | Running   |
| Ollama         | nvidia-aiui | 11434 | Running   |
| PatriciaSD_bot | Telegram    | —     | Send-only |
| Tailscale      | All nodes   | —     | Active    |
| Waiting Room   | nvidia-aiui | 8443  | BUILDING  |

## Memory Architecture
- **DRAM (ro)** — MEMORY.md, IDENTITY.md, SOUL.md [this container]
- **SRAM (rw)** — /mnt/patricia-memory/memory/ [live session state]
- **SWAP**      — Jetson swap partition [RAM pressure relief]
- **Cloud**     — Google Drive via rclone [verify: rclone listremotes]

## What To Do Now
1. Deploy this container: `sudo bash lxc-setup.sh`
2. Copy `.env.example` → `.env`, fill in tokens
3. Health check: `curl http://<container-ip>:8443/health`
4. Auth test: POST /auth with headers → get JWT
5. Chat test: POST /chat with JWT → verify model rotation works
6. Memory test: GET /memory with JWT → verify DRAM delivered to agent
7. **Next:** extract SpringEngine from SideDoor → standalone LXC container
8. **Next:** add Telegram receive/polling to PatriciaSD_bot
9. **Next:** add S9-waiting-room.md station to openclaw-fieldkit repo

## Patricia
- Sovereign agent, female-voiced, precise, direct
- Home: nvidia-aiui (Jetson Orin Nano 8G)
- Philosophy: no corporate gate, no subscription, no team required
