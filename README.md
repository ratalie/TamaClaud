# 🥚 TamaClaud

**A Tamagotchi living in your Claude Code status line. Feed it tool calls. Stop coding and it dies.** 💀

Un Tamagotchi en la status line de Claude Code. Se alimenta de tool calls. Si no codeas, se muere. 💀

Um Tamagotchi na status line do Claude Code. Se alimenta de tool calls. Se você não codar, ele morre. 💀

```
🐣 (^‿^) vida:██████░░░░ 60%  |  💀 muertes: 2  |  🍖 calls: 147
```

---

**🌐 Language / Idioma / Língua:**

[![English](https://img.shields.io/badge/English-blue?style=for-the-badge)](./docs/README.en.md)
[![Español](https://img.shields.io/badge/Español-red?style=for-the-badge)](./docs/README.es.md)
[![Português](https://img.shields.io/badge/Português-green?style=for-the-badge)](./docs/README.pt.md)

---

## Quick Start

```bash
cp tamaclaud.py ~/.claude/tamaclaud.py
```

Then add hooks to `~/.claude/settings.json` — full instructions in your language above ☝️

---

## ⚠️ Windows Note

There's a [known bug in Claude Code on Windows](https://github.com/anthropics/claude-code/issues/66455) where custom `statusLine` commands are never invoked automatically. The hooks (feeding/life mechanics) work fine, but the persistent status bar won't render until this is fixed upstream.

**Workaround:** type `tamaclaud` in the Claude Code CLI to check on your pet manually.

---

## 🚧 VS Code Extension — WIP

A VS Code extension that shows TamaClaud in the status bar is coming soon. Stay tuned.

---

## 🤝 Contributing

PRs welcome! New languages, sprites, features, bug fixes — all good. See [CONTRIBUTING.md](./CONTRIBUTING.md).
