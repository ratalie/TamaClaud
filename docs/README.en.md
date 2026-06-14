<div align="center">

![TamaClaud](../assets/banner.svg)

**A Tamagotchi that lives in your Claude Code status line.**
**Feed it tool calls. Stop coding and it dies. Then it haunts you.** 💀

🌐 [English](./README.en.md) · [Español](./README.es.md) · [Português](./README.pt.md)

</div>

---

## The pitch

You open Claude Code. A little egg hatches in your status line. Every tool call feeds it. It dances when things work, panics when they fail.

Then you go to a meeting. Two hours later it's starving. Four hours later it's dead, and your death counter ticks up one. It remembers. Forever.

Come back and it resurrects as an egg — but the scars stay in the JSON.

```
🐣 (^‿^) hp:██████░░░░ 60%  |  💀 deaths: 2  |  🍖 calls: 147
```

## States

| | Sprite | When |
|---|---|---|
| 🥚 Egg | `(·)` | First run / resurrecting |
| 😴 Sleeping | `(-.-)zzz` | Claude is thinking |
| 😊 Happy | `(^‿^)` | Idle, all good |
| 🍖 Eating | `(°ᴗ°)♪` | Tool call in progress |
| 🎉 Dancing | `\(^o^)/` | Tool success |
| 😰 Stressed | `(ó﹏ò)` | Tool failure |
| 😱 Hungry | `(×_×)` | No coding for 2h |
| 💀 Dead | `(x_x)` | No coding for 4h |
| 👻 Ghost | `(†_†)` | Waiting for resurrection |

## Install

1. Copy the script to your Claude directory:

```bash
cp tamaclaud.py ~/.claude/tamaclaud.py
```

2. Add hooks and statusLine to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "hooks": [{
          "type": "command",
          "command": "python3 ~/.claude/tamaclaud.py --event pre_tool"
        }]
      }
    ],
    "PostToolUse": [
      {
        "hooks": [{
          "type": "command",
          "command": "python3 ~/.claude/tamaclaud.py --event post_tool --success $CLAUDE_TOOL_SUCCESS"
        }]
      }
    ],
    "Stop": [
      {
        "hooks": [{
          "type": "command",
          "command": "python3 ~/.claude/tamaclaud.py --event stop"
        }]
      }
    ]
  },
  "statusLine": {
    "type": "command",
    "command": "python3 ~/.claude/tamaclaud.py --status"
  }
}
```

3. Done! Open Claude Code and start coding to feed your TamaClaud.

> **Windows tip:** use absolute paths like `python3 "C:/Users/you/.claude/tamaclaud.py" --status` instead of `~`.

## How life works

```
Each successful tool call    → +10 hp
Each tool failure            → -5 hp
No activity for 30 min       → -1 hp per minute
No activity for 2h           → HUNGRY
No activity for 4h           → DEAD (death counter +1)
New session while dead       → resurrection (back at 50 hp)
hp hits 0                    → instant DEATH
```

## Change the language

English by default. Switch any time:

```bash
python3 ~/.claude/tamaclaud.py --lang es   # Español
python3 ~/.claude/tamaclaud.py --lang pt   # Português
python3 ~/.claude/tamaclaud.py --lang en   # English
```

## State file

Saved at `~/.claude/tamaclaud.json`:

```json
{
  "hp": 80,
  "state": "happy",
  "last_activity": "2026-06-13T10:30:00+00:00",
  "deaths": 2,
  "total_tool_calls": 147,
  "born": "2026-06-01T09:00:00+00:00",
  "lang": "en"
}
```

## Manual usage (debug)

```bash
# Show status
python3 ~/.claude/tamaclaud.py --status

# Simulate events
python3 ~/.claude/tamaclaud.py --event pre_tool
python3 ~/.claude/tamaclaud.py --event post_tool --success true
python3 ~/.claude/tamaclaud.py --event post_tool --success false
python3 ~/.claude/tamaclaud.py --event stop
```

## ⚠️ Windows note

There's a [known bug in Claude Code on Windows](https://github.com/anthropics/claude-code/issues/66455) where custom `statusLine` commands never get invoked. The hooks (feeding, life, death) all work — only the always-on status bar doesn't render yet. **Workaround:** type `tamaclaud` in the CLI to check on your pet.

## 🔒 Security & privacy

Everything stays local. No network calls. No telemetry. Nothing leaves your machine, ever. The state file holds only: hp, state name, timestamps, death count, call count. No code, no paths, no personal data.

## FAQ

**Does it need a config file?**
Just one JSON it manages itself. You never touch it.

**What happens if it dies while I'm asleep?**
It becomes a ghost. When you come back and code, it resurrects as an egg at 50 hp. The death stays on its record.

**Can I have more than one?**
One pet, one machine. Like real responsibility.

**Why "TamaClaud"?**
You know exactly why.

## Requirements

- Python 3.6+ (no external dependencies)
- Claude Code with hooks and status line support
