"""
RPG QUEST 2.0 — Settings & Theme System
Complete UI customization, theming, and configuration.
"""
import json
import os
import random
from typing import Any, Dict, Optional, Tuple
from pathlib import Path

SETTINGS_FILE = Path(__file__).parent / "settings.json"

# ============================================================
#  THEME DEFINITIONS
# ============================================================
THEMES: Dict[str, Dict[str, str]] = {
    "default": {
        "name": "Default",
        "primary": "bright_blue",
        "secondary": "cyan",
        "accent": "yellow",
        "text": "white",
        "border": "bright_blue",
        "success": "green",
        "danger": "red",
        "warning": "yellow",
        "info": "cyan",
        "magic": "magenta",
        "rare": "yellow",
        "epic": "magenta",
        "legendary": "bright_yellow",
        "title": "bold white",
        "hp_high": "green",
        "hp_mid": "yellow",
        "hp_low": "red",
        "weapon": "bold red",
        "armor": "bold blue",
        "potion": "bold green",
        "gold": "bright_yellow",
    },
    "dark": {
        "name": "Dark Mode",
        "primary": "dim white",
        "secondary": "blue",
        "accent": "cyan",
        "text": "bright_white",
        "border": "blue",
        "success": "green",
        "danger": "red",
        "warning": "yellow",
        "info": "blue",
        "magic": "magenta",
        "rare": "yellow",
        "epic": "magenta",
        "legendary": "bright_yellow",
        "title": "bold bright_white",
        "hp_high": "green",
        "hp_mid": "yellow",
        "hp_low": "red",
        "weapon": "bold red",
        "armor": "bold blue",
        "potion": "bold green",
        "gold": "bright_yellow",
    },
    "fire": {
        "name": "Fire & Brimstone",
        "primary": "red",
        "secondary": "yellow",
        "accent": "bright_yellow",
        "text": "white",
        "border": "red",
        "success": "green",
        "danger": "bright_red",
        "warning": "yellow",
        "info": "orange1",
        "magic": "orange_red1",
        "rare": "yellow",
        "epic": "magenta",
        "legendary": "bright_yellow",
        "title": "bold red",
        "hp_high": "green",
        "hp_mid": "yellow",
        "hp_low": "bright_red",
        "weapon": "bold red",
        "armor": "bold orange1",
        "potion": "bold green",
        "gold": "bright_yellow",
    },
    "ocean": {
        "name": "Ocean Depths",
        "primary": "cyan",
        "secondary": "blue",
        "accent": "bright_cyan",
        "text": "white",
        "border": "cyan",
        "success": "green",
        "danger": "red",
        "warning": "yellow",
        "info": "light_cyan3",
        "magic": "purple",
        "rare": "yellow",
        "epic": "magenta",
        "legendary": "bright_yellow",
        "title": "bold cyan",
        "hp_high": "green",
        "hp_mid": "yellow",
        "hp_low": "red",
        "weapon": "bold cyan",
        "armor": "bold blue",
        "potion": "bold green",
        "gold": "bright_yellow",
    },
    "forest": {
        "name": "Forest Realm",
        "primary": "green",
        "secondary": "bright_green",
        "accent": "yellow",
        "text": "white",
        "border": "green",
        "success": "bright_green",
        "danger": "red",
        "warning": "gold1",
        "info": "spring_green3",
        "magic": "magenta",
        "rare": "yellow",
        "epic": "magenta",
        "legendary": "bright_yellow",
        "title": "bold green",
        "hp_high": "green",
        "hp_mid": "yellow",
        "hp_low": "red",
        "weapon": "bold green",
        "armor": "bold bright_green",
        "potion": "bold green",
        "gold": "bright_yellow",
    },
    "night": {
        "name": "Night Sky",
        "primary": "blue",
        "secondary": "purple",
        "accent": "cyan",
        "text": "bright_white",
        "border": "blue",
        "success": "green",
        "danger": "red",
        "warning": "yellow",
        "info": "plum2",
        "magic": "bright_magenta",
        "rare": "yellow",
        "epic": "magenta",
        "legendary": "bright_yellow",
        "title": "bold blue",
        "hp_high": "green",
        "hp_mid": "yellow",
        "hp_low": "red",
        "weapon": "bold purple",
        "armor": "bold blue",
        "potion": "bold green",
        "gold": "bright_yellow",
    },
    "toxic": {
        "name": "Toxic Waste",
        "primary": "green_yellow",
        "secondary": "bright_green",
        "accent": "yellow",
        "text": "white",
        "border": "green_yellow",
        "success": "green",
        "danger": "red",
        "warning": "bright_yellow",
        "info": "green",
        "magic": "magenta",
        "rare": "yellow",
        "epic": "magenta",
        "legendary": "bright_yellow",
        "title": "bold green_yellow",
        "hp_high": "green",
        "hp_mid": "yellow",
        "hp_low": "red",
        "weapon": "bold green_yellow",
        "armor": "bold bright_green",
        "potion": "bold green",
        "gold": "bright_yellow",
    },
    "royal": {
        "name": "Royal Court",
        "primary": "magenta",
        "secondary": "yellow",
        "accent": "bright_white",
        "text": "white",
        "border": "magenta",
        "success": "green",
        "danger": "red",
        "warning": "yellow",
        "info": "plum2",
        "magic": "bright_magenta",
        "rare": "yellow",
        "epic": "magenta",
        "legendary": "bright_yellow",
        "title": "bold magenta",
        "hp_high": "green",
        "hp_mid": "yellow",
        "hp_low": "red",
        "weapon": "bold magenta",
        "armor": "bold purple",
        "potion": "bold green",
        "gold": "bright_yellow",
    },
}

# ============================================================
#  PANEL STYLES
# ============================================================
PANEL_STYLES = {
    "heavy": "heavy",
    "rounded": "rounded",
    "double": "double",
    "square": "square",
    "minimal": "minimal",
    "none": "none",
}

# ============================================================
#  ANIMATION LEVELS
# ============================================================
ANIMATION_LEVELS = {
    "off": {"shake": False, "particles": False, "flash": False, "cinematic": False, "transition": 0.0},
    "minimal": {"shake": False, "particles": True, "flash": False, "cinematic": False, "transition": 0.1},
    "normal": {"shake": True, "particles": True, "flash": True, "cinematic": False, "transition": 0.2},
    "max": {"shake": True, "particles": True, "flash": True, "cinematic": True, "transition": 0.4},
    "insane": {"shake": True, "particles": True, "flash": True, "cinematic": True, "transition": 0.6},
}

# ============================================================
#  TEXT SPEEDS
# ============================================================
TEXT_SPEEDS = {
    "instant": 0.0,
    "fast": 0.003,
    "normal": 0.01,
    "slow": 0.025,
    "glacial": 0.05,
}

# ============================================================
#  SETTINGS CLASS
# ============================================================
DEFAULT_SETTINGS: Dict[str, Any] = {
    "theme": "default",
    "text_speed": "normal",
    "fast_text_speed": "fast",
    "animation_level": "normal",
    "panel_style": "heavy",
    "show_hp_bars": True,
    "show_particles": True,
    "screen_shake": True,
    "show_tips": True,
    "compact_mode": False,
    "auto_save": True,
    "show_borders": True,
    "difficulty": "normal",
    "custom_colors": {},
    "border_animation": False,
    "typing_effect": True,
    "colorize_events": True,
    "show_damage_numbers": True,
    "screen_flash": True,
    "menu_animation": True,
    "combat_animation": True,
}


class Settings:
    """Global settings manager. All UI functions read from this."""

    def __init__(self):
        self._data: Dict[str, Any] = dict(DEFAULT_SETTINGS)
        self._theme_name: str = "default"
        self._theme: Dict[str, str] = dict(THEMES["default"])

    # ---- Loading / Saving ----

    def load(self) -> None:
        if SETTINGS_FILE.exists():
            try:
                with open(SETTINGS_FILE) as f:
                    loaded = json.load(f)
                    for key, value in loaded.items():
                        if key in self._data:
                            self._data[key] = value
                self._apply_theme()
            except (json.JSONDecodeError, IOError):
                pass

    def save(self) -> None:
        try:
            with open(SETTINGS_FILE, "w") as f:
                json.dump(self._data, f, indent=2)
        except IOError:
            pass

    def reset(self) -> None:
        self._data = dict(DEFAULT_SETTINGS)
        self._apply_theme()
        self.save()

    # ---- Theme ----

    def _apply_theme(self) -> None:
        tname = self._data.get("theme", "default")
        if tname in THEMES:
            self._theme_name = tname
            self._theme = dict(THEMES[tname])
        custom = self._data.get("custom_colors", {})
        self._theme.update(custom)

    def set_theme(self, name: str) -> None:
        if name in THEMES:
            self._data["theme"] = name
            self._apply_theme()
            self.save()

    def get_theme(self) -> Dict[str, str]:
        return dict(self._theme)

    def get_theme_name(self) -> str:
        return self._theme_name

    def color(self, key: str, default: str = "white") -> str:
        return self._theme.get(key, default)

    def sc(self, key: str, default: str = "white") -> str:
        """Shortcut: return style string like 'bold COLOR'."""
        return f"bold {self._theme.get(key, default)}"

    def style(self, key: str) -> str:
        """Return the stored style string directly (e.g. 'bold red')."""
        return self._theme.get(key, "bold white")

    # ---- Getters ----

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def set(self, key: str, value) -> None:
        if key in self._data:
            self._data[key] = value
            self.save()

    def get_text_speed(self) -> float:
        speed_name = self._data.get("text_speed", "normal")
        return TEXT_SPEEDS.get(speed_name, 0.01)

    def get_fast_speed(self) -> float:
        speed_name = self._data.get("fast_text_speed", "fast")
        return TEXT_SPEEDS.get(speed_name, 0.003)

    def get_anim_level(self) -> str:
        return self._data.get("animation_level", "normal")

    def get_anim(self) -> Dict[str, Any]:
        level = self.get_anim_level()
        return ANIMATION_LEVELS.get(level, ANIMATION_LEVELS["normal"])

    def get_panel_style(self) -> str:
        style_name = self._data.get("panel_style", "heavy")
        return PANEL_STYLES.get(style_name, "heavy")

    def get_difficulty(self) -> Dict[str, Any]:
        diff = self._data.get("difficulty", "normal")
        from main import DIFFICULTY
        return DIFFICULTY.get(diff, DIFFICULTY["normal"])

    def get_difficulty_name(self) -> str:
        return self._data.get("difficulty", "normal")

    # ---- Config display ----

    def get_all(self) -> Dict[str, Any]:
        return dict(self._data)

    def get_theme_list(self) -> list:
        return [(k, v["name"]) for k, v in THEMES.items()]

    def get_speed_list(self) -> list:
        return list(TEXT_SPEEDS.keys())

    def get_anim_levels(self) -> list:
        return list(ANIMATION_LEVELS.keys())

    def get_panel_style_list(self) -> list:
        return list(PANEL_STYLES.keys())

    def get_difficulty_list(self) -> list:
        from main import DIFFICULTY
        return [(k, v["label"], v["desc"]) for k, v in DIFFICULTY.items()]


# ============================================================
#  GLOBAL INSTANCE
# ============================================================
SETTINGS = Settings()
SETTINGS.load()
