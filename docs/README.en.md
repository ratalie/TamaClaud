# 🥚 TamaClaud

A Tamagotchi living in your Claude Code status line. Feed it tool calls. Stop coding and it dies.

```
🐣 (^‿^) hp:██████░░░░ 60%  |  💀 deaths: 2  |  🍖 calls: 147
```

## States

| State | Sprite | When |
|-------|--------|------|
| 🥚 Egg | `(·)` | First run / resurrecting |
| 😴 Sleeping | `(-.-)zzz` | Claude is thinking |
| 😊 Happy | `(^‿^)` | Idle, all good |
| 🍖 Eating | `(°ᴗ°)♪` | Tool call in progress |
| 🎉 Dancing | `\(^o^)/` | Tool success |
| 😰 Stressed | `(ó﹏ò)` | Tool failure |
| 😱 Hungry | `(×_×)` | No coding for 2h |
| 💀 Dead | `(x_x)` | No coding for 4h |
| 👻 Ghost | `(†_†)` | Waiting for resurrection |

## Installation

1. Copy the script to your Claude directory:

```bash
cp tamaclaud.py ~/.claude/tamaclaud.py
```

2. Add hooks to `~/.claude/settings.json`:

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

## Life mechanics

- **max_hp**: 100
- Each successful tool call: **+10 hp**
- Each tool failure: **-5 hp**
- No activity for 30 min: **-1 hp per minute**
- No activity for 2h: **HUNGRY** state
- No activity for 4h: **DEAD** state
- Starting a new session while dead: **resurrection** (comes back with 50 hp)
- HP reaches 0: **instant DEATH**

## State file

Saved at `~/.claude/tamaclaud.json`:

```json
{
  "vida": 80,
  "estado": "feliz",
  "ultima_actividad": "2026-06-13T10:30:00+00:00",
  "muertes": 2,
  "tool_calls_totales": 147,
  "nacimiento": "2026-06-01T09:00:00+00:00"
}
```

## Requirements

- Python 3.6+ (no external dependencies)
- Claude Code with hooks and status line support

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

## ⚠️ Windows Note

There's a [known bug in Claude Code on Windows](https://github.com/anthropics/claude-code/issues/66455) where custom `statusLine` commands are never invoked automatically. The hooks (feeding/life mechanics) still work, but the persistent status bar won't render until this is fixed upstream.

**Workaround:** type `tamaclaud` in the Claude Code CLI to check on your pet manually.
