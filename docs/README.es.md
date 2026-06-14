<div align="center">

![TamaClaud](../assets/banner.svg)

**Un Tamagotchi que vive en la status line de Claude Code.**
**Se alimenta de tool calls. Si no codeas, se muere. Y después te persigue.** 💀

🌐 [English](./README.en.md) · [Español](./README.es.md) · [Português](./README.pt.md)

</div>

---

## La idea

Abrís Claude Code. Un huevito eclosiona en tu status line. Cada tool call lo alimenta. Baila cuando todo sale bien, entra en pánico cuando falla.

Después te vas a una reunión. Dos horas más tarde se está muriendo de hambre. Cuatro horas después está muerto, y tu contador de muertes sube en uno. Se acuerda. Para siempre.

Volvés y resucita como huevo — pero las cicatrices quedan en el JSON.

```
🐣 (^‿^) vida:██████░░░░ 60%  |  💀 muertes: 2  |  🍖 calls: 147
```

## Estados

| | Sprite | Cuándo |
|---|---|---|
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

2. Agregar los hooks y statusLine en `~/.claude/settings.json`:

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

> **Tip Windows:** usá rutas absolutas como `python3 "C:/Users/vos/.claude/tamaclaud.py" --status` en vez de `~`.

## Cómo funciona la vida

```
Cada tool call exitoso       → +10 vida
Cada tool failure            → -5 vida
Sin actividad 30 min         → -1 vida por minuto
Sin actividad 2hs            → HAMBRE
Sin actividad 4hs            → MUERTO (contador de muertes +1)
Nueva sesión estando muerto  → resurrección (vuelve con 50 de vida)
La vida llega a 0            → MUERTE instantánea
```

## Cambiar el idioma

Inglés por defecto. Cambialo cuando quieras:

```bash
python3 ~/.claude/tamaclaud.py --lang es   # Español
python3 ~/.claude/tamaclaud.py --lang pt   # Português
python3 ~/.claude/tamaclaud.py --lang en   # English
```

## Archivo de estado

Se guarda en `~/.claude/tamaclaud.json`:

```json
{
  "hp": 80,
  "state": "happy",
  "last_activity": "2026-06-13T10:30:00+00:00",
  "deaths": 2,
  "total_tool_calls": 147,
  "born": "2026-06-01T09:00:00+00:00",
  "lang": "es"
}
```

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

Hay un [bug conocido en Claude Code en Windows](https://github.com/anthropics/claude-code/issues/66455) donde el `statusLine` custom nunca se invoca automáticamente. Los hooks (alimentar, vida, muerte) funcionan bien — solo la barra persistente no se renderiza todavía. **Workaround:** escribí `tamaclaud` en el CLI para ver a tu mascota.

## 🔒 Seguridad y privacidad

Todo queda local. Sin llamadas de red. Sin telemetría. Nada sale de tu máquina, nunca. El archivo de estado solo contiene: vida, nombre del estado, timestamps, contador de muertes y de calls. Sin código, sin rutas, sin datos personales.

## FAQ

**¿Necesita un archivo de config?**
Solo un JSON que él mismo maneja. Nunca lo tocás.

**¿Qué pasa si se muere mientras duermo?**
Se vuelve fantasma. Cuando volvés y codeás, resucita como huevo con 50 de vida. La muerte queda en su récord.

**¿Puedo tener más de uno?**
Una mascota, una máquina. Como la responsabilidad real.

**¿Por qué "TamaClaud"?**
Sabés exactamente por qué.

## Requisitos

- Python 3.6+ (sin dependencias externas)
- Claude Code con soporte de hooks y status line
