# 🥚 TamaClaud

Um Tamagotchi que vive na status line do Claude Code. Se alimenta de tool calls. Se você não codar, ele morre.

```
🐣 (^‿^) vida:██████░░░░ 60%  |  💀 mortes: 2  |  🍖 calls: 147
```

## Estados

| Estado | Sprite | Quando |
|--------|--------|--------|
| 🥚 Ovo | `(·)` | Primeira vez / ressuscitando |
| 😴 Dormindo | `(-.-)zzz` | Claude está pensando |
| 😊 Feliz | `(^‿^)` | Idle, tudo bem |
| 🍖 Comendo | `(°ᴗ°)♪` | Tool call em progresso |
| 🎉 Dançando | `\(^o^)/` | Tool success |
| 😰 Estressado | `(ó﹏ò)` | Tool failure |
| 😱 Faminto | `(×_×)` | Sem codar há 2h |
| 💀 Morto | `(x_x)` | Sem codar há 4h |
| 👻 Fantasma | `(†_†)` | Esperando ressurreição |

## Instalação

1. Copie o script para o diretório do Claude:

```bash
cp tamaclaud.py ~/.claude/tamaclaud.py
```

2. Adicione os hooks em `~/.claude/settings.json`:

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

3. Pronto! Abra o Claude Code e comece a codar para alimentar seu TamaClaud.

## Mecânica de vida

- **vida_max**: 100
- Cada tool call bem-sucedido: **+10 vida**
- Cada tool failure: **-5 vida**
- Sem atividade por 30 min: **-1 vida por minuto**
- Sem atividade por 2h: estado **FAMINTO**
- Sem atividade por 4h: estado **MORTO**
- Ao iniciar nova sessão se estiver morto: **ressurreição** (volta com 50 de vida)
- Vida chega a 0: **MORTE instantânea**

## Arquivo de estado

Salvo em `~/.claude/tamaclaud.json`:

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

## Requisitos

- Python 3.6+ (sem dependências externas)
- Claude Code com suporte a hooks e status line

## Uso manual (debug)

```bash
# Ver status
python3 ~/.claude/tamaclaud.py --status

# Simular eventos
python3 ~/.claude/tamaclaud.py --event pre_tool
python3 ~/.claude/tamaclaud.py --event post_tool --success true
python3 ~/.claude/tamaclaud.py --event post_tool --success false
python3 ~/.claude/tamaclaud.py --event stop
```

## ⚠️ Nota sobre Windows

Há um [bug conhecido no Claude Code no Windows](https://github.com/anthropics/claude-code/issues/66455) onde o `statusLine` custom nunca é invocado automaticamente. Os hooks (alimentar/mecânica de vida) funcionam bem, mas a barra persistente não renderiza até que isso seja corrigido upstream.

**Workaround:** digite `tamaclaud` no CLI do Claude Code para ver seu pet manualmente.
