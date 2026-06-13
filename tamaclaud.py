#!/usr/bin/env python3
"""
TamaClaud — Un Tamagotchi que vive en la status line de Claude Code.
Se alimenta de tool calls, muere si no codeas, y hay que resucitarlo.
"""

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# --- Configuración ---
STATE_FILE = Path.home() / ".claude" / "tamaclaud.json"
VIDA_MAX = 100
TOOL_SUCCESS_BONUS = 10
TOOL_FAILURE_PENALTY = 5
INACTIVIDAD_DECAY_MIN = 30  # minutos antes de empezar a perder vida
HAMBRE_MIN = 120            # 2 horas sin actividad → HAMBRE
MUERTE_MIN = 240            # 4 horas sin actividad → MUERTO

# --- Sprites ---
SPRITES = {
    "huevo":      "(·)",
    "durmiendo":  "(-.-)zzz",
    "feliz":      "(^‿^)",
    "comiendo":   "(°ᴗ°)♪",
    "bailando":   "\\(^o^)/",
    "estresado":  "(ó﹏ò)",
    "hambre":     "(×_×)",
    "muerto":     "(x_x)",
    "fantasma":   "(†_†)",
}


def load_state() -> dict:
    """Lee el estado desde el JSON. Si no existe, crea uno nuevo."""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return crear_estado_nuevo()


def crear_estado_nuevo() -> dict:
    """Crea un estado fresco para un TamaClaud recién nacido."""
    ahora = datetime.now(timezone.utc).isoformat()
    return {
        "vida": VIDA_MAX,
        "estado": "huevo",
        "ultima_actividad": ahora,
        "muertes": 0,
        "tool_calls_totales": 0,
        "nacimiento": ahora,
    }


def save_state(state: dict):
    """Guarda el estado en el JSON."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def minutos_inactivo(state: dict) -> float:
    """Calcula cuántos minutos han pasado desde la última actividad."""
    try:
        ultima = datetime.fromisoformat(state["ultima_actividad"])
        ahora = datetime.now(timezone.utc)
        # Asegurar que ultima tenga timezone
        if ultima.tzinfo is None:
            ultima = ultima.replace(tzinfo=timezone.utc)
        delta = (ahora - ultima).total_seconds() / 60.0
        return max(0, delta)
    except (ValueError, KeyError):
        return 0


def aplicar_decay_inactividad(state: dict) -> dict:
    """Aplica pérdida de vida por inactividad."""
    mins = minutos_inactivo(state)

    if mins >= MUERTE_MIN:
        if state["estado"] != "muerto" and state["estado"] != "fantasma":
            state["vida"] = 0
            state["estado"] = "muerto"
            state["muertes"] = state.get("muertes", 0) + 1
    elif mins >= HAMBRE_MIN:
        state["estado"] = "hambre"
        # Decay continuo después de 30 min
        mins_decay = mins - INACTIVIDAD_DECAY_MIN
        vida_perdida = int(mins_decay)
        state["vida"] = max(0, VIDA_MAX - vida_perdida)
        if state["vida"] == 0:
            state["estado"] = "muerto"
            state["muertes"] = state.get("muertes", 0) + 1
    elif mins >= INACTIVIDAD_DECAY_MIN:
        mins_decay = mins - INACTIVIDAD_DECAY_MIN
        vida_perdida = int(mins_decay)
        state["vida"] = max(0, state.get("vida", VIDA_MAX) - vida_perdida)
        if state["vida"] == 0:
            state["estado"] = "muerto"
            state["muertes"] = state.get("muertes", 0) + 1

    return state


def calcular_estado(state: dict) -> str:
    """Decide el estado/sprite basado en vida y tiempo."""
    if state["vida"] <= 0:
        return "fantasma" if state.get("estado") == "muerto" else "muerto"

    mins = minutos_inactivo(state)

    if mins >= MUERTE_MIN:
        return "muerto"
    elif mins >= HAMBRE_MIN:
        return "hambre"
    elif state["vida"] > 70:
        return "feliz"
    elif state["vida"] > 40:
        return "feliz"
    else:
        return "estresado"


def handle_event(state: dict, event: str, success: bool = True) -> dict:
    """Procesa eventos de hooks."""
    ahora = datetime.now(timezone.utc).isoformat()

    # Si está muerto, resucitar
    if state["estado"] in ("muerto", "fantasma"):
        state = resucitar(state)
        return state

    if event == "pre_tool":
        state["estado"] = "comiendo"
        state["ultima_actividad"] = ahora

    elif event == "post_tool":
        state["tool_calls_totales"] = state.get("tool_calls_totales", 0) + 1
        state["ultima_actividad"] = ahora

        if success:
            state["vida"] = min(VIDA_MAX, state.get("vida", 0) + TOOL_SUCCESS_BONUS)
            state["estado"] = "bailando"
        else:
            state["vida"] = max(0, state.get("vida", 0) - TOOL_FAILURE_PENALTY)
            state["estado"] = "estresado"
            if state["vida"] <= 0:
                state["estado"] = "muerto"
                state["muertes"] = state.get("muertes", 0) + 1

    elif event == "stop":
        state["ultima_actividad"] = ahora
        state["estado"] = "durmiendo"

    return state


def resucitar(state: dict) -> dict:
    """Resucita al TamaClaud muerto."""
    ahora = datetime.now(timezone.utc).isoformat()
    state["vida"] = 50  # Resucita con media vida
    state["estado"] = "huevo"
    state["ultima_actividad"] = ahora
    return state


def barra_vida(vida: int) -> str:
    """Genera la barra de vida visual."""
    bloques_llenos = int((vida / VIDA_MAX) * 10)
    bloques_vacios = 10 - bloques_llenos
    return "█" * bloques_llenos + "░" * bloques_vacios


def render_status(state: dict) -> str:
    """Genera la línea de status para mostrar."""
    # Aplicar decay por inactividad para mostrar estado actualizado
    state = aplicar_decay_inactividad(state)

    # Recalcular estado si no está en un estado transitorio
    if state["estado"] not in ("comiendo", "bailando", "durmiendo", "huevo"):
        state["estado"] = calcular_estado(state)

    vida = state.get("vida", 0)
    estado = state.get("estado", "feliz")
    muertes = state.get("muertes", 0)
    calls = state.get("tool_calls_totales", 0)
    sprite = SPRITES.get(estado, "(？)")

    # Emoji según estado
    if estado == "muerto" or estado == "fantasma":
        emoji = "💀"
    elif estado == "hambre":
        emoji = "😱"
    elif estado == "comiendo":
        emoji = "🍖"
    elif estado == "bailando":
        emoji = "🎉"
    elif estado == "estresado":
        emoji = "😰"
    elif estado == "durmiendo":
        emoji = "😴"
    elif estado == "huevo":
        emoji = "🥚"
    else:
        emoji = "🐣"

    barra = barra_vida(vida)
    porcentaje = vida

    linea = (
        f"{emoji} {sprite} vida:{barra} {porcentaje}%"
        f"  |  💀 muertes: {muertes}"
        f"  |  🍖 calls: {calls}"
    )

    return linea


def render_statusline() -> str:
    """Status line mode: lee JSON de stdin (requerido por Claude Code) y muestra el TamaClaud."""
    # Claude Code manda JSON por stdin, lo leemos pero no lo necesitamos
    try:
        import select
        if not sys.stdin.isatty():
            sys.stdin.read()
    except Exception:
        pass

    state = load_state()
    output = render_status(state)
    save_state(state)
    return output


def main():
    """Punto de entrada principal. Parsea argumentos."""
    args = sys.argv[1:]
    state = load_state()

    if "--status" in args:
        # Modo status line para Claude Code: lee stdin JSON y muestra
        print(render_statusline())
        sys.exit(0)

    if "--event" in args:
        idx = args.index("--event")
        if idx + 1 < len(args):
            event = args[idx + 1]
        else:
            sys.exit(1)

        # Determinar success para post_tool
        success = True
        if "--success" in args:
            sidx = args.index("--success")
            if sidx + 1 < len(args):
                val = args[sidx + 1].lower()
                success = val in ("true", "1", "yes")

        state = handle_event(state, event, success)
        save_state(state)
        sys.exit(0)

    # Sin argumentos válidos: mostrar status
    print(render_status(state))
    save_state(state)


if __name__ == "__main__":
    main()
