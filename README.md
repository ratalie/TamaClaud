<div align="center">

![TamaClaud](./assets/banner.svg)

**A Tamagotchi that lives in your Claude Code status line.**
**Feed it tool calls. Stop coding and it dies. Then it haunts you.** 💀

🌐 [English](./docs/README.en.md) · [Español](./docs/README.es.md) · [Português](./docs/README.pt.md)

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

The most effort TamaClaud will ever ask of you:

```bash
cp tamaclaud.py ~/.claude/tamaclaud.py
```

Then add hooks + statusLine to `~/.claude/settings.json` — full snippet in the [docs](./docs/README.en.md). That's it. It's born.

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

---

## ⚠️ Windows note

There's a [known bug in Claude Code on Windows](https://github.com/anthropics/claude-code/issues/66455) where custom `statusLine` commands never get invoked. The hooks (feeding, life, death) all work — only the always-on status bar doesn't render yet. **Workaround:** type `tamaclaud` in the CLI to check on your pet.

## 🚧 VS Code extension — WIP

A cross-platform VS Code extension is on the roadmap. [Want to build it?](https://github.com/ratalie/TamaClaud/issues)

## 🤝 Contributing

PRs welcome — new languages, sprites, features, fixes. See [CONTRIBUTING.md](./CONTRIBUTING.md).

## 🔒 Security & privacy

Everything stays local. No network calls. No telemetry. Nothing leaves your machine, ever.

- **Atomic writes** — saves to `.tmp` then renames, no corruption from concurrent hooks
- **File permissions** — `chmod 600` on Unix, owner-only
- **stdin limit** — reads max 64KB, no memory surprises
- **Input validation** — only known events accepted, state validated on load
- **Zero dependencies** — pure Python stdlib, no supply chain

The state file holds only: hp, state name, timestamps, death count, call count. No code, no paths, no personal data.

---

## FAQ

**Does it need a config file?**
Just one JSON it manages itself. You never touch it.

**What happens if it dies while I'm asleep?**
It becomes a ghost. When you come back and code, it resurrects as an egg at 50 hp. The death stays on its record.

**Can I have more than one?**
One pet, one machine. Like real responsibility.

**Why does it eat tool calls?**
Because that's how it knows you're alive too.

**Why "TamaClaud"?**
You know exactly why.

## License

MIT. The shortest license that keeps it alive.
