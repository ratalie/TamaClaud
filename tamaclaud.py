#!/usr/bin/env python3
"""
TamaClaud — A Tamagotchi living in your Claude Code status line.
Feed it tool calls. Stop coding and it dies.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# --- Config ---
STATE_FILE = Path.home() / ".claude" / "tamaclaud.json"
HP_MAX = 100
TOOL_SUCCESS_BONUS = 10
TOOL_FAILURE_PENALTY = 5
INACTIVITY_DECAY_MIN = 30   # minutes before hp starts draining
HUNGRY_MIN = 120            # 2 hours → HUNGRY
DEAD_MIN = 240              # 4 hours → DEAD

# --- Sprites (universal, no translation needed) ---
SPRITES = {
    "egg":       "(·)",
    "sleeping":  "(-.-)zzz",
    "happy":     "(^‿^)",
    "eating":    "(°ᴗ°)♪",
    "dancing":   "\\(^o^)/",
    "stressed":  "(ó﹏ò)",
    "hungry":    "(×_×)",
    "dead":      "(x_x)",
    "ghost":     "(†_†)",
}

# --- i18n ---
TRANSLATIONS = {
    "en": {
        "hp": "hp",
        "deaths": "deaths",
        "calls": "calls",
        "lang_set": "Language set to: English",
    },
    "es": {
        "hp": "vida",
        "deaths": "muertes",
        "calls": "calls",
        "lang_set": "Idioma configurado: Español",
    },
    "pt": {
        "hp": "vida",
        "deaths": "mortes",
        "calls": "calls",
        "lang_set": "Língua configurada: Português",
    },
}

DEFAULT_LANG = "en"


def get_lang(state: dict) -> str:
    """Get language from state, default to English."""
    lang = state.get("lang", DEFAULT_LANG)
    if lang not in TRANSLATIONS:
        lang = DEFAULT_LANG
    return lang


def t(state: dict, key: str) -> str:
    """Translate a key based on current language."""
    lang = get_lang(state)
    return TRANSLATIONS[lang].get(key, TRANSLATIONS[DEFAULT_LANG].get(key, key))


# --- State management ---

def load_state() -> dict:
    """Load state from JSON. Creates new one if it doesn't exist."""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Validate it's a dict with expected structure
            if not isinstance(data, dict):
                return create_new_state()
            return data
        except (json.JSONDecodeError, IOError):
            pass
    return create_new_state()


def create_new_state() -> dict:
    """Create a fresh state for a newborn TamaClaud."""
    now = datetime.now(timezone.utc).isoformat()
    return {
        "hp": HP_MAX,
        "state": "egg",
        "last_activity": now,
        "deaths": 0,
        "total_tool_calls": 0,
        "born": now,
        "lang": DEFAULT_LANG,
    }


def save_state(state: dict):
    """Save state to JSON."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    # Write atomically to avoid corruption from concurrent access
    tmp_file = STATE_FILE.with_suffix(".tmp")
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    tmp_file.replace(STATE_FILE)
    # Restrict permissions on Unix (owner-only read/write)
    try:
        import stat
        STATE_FILE.chmod(stat.S_IRUSR | stat.S_IWUSR)
    except (OSError, AttributeError):
        pass  # Windows handles permissions differently


# --- Logic ---

def minutes_inactive(state: dict) -> float:
    """Calculate minutes since last activity."""
    try:
        last = datetime.fromisoformat(state["last_activity"])
        now = datetime.now(timezone.utc)
        if last.tzinfo is None:
            last = last.replace(tzinfo=timezone.utc)
        delta = (now - last).total_seconds() / 60.0
        return max(0, delta)
    except (ValueError, KeyError):
        return 0


def apply_inactivity_decay(state: dict) -> dict:
    """Apply hp loss from inactivity."""
    mins = minutes_inactive(state)

    if mins >= DEAD_MIN:
        if state["state"] not in ("dead", "ghost"):
            state["hp"] = 0
            state["state"] = "dead"
            state["deaths"] = state.get("deaths", 0) + 1
    elif mins >= HUNGRY_MIN:
        state["state"] = "hungry"
        mins_decay = mins - INACTIVITY_DECAY_MIN
        hp_lost = int(mins_decay)
        state["hp"] = max(0, HP_MAX - hp_lost)
        if state["hp"] == 0:
            state["state"] = "dead"
            state["deaths"] = state.get("deaths", 0) + 1
    elif mins >= INACTIVITY_DECAY_MIN:
        mins_decay = mins - INACTIVITY_DECAY_MIN
        hp_lost = int(mins_decay)
        state["hp"] = max(0, state.get("hp", HP_MAX) - hp_lost)
        if state["hp"] == 0:
            state["state"] = "dead"
            state["deaths"] = state.get("deaths", 0) + 1

    return state


def calculate_state(state: dict) -> str:
    """Determine state/sprite based on hp and time."""
    if state["hp"] <= 0:
        return "ghost" if state.get("state") == "dead" else "dead"

    mins = minutes_inactive(state)

    if mins >= DEAD_MIN:
        return "dead"
    elif mins >= HUNGRY_MIN:
        return "hungry"
    elif state["hp"] > 40:
        return "happy"
    else:
        return "stressed"


def handle_event(state: dict, event: str, success: bool = True) -> dict:
    """Process hook events."""
    now = datetime.now(timezone.utc).isoformat()

    # If dead, resurrect
    if state["state"] in ("dead", "ghost"):
        state = resurrect(state)
        return state

    if event == "pre_tool":
        state["state"] = "eating"
        state["last_activity"] = now

    elif event == "post_tool":
        state["total_tool_calls"] = state.get("total_tool_calls", 0) + 1
        state["last_activity"] = now

        if success:
            state["hp"] = min(HP_MAX, state.get("hp", 0) + TOOL_SUCCESS_BONUS)
            state["state"] = "dancing"
        else:
            state["hp"] = max(0, state.get("hp", 0) - TOOL_FAILURE_PENALTY)
            state["state"] = "stressed"
            if state["hp"] <= 0:
                state["state"] = "dead"
                state["deaths"] = state.get("deaths", 0) + 1

    elif event == "stop":
        state["last_activity"] = now
        state["state"] = "sleeping"

    return state


def resurrect(state: dict) -> dict:
    """Resurrect a dead TamaClaud."""
    now = datetime.now(timezone.utc).isoformat()
    state["hp"] = 50
    state["state"] = "egg"
    state["last_activity"] = now
    return state


# --- Rendering ---

def hp_bar(hp: int) -> str:
    """Generate visual hp bar."""
    filled = int((hp / HP_MAX) * 10)
    empty = 10 - filled
    return "█" * filled + "░" * empty


def render_status(state: dict) -> str:
    """Generate the status line output."""
    state = apply_inactivity_decay(state)

    # Recalculate state if not in a transient state
    if state["state"] not in ("eating", "dancing", "sleeping", "egg"):
        state["state"] = calculate_state(state)

    hp = state.get("hp", 0)
    current_state = state.get("state", "happy")
    deaths = state.get("deaths", 0)
    calls = state.get("total_tool_calls", 0)
    sprite = SPRITES.get(current_state, "(？)")

    # Emoji by state
    emoji_map = {
        "dead": "💀", "ghost": "💀",
        "hungry": "😱", "eating": "🍖",
        "dancing": "🎉", "stressed": "😰",
        "sleeping": "😴", "egg": "🥚",
    }
    emoji = emoji_map.get(current_state, "🐣")

    bar = hp_bar(hp)
    hp_label = t(state, "hp")
    deaths_label = t(state, "deaths")
    calls_label = t(state, "calls")

    line = (
        f"{emoji} {sprite} {hp_label}:{bar} {hp}%"
        f"  |  💀 {deaths_label}: {deaths}"
        f"  |  🍖 {calls_label}: {calls}"
    )

    return line


def render_statusline() -> str:
    """Status line mode: read stdin JSON (required by Claude Code) and show TamaClaud."""
    # Claude Code pipes JSON via stdin; consume it with a size limit
    try:
        if not sys.stdin.isatty():
            sys.stdin.read(65536)  # 64KB max — more than enough for session data
    except Exception:
        pass

    state = load_state()
    state = migrate_state(state)
    output = render_status(state)
    save_state(state)
    return output


# --- Migration ---

def migrate_state(state: dict) -> dict:
    """Migrate old Spanish-key state to new English-key format."""
    migrated = False

    if "vida" in state and "hp" not in state:
        state["hp"] = state.pop("vida")
        migrated = True
    if "estado" in state and "state" not in state:
        # Map old Spanish states to English
        state_map = {
            "huevo": "egg", "durmiendo": "sleeping", "feliz": "happy",
            "comiendo": "eating", "bailando": "dancing", "estresado": "stressed",
            "hambre": "hungry", "muerto": "dead", "fantasma": "ghost",
        }
        old = state.pop("estado")
        state["state"] = state_map.get(old, old)
        migrated = True
    if "ultima_actividad" in state and "last_activity" not in state:
        state["last_activity"] = state.pop("ultima_actividad")
        migrated = True
    if "muertes" in state and "deaths" not in state:
        state["deaths"] = state.pop("muertes")
        migrated = True
    if "tool_calls_totales" in state and "total_tool_calls" not in state:
        state["total_tool_calls"] = state.pop("tool_calls_totales")
        migrated = True
    if "nacimiento" in state and "born" not in state:
        state["born"] = state.pop("nacimiento")
        migrated = True
    if "lang" not in state:
        state["lang"] = DEFAULT_LANG
        migrated = True

    return state


# --- Main ---

def main():
    """Main entry point. Parse args."""
    args = sys.argv[1:]
    state = load_state()
    state = migrate_state(state)

    # --lang: set language
    if "--lang" in args:
        idx = args.index("--lang")
        if idx + 1 < len(args):
            lang = args[idx + 1].lower()
            if lang in TRANSLATIONS:
                state["lang"] = lang
                save_state(state)
                print(TRANSLATIONS[lang]["lang_set"])
            else:
                print(f"Available languages: {', '.join(TRANSLATIONS.keys())}")
            sys.exit(0)

    if "--status" in args:
        print(render_statusline())
        sys.exit(0)

    if "--event" in args:
        idx = args.index("--event")
        if idx + 1 < len(args):
            event = args[idx + 1]
        else:
            sys.exit(1)

        # Validate event type
        valid_events = ("pre_tool", "post_tool", "stop")
        if event not in valid_events:
            sys.exit(1)

        success = True
        if "--success" in args:
            sidx = args.index("--success")
            if sidx + 1 < len(args):
                val = args[sidx + 1].lower()
                success = val in ("true", "1", "yes")

        state = handle_event(state, event, success)
        save_state(state)
        sys.exit(0)

    # No valid args: show status
    print(render_status(state))
    save_state(state)


if __name__ == "__main__":
    main()
