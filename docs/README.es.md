# 🥚 TamaClaud

Un Tamagotchi que vive en la status line de Claude Code. Se alimenta de tool calls. Si no codeas, se muere.

```
🐣 (^‿^) vida:██████░░░░ 60%  |  💀 muertes: 2  |  🍖 calls: 147
```

## Estados

| Estado | Sprite | Cuándo |
|--------|--------|--------|
| 🥚 Huevo | `(·)` | Primera vez / resucitando |
| 😴 Durmiendo | `(-.-)zzz` | Claude está pensando |
| 😊 Feliz | `(^‿^)` | Idle, todo bien |
| 🍖 Comiendo | `(°ᴗ°)♪` | Tool call en progreso |
| 🎉 Bailando | `\(^o^)/` | Tool success |
| 😰 Estresado | `(ó﹏ò)` | Tool failure |
| 😱 Hambre | `(×_×)` | Sin codear hace 2hs |
| 💀 Muerto | `(x_x)` | Sin codear hace 4hs |
| 👻 Fantasma | `(†_†)` | Esperando resurrección |

## Instalación

1. Copiar el script a tu directorio de Claude:

```bash
cp tamaclaud.py ~/.claude/tamaclaud.py
```

2. Agregar los hooks en `~/.claude/settings.json`:

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

3. ¡Listo! Abrí Claude Code y empezá a codear para alimentar a tu TamaClaud.

## Lógica de vida

- **vida_max**: 100
- Cada tool call exitoso: **+10 vida**
- Cada tool failure: **-5 vida**
- Sin actividad 30 min: **-1 vida por minuto**
- Sin actividad 2hs: estado **HAMBRE**
- Sin actividad 4hs: estado **MUERTO**
- Al iniciar nueva sesión si está muerto: **resurrección** (vuelve con 50 de vida)
- Vida llega a 0: **MUERTO instantáneo**

## Archivo de estado

Se guarda en `~/.claude/tamaclaud.json`:

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

- Python 3.6+ (sin dependencias externas)
- Claude Code con soporte de hooks y status line

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
